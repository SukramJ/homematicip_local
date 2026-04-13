"""Tests for the generic entity base class."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.const import DOMAIN
from custom_components.homematicip_local.control_unit import ControlUnit
from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity

# pylint: disable=protected-access

_DEVICE_IDENTIFIER = "TEST_DEVICE"
_CENTRAL_NAME = "test_central"


def _create_mock_data_point(
    *,
    category: DataPointCategory = DataPointCategory.SWITCH,
    device_name: str = "HmIP-PSM Test",
) -> MagicMock:
    """Create a mock data point for testing."""
    mock_dp = MagicMock()
    mock_dp.category = category
    mock_dp.unique_id = "test_unique_id"
    mock_dp.full_name = f"{device_name} Switch"
    mock_dp.available = True
    mock_dp.enabled_default = True
    mock_dp.is_valid = True
    mock_dp.additional_information = {}
    mock_dp.is_in_multiple_channels = False
    mock_dp.name_data = MagicMock()
    mock_dp.name_data.parameter_name = None

    # Device mock
    mock_device = MagicMock()
    mock_device.configure_mock(name=device_name)
    mock_device.identifier = _DEVICE_IDENTIFIER
    mock_device.manufacturer = "eQ-3"
    mock_device.model = "HmIP-PSM"
    mock_device.model_description = "Pluggable Switch and Meter"
    mock_device.address = "ABC1234567"
    mock_device.firmware = "1.0.0"
    mock_device.room = "Living Room"
    mock_device.interface_id = "test_interface"
    mock_device.has_sub_devices = False

    mock_central_info = MagicMock()
    mock_central_info.configure_mock(name=_CENTRAL_NAME)
    mock_device.central_info = mock_central_info

    mock_config = MagicMock()
    mock_config.locale = "de"
    mock_device.config_provider.config = mock_config

    mock_dp.device = mock_device

    mock_channel = MagicMock()
    mock_channel.address = "ABC1234567:1"
    mock_channel.is_in_multi_group = False
    mock_dp.channel = mock_channel

    return mock_dp


def _create_mock_control_unit(*, enable_sub_devices: bool = False) -> MagicMock:
    """Create a mock control unit."""
    mock_cu = MagicMock(spec=ControlUnit)
    mock_cu.enable_sub_devices = enable_sub_devices
    mock_cu.disable_config_panel = True
    return mock_cu


def _create_entity(
    *,
    mock_dp: MagicMock,
    mock_cu: MagicMock,
) -> AioHomematicGenericEntity:
    """Create an AioHomematicGenericEntity with patched get_data_point."""
    with patch(
        "custom_components.homematicip_local.generic_entity.get_data_point",
        side_effect=lambda data_point: data_point,
    ):
        return AioHomematicGenericEntity(
            control_unit=mock_cu,
            data_point=mock_dp,
        )


class TestHaDeviceName:
    """Tests for _ha_device_name property."""

    def test_non_schedule_device_name(self) -> None:
        """Test that non-schedule device name is just the device name."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SWITCH,
            device_name="HmIP-PSM Test",
        )
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        assert entity._ha_device_name == "HmIP-PSM Test"

    def test_non_schedule_device_name_sub_devices_disabled(self) -> None:
        """Test that device name is plain when sub devices are disabled."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SCHEDULE_SWITCH,
            device_name="HmIP-PSM Test",
        )
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        # Without sub devices, schedule entities are on the main device
        assert entity._ha_device_name == "HmIP-PSM Test"

    def test_schedule_device_name_fallback_to_schedule(self) -> None:
        """Test that schedule device name falls back to 'Schedule' when no translation."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SCHEDULE_SWITCH,
            device_name="HmIP-PSM Test",
        )
        # Use a locale that has no translation
        mock_dp.device.config_provider.config.locale = "xx"
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        assert entity._ha_device_name == "HmIP-PSM Test Schedule"

    def test_schedule_device_name_uses_translation(self) -> None:
        """Test that schedule device name uses CCU translation when available."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SCHEDULE_SWITCH,
            device_name="HmIP-PSM Test",
        )
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)

        with patch(
            "custom_components.homematicip_local.generic_entity.ccu_translations.get_parameter_translation",
            return_value="Zeitplan",
        ) as mock_translation:
            entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        mock_translation.assert_called_once_with(
            parameter="SCHEDULE_CHANNEL_SWITCH",
            locale="de",
        )
        assert entity._ha_device_name == "HmIP-PSM Test Zeitplan"

    @pytest.mark.parametrize(
        "category",
        [
            DataPointCategory.SCHEDULE_SWITCH,
            DataPointCategory.WEEK_PROFILE,
        ],
    )
    def test_schedule_device_name_with_sub_devices_enabled(
        self,
        category: DataPointCategory,
    ) -> None:
        """Test that schedule device name contains 'Schedule' when sub devices are enabled."""
        mock_dp = _create_mock_data_point(category=category, device_name="HmIP-PSM Test")
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        assert "Schedule" in entity._ha_device_name or "Zeitplan" in entity._ha_device_name


class TestScheduleSubdevice:
    """Tests for schedule sub-device creation logic."""

    def test_non_schedule_no_subdevice(self) -> None:
        """Test that non-schedule entities do not create a sub-device."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SWITCH)
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        assert device_info["identifiers"] == {(DOMAIN, _DEVICE_IDENTIFIER)}
        assert device_info["via_device"] == (DOMAIN, _CENTRAL_NAME)

    @pytest.mark.parametrize(
        "category",
        [
            DataPointCategory.SCHEDULE_SWITCH,
            DataPointCategory.WEEK_PROFILE,
        ],
    )
    def test_schedule_creates_subdevice_when_sub_devices_enabled(
        self,
        category: DataPointCategory,
    ) -> None:
        """Test that a separate schedule sub-device is created when sub devices are enabled."""
        mock_dp = _create_mock_data_point(category=category)
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        assert device_info["identifiers"] == {(DOMAIN, f"{_DEVICE_IDENTIFIER}-schedule")}
        assert device_info["via_device"] == (DOMAIN, _DEVICE_IDENTIFIER)

    @pytest.mark.parametrize(
        "category",
        [
            DataPointCategory.SCHEDULE_SWITCH,
            DataPointCategory.WEEK_PROFILE,
        ],
    )
    def test_schedule_no_subdevice_when_sub_devices_disabled(
        self,
        category: DataPointCategory,
    ) -> None:
        """Test that no separate schedule sub-device is created when sub devices are disabled."""
        mock_dp = _create_mock_data_point(category=category)
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        # Entity stays on main device, not a separate schedule sub-device
        assert device_info["identifiers"] == {(DOMAIN, _DEVICE_IDENTIFIER)}
        assert device_info["via_device"] == (DOMAIN, _CENTRAL_NAME)
