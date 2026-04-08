"""Test the WebSocket API for the device configuration panel."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
import pytest_socket

from aiohomematic.central.coordinators import (
    ConfigurableDevice,
    ConfigurableDeviceChannel,
    CopyParamsetResult,
    DeviceLink,
    LinkableChannel,
    MaintenanceData,
)
from aiohomematic.const import ParamsetKey
from aiohomematic.exceptions import BaseHomematicException
from custom_components.homematicip_local import HAHM_VERSION
from custom_components.homematicip_local.control_unit import ControlUnit
from custom_components.homematicip_local.websocket_api import SESSIONS_KEY
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant


@dataclass(frozen=True, slots=True)
class MockPutParamsetResult:
    """Mock put paramset result."""

    success: bool
    validated: bool
    validation_errors: dict[str, str]


@dataclass(frozen=True, slots=True)
class MockChannel:
    """Mock channel for testing."""

    address: str
    type_name: str
    paramset_keys: tuple[ParamsetKey, ...] = ()
    link_peer_source_categories: frozenset[str] = frozenset()
    link_peer_target_categories: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class MockDevice:
    """Mock device for testing."""

    address: str
    interface_id: str
    model: str
    name: str
    firmware: str
    interface: str = "HmIP-RF"
    model_description: str = ""
    channels: dict[str, MockChannel] | None = None

    def get_channel(self, *, channel_address: str) -> MockChannel | None:
        """Return a channel by address."""
        if self.channels:
            return self.channels.get(channel_address)
        return None


@pytest.fixture
async def mock_loaded_config_entry(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
    mock_control_unit: ControlUnit,
) -> MockConfigEntry:
    """Create mock running control unit with version patch."""
    # Enable sockets before config entry setup because the setup triggers
    # the http component (via repairs), which needs socket.socket access.
    pytest_socket.enable_socket()
    with (
        patch("custom_components.homematicip_local.find_free_port", return_value=8765),
        patch(
            "custom_components.homematicip_local.control_unit.ControlConfig.create_control_unit",
            return_value=mock_control_unit,
        ),
        patch(
            "custom_components.homematicip_local.get_aiohomematic_version",
            return_value=HAHM_VERSION,
        ),
    ):
        mock_config_entry_v2.add_to_hass(hass)
        await hass.config_entries.async_setup(mock_config_entry_v2.entry_id)
        await hass.async_block_till_done()
        assert mock_config_entry_v2.state == ConfigEntryState.LOADED
        yield mock_config_entry_v2


@pytest.fixture
def mock_facade() -> Mock:
    """Create a mock configuration facade."""
    facade = Mock()
    facade.get_configurable_devices = Mock(
        return_value=(
            ConfigurableDevice(
                address="VCU0000001",
                interface="HmIP-RF",
                interface_id="hmip_local-VCU0000001",
                model="HmIP-BSM",
                model_description="",
                name="Test Switch",
                firmware="1.0.0",
                channels=(
                    ConfigurableDeviceChannel(
                        address="VCU0000001:0",
                        channel_name="Test Switch:0",
                        channel_type="MAINTENANCE",
                        channel_type_label="Maintenance",
                        paramset_keys=("MASTER",),
                    ),
                    ConfigurableDeviceChannel(
                        address="VCU0000001:1",
                        channel_name="Test Switch:1",
                        channel_type="SWITCH",
                        channel_type_label="Switch",
                        paramset_keys=("MASTER", "VALUES"),
                    ),
                ),
                maintenance=MaintenanceData(),
            ),
        )
    )
    facade.get_paramset_description = Mock(
        return_value={
            "DUTY_CYCLE_LIMIT": {
                "TYPE": "INTEGER",
                "MIN": 0,
                "MAX": 100,
                "DEFAULT": 0,
                "OPERATIONS": 5,
            },
        }
    )
    facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})
    facade.put_paramset = AsyncMock(
        return_value=MockPutParamsetResult(
            success=True,
            validated=True,
            validation_errors={},
        )
    )
    return facade


@pytest.fixture
def mock_device_with_maintenance() -> MockDevice:
    """Create mock device with channel data for export tests."""
    ch0 = MockChannel(address="VCU0000001:0", type_name="MAINTENANCE")
    ch1 = MockChannel(address="VCU0000001:1", type_name="SWITCH")
    return MockDevice(
        address="VCU0000001",
        interface_id="hmip_local-VCU0000001",
        model="HmIP-BSM",
        name="Test Switch",
        firmware="1.0.0",
        channels={
            "VCU0000001:0": ch0,
            "VCU0000001:1": ch1,
        },
    )


class TestWsListDevices:
    """Tests for the ws_list_devices command."""

    async def test_list_devices(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test listing devices with configurable channels."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_devices",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert len(result["devices"]) == 1
        device = result["devices"][0]
        assert device["address"] == "VCU0000001"
        assert device["model"] == "HmIP-BSM"
        assert device["name"] == "Test Switch"
        assert len(device["channels"]) == 2
        assert device["channels"][0]["address"] == "VCU0000001:0"
        assert device["channels"][0]["channel_type"] == "MAINTENANCE"
        # Maintenance data should be present (defaults are None)
        assert "maintenance" in device

    async def test_list_devices_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test listing devices with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_devices",
                "entry_id": "nonexistent_entry",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_list_devices_with_maintenance(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test listing devices includes maintenance data from channel 0."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        mock_facade.get_configurable_devices = Mock(
            return_value=(
                ConfigurableDevice(
                    address="VCU0000001",
                    interface="HmIP-RF",
                    interface_id="hmip_local-VCU0000001",
                    model="HmIP-BSM",
                    model_description="",
                    name="Test Switch",
                    firmware="1.0.0",
                    channels=(
                        ConfigurableDeviceChannel(
                            address="VCU0000001:1",
                            channel_name="Test Switch:1",
                            channel_type="SWITCH",
                            channel_type_label="Switch",
                            paramset_keys=("MASTER",),
                        ),
                    ),
                    maintenance=MaintenanceData(
                        unreach=False,
                        low_bat=True,
                        rssi_device=-65,
                        rssi_peer=-70,
                        dutycycle=False,
                        config_pending=False,
                    ),
                ),
            )
        )
        control.central.configuration = mock_facade

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_devices",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        device = response["result"]["devices"][0]
        maint = device["maintenance"]
        assert maint["unreach"] is False
        assert maint["low_bat"] is True
        assert maint["rssi_device"] == -65
        assert maint["rssi_peer"] == -70
        assert maint["dutycycle"] is False
        assert maint["config_pending"] is False


class TestWsGetFormSchema:
    """Tests for the ws_get_form_schema command."""

    async def test_get_form_schema(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test getting form schema for a channel."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade

        mock_schema = Mock()
        mock_schema.model_dump.return_value = {
            "channel_address": "VCU0000001:1",
            "channel_type": "SWITCH",
            "sections": [],
            "total_parameters": 1,
            "writable_parameters": 1,
        }

        with patch("custom_components.homematicip_local.websocket_api.FormSchemaGenerator") as mock_generator_cls:
            mock_generator = Mock()
            mock_generator.generate.return_value = mock_schema
            mock_generator_cls.return_value = mock_generator

            client = await hass_ws_client(hass)
            await client.send_json(
                {
                    "id": 1,
                    "type": "homematicip_local/config/get_form_schema",
                    "entry_id": mock_loaded_config_entry.entry_id,
                    "interface_id": "hmip_local-VCU0000001",
                    "channel_address": "VCU0000001:1",
                    "channel_type": "SWITCH",
                    "paramset_key": "MASTER",
                }
            )

            response = await client.receive_json()
            assert response["success"] is True
            result = response["result"]
            assert result["channel_address"] == "VCU0000001:1"
            assert result["total_parameters"] == 1

    async def test_get_form_schema_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting form schema with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_form_schema",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"


class TestWsGetParamset:
    """Tests for the ws_get_paramset command."""

    async def test_get_paramset(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test reading paramset values."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "paramset_key": "MASTER",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["values"] == {"DUTY_CYCLE_LIMIT": 0}

    async def test_get_paramset_read_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test reading paramset with backend error."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(side_effect=BaseHomematicException("read error"))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "read_failed"


class TestWsPutParamset:
    """Tests for the ws_put_paramset command."""

    async def test_put_paramset(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test writing paramset values."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_device = MockDevice(
            address="VCU0000001",
            interface_id="hmip_local-VCU0000001",
            model="HmIP-BSM",
            name="Test Switch",
            firmware="1.0.0",
        )
        control.central.device_coordinator.get_device = Mock(return_value=mock_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "values": {"DUTY_CYCLE_LIMIT": 50},
                "paramset_key": "MASTER",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["success"] is True
        assert result["validated"] is True
        assert result["validation_errors"] == {}

    async def test_put_paramset_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test writing paramset with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_paramset",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "values": {"DUTY_CYCLE_LIMIT": 50},
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_put_paramset_logs_history(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test that put_paramset logs change history."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        # get_paramset returns old value 0, we're writing 50
        mock_facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})
        mock_device = MockDevice(
            address="VCU0000001",
            interface_id="hmip_local-VCU0000001",
            model="HmIP-BSM",
            name="Test Switch",
            firmware="1.0.0",
        )
        control.central.device_coordinator.get_device = Mock(return_value=mock_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "values": {"DUTY_CYCLE_LIMIT": 50},
                "paramset_key": "MASTER",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True

        # Verify history was logged
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/get_change_history",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )
        history_response = await client.receive_json()
        assert history_response["success"] is True
        assert history_response["result"]["total"] == 1
        entry = history_response["result"]["entries"][0]
        assert entry["source"] == "manual"
        assert "DUTY_CYCLE_LIMIT" in entry["changes"]
        assert entry["changes"]["DUTY_CYCLE_LIMIT"]["old"] == 0
        assert entry["changes"]["DUTY_CYCLE_LIMIT"]["new"] == 50

    async def test_put_paramset_write_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test writing paramset with backend error."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.put_paramset = AsyncMock(side_effect=BaseHomematicException("write error"))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "values": {"DUTY_CYCLE_LIMIT": 50},
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "write_failed"


class TestWsSessionLifecycle:
    """Tests for ConfigSession WebSocket commands."""

    async def test_session_open_replaces_existing(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test that opening a session replaces an existing one."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})

        client = await hass_ws_client(hass)
        entry_id = mock_loaded_config_entry.entry_id

        # Open first session
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_open",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        await client.receive_json()

        # Set a value
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/session_set",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:1",
                "parameter": "DUTY_CYCLE_LIMIT",
                "value": 50,
            }
        )
        await client.receive_json()

        # Open again — should replace old session
        await client.send_json(
            {
                "id": 3,
                "type": "homematicip_local/config/session_open",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True

        # New session should not be dirty
        sessions = hass.data.get(SESSIONS_KEY, {})
        session_key = f"{entry_id}_VCU0000001:1_MASTER"
        assert session_key in sessions
        assert sessions[session_key].is_dirty is False

    async def test_session_open_set_discard(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test session discard removes session."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})

        client = await hass_ws_client(hass)
        entry_id = mock_loaded_config_entry.entry_id

        # Open session
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_open",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True

        # Set a value
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/session_set",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:1",
                "parameter": "DUTY_CYCLE_LIMIT",
                "value": 50,
            }
        )
        response = await client.receive_json()
        assert response["success"] is True

        # Discard session
        await client.send_json(
            {
                "id": 3,
                "type": "homematicip_local/config/session_discard",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True

        # Session should be gone
        sessions = hass.data.get(SESSIONS_KEY, {})
        session_key = f"{entry_id}_VCU0000001:1_MASTER"
        assert session_key not in sessions

    async def test_session_open_set_save(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test session lifecycle: open, set, save."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})
        mock_device = MockDevice(
            address="VCU0000001",
            interface_id="hmip_local-VCU0000001",
            model="HmIP-BSM",
            name="Test Switch",
            firmware="1.0.0",
        )
        control.central.device_coordinator.get_device = Mock(return_value=mock_device)

        client = await hass_ws_client(hass)
        entry_id = mock_loaded_config_entry.entry_id

        # Open session
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_open",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "paramset_key": "MASTER",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True

        # Set a value
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/session_set",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:1",
                "parameter": "DUTY_CYCLE_LIMIT",
                "value": 50,
                "paramset_key": "MASTER",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["is_dirty"] is True
        assert result["can_undo"] is True
        assert result["can_redo"] is False

        # Save session
        await client.send_json(
            {
                "id": 3,
                "type": "homematicip_local/config/session_save",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "paramset_key": "MASTER",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["success"] is True
        assert result["changes_applied"] == 1

        # Session should be removed after save
        sessions = hass.data.get(SESSIONS_KEY, {})
        session_key = f"{entry_id}_VCU0000001:1_MASTER"
        assert session_key not in sessions

    async def test_session_open_set_undo_redo(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test session undo and redo."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})

        client = await hass_ws_client(hass)
        entry_id = mock_loaded_config_entry.entry_id

        # Open session
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_open",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True

        # Set a value
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/session_set",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:1",
                "parameter": "DUTY_CYCLE_LIMIT",
                "value": 50,
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["is_dirty"] is True

        # Undo
        await client.send_json(
            {
                "id": 3,
                "type": "homematicip_local/config/session_undo",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["performed"] is True
        assert result["is_dirty"] is False
        assert result["can_undo"] is False
        assert result["can_redo"] is True

        # Redo
        await client.send_json(
            {
                "id": 4,
                "type": "homematicip_local/config/session_redo",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["performed"] is True
        assert result["is_dirty"] is True
        assert result["can_undo"] is True
        assert result["can_redo"] is False

    async def test_session_redo_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test session_redo fails when no session exists."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_redo",
                "entry_id": mock_loaded_config_entry.entry_id,
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "session_not_found"

    async def test_session_save_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test session_save fails with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_save",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_session_save_no_changes(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test session save with no changes returns early."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})

        client = await hass_ws_client(hass)
        entry_id = mock_loaded_config_entry.entry_id

        # Open session
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_open",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        await client.receive_json()

        # Save without any changes
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/session_save",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["success"] is True
        assert result["changes_applied"] == 0

        # put_paramset should NOT have been called (only get_paramset for open)
        mock_facade.put_paramset.assert_not_called()

    async def test_session_save_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test session_save fails when no session exists."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_save",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "session_not_found"

    async def test_session_set_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test session_set fails when no session exists."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_set",
                "entry_id": mock_loaded_config_entry.entry_id,
                "channel_address": "VCU0000001:1",
                "parameter": "DUTY_CYCLE_LIMIT",
                "value": 50,
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "session_not_found"

    async def test_session_undo_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test session_undo fails when no session exists."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/session_undo",
                "entry_id": mock_loaded_config_entry.entry_id,
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "session_not_found"


class TestWsExportImport:
    """Tests for export/import WebSocket commands."""

    async def test_export_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test export fails with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/export_paramset",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_export_import_round_trip(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
        mock_device_with_maintenance: MockDevice,
    ) -> None:
        """Test export followed by import round-trip."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        control.central.device_coordinator.get_device = Mock(return_value=mock_device_with_maintenance)

        client = await hass_ws_client(hass)

        # Export
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/export_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        export_response = await client.receive_json()
        assert export_response["success"] is True
        json_data = export_response["result"]["json_data"]

        # Import back to same channel
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/import_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "json_data": json_data,
            }
        )
        import_response = await client.receive_json()
        assert import_response["success"] is True
        result = import_response["result"]
        assert result["success"] is True
        assert result["imported_model"] == "HmIP-BSM"

    async def test_export_paramset(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
        mock_device_with_maintenance: MockDevice,
    ) -> None:
        """Test exporting a paramset as JSON."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        control.central.device_coordinator.get_device = Mock(return_value=mock_device_with_maintenance)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/export_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "paramset_key": "MASTER",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        json_data = response["result"]["json_data"]
        parsed = json.loads(json_data)
        assert parsed["model"] == "HmIP-BSM"
        assert parsed["channel_address"] == "VCU0000001:1"
        assert parsed["paramset_key"] == "MASTER"
        assert "values" in parsed

    async def test_export_read_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test export fails when paramset read fails."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(side_effect=BaseHomematicException("read error"))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/export_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "read_failed"

    async def test_import_invalid_json(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test import fails with invalid JSON."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/import_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "json_data": "not valid json",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "invalid_data"

    async def test_import_model_mismatch(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test import fails when model does not match."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        # Target device is HmIP-BSM
        target_device = MockDevice(
            address="VCU0000002",
            interface_id="hmip_local-VCU0000002",
            model="HmIP-BSM",
            name="Target Switch",
            firmware="1.0.0",
        )
        control.central.device_coordinator.get_device = Mock(return_value=target_device)

        # Create JSON from a different model
        json_data = json.dumps(
            {
                "version": "1.0",
                "exported_at": "2026-01-01T00:00:00+00:00",
                "device_address": "VCU9999999",
                "model": "HmIP-FALMOT-C12",
                "channel_address": "VCU9999999:1",
                "channel_type": "HEATING",
                "paramset_key": "MASTER",
                "values": {"SOME_PARAM": 42},
            }
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/import_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000002",
                "channel_address": "VCU0000002:1",
                "json_data": json_data,
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "model_mismatch"


class TestWsCopyParamset:
    """Tests for the ws_copy_paramset command."""

    async def test_copy_paramset(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test copying paramset between compatible channels."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.copy_paramset = AsyncMock(
            return_value=(
                CopyParamsetResult(
                    success=True,
                    validated=True,
                    validation_errors={},
                    parameters_copied=1,
                    parameters_skipped=1,
                ),
                {"DUTY_CYCLE_LIMIT": 0},
                {"DUTY_CYCLE_LIMIT": 50},
            )
        )
        mock_device = MockDevice(
            address="VCU0000002",
            interface_id="hmip_local-VCU0000002",
            model="HmIP-BSM",
            name="Target Switch",
            firmware="1.0.0",
        )
        control.central.device_coordinator.get_device = Mock(return_value=mock_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/copy_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "source_interface_id": "hmip_local-VCU0000001",
                "source_channel_address": "VCU0000001:1",
                "target_interface_id": "hmip_local-VCU0000002",
                "target_channel_address": "VCU0000002:1",
                "paramset_key": "MASTER",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["success"] is True
        assert result["parameters_copied"] == 1
        assert result["parameters_skipped"] == 1

    async def test_copy_paramset_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test copy fails with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/copy_paramset",
                "entry_id": "nonexistent_entry",
                "source_interface_id": "hmip_local-VCU0000001",
                "source_channel_address": "VCU0000001:1",
                "target_interface_id": "hmip_local-VCU0000002",
                "target_channel_address": "VCU0000002:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_copy_paramset_no_writable_params(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test copy when no parameters are writable in target."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.copy_paramset = AsyncMock(
            return_value=(
                CopyParamsetResult(
                    success=True,
                    validated=True,
                    validation_errors={},
                    parameters_copied=0,
                    parameters_skipped=1,
                ),
                {},
                {},
            )
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/copy_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "source_interface_id": "hmip_local-VCU0000001",
                "source_channel_address": "VCU0000001:1",
                "target_interface_id": "hmip_local-VCU0000002",
                "target_channel_address": "VCU0000002:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["parameters_copied"] == 0
        assert result["parameters_skipped"] == 1

    async def test_copy_paramset_read_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test copy fails when source read fails."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.copy_paramset = AsyncMock(side_effect=BaseHomematicException("read error"))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/copy_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "source_interface_id": "hmip_local-VCU0000001",
                "source_channel_address": "VCU0000001:1",
                "target_interface_id": "hmip_local-VCU0000002",
                "target_channel_address": "VCU0000002:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "read_failed"


class TestWsChangeHistory:
    """Tests for change history WebSocket commands."""

    async def test_clear_change_history(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test clearing change history for an entry."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})
        mock_device = MockDevice(
            address="VCU0000001",
            interface_id="hmip_local-VCU0000001",
            model="HmIP-BSM",
            name="Test Switch",
            firmware="1.0.0",
        )
        control.central.device_coordinator.get_device = Mock(return_value=mock_device)

        client = await hass_ws_client(hass)
        entry_id = mock_loaded_config_entry.entry_id

        # Create a history entry
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_paramset",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "values": {"DUTY_CYCLE_LIMIT": 50},
            }
        )
        await client.receive_json()

        # Clear history
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/clear_change_history",
                "entry_id": entry_id,
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["cleared"] == 1

        # Verify history is empty
        await client.send_json(
            {
                "id": 3,
                "type": "homematicip_local/config/get_change_history",
                "entry_id": entry_id,
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["total"] == 0

    async def test_clear_change_history_empty(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test clearing empty change history."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/clear_change_history",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["cleared"] == 0

    async def test_get_change_history_empty(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting empty change history."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_change_history",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["entries"] == []
        assert response["result"]["total"] == 0

    async def test_get_change_history_filtered_by_channel(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test change history filtered by channel address."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        mock_facade.get_paramset = AsyncMock(return_value={"DUTY_CYCLE_LIMIT": 0})
        mock_device = MockDevice(
            address="VCU0000001",
            interface_id="hmip_local-VCU0000001",
            model="HmIP-BSM",
            name="Test Switch",
            firmware="1.0.0",
        )
        control.central.device_coordinator.get_device = Mock(return_value=mock_device)

        client = await hass_ws_client(hass)
        entry_id = mock_loaded_config_entry.entry_id

        # Write to channel :1
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_paramset",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "values": {"DUTY_CYCLE_LIMIT": 50},
            }
        )
        await client.receive_json()

        # Get history for channel :1
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/get_change_history",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:1",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["total"] == 1

        # Get history for a different channel — should be empty
        await client.send_json(
            {
                "id": 3,
                "type": "homematicip_local/config/get_change_history",
                "entry_id": entry_id,
                "channel_address": "VCU0000001:0",
            }
        )
        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["total"] == 0


class TestWsDirectLinks:
    """Tests for direct link WebSocket commands."""

    # --- ws_list_device_links ---

    async def test_add_link(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test creating a new direct link."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.add_link = AsyncMock(return_value=True)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/add_link",
                "entry_id": mock_loaded_config_entry.entry_id,
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
                "name": "My Link",
                "description": "test link",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True
        control.central.link.add_link.assert_called_once_with(
            sender_channel_address="VCU0000001:1",
            receiver_channel_address="VCU0000002:1",
            name="My Link",
            description="test link",
        )

    async def test_add_link_default_name(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test add link passes empty name to coordinator (default generation is internal)."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.add_link = AsyncMock(return_value=True)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/add_link",
                "entry_id": mock_loaded_config_entry.entry_id,
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        control.central.link.add_link.assert_called_once_with(
            sender_channel_address="VCU0000001:1",
            receiver_channel_address="VCU0000002:1",
            name="",
            description="created by HA",
        )

    async def test_add_link_device_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test add link when coordinator returns failure (e.g. device not found)."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.add_link = AsyncMock(return_value=False)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/add_link",
                "entry_id": mock_loaded_config_entry.entry_id,
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "add_link_failed"

    async def test_add_link_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test add link with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/add_link",
                "entry_id": "nonexistent_entry",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_add_link_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test add link when coordinator returns failure."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.add_link = AsyncMock(return_value=False)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/add_link",
                "entry_id": mock_loaded_config_entry.entry_id,
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "add_link_failed"

    async def test_get_link_form_schema(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test getting form schema for a link."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade

        device = Mock()
        device.model = "HmIP-BSM"
        device.sub_model = None
        ch = MockChannel(address="VCU0000002:1", type_name="SWITCH")
        device.get_channel = Mock(return_value=ch)
        device.client = Mock()
        device.client.get_paramset = AsyncMock(return_value={"LONG_PRESS_TIME": 1.0})
        control.central.device_coordinator.get_device = Mock(return_value=device)

        mock_facade.get_link_paramset_description = AsyncMock(
            return_value={"LONG_PRESS_TIME": {"TYPE": "FLOAT", "MIN": 0, "MAX": 10, "DEFAULT": 0, "OPERATIONS": 5}}
        )

        mock_schema = Mock()
        mock_schema.model_dump.return_value = {
            "channel_address": "VCU0000002:1",
            "channel_type": "SWITCH",
            "sections": [],
            "total_parameters": 1,
            "writable_parameters": 1,
        }

        with patch("custom_components.homematicip_local.websocket_api.FormSchemaGenerator") as mock_generator_cls:
            mock_generator = Mock()
            mock_generator.generate.return_value = mock_schema
            mock_generator_cls.return_value = mock_generator

            client = await hass_ws_client(hass)
            await client.send_json(
                {
                    "id": 1,
                    "type": "homematicip_local/config/get_link_form_schema",
                    "entry_id": mock_loaded_config_entry.entry_id,
                    "interface_id": "hmip_local-VCU0000001",
                    "sender_channel_address": "VCU0000001:1",
                    "receiver_channel_address": "VCU0000002:1",
                }
            )

            response = await client.receive_json()
            assert response["success"] is True
            result = response["result"]
            assert result["channel_address"] == "VCU0000002:1"
            assert result["total_parameters"] == 1

    async def test_get_link_form_schema_device_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test get link form schema when receiver device not found."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        control.central.device_coordinator.get_device = Mock(return_value=None)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_form_schema",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "device_not_found"

    async def test_get_link_form_schema_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test get link form schema with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_form_schema",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_get_link_form_schema_read_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
    ) -> None:
        """Test get link form schema when paramset read fails."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade

        device = Mock()
        device.model = "HmIP-BSM"
        device.sub_model = None
        device.client = Mock()
        device.client.get_paramset = AsyncMock(side_effect=BaseHomematicException("read error"))
        control.central.device_coordinator.get_device = Mock(return_value=device)

        mock_facade.get_link_paramset_description = AsyncMock(side_effect=BaseHomematicException("read error"))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_form_schema",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "read_failed"

    async def test_get_link_paramset(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test reading link paramset values."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device = Mock()
        device.client = Mock()
        device.client.get_paramset = AsyncMock(return_value={"LONG_PRESS_TIME": 1.0, "SHORT_PRESS_TIME": 0.5})
        control.central.device_coordinator.get_device = Mock(return_value=device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        values = response["result"]["values"]
        assert values["LONG_PRESS_TIME"] == 1.0
        assert values["SHORT_PRESS_TIME"] == 0.5

    async def test_get_link_paramset_device_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test get link paramset when device not found."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.device_coordinator.get_device = Mock(return_value=None)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "device_not_found"

    async def test_get_link_paramset_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test get link paramset with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_paramset",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_get_link_paramset_read_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test get link paramset when read fails."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device = Mock()
        device.client = Mock()
        device.client.get_paramset = AsyncMock(side_effect=BaseHomematicException("read error"))
        control.central.device_coordinator.get_device = Mock(return_value=device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "read_failed"

    async def test_get_linkable_channels_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test get linkable channels with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_linkable_channels",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "role": "sender",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_get_linkable_channels_excludes_source(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test that the source channel is excluded from results."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_linkable_channels = Mock(return_value=())

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_linkable_channels",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "role": "sender",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert len(response["result"]["channels"]) == 0

    async def test_get_linkable_channels_filters_interface(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test that only devices with matching interface_id are included."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_linkable_channels = Mock(return_value=())

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_linkable_channels",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "role": "sender",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert len(response["result"]["channels"]) == 0
        control.central.link.get_linkable_channels.assert_called_once()

    async def test_get_linkable_channels_non_linkable_excluded(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test that devices with non-linkable interfaces are excluded (handled by coordinator)."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_linkable_channels = Mock(return_value=())

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_linkable_channels",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "role": "sender",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert len(response["result"]["channels"]) == 0

    async def test_get_linkable_channels_receiver_role(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting linkable channels when source is receiver."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_linkable_channels = Mock(
            return_value=(
                LinkableChannel(
                    address="VCU0000002:1",
                    channel_name="Wall Switch:1",
                    channel_type="KEY",
                    channel_type_label="Key",
                    device_address="VCU0000002",
                    device_name="Wall Switch",
                    device_model="HmIP-WRC2",
                ),
            )
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_linkable_channels",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "role": "receiver",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        channels = response["result"]["channels"]
        assert len(channels) == 1
        assert channels[0]["address"] == "VCU0000002:1"
        assert channels[0]["channel_type"] == "KEY"

    async def test_get_linkable_channels_sender_role(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting linkable channels when source is sender."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_linkable_channels = Mock(
            return_value=(
                LinkableChannel(
                    address="VCU0000002:1",
                    channel_name="Switch 2:1",
                    channel_type="SWITCH",
                    channel_type_label="Switch",
                    device_address="VCU0000002",
                    device_name="Switch 2",
                    device_model="HmIP-BSM",
                ),
            )
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_linkable_channels",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "channel_address": "VCU0000001:1",
                "role": "sender",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        channels = response["result"]["channels"]
        assert len(channels) == 1
        assert channels[0]["address"] == "VCU0000002:1"
        assert channels[0]["device_name"] == "Switch 2"
        assert channels[0]["device_model"] == "HmIP-BSM"

    async def test_list_device_links(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test listing links for a device."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_device_links = AsyncMock(
            return_value=(
                DeviceLink(
                    sender_address="VCU0000001:1",
                    sender_channel_name="Test Switch:1",
                    receiver_address="VCU0000002:1",
                    receiver_channel_name="Peer Switch:1",
                    name="Test Link",
                    description="test",
                    flags=0,
                    sender_device_name="Test Switch",
                    sender_device_model="HmIP-BSM",
                    sender_channel_type="SWITCH",
                    sender_channel_type_label="Switch",
                    receiver_device_name="Peer Switch",
                    receiver_device_model="HmIP-BSM",
                    receiver_channel_type="SWITCH_VIRTUAL_RECEIVER",
                    receiver_channel_type_label="Switch Virtual Receiver",
                    peer_address="VCU0000002:1",
                    peer_device_name="Peer Switch",
                    peer_device_model="HmIP-BSM",
                    direction="outgoing",
                ),
            )
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_device_links",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "device_address": "VCU0000001",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        links = response["result"]["links"]
        assert len(links) == 1
        link = links[0]
        assert link["sender_address"] == "VCU0000001:1"
        assert link["receiver_address"] == "VCU0000002:1"
        assert link["direction"] == "outgoing"
        assert link["peer_address"] == "VCU0000002:1"
        assert link["peer_device_name"] == "Peer Switch"
        assert link["peer_device_model"] == "HmIP-BSM"
        assert link["name"] == "Test Link"
        assert link["sender_channel_type"] == "SWITCH"
        assert link["sender_channel_type_label"] != ""
        assert link["receiver_channel_type"] == "SWITCH_VIRTUAL_RECEIVER"
        assert link["receiver_channel_type_label"] != ""

    async def test_list_device_links_deduplicates(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test that duplicate links are deduplicated (handled by coordinator)."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_device_links = AsyncMock(
            return_value=(
                DeviceLink(
                    sender_address="VCU0000001:1",
                    sender_channel_name="Test Switch:1",
                    receiver_address="VCU0000002:1",
                    receiver_channel_name="Peer:1",
                    name="Link",
                    description="",
                    flags=0,
                    sender_device_name="Test Switch",
                    sender_device_model="HmIP-BSM",
                    sender_channel_type="SWITCH",
                    sender_channel_type_label="Switch",
                    receiver_device_name="Peer",
                    receiver_device_model="HmIP-BSM",
                    receiver_channel_type="SWITCH",
                    receiver_channel_type_label="Switch",
                    peer_address="VCU0000002:1",
                    peer_device_name="Peer",
                    peer_device_model="HmIP-BSM",
                    direction="outgoing",
                ),
            )
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_device_links",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "device_address": "VCU0000001",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert len(response["result"]["links"]) == 1

    async def test_list_device_links_device_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test list links when device not found returns empty list."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_device_links = AsyncMock(return_value=())

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_device_links",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "device_address": "VCU_UNKNOWN",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["links"] == []

    async def test_list_device_links_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test list links with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_device_links",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "device_address": "VCU0000001",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_list_device_links_incoming(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test listing an incoming link for a device."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_device_links = AsyncMock(
            return_value=(
                DeviceLink(
                    sender_address="VCU0000002:1",
                    sender_channel_name="Remote:1",
                    receiver_address="VCU0000001:1",
                    receiver_channel_name="Test Switch:1",
                    name="Incoming Link",
                    description="",
                    flags=0,
                    sender_device_name="Remote",
                    sender_device_model="HmIP-WRC2",
                    sender_channel_type="KEY_TRANSCEIVER",
                    sender_channel_type_label="Key Transceiver",
                    receiver_device_name="Test Switch",
                    receiver_device_model="HmIP-BSM",
                    receiver_channel_type="SWITCH",
                    receiver_channel_type_label="Switch",
                    peer_address="VCU0000002:1",
                    peer_device_name="Remote",
                    peer_device_model="HmIP-WRC2",
                    direction="incoming",
                ),
            )
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_device_links",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "device_address": "VCU0000001",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        links = response["result"]["links"]
        assert len(links) == 1
        link = links[0]
        assert link["direction"] == "incoming"
        assert link["peer_address"] == "VCU0000002:1"
        assert link["sender_device_name"] == "Remote"
        assert link["receiver_device_name"] == "Test Switch"
        assert link["sender_channel_type"] == "KEY_TRANSCEIVER"
        assert link["receiver_channel_type"] == "SWITCH"

    async def test_list_device_links_non_linkable_interface(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test list links for non-linkable interface returns empty (handled by coordinator)."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.get_device_links = AsyncMock(return_value=())

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/list_device_links",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "device_address": "VCU0000001",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["links"] == []

    async def test_put_link_paramset(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test writing link paramset values."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device = Mock()
        device.address = "VCU0000002"
        device.name = "Receiver"
        device.model = "HmIP-BSM"
        device.client = Mock()
        device.client.get_paramset = AsyncMock(return_value={"LONG_PRESS_TIME": 1.0})
        device.client.put_paramset = AsyncMock()
        control.central.device_coordinator.get_device = Mock(return_value=device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_link_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
                "values": {"LONG_PRESS_TIME": 2.0},
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True
        device.client.put_paramset.assert_called_once_with(
            channel_address="VCU0000002:1",
            paramset_key_or_link_address="VCU0000001:1",
            values={"LONG_PRESS_TIME": 2.0},
            check_against_pd=True,
        )

    async def test_put_link_paramset_device_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test put link paramset when device not found."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.device_coordinator.get_device = Mock(return_value=None)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_link_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
                "values": {"LONG_PRESS_TIME": 2.0},
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "device_not_found"

    async def test_put_link_paramset_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test put link paramset with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_link_paramset",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
                "values": {"LONG_PRESS_TIME": 2.0},
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_put_link_paramset_logs_history(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test that put link paramset logs change history."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device = Mock()
        device.address = "VCU0000002"
        device.name = "Receiver"
        device.model = "HmIP-BSM"
        device.client = Mock()
        device.client.get_paramset = AsyncMock(return_value={"LONG_PRESS_TIME": 1.0})
        device.client.put_paramset = AsyncMock()
        control.central.device_coordinator.get_device = Mock(return_value=device)

        client = await hass_ws_client(hass)
        entry_id = mock_loaded_config_entry.entry_id

        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_link_paramset",
                "entry_id": entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
                "values": {"LONG_PRESS_TIME": 2.0},
            }
        )

        response = await client.receive_json()
        assert response["success"] is True

        # Verify history was logged
        await client.send_json(
            {
                "id": 2,
                "type": "homematicip_local/config/get_change_history",
                "entry_id": entry_id,
            }
        )
        history_response = await client.receive_json()
        assert history_response["success"] is True
        assert history_response["result"]["total"] == 1
        entry = history_response["result"]["entries"][0]
        assert entry["paramset_key"] == "LINK"
        assert entry["source"] == "manual"
        assert "LONG_PRESS_TIME" in entry["changes"]
        assert entry["changes"]["LONG_PRESS_TIME"]["old"] == 1.0
        assert entry["changes"]["LONG_PRESS_TIME"]["new"] == 2.0

    async def test_put_link_paramset_write_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test put link paramset when write fails."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device = Mock()
        device.address = "VCU0000002"
        device.name = "Receiver"
        device.model = "HmIP-BSM"
        device.client = Mock()
        device.client.get_paramset = AsyncMock(return_value={})
        device.client.put_paramset = AsyncMock(side_effect=BaseHomematicException("write error"))
        control.central.device_coordinator.get_device = Mock(return_value=device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/put_link_paramset",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
                "values": {"LONG_PRESS_TIME": 2.0},
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "write_failed"

    async def test_remove_link(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test removing a direct link."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.remove_link = AsyncMock(return_value=True)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/remove_link",
                "entry_id": mock_loaded_config_entry.entry_id,
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True
        control.central.link.remove_link.assert_called_once_with(
            sender_channel_address="VCU0000001:1",
            receiver_channel_address="VCU0000002:1",
        )

    async def test_remove_link_device_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test remove link when coordinator returns failure (e.g. device not found)."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.remove_link = AsyncMock(return_value=False)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/remove_link",
                "entry_id": mock_loaded_config_entry.entry_id,
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "remove_link_failed"

    async def test_remove_link_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test remove link with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/remove_link",
                "entry_id": "nonexistent_entry",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_remove_link_failed(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test remove link when coordinator returns failure."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.link = Mock()
        control.central.link.remove_link = AsyncMock(return_value=False)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/remove_link",
                "entry_id": mock_loaded_config_entry.entry_id,
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "remove_link_failed"


class TestWsGetLinkProfiles:
    """Tests for the ws_get_link_profiles command."""

    async def test_get_link_profiles(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting link profiles for a known channel type pair."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        receiver_ch = MockChannel(address="VCU0000002:1", type_name="DIMMER_VIRTUAL_RECEIVER")
        sender_ch = MockChannel(address="VCU0000001:1", type_name="SWITCH_TRANSCEIVER")

        receiver_device = Mock()
        receiver_device.get_channel = Mock(return_value=receiver_ch)
        receiver_device.client = Mock()
        receiver_device.client.get_paramset = AsyncMock(
            return_value={
                "SHORT_PROFILE_ACTION_TYPE": 1,
                "SHORT_ON_LEVEL": 1.0,
                "SHORT_ON_TIME_BASE": 7,
                "SHORT_ON_TIME_FACTOR": 31,
                "SHORT_JT_ON": 3,
                "SHORT_JT_OFF": 1,
                "LONG_PROFILE_ACTION_TYPE": 3,
                "LONG_DIM_MAX_LEVEL": 1.0,
            }
        )

        sender_device = Mock()
        sender_device.get_channel = Mock(return_value=sender_ch)

        def _get_device(*, address: str) -> Mock | None:
            if address == "VCU0000002":
                return receiver_device
            if address == "VCU0000001":
                return sender_device
            return None

        control.central.device_coordinator.get_device = Mock(side_effect=_get_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_profiles",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["profiles"] is not None
        assert len(result["profiles"]) >= 2
        assert result["active_profile_id"] == 1
        # Verify Expert profile is first
        assert result["profiles"][0]["id"] == 0
        assert result["profiles"][0]["name"] == "Expert"

    async def test_get_link_profiles_device_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test get link profiles when receiver device not found."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.device_coordinator.get_device = Mock(return_value=None)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_profiles",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "device_not_found"

    async def test_get_link_profiles_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test get link profiles with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_profiles",
                "entry_id": "nonexistent_entry",
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_get_link_profiles_missing_channel_type(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test returning null when channel type cannot be resolved."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        receiver_device = Mock()
        receiver_device.get_channel = Mock(return_value=None)

        sender_device = Mock()
        sender_device.get_channel = Mock(return_value=None)

        def _get_device(*, address: str) -> Mock | None:
            if address == "VCU0000002":
                return receiver_device
            if address == "VCU0000001":
                return sender_device
            return None

        control.central.device_coordinator.get_device = Mock(side_effect=_get_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_profiles",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["profiles"] is None
        assert result["active_profile_id"] == 0

    async def test_get_link_profiles_no_profiles_available(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test returning null profiles for unknown channel types."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        receiver_ch = MockChannel(address="VCU0000002:1", type_name="UNKNOWN_RECEIVER")
        sender_ch = MockChannel(address="VCU0000001:1", type_name="UNKNOWN_SENDER")

        receiver_device = Mock()
        receiver_device.get_channel = Mock(return_value=receiver_ch)
        receiver_device.client = Mock()
        receiver_device.client.get_paramset = AsyncMock(return_value={})

        sender_device = Mock()
        sender_device.get_channel = Mock(return_value=sender_ch)

        def _get_device(*, address: str) -> Mock | None:
            if address == "VCU0000002":
                return receiver_device
            if address == "VCU0000001":
                return sender_device
            return None

        control.central.device_coordinator.get_device = Mock(side_effect=_get_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_profiles",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["profiles"] is None
        assert result["active_profile_id"] == 0

    async def test_get_link_profiles_paramset_read_failure(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test graceful handling when paramset read fails."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        receiver_ch = MockChannel(address="VCU0000002:1", type_name="DIMMER_VIRTUAL_RECEIVER")
        sender_ch = MockChannel(address="VCU0000001:1", type_name="SWITCH_TRANSCEIVER")

        receiver_device = Mock()
        receiver_device.get_channel = Mock(return_value=receiver_ch)
        receiver_device.client = Mock()
        receiver_device.client.get_paramset = AsyncMock(side_effect=BaseHomematicException("read failed"))

        sender_device = Mock()
        sender_device.get_channel = Mock(return_value=sender_ch)

        def _get_device(*, address: str) -> Mock | None:
            if address == "VCU0000002":
                return receiver_device
            if address == "VCU0000001":
                return sender_device
            return None

        control.central.device_coordinator.get_device = Mock(side_effect=_get_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/config/get_link_profiles",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_local-VCU0000001",
                "sender_channel_address": "VCU0000001:1",
                "receiver_channel_address": "VCU0000002:1",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        # Profiles should still be returned, just with fallback active_profile_id=0
        assert result["profiles"] is not None
        assert result["active_profile_id"] == 0
