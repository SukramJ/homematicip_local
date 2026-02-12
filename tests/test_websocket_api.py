"""Test the WebSocket API for the device configuration panel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from aiohomematic.const import ParamsetKey
from aiohomematic.exceptions import BaseHomematicException
from custom_components.homematicip_local import HAHM_VERSION
from custom_components.homematicip_local.control_unit import ControlUnit
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant


@dataclass(frozen=True, slots=True)
class MockConfigurableChannel:
    """Mock configurable channel."""

    address: str
    channel_type: str
    paramset_keys: tuple[ParamsetKey, ...]


@dataclass(frozen=True, slots=True)
class MockPutParamsetResult:
    """Mock put paramset result."""

    success: bool
    validated: bool
    validation_errors: dict[str, str]


@dataclass(frozen=True, slots=True)
class MockDevice:
    """Mock device for testing."""

    address: str
    interface_id: str
    model: str
    name: str
    firmware: str
    model_description: str = ""


@pytest.fixture
async def mock_loaded_config_entry(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
    mock_control_unit: ControlUnit,
) -> MockConfigEntry:
    """Create mock running control unit with version patch."""
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
    facade.get_configurable_channels = Mock(
        return_value=(
            MockConfigurableChannel(
                address="VCU0000001:0",
                channel_type="MAINTENANCE",
                paramset_keys=(ParamsetKey.MASTER,),
            ),
            MockConfigurableChannel(
                address="VCU0000001:1",
                channel_type="SWITCH",
                paramset_keys=(ParamsetKey.MASTER, ParamsetKey.VALUES),
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
def mock_devices() -> list[MockDevice]:
    """Create mock devices."""
    return [
        MockDevice(
            address="VCU0000001",
            interface_id="hmip_local-VCU0000001",
            model="HmIP-BSM",
            name="Test Switch",
            firmware="1.0.0",
        ),
    ]


class TestWsListDevices:
    """Tests for the ws_list_devices command."""

    async def test_list_devices(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        mock_facade: Mock,
        mock_devices: list[MockDevice],
    ) -> None:
        """Test listing devices with configurable channels."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.configuration = mock_facade
        control.central.devices = mock_devices

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
