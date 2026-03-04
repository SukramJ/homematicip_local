"""Test the WebSocket API for the Integration and OpenCCU panel tabs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, Mock, PropertyMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
import pytest_socket

from aiohomematic.const import DeviceFirmwareState, Interface
from aiohomematic.exceptions import BaseHomematicException
from custom_components.homematicip_local import HAHM_VERSION
from custom_components.homematicip_local.control_unit import ControlUnit
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant


@dataclass(frozen=True, slots=True)
class MockAvailabilityInfo:
    """Mock availability info."""

    is_reachable: bool = True
    last_updated: None = None
    battery_level: int | None = None
    low_battery: bool | None = None
    signal_strength: int | None = None


@dataclass(frozen=True, slots=True)
class MockBackupData:
    """Mock backup data."""

    filename: str = "backup_20260304.tar.gz"
    content: bytes = b"backup_content_data"


@pytest.fixture
async def mock_loaded_config_entry(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
    mock_control_unit: ControlUnit,
) -> MockConfigEntry:
    """Create mock running control unit with version patch."""
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


def _make_mock_device(
    *,
    address: str = "VCU0000001",
    name: str = "Test Device",
    model: str = "HmIP-BSM",
    interface_id: str = "hmip_local-VCU0000001",
    firmware: str = "1.0.0",
    available_firmware: str | None = None,
    firmware_updatable: bool = False,
    firmware_update_state: DeviceFirmwareState = DeviceFirmwareState.UP_TO_DATE,
    is_reachable: bool = True,
    signal_strength: int | None = -65,
    low_battery: bool | None = None,
    rssi_device: int | None = -70,
    rssi_peer: int | None = -72,
) -> Mock:
    """Create a mock device with common properties."""
    device = Mock()
    device.address = address
    device.name = name
    device.model = model
    device.interface_id = interface_id
    device.firmware = firmware
    device.available_firmware = available_firmware
    device.firmware_updatable = firmware_updatable
    device.firmware_update_state = firmware_update_state
    device.availability = MockAvailabilityInfo(
        is_reachable=is_reachable,
        signal_strength=signal_strength,
        low_battery=low_battery,
    )

    rssi_device_dp = Mock()
    rssi_device_dp.value = rssi_device

    rssi_peer_dp = Mock()
    rssi_peer_dp.value = rssi_peer

    def get_generic_data_point(*, parameter: str | None = None, **kwargs: Any) -> Mock | None:
        """Return mock data point by parameter name."""
        if parameter == "RSSI_DEVICE":
            return rssi_device_dp if rssi_device is not None else None
        if parameter == "RSSI_PEER":
            return rssi_peer_dp if rssi_peer is not None else None
        return None

    device.get_generic_data_point = get_generic_data_point
    device.reload_device_config = AsyncMock()
    return device


def _make_mock_client(*, interface_id: str = "hmip_local-VCU0000001") -> Mock:
    """Create a mock client with command throttle."""
    client = Mock()
    client.interface_id = interface_id
    client.command_throttle.interval = 0.5
    client.command_throttle.is_enabled = True
    client.command_throttle.queue_size = 0
    client.command_throttle.throttled_count = 5
    client.command_throttle.critical_count = 1
    client.command_throttle.burst_count = 2
    client.command_throttle.burst_threshold = 5
    client.command_throttle.burst_window = 0.5
    return client


# ---------------------------------------------------------------------------
# Integration tab tests
# ---------------------------------------------------------------------------


class TestWsGetSystemHealth:
    """Tests for ws_get_system_health."""

    async def test_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test with invalid entry_id."""
        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/get_system_health",
                "entry_id": "invalid_entry_id",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_found"

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting system health data."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.health.to_dict.return_value = {
            "central_state": "CONNECTED",
            "overall_health_score": 100.0,
        }

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/get_system_health",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["central_state"] == "CONNECTED"
        assert response["result"]["overall_health_score"] == 100.0


class TestWsGetCommandThrottleStats:
    """Tests for ws_get_command_throttle_stats."""

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting command throttle statistics."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        mock_client = _make_mock_client(interface_id="hmip_rf")
        control.central.client_coordinator.clients = (mock_client,)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/get_command_throttle_stats",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        stats = response["result"]["throttle_stats"]
        assert "hmip_rf" in stats
        assert stats["hmip_rf"]["is_enabled"] is True
        assert stats["hmip_rf"]["throttled_count"] == 5


class TestWsGetIncidents:
    """Tests for ws_get_incidents."""

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting incidents."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        store = control.central.cache_coordinator.incident_store
        store.get_recent_incidents = AsyncMock(
            return_value=[{"type": "connection_loss", "severity": "error", "message": "Connection lost"}]
        )
        store.get_diagnostics = AsyncMock(
            return_value={
                "total_incidents": 1,
                "incidents_by_type": {"connection_loss": 1},
                "incidents_by_severity": {"error": 1},
            }
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/get_incidents",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert len(response["result"]["incidents"]) == 1
        assert response["result"]["summary"]["total_incidents"] == 1

    async def test_with_interface_filter(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting incidents filtered by interface."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        store = control.central.cache_coordinator.incident_store

        mock_incident = Mock()
        mock_incident.to_dict.return_value = {"type": "rpc_error", "interface_id": "hmip_rf"}
        store.get_incidents_by_interface = AsyncMock(return_value=[mock_incident])
        store.get_diagnostics = AsyncMock(
            return_value={
                "total_incidents": 1,
                "incidents_by_type": {"rpc_error": 1},
                "incidents_by_severity": {"warning": 1},
            }
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/get_incidents",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface_id": "hmip_rf",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert len(response["result"]["incidents"]) == 1

    async def test_with_limit(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting incidents with custom limit."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        store = control.central.cache_coordinator.incident_store
        store.get_recent_incidents = AsyncMock(return_value=[])
        store.get_diagnostics = AsyncMock(
            return_value={"total_incidents": 0, "incidents_by_type": {}, "incidents_by_severity": {}}
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/get_incidents",
                "entry_id": mock_loaded_config_entry.entry_id,
                "limit": 10,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        store.get_recent_incidents.assert_called_once_with(limit=10)


class TestWsClearIncidents:
    """Tests for ws_clear_incidents."""

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test clearing incidents."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/clear_incidents",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True
        control.central.cache_coordinator.incident_store.clear_incidents.assert_called_once()


class TestWsClearCache:
    """Tests for ws_clear_cache."""

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test clearing cache."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.cache_coordinator.clear_all = AsyncMock()

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/clear_cache",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True
        control.central.cache_coordinator.clear_all.assert_called_once()


class TestWsGetDeviceStatistics:
    """Tests for ws_get_device_statistics."""

    async def test_empty(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test with no devices."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        type(control.central.device_coordinator).devices = PropertyMock(return_value=())

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/get_device_statistics",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["total_devices"] == 0

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting device statistics."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device1 = _make_mock_device(
            address="VCU0000001",
            interface_id="hmip_rf",
            is_reachable=True,
            firmware_updatable=False,
        )
        device2 = _make_mock_device(
            address="VCU0000002",
            interface_id="hmip_rf",
            is_reachable=False,
            firmware_updatable=True,
        )
        device3 = _make_mock_device(
            address="VCU0000003",
            interface_id="bidcos_rf",
            is_reachable=True,
            firmware_updatable=False,
        )
        type(control.central.device_coordinator).devices = PropertyMock(return_value=(device1, device2, device3))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/integration/get_device_statistics",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["total_devices"] == 3
        assert result["unreachable_devices"] == 1
        assert result["firmware_updatable_devices"] == 1
        assert result["by_interface"]["hmip_rf"]["total"] == 2
        assert result["by_interface"]["hmip_rf"]["unreachable"] == 1
        assert result["by_interface"]["bidcos_rf"]["total"] == 1


# ---------------------------------------------------------------------------
# OpenCCU tab tests
# ---------------------------------------------------------------------------


class TestWsGetSystemInformation:
    """Tests for ws_get_system_information."""

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting CCU system information."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        central = control.central

        central.name = "TestCCU"
        central.model = "CCU3"
        central.version = "3.75.7"
        central.url = "http://192.168.1.100"

        sys_info = Mock()
        sys_info.serial = "ABC1234567"
        sys_info.hostname = "ccu3-abc"
        sys_info.ccu_type.value = "CCU"
        sys_info.auth_enabled = True
        sys_info.https_redirect_enabled = False
        sys_info.available_interfaces = ("HmIP-RF", "BidCos-RF")
        sys_info.has_backup = True
        sys_info.has_system_update = False
        central.system_information = sys_info

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/get_system_information",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["name"] == "TestCCU"
        assert result["model"] == "CCU3"
        assert result["version"] == "3.75.7"
        assert result["serial"] == "ABC1234567"
        assert result["has_backup"] is True
        assert "HmIP-RF" in result["available_interfaces"]


class TestWsCreateBackup:
    """Tests for ws_create_backup."""

    async def test_backup_exception(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test backup raising exception."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.create_backup_and_download = AsyncMock(
            side_effect=BaseHomematicException("Backup error"),
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/create_backup",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "backup_failed"

    async def test_backup_returns_none(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test backup returning None."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.create_backup_and_download = AsyncMock(return_value=None)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/create_backup",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "backup_failed"

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
        tmp_path: Any,
    ) -> None:
        """Test creating a CCU backup."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.create_backup_and_download = AsyncMock(return_value=MockBackupData())
        control.backup_directory = str(tmp_path)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/create_backup",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True
        assert response["result"]["filename"] == "backup_20260304.tar.gz"
        assert response["result"]["size"] == len(b"backup_content_data")


class TestWsGetHubData:
    """Tests for ws_get_hub_data."""

    async def test_no_messages(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting hub data with no message data points."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        type(control.central.hub_coordinator).sysvar_data_points = PropertyMock(return_value=())

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/get_hub_data",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["service_messages"] is None
        assert response["result"]["alarm_messages"] is None

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting hub data with service and alarm messages."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        sysvar_service = Mock()
        sysvar_service.name = "SERVICE_MESSAGES"
        sysvar_service.value = 3

        sysvar_alarm = Mock()
        sysvar_alarm.name = "ALARM_MESSAGES"
        sysvar_alarm.value = 1

        type(control.central.hub_coordinator).sysvar_data_points = PropertyMock(
            return_value=(sysvar_service, sysvar_alarm)
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/get_hub_data",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["service_messages"] == 3
        assert response["result"]["alarm_messages"] == 1


class TestWsGetInstallModeStatus:
    """Tests for ws_get_install_mode_status."""

    async def test_no_install_mode_dps(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test when install mode data points are not available."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        type(control.central.hub_coordinator).install_mode_dps = PropertyMock(return_value={})

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/get_install_mode_status",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["hmip"]["remaining_seconds"] is None
        assert response["result"]["hmip"]["active"] is False
        assert response["result"]["bidcos"]["remaining_seconds"] is None

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting install mode status."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        hmip_sensor = Mock()
        hmip_sensor.value = 45
        hmip_sensor.is_active = True

        bidcos_sensor = Mock()
        bidcos_sensor.value = 0
        bidcos_sensor.is_active = False

        hmip_dp = Mock()
        hmip_dp.sensor = hmip_sensor

        bidcos_dp = Mock()
        bidcos_dp.sensor = bidcos_sensor

        type(control.central.hub_coordinator).install_mode_dps = PropertyMock(
            return_value={Interface.HMIP_RF: hmip_dp, Interface.BIDCOS_RF: bidcos_dp}
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/get_install_mode_status",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["hmip"]["remaining_seconds"] == 45
        assert response["result"]["hmip"]["active"] is True
        assert response["result"]["bidcos"]["remaining_seconds"] == 0
        assert response["result"]["bidcos"]["active"] is False


class TestWsTriggerInstallMode:
    """Tests for ws_trigger_install_mode."""

    async def test_activate_exception(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test triggering install mode with exception."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        hmip_button = AsyncMock(side_effect=BaseHomematicException("Activate failed"))
        hmip_dp = Mock()
        hmip_dp.button.activate = hmip_button

        type(control.central.hub_coordinator).install_mode_dps = PropertyMock(return_value={Interface.HMIP_RF: hmip_dp})

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/trigger_install_mode",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface": "hmip",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "activate_failed"

    async def test_interface_not_available(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test triggering install mode for unavailable interface."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        type(control.central.hub_coordinator).install_mode_dps = PropertyMock(return_value={})

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/trigger_install_mode",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface": "hmip",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "not_available"

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test triggering install mode."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data

        hmip_button = AsyncMock()
        hmip_dp = Mock()
        hmip_dp.button = hmip_button

        type(control.central.hub_coordinator).install_mode_dps = PropertyMock(return_value={Interface.HMIP_RF: hmip_dp})

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/trigger_install_mode",
                "entry_id": mock_loaded_config_entry.entry_id,
                "interface": "hmip",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        hmip_button.activate.assert_called_once()


class TestWsGetSignalQuality:
    """Tests for ws_get_signal_quality."""

    async def test_no_rssi_data(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test signal quality with no RSSI data points."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device = _make_mock_device(rssi_device=None, rssi_peer=None)
        type(control.central.device_coordinator).devices = PropertyMock(return_value=(device,))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/get_signal_quality",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        devices = response["result"]["devices"]
        assert devices[0]["rssi_device"] is None
        assert devices[0]["rssi_peer"] is None

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting signal quality data."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device = _make_mock_device(
            rssi_device=-70,
            rssi_peer=-72,
            signal_strength=-65,
        )
        type(control.central.device_coordinator).devices = PropertyMock(return_value=(device,))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/get_signal_quality",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        devices = response["result"]["devices"]
        assert len(devices) == 1
        assert devices[0]["rssi_device"] == -70
        assert devices[0]["rssi_peer"] == -72
        assert devices[0]["signal_strength"] == -65


class TestWsGetFirmwareOverview:
    """Tests for ws_get_firmware_overview."""

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test getting firmware overview."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        device1 = _make_mock_device(
            address="VCU0000001",
            firmware="1.0.0",
            available_firmware="1.1.0",
            firmware_updatable=True,
            firmware_update_state=DeviceFirmwareState.NEW_FIRMWARE_AVAILABLE,
        )
        device2 = _make_mock_device(
            address="VCU0000002",
            firmware="2.0.0",
            firmware_updatable=False,
        )
        type(control.central.device_coordinator).devices = PropertyMock(return_value=(device1, device2))

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/get_firmware_overview",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        result = response["result"]
        assert result["summary"]["total_devices"] == 2
        assert result["summary"]["firmware_updatable"] == 1
        assert len(result["devices"]) == 2
        assert result["devices"][0]["firmware"] == "1.0.0"
        assert result["devices"][0]["available_firmware"] == "1.1.0"
        assert result["devices"][0]["firmware_update_state"] == "NEW_FIRMWARE_AVAILABLE"


class TestWsRefreshFirmwareData:
    """Tests for ws_refresh_firmware_data."""

    async def test_exception(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test refreshing firmware data with exception."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.device_coordinator.refresh_firmware_data = AsyncMock(
            side_effect=BaseHomematicException("Refresh failed"),
        )

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/refresh_firmware_data",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "refresh_failed"

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test refreshing firmware data."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.device_coordinator.refresh_firmware_data = AsyncMock()

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/refresh_firmware_data",
                "entry_id": mock_loaded_config_entry.entry_id,
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True


class TestWsReloadDeviceConfig:
    """Tests for ws_reload_device_config."""

    async def test_device_not_found(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test reloading config for non-existent device."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        control.central.device_coordinator.get_device = Mock(return_value=None)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/reload_device_config",
                "entry_id": mock_loaded_config_entry.entry_id,
                "device_address": "VCU_INVALID",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "device_not_found"

    async def test_reload_exception(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test reloading device config with exception."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        mock_device = _make_mock_device()
        mock_device.reload_device_config = AsyncMock(side_effect=BaseHomematicException("Reload failed"))
        control.central.device_coordinator.get_device = Mock(return_value=mock_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/reload_device_config",
                "entry_id": mock_loaded_config_entry.entry_id,
                "device_address": "VCU0000001",
            }
        )

        response = await client.receive_json()
        assert response["success"] is False
        assert response["error"]["code"] == "reload_failed"

    async def test_success(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry: MockConfigEntry,
        hass_ws_client: Any,
    ) -> None:
        """Test reloading device config."""
        control: ControlUnit = mock_loaded_config_entry.runtime_data
        mock_device = _make_mock_device()
        control.central.device_coordinator.get_device = Mock(return_value=mock_device)

        client = await hass_ws_client(hass)
        await client.send_json(
            {
                "id": 1,
                "type": "homematicip_local/ccu/reload_device_config",
                "entry_id": mock_loaded_config_entry.entry_id,
                "device_address": "VCU0000001",
            }
        )

        response = await client.receive_json()
        assert response["success"] is True
        assert response["result"]["success"] is True
        mock_device.reload_device_config.assert_called_once()
