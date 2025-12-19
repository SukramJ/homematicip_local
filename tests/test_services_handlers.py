"""
Tests for service handler functions in custom_components.homematicip_local.services.

This module tests the actual service handler implementations to improve coverage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest

from aiohomematic.const import ForcedDeviceAvailability, ParamsetKey
from aiohomematic.exceptions import BaseHomematicException
from custom_components.homematicip_local.control_unit import ControlUnit
import custom_components.homematicip_local.services as hm_services
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from tests import const


class MockServiceCall:
    """Mock ServiceCall for testing."""

    def __init__(self, service: str, data: dict[str, Any], domain: str = "homematicip_local") -> None:
        """Initialize mock service call."""
        self.service = service
        self.data = data
        self.domain = domain
        self.context = type("_Ctx", (), {"user_id": None})()


@pytest.fixture
def mock_hm_device():
    """Create a mock HM device."""
    device = Mock()
    device.address = "VCU1234567"
    device.name = "Test Device"
    device.client = Mock()
    device.client.add_link = AsyncMock()
    device.client.remove_link = AsyncMock()
    device.client.get_value = AsyncMock(return_value=42)
    device.client.get_link_peers = AsyncMock(return_value=["peer1", "peer2"])
    device.client.get_paramset = AsyncMock(return_value={"PARAM1": 1, "PARAM2": 2})
    device.client.put_paramset = AsyncMock()
    device.client.set_value = AsyncMock()
    device.create_central_links = AsyncMock()
    device.remove_central_links = AsyncMock()
    device.export_device_definition = AsyncMock()
    device.set_forced_availability = Mock()
    return device


@pytest.fixture
def mock_control_unit():
    """Create a mock control unit."""
    control = Mock(spec=ControlUnit)
    control.central = Mock()
    control.central.device_coordinator = Mock()
    control.central.device_coordinator.create_central_links = AsyncMock()
    control.central.device_coordinator.remove_central_links = AsyncMock()
    control.central.device_coordinator.get_device = Mock(return_value=None)
    control.central.device_coordinator.refresh_firmware_data = AsyncMock()
    control.central.hub_coordinator = Mock()
    control.central.hub_coordinator.get_system_variable = AsyncMock(return_value="test_value")
    control.central.hub_coordinator.set_system_variable = AsyncMock()
    control.central.hub_coordinator.fetch_program_data = AsyncMock()
    control.central.hub_coordinator.fetch_sysvar_data = AsyncMock()
    control.central.cache_coordinator = Mock()
    control.central.cache_coordinator.clear_all = AsyncMock()
    control.central.cache_coordinator.recorder = Mock()
    control.central.cache_coordinator.recorder.activate = AsyncMock()
    control.central.client_coordinator = Mock()
    control.central.client_coordinator.has_client = Mock(return_value=False)
    control.central.create_backup_and_download = AsyncMock()
    control.backup_directory = "backups"  # noqa: S108
    return control


class TestServiceAddLink:
    """Tests for _async_service_add_link."""

    @pytest.mark.asyncio
    async def test_add_link_default_name(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test link creation with default name."""
        service = MockServiceCall(
            service="add_link",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_add_link(hass=hass, service=service)

        mock_hm_device.client.add_link.assert_called_once_with(
            sender_address="VCU1234567:1",
            receiver_address="VCU7654321:1",
            name="VCU1234567:1 -> VCU7654321:1",
            description="created by HA",
        )

    @pytest.mark.asyncio
    async def test_add_link_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test link creation with exception."""
        mock_hm_device.client.add_link.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="add_link",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
            },
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_add_link(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_add_link_success(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test successful link creation."""
        service = MockServiceCall(
            service="add_link",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
                hm_services.CONF_NAME: "Test Link",
                hm_services.CONF_DESCRIPTION: "Test Description",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_add_link(hass=hass, service=service)

        mock_hm_device.client.add_link.assert_called_once_with(
            sender_address="VCU1234567:1",
            receiver_address="VCU7654321:1",
            name="Test Link",
            description="Test Description",
        )


class TestServiceCreateCentralLink:
    """Tests for _async_service_create_central_link."""

    @pytest.mark.asyncio
    async def test_create_central_link_by_device(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test central link creation by device."""
        service = MockServiceCall(
            service="create_central_links",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with (
            patch.object(hm_services, "_async_get_control_unit", return_value=None),
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
        ):
            await hm_services._async_service_create_central_link(hass=hass, service=service)

        mock_hm_device.create_central_links.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_central_link_by_entry_id(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test central link creation by entry_id."""
        service = MockServiceCall(
            service="create_central_links",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            await hm_services._async_service_create_central_link(hass=hass, service=service)

        mock_control_unit.central.device_coordinator.create_central_links.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_central_link_exception(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test central link creation with exception."""
        mock_control_unit.central.device_coordinator.create_central_links.side_effect = BaseHomematicException(
            "Test error"
        )

        service = MockServiceCall(
            service="create_central_links",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with (
            patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_create_central_link(hass=hass, service=service)


class TestServiceRemoveCentralLink:
    """Tests for _async_service_remove_central_link."""

    @pytest.mark.asyncio
    async def test_remove_central_link_by_device(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test central link removal by device."""
        service = MockServiceCall(
            service="remove_central_links",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with (
            patch.object(hm_services, "_async_get_control_unit", return_value=None),
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
        ):
            await hm_services._async_service_remove_central_link(hass=hass, service=service)

        mock_hm_device.remove_central_links.assert_called_once()

    @pytest.mark.asyncio
    async def test_remove_central_link_by_entry_id(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test central link removal by entry_id."""
        service = MockServiceCall(
            service="remove_central_links",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            await hm_services._async_service_remove_central_link(hass=hass, service=service)

        mock_control_unit.central.device_coordinator.remove_central_links.assert_called_once()

    @pytest.mark.asyncio
    async def test_remove_central_link_exception(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test central link removal with exception."""
        mock_control_unit.central.device_coordinator.remove_central_links.side_effect = BaseHomematicException(
            "Test error"
        )

        service = MockServiceCall(
            service="remove_central_links",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with (
            patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_remove_central_link(hass=hass, service=service)


class TestServiceRemoveLink:
    """Tests for _async_service_remove_link."""

    @pytest.mark.asyncio
    async def test_remove_link_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test link removal with exception."""
        mock_hm_device.client.remove_link.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="remove_link",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
            },
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_remove_link(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_remove_link_success(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test successful link removal."""
        service = MockServiceCall(
            service="remove_link",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_remove_link(hass=hass, service=service)

        mock_hm_device.client.remove_link.assert_called_once_with(
            sender_address="VCU1234567:1",
            receiver_address="VCU7654321:1",
        )


class TestServiceExportDeviceDefinition:
    """Tests for _async_service_export_device_definition."""

    @pytest.mark.asyncio
    async def test_export_device_definition_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test device definition export with exception."""
        mock_hm_device.export_device_definition.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="export_device_definition",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_export_device_definition(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_export_device_definition_success(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test successful device definition export."""
        service = MockServiceCall(
            service="export_device_definition",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_export_device_definition(hass=hass, service=service)

        mock_hm_device.export_device_definition.assert_called_once()


class TestServiceForceDeviceAvailability:
    """Tests for _async_service_force_device_availability."""

    @pytest.mark.asyncio
    async def test_force_device_availability_success(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test successful force device availability."""
        service = MockServiceCall(
            service="force_device_availability",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_force_device_availability(hass=hass, service=service)

        mock_hm_device.set_forced_availability.assert_called_once_with(
            forced_availability=ForcedDeviceAvailability.FORCE_TRUE
        )


class TestServiceGetDeviceValue:
    """Tests for _async_service_get_device_value."""

    @pytest.mark.asyncio
    async def test_get_device_value_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get device value with exception."""
        mock_hm_device.client.get_value.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="get_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "STATE",
            },
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_get_device_value(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_get_device_value_none(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get device value returns None."""
        mock_hm_device.client.get_value.return_value = None

        service = MockServiceCall(
            service="get_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "STATE",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            result = await hm_services._async_service_get_device_value(hass=hass, service=service)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_device_value_success(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test successful get device value."""
        mock_hm_device.client.get_value.return_value = 42

        service = MockServiceCall(
            service="get_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "STATE",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            result = await hm_services._async_service_get_device_value(hass=hass, service=service)

        assert result == {"result": 42}
        mock_hm_device.client.get_value.assert_called_once_with(
            channel_address="VCU1234567:1",
            paramset_key=ParamsetKey.VALUES,
            parameter="STATE",
        )


class TestServiceGetLinkPeers:
    """Tests for _async_service_get_link_peers."""

    @pytest.mark.asyncio
    async def test_get_link_peers_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get link peers with exception."""
        mock_hm_device.client.get_link_peers.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="get_link_peers",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_get_link_peers(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_get_link_peers_with_channel(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get link peers with channel."""
        mock_hm_device.client.get_link_peers.return_value = ["peer1", "peer2"]

        service = MockServiceCall(
            service="get_link_peers",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            result = await hm_services._async_service_get_link_peers(hass=hass, service=service)

        assert result == {"VCU1234567:1": ["peer1", "peer2"]}

    @pytest.mark.asyncio
    async def test_get_link_peers_without_channel(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get link peers without channel."""
        mock_hm_device.client.get_link_peers.return_value = ["peer1"]

        service = MockServiceCall(
            service="get_link_peers",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            result = await hm_services._async_service_get_link_peers(hass=hass, service=service)

        assert result == {"VCU1234567": ["peer1"]}


class TestServiceGetLinkParamset:
    """Tests for _async_service_get_link_paramset."""

    @pytest.mark.asyncio
    async def test_get_link_paramset_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get link paramset with exception."""
        mock_hm_device.client.get_paramset.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="get_link_paramset",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
            },
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_get_link_paramset(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_get_link_paramset_success(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test successful get link paramset."""
        mock_hm_device.client.get_paramset.return_value = {"PARAM1": 1}

        service = MockServiceCall(
            service="get_link_paramset",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            result = await hm_services._async_service_get_link_paramset(hass=hass, service=service)

        assert result == {"PARAM1": 1}


class TestServiceGetParamset:
    """Tests for _async_service_get_paramset."""

    @pytest.mark.asyncio
    async def test_get_paramset_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get paramset with exception."""
        mock_hm_device.client.get_paramset.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="get_paramset",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_PARAMSET_KEY: "VALUES",
            },
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_get_paramset(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_get_paramset_with_channel(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get paramset with channel."""
        mock_hm_device.client.get_paramset.return_value = {"PARAM1": 1, "PARAM2": 2}

        service = MockServiceCall(
            service="get_paramset",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMSET_KEY: "MASTER",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            result = await hm_services._async_service_get_paramset(hass=hass, service=service)

        assert result == {"PARAM1": 1, "PARAM2": 2}

    @pytest.mark.asyncio
    async def test_get_paramset_without_channel(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get paramset without channel."""
        mock_hm_device.client.get_paramset.return_value = {"PARAM1": 1}

        service = MockServiceCall(
            service="get_paramset",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_PARAMSET_KEY: "VALUES",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            result = await hm_services._async_service_get_paramset(hass=hass, service=service)

        assert result == {"PARAM1": 1}


class TestServiceGetVariableValue:
    """Tests for _async_service_get_variable_value."""

    @pytest.mark.asyncio
    async def test_get_variable_value_exception(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test get variable value with exception."""
        mock_control_unit.central.hub_coordinator.get_system_variable.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="get_variable_value",
            data={
                hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID,
                hm_services.CONF_NAME: "test_var",
            },
        )

        with (
            patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_get_variable_value(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_get_variable_value_none(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test get variable value returns None."""
        mock_control_unit.central.hub_coordinator.get_system_variable.return_value = None

        service = MockServiceCall(
            service="get_variable_value",
            data={
                hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID,
                hm_services.CONF_NAME: "test_var",
            },
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            result = await hm_services._async_service_get_variable_value(hass=hass, service=service)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_variable_value_success(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test successful get variable value."""
        mock_control_unit.central.hub_coordinator.get_system_variable.return_value = "test_value"

        service = MockServiceCall(
            service="get_variable_value",
            data={
                hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID,
                hm_services.CONF_NAME: "test_var",
            },
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            result = await hm_services._async_service_get_variable_value(hass=hass, service=service)

        assert result == {"result": "test_value"}


class TestServiceSetDeviceValue:
    """Tests for _async_service_set_device_value."""

    @pytest.mark.asyncio
    async def test_set_device_value_boolean(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test set device value with boolean type."""
        service = MockServiceCall(
            service="set_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "STATE",
                hm_services.CONF_VALUE: "true",
                hm_services.CONF_VALUE_TYPE: "boolean",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_set_device_value(hass=hass, service=service)

        mock_hm_device.client.set_value.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_device_value_datetime(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test set device value with datetime type."""
        service = MockServiceCall(
            service="set_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "TIMESTAMP",
                hm_services.CONF_VALUE: "20231015T10:30:00",
                hm_services.CONF_VALUE_TYPE: "dateTime.iso8601",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_set_device_value(hass=hass, service=service)

        mock_hm_device.client.set_value.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_device_value_double(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test set device value with double type."""
        service = MockServiceCall(
            service="set_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "TEMPERATURE",
                hm_services.CONF_VALUE: "21.5",
                hm_services.CONF_VALUE_TYPE: "double",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_set_device_value(hass=hass, service=service)

        mock_hm_device.client.set_value.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_device_value_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test set device value with exception."""
        mock_hm_device.client.set_value.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="set_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "STATE",
                hm_services.CONF_VALUE: True,
            },
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_set_device_value(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_set_device_value_int(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test set device value with int type."""
        service = MockServiceCall(
            service="set_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "LEVEL",
                hm_services.CONF_VALUE: "42",
                hm_services.CONF_VALUE_TYPE: "int",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_set_device_value(hass=hass, service=service)

        mock_hm_device.client.set_value.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_device_value_string(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test set device value with string type."""
        service = MockServiceCall(
            service="set_device_value",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMETER: "STATE",
                hm_services.CONF_VALUE: "test",
                hm_services.CONF_VALUE_TYPE: "string",
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_set_device_value(hass=hass, service=service)

        mock_hm_device.client.set_value.assert_called_once()


class TestServiceSetVariableValue:
    """Tests for _async_service_set_variable_value."""

    @pytest.mark.asyncio
    async def test_set_variable_value_success(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test successful set variable value."""
        service = MockServiceCall(
            service="set_variable_value",
            data={
                hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID,
                hm_services.CONF_NAME: "test_var",
                hm_services.CONF_VALUE: "new_value",
            },
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            await hm_services._async_service_set_variable_value(hass=hass, service=service)

        mock_control_unit.central.hub_coordinator.set_system_variable.assert_called_once_with(
            legacy_name="test_var", value="new_value"
        )


class TestServiceClearCache:
    """Tests for _async_service_clear_cache."""

    @pytest.mark.asyncio
    async def test_clear_cache_success(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test successful cache clear."""
        service = MockServiceCall(
            service="clear_cache",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            await hm_services._async_service_clear_cache(hass=hass, service=service)

        mock_control_unit.central.cache_coordinator.clear_all.assert_called_once()


class TestServiceFetchSystemVariables:
    """Tests for _async_service_fetch_system_variables."""

    @pytest.mark.asyncio
    async def test_fetch_system_variables_success(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test successful fetch system variables."""
        service = MockServiceCall(
            service="fetch_system_variables",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            await hm_services._async_service_fetch_system_variables(hass=hass, service=service)

        mock_control_unit.central.hub_coordinator.fetch_program_data.assert_called_once_with(scheduled=False)
        mock_control_unit.central.hub_coordinator.fetch_sysvar_data.assert_called_once_with(scheduled=False)


class TestServicePutLinkParamset:
    """Tests for _async_service_put_link_paramset."""

    @pytest.mark.asyncio
    async def test_put_link_paramset_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test put link paramset with exception."""
        mock_hm_device.client.put_paramset.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="put_link_paramset",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
                hm_services.CONF_PARAMSET: {"PARAM1": 1},
            },
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_put_link_paramset(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_put_link_paramset_success(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test successful put link paramset."""
        service = MockServiceCall(
            service="put_link_paramset",
            data={
                hm_services.CONF_SENDER_CHANNEL_ADDRESS: "VCU1234567:1",
                hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU7654321:1",
                hm_services.CONF_PARAMSET: {"PARAM1": 1},
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_put_link_paramset(hass=hass, service=service)

        mock_hm_device.client.put_paramset.assert_called_once()


class TestServicePutParamset:
    """Tests for _async_service_put_paramset."""

    @pytest.mark.asyncio
    async def test_put_paramset_exception(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test put paramset with exception."""
        mock_hm_device.client.put_paramset.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="put_paramset",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_PARAMSET_KEY: "VALUES",
                hm_services.CONF_PARAMSET: {"STATE": True},
            },
        )

        with (
            patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_put_paramset(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_put_paramset_with_channel(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test put paramset with channel."""
        service = MockServiceCall(
            service="put_paramset",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_CHANNEL: 1,
                hm_services.CONF_PARAMSET_KEY: "VALUES",
                hm_services.CONF_PARAMSET: {"STATE": True},
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_put_paramset(hass=hass, service=service)

        mock_hm_device.client.put_paramset.assert_called_once()

    @pytest.mark.asyncio
    async def test_put_paramset_without_channel(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test put paramset without channel."""
        service = MockServiceCall(
            service="put_paramset",
            data={
                hm_services.CONF_DEVICE_ID: "device_123",
                hm_services.CONF_PARAMSET_KEY: "MASTER",
                hm_services.CONF_PARAMSET: {"PARAM1": 1},
            },
        )

        with patch.object(hm_services, "_async_get_hm_device_by_service_data", return_value=mock_hm_device):
            await hm_services._async_service_put_paramset(hass=hass, service=service)

        mock_hm_device.client.put_paramset.assert_called_once()


class TestServiceRecordSession:
    """Tests for _async_service_record_session."""

    @pytest.mark.asyncio
    async def test_record_session_success(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test successful record session."""
        service = MockServiceCall(
            service="record_session",
            data={
                hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID,
                hm_services.CONF_ON_TIME: 60,
                hm_services.CONF_RANDOMIZE_OUTPUT: True,
            },
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            await hm_services._async_service_record_session(hass=hass, service=service)

        mock_control_unit.central.cache_coordinator.recorder.activate.assert_called_once_with(
            on_time=60, auto_save=True, randomize_output=True, use_ts_in_file_name=True
        )


class TestServiceUpdateDeviceFirmwareData:
    """Tests for _async_service_update_device_firmware_data."""

    @pytest.mark.asyncio
    async def test_update_device_firmware_data_success(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test successful update device firmware data."""
        service = MockServiceCall(
            service="update_device_firmware_data",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit):
            await hm_services._async_service_update_device_firmware_data(hass=hass, service=service)

        mock_control_unit.central.device_coordinator.refresh_firmware_data.assert_called_once()


class TestServiceCreateCcuBackup:
    """Tests for _async_service_create_ccu_backup."""

    @pytest.mark.asyncio
    async def test_create_ccu_backup_exception(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test CCU backup creation with exception."""
        mock_control_unit.central.create_backup_and_download.side_effect = BaseHomematicException("Test error")

        service = MockServiceCall(
            service="create_ccu_backup",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with (
            patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit),
            pytest.raises(HomeAssistantError),
        ):
            await hm_services._async_service_create_ccu_backup(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_create_ccu_backup_no_data(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test CCU backup creation with no data returned."""
        mock_control_unit.central.create_backup_and_download.return_value = None

        service = MockServiceCall(
            service="create_ccu_backup",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with (
            patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit),
            pytest.raises(HomeAssistantError, match="Failed to create and download backup"),
        ):
            await hm_services._async_service_create_ccu_backup(hass=hass, service=service)

    @pytest.mark.asyncio
    async def test_create_ccu_backup_success(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test successful CCU backup creation."""
        backup_data = Mock()
        backup_data.filename = "test_backup.sbk"
        backup_data.content = b"backup_content"
        mock_control_unit.central.create_backup_and_download.return_value = backup_data

        service = MockServiceCall(
            service="create_ccu_backup",
            data={hm_services.CONF_ENTRY_ID: const.CONFIG_ENTRY_ID},
        )

        with (
            patch.object(hm_services, "_async_get_control_unit", return_value=mock_control_unit),
            patch.object(Path, "mkdir"),
            patch.object(Path, "write_bytes"),
        ):
            result = await hm_services._async_service_create_ccu_backup(hass=hass, service=service)

        assert result["success"] is True
        assert result["filename"] == "test_backup.sbk"
        assert result["size"] == 14


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_get_control_unit_no_runtime_data(self, hass: HomeAssistant) -> None:
        """Test get control unit when entry has no runtime data."""
        mock_entry = Mock()
        mock_entry.runtime_data = None

        with patch.object(hass.config_entries, "async_get_entry", return_value=mock_entry):
            result = hm_services._async_get_control_unit(hass=hass, entry_id=const.CONFIG_ENTRY_ID)

        assert result is None

    def test_get_control_unit_not_found(self, hass: HomeAssistant) -> None:
        """Test get control unit when not found."""
        with patch.object(hass.config_entries, "async_get_entry", return_value=None):
            result = hm_services._async_get_control_unit(hass=hass, entry_id="invalid_entry")

        assert result is None

    def test_get_control_unit_success(self, hass: HomeAssistant, mock_control_unit: Mock) -> None:
        """Test get control unit success."""
        mock_entry = Mock()
        mock_entry.runtime_data = mock_control_unit

        with patch.object(hass.config_entries, "async_get_entry", return_value=mock_entry):
            result = hm_services._async_get_control_unit(hass=hass, entry_id=const.CONFIG_ENTRY_ID)

        assert result == mock_control_unit

    @pytest.mark.asyncio
    async def test_get_hm_device_by_service_data_by_channel_address(
        self, hass: HomeAssistant, mock_hm_device: Mock
    ) -> None:
        """Test get hm device by channel_address."""
        service = MockServiceCall(
            service="test",
            data={hm_services.CONF_CHANNEL_ADDRESS: "VCU1234567:1"},
        )

        with patch.object(hm_services, "_async_get_hm_device_by_address", return_value=mock_hm_device):
            result = hm_services._async_get_hm_device_by_service_data(hass=hass, service=service)

        assert result == mock_hm_device

    @pytest.mark.asyncio
    async def test_get_hm_device_by_service_data_by_device_address(
        self, hass: HomeAssistant, mock_hm_device: Mock
    ) -> None:
        """Test get hm device by device_address."""
        service = MockServiceCall(
            service="test",
            data={hm_services.CONF_DEVICE_ADDRESS: "VCU1234567"},
        )

        with patch.object(hm_services, "_async_get_hm_device_by_address", return_value=mock_hm_device):
            result = hm_services._async_get_hm_device_by_service_data(hass=hass, service=service)

        assert result == mock_hm_device

    @pytest.mark.asyncio
    async def test_get_hm_device_by_service_data_by_device_id(self, hass: HomeAssistant, mock_hm_device: Mock) -> None:
        """Test get hm device by device_id."""
        service = MockServiceCall(
            service="test",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with patch.object(hm_services, "_asnyc_get_hm_device_by_id", return_value=mock_hm_device):
            result = hm_services._async_get_hm_device_by_service_data(hass=hass, service=service)

        assert result == mock_hm_device

    @pytest.mark.asyncio
    async def test_get_hm_device_by_service_data_by_receiver_channel_address(
        self, hass: HomeAssistant, mock_hm_device: Mock
    ) -> None:
        """Test get hm device by receiver_channel_address."""
        service = MockServiceCall(
            service="test",
            data={hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "VCU1234567:1"},
        )

        with patch.object(hm_services, "_async_get_hm_device_by_address", return_value=mock_hm_device):
            result = hm_services._async_get_hm_device_by_service_data(hass=hass, service=service)

        assert result == mock_hm_device

    @pytest.mark.asyncio
    async def test_get_hm_device_by_service_data_not_found(self, hass: HomeAssistant) -> None:
        """Test get hm device when not found."""
        service = MockServiceCall(
            service="test",
            data={hm_services.CONF_DEVICE_ID: "device_123"},
        )

        with (
            patch.object(hm_services, "_asnyc_get_hm_device_by_id", return_value=None),
            pytest.raises(HomeAssistantError, match="No device found"),
        ):
            hm_services._async_get_hm_device_by_service_data(hass=hass, service=service)
