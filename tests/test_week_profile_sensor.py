"""Tests for the week profile sensor entity."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from aiohomematic.const import DataPointCategory, ScheduleProfile, ScheduleType
from aiohomematic.interfaces import ClimateWeekProfileDataPointProtocol, WeekProfileDataPointProtocol
from aiohomematic.model.week_profile_data_point import WeekProfileDataPoint
from custom_components.homematicip_local import HAHM_VERSION
from custom_components.homematicip_local.control_unit import ControlUnit, signal_new_data_point
from custom_components.homematicip_local.sensor import AioHomematicWeekProfileSensor
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

# pylint: disable=protected-access


@pytest.fixture(autouse=True)
def patch_aiohomematic_version() -> Generator[None]:
    """Patch aiohomematic version check for all tests in this module."""
    with patch(
        "custom_components.homematicip_local.get_aiohomematic_version",
        return_value=HAHM_VERSION,
    ):
        yield


def _create_mock_data_point(
    *,
    is_climate: bool = False,
    value: int = 5,
    schedule_type: ScheduleType = ScheduleType.DEFAULT,
    max_entries: int = 24,
    schedule_channel_address: str | None = "ABC1234567:1",
    schedule: dict | None = None,
    active_schedule: dict | None = None,
    active_profile: ScheduleProfile = ScheduleProfile.P1,
    min_temp: float | None = None,
    max_temp: float | None = None,
    available_profiles: tuple[ScheduleProfile, ...] = (),
) -> MagicMock:
    """Create a mock week profile data point."""
    if is_climate:
        mock_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
        mock_dp.min_temp = min_temp
        mock_dp.max_temp = max_temp
        mock_dp.available_profiles = available_profiles
        mock_dp.current_profile_schedule = active_schedule
        mock_dp.current_schedule_profile = active_profile
        mock_dp.schedule_type = ScheduleType.CLIMATE
    else:
        mock_dp = MagicMock(spec=WeekProfileDataPointProtocol)
        mock_dp.schedule_type = schedule_type

    mock_dp.value = value
    mock_dp.max_entries = max_entries
    mock_dp.schedule_channel_address = schedule_channel_address
    mock_dp.schedule = schedule or {}
    mock_dp.unique_id = "test_unique_id"
    mock_dp.full_name = "Test Device Week Profile"
    mock_dp.name = "Week Profile"
    mock_dp.available = True
    mock_dp.enabled_default = True
    mock_dp.is_valid = True
    mock_dp.additional_information = {}

    # Device and channel mocks
    mock_device = MagicMock()
    mock_device.configure_mock(name="Test Device")
    mock_device.identifier = "TEST_DEVICE"
    mock_device.manufacturer = "eQ-3"
    mock_device.model = "HmIP-eTRV-2"
    mock_device.model_description = "Radiator Thermostat"
    mock_device.address = "ABC1234567"
    mock_device.firmware = "1.0.0"
    mock_device.room = "Living Room"
    mock_device.interface_id = "test_interface"
    mock_device.has_sub_devices = False
    mock_central_info = MagicMock()
    mock_central_info.configure_mock(name="test_central")
    mock_device.central_info = mock_central_info
    mock_dp.device = mock_device

    mock_channel = MagicMock()
    mock_channel.address = "ABC1234567:1"
    mock_channel.is_in_multi_group = False
    mock_dp.channel = mock_channel

    mock_dp.is_in_multiple_channels = False
    mock_dp.name_data = MagicMock()
    mock_dp.name_data.parameter_name = None

    return mock_dp


def _create_mock_control_unit() -> MagicMock:
    """Create a mock control unit."""
    mock_cu = MagicMock(spec=ControlUnit)
    mock_cu.enable_sub_devices = False
    return mock_cu


class TestWeekProfileSensor:
    """Tests for week profile sensor entities."""

    @pytest.mark.asyncio
    async def test_dispatcher_creates_entity(
        self,
        hass: HomeAssistant,
        mock_loaded_config_entry,
    ) -> None:
        """Test that dispatching WEEK_PROFILE signal creates entities."""
        entry = mock_loaded_config_entry

        mock_dp = _create_mock_data_point(value=3)
        # Make it appear as WeekProfileDataPoint for the dispatcher type hint
        mock_dp.__class__ = WeekProfileDataPoint

        signal = signal_new_data_point(
            entry_id=entry.entry_id,
            platform=DataPointCategory.WEEK_PROFILE,
        )

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            async_dispatcher_send(hass, signal, (mock_dp,))
            await hass.async_block_till_done()
            await hass.async_block_till_done()

    def test_extra_state_attributes_climate(self) -> None:
        """Test extra_state_attributes for climate schedule type."""
        mock_dp = _create_mock_data_point(
            is_climate=True,
            value=42,
            max_entries=546,
            schedule_channel_address="ABC1234567:1",
            min_temp=4.5,
            max_temp=30.5,
            available_profiles=(ScheduleProfile.P1, ScheduleProfile.P2, ScheduleProfile.P3),
            active_schedule={"MONDAY": [{"start": "06:00", "temp": 21.0}]},
        )
        mock_cu = _create_mock_control_unit()

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicWeekProfileSensor(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        attrs = entity.extra_state_attributes
        assert attrs["schedule_type"] == "climate"
        assert attrs["max_entries"] == 546
        assert attrs["min_temp"] == 4.5
        assert attrs["max_temp"] == 30.5
        assert attrs["available_profiles"] == ["P1", "P2", "P3"]
        assert attrs["schedule_data"] == {"MONDAY": [{"start": "06:00", "temp": 21.0}]}

    def test_extra_state_attributes_climate_no_temp(self) -> None:
        """Test extra_state_attributes for climate with None temps."""
        mock_dp = _create_mock_data_point(
            is_climate=True,
            min_temp=None,
            max_temp=None,
            available_profiles=(ScheduleProfile.P1,),
        )
        mock_cu = _create_mock_control_unit()

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicWeekProfileSensor(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        attrs = entity.extra_state_attributes
        assert "min_temp" not in attrs
        assert "max_temp" not in attrs
        assert attrs["available_profiles"] == ["P1"]

    def test_extra_state_attributes_default(self) -> None:
        """Test extra_state_attributes for default schedule type."""
        mock_dp = _create_mock_data_point(
            value=5,
            schedule_type=ScheduleType.DEFAULT,
            max_entries=24,
            schedule_channel_address="ABC1234567:1",
            schedule={"MONDAY": [{"start": "06:00", "end": "22:00"}]},
        )
        mock_cu = _create_mock_control_unit()

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicWeekProfileSensor(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        attrs = entity.extra_state_attributes
        assert attrs["schedule_type"] == "default"
        assert attrs["max_entries"] == 24
        assert attrs["schedule_channel_address"] == "ABC1234567:1"
        assert attrs["schedule_data"] == {"MONDAY": [{"start": "06:00", "end": "22:00"}]}

    def test_extra_state_attributes_empty_schedule(self) -> None:
        """Test extra_state_attributes when schedule is empty."""
        mock_dp = _create_mock_data_point(schedule={})
        mock_cu = _create_mock_control_unit()

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicWeekProfileSensor(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        attrs = entity.extra_state_attributes
        assert "schedule_data" not in attrs

    def test_extra_state_attributes_no_schedule_channel_address(self) -> None:
        """Test extra_state_attributes when schedule_channel_address is None."""
        mock_dp = _create_mock_data_point(
            schedule_channel_address=None,
        )
        mock_cu = _create_mock_control_unit()

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicWeekProfileSensor(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        attrs = entity.extra_state_attributes
        assert "schedule_channel_address" not in attrs

    def test_native_value(self) -> None:
        """Test that native_value returns the active entry count."""
        mock_dp = _create_mock_data_point(value=7)
        mock_cu = _create_mock_control_unit()

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicWeekProfileSensor(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        assert entity.native_value == 7

    def test_native_value_zero(self) -> None:
        """Test that native_value returns zero when no active entries."""
        mock_dp = _create_mock_data_point(value=0)
        mock_cu = _create_mock_control_unit()

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicWeekProfileSensor(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        assert entity.native_value == 0

    def test_translation_key(self) -> None:
        """Test that translation_key is set to week_profile."""
        mock_dp = _create_mock_data_point()
        mock_cu = _create_mock_control_unit()

        with patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ):
            entity = AioHomematicWeekProfileSensor(
                control_unit=mock_cu,
                data_point=mock_dp,
            )

        assert entity._attr_translation_key == "week_profile"
