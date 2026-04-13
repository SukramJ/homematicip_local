"""Tests for the generic entity base class."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.control_unit import ControlUnit
from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity

# pylint: disable=protected-access


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
    mock_device.identifier = "TEST_DEVICE"
    mock_device.manufacturer = "eQ-3"
    mock_device.model = "HmIP-PSM"
    mock_device.model_description = "Pluggable Switch and Meter"
    mock_device.address = "ABC1234567"
    mock_device.firmware = "1.0.0"
    mock_device.room = "Living Room"
    mock_device.interface_id = "test_interface"
    mock_device.has_sub_devices = False

    mock_central_info = MagicMock()
    mock_central_info.configure_mock(name="test_central")
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


class TestHaDeviceName:
    """Tests for _ha_device_name property."""

    def test_non_schedule_device_name(self) -> None:
        """Test that non-schedule device name is just the device name."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SWITCH,
            device_name="HmIP-PSM Test",
        )
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicGenericEntity(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        assert entity._ha_device_name == "HmIP-PSM Test"

    @pytest.mark.parametrize(
        "category",
        [
            DataPointCategory.SCHEDULE_SWITCH,
            DataPointCategory.WEEK_PROFILE,
        ],
    )
    def test_schedule_device_name_contains_schedule(
        self,
        category: DataPointCategory,
    ) -> None:
        """Test that schedule device name contains 'Schedule' regardless of enable_sub_devices."""
        mock_dp = _create_mock_data_point(category=category, device_name="HmIP-PSM Test")
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicGenericEntity(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        assert "Schedule" in entity._ha_device_name or "Zeitplan" in entity._ha_device_name

    def test_schedule_device_name_fallback_to_schedule(self) -> None:
        """Test that schedule device name falls back to 'Schedule' when no translation."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SCHEDULE_SWITCH,
            device_name="HmIP-PSM Test",
        )
        # Use a locale that has no translation
        mock_dp.device.config_provider.config.locale = "xx"
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicGenericEntity(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        assert entity._ha_device_name == "HmIP-PSM Test Schedule"

    def test_schedule_device_name_uses_translation(self) -> None:
        """Test that schedule device name uses CCU translation when available."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SCHEDULE_SWITCH,
            device_name="HmIP-PSM Test",
        )
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)

        with (
            patch(
                "custom_components.homematicip_local.generic_entity.get_data_point",
                side_effect=lambda data_point: data_point,
            ),
            patch(
                "custom_components.homematicip_local.generic_entity.ccu_translations.get_parameter_translation",
                return_value="Zeitplan",
            ) as mock_translation,
        ):
            entity = AioHomematicGenericEntity(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

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

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicGenericEntity(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        assert "Schedule" in entity._ha_device_name or "Zeitplan" in entity._ha_device_name
