"""
End-to-end tests for device-based schedule services with CCU data validation.

These tests validate the complete data flow:
1. Service call → device lookup → week_profile_data_point → CCU data
2. CCU get data → service response
3. CCU set data → week_profile_data_point.set_schedule
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiohomematic.interfaces import ClimateWeekProfileDataPointProtocol, WeekProfileDataPointProtocol
from homeassistant.exceptions import HomeAssistantError


@pytest.fixture
def mock_wp_data_point() -> MagicMock:
    """Create a mock WeekProfileDataPoint for non-climate devices."""
    wp_dp = MagicMock(spec=WeekProfileDataPointProtocol)
    wp_dp.schedule_channel_address = "VCU0000001:1"
    wp_dp.set_schedule = AsyncMock()
    wp_dp.get_schedule = AsyncMock()
    wp_dp.schedule = {}

    return wp_dp


@pytest.fixture
def mock_wp_data_point_climate() -> MagicMock:
    """Create a mock WeekProfileDataPoint for climate devices."""
    wp_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
    wp_dp.schedule_channel_address = "VCU0000002:7"
    wp_dp.set_schedule = AsyncMock()
    wp_dp.get_schedule = AsyncMock()
    wp_dp.get_schedule_profile = AsyncMock()
    wp_dp.get_schedule_weekday = AsyncMock()
    wp_dp.set_schedule_profile = AsyncMock()
    wp_dp.set_schedule_weekday = AsyncMock()
    wp_dp.copy_schedule = AsyncMock()
    wp_dp.copy_schedule_profile = AsyncMock()
    wp_dp.schedule = {}

    return wp_dp


# =============================================================================
# Test: Non-Climate Devices - get_schedule Service → CCU Data
# =============================================================================


class TestNonClimateGetScheduleEndToEnd:
    """Test get_schedule service end-to-end for non-climate devices."""

    @pytest.mark.asyncio
    async def test_get_schedule_dimmer_values(self, mock_wp_data_point: MagicMock) -> None:
        """Test that dimmer schedule from CCU is correctly returned."""
        from custom_components.homematicip_local.services import _async_service_get_schedule

        ccu_schedule_data = {
            0: {"start": "00:00", "end": "06:00", "value": 0},
            1: {"start": "06:00", "end": "22:00", "value": 75},
            2: {"start": "22:00", "end": "00:00", "value": 25},
        }
        mock_wp_data_point.get_schedule = AsyncMock(return_value=ccu_schedule_data)

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_data_point
        mock_device.name = "Hallway Dimmer"

        mock_service = MagicMock()

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            result = await _async_service_get_schedule(hass=MagicMock(), service=mock_service)

        assert result == ccu_schedule_data

    @pytest.mark.asyncio
    async def test_get_schedule_returns_ccu_data(self, mock_wp_data_point: MagicMock) -> None:
        """Test that get_schedule service returns CCU schedule data."""
        from custom_components.homematicip_local.services import _async_service_get_schedule

        ccu_schedule_data = {
            0: {"start": "06:00", "end": "22:00", "value": True},
            1: {"start": "22:00", "end": "06:00", "value": False},
        }
        mock_wp_data_point.get_schedule = AsyncMock(return_value=ccu_schedule_data)

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_data_point
        mock_device.name = "Test Switch"

        mock_service = MagicMock()

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            result = await _async_service_get_schedule(hass=MagicMock(), service=mock_service)

        mock_wp_data_point.get_schedule.assert_awaited_once_with(force_load=True)
        assert result == ccu_schedule_data


# =============================================================================
# Test: Non-Climate Devices - set_schedule Service → CCU Data
# =============================================================================


class TestNonClimateSetScheduleEndToEnd:
    """Test set_schedule service end-to-end for non-climate devices."""

    @pytest.mark.asyncio
    async def test_set_schedule_raises_if_no_wp_dp(self) -> None:
        """Test that set_schedule raises error if device has no week_profile_data_point."""
        from custom_components.homematicip_local.services import ATTR_SCHEDULE_DATA, _async_service_set_schedule

        mock_device = MagicMock()
        mock_device.week_profile_data_point = None
        mock_device.name = "Unsupported Device"

        mock_service = MagicMock()
        mock_service.data = {ATTR_SCHEDULE_DATA: {}}

        with (
            patch(
                "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
                return_value=mock_device,
            ),
            pytest.raises(HomeAssistantError, match="does not support schedules"),
        ):
            await _async_service_set_schedule(hass=MagicMock(), service=mock_service)

    @pytest.mark.asyncio
    async def test_set_schedule_sends_data_to_ccu(self, mock_wp_data_point: MagicMock) -> None:
        """Test that set_schedule service sends schedule data to CCU via week_profile_data_point."""
        from custom_components.homematicip_local.services import ATTR_SCHEDULE_DATA, _async_service_set_schedule

        schedule_data = {
            "MONDAY": [{"start": "06:00", "end": "22:00", "value": True}],
        }

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_data_point
        mock_device.name = "Test Switch"

        mock_service = MagicMock()
        mock_service.data = {ATTR_SCHEDULE_DATA: schedule_data}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            await _async_service_set_schedule(hass=MagicMock(), service=mock_service)

        mock_wp_data_point.set_schedule.assert_awaited_once_with(schedule_data=schedule_data)


# =============================================================================
# Test: Climate Devices - Profile Service → CCU Data
# =============================================================================


class TestClimateScheduleProfileEndToEnd:
    """Test climate schedule profile services end-to-end."""

    @pytest.mark.asyncio
    async def test_get_schedule_profile_returns_ccu_data(self, mock_wp_data_point_climate: MagicMock) -> None:
        """Test that get_schedule_profile returns CCU profile data."""
        from custom_components.homematicip_local.services import ATTR_PROFILE, _async_service_get_schedule_profile

        ccu_profile_data = {
            "MONDAY": {"base_temperature": 17.0, "periods": [{"starttime": "06:00", "temperature": 21.0}]},
            "TUESDAY": {"base_temperature": 17.0, "periods": [{"starttime": "07:00", "temperature": 20.0}]},
        }
        mock_wp_data_point_climate.get_schedule_profile = AsyncMock(return_value=ccu_profile_data)

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_data_point_climate
        mock_device.name = "Living Room Thermostat"

        mock_service = MagicMock()
        mock_service.data = {ATTR_PROFILE: "P1"}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            result = await _async_service_get_schedule_profile(hass=MagicMock(), service=mock_service)

        mock_wp_data_point_climate.get_schedule_profile.assert_awaited_once()
        assert result == ccu_profile_data

    @pytest.mark.asyncio
    async def test_set_schedule_profile_sends_data_to_ccu(self, mock_wp_data_point_climate: MagicMock) -> None:
        """Test that set_schedule_profile sends profile data to CCU."""
        from custom_components.homematicip_local.services import (
            ATTR_PROFILE,
            ATTR_SIMPLE_PROFILE_DATA,
            _async_service_set_schedule_profile,
        )

        profile_data = {
            "MONDAY": {"base_temperature": 17.0, "periods": [{"starttime": "06:00", "temperature": 21.0}]},
        }

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_data_point_climate
        mock_device.name = "Living Room Thermostat"

        mock_service = MagicMock()
        mock_service.data = {ATTR_PROFILE: "P1", ATTR_SIMPLE_PROFILE_DATA: profile_data}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            await _async_service_set_schedule_profile(hass=MagicMock(), service=mock_service)

        mock_wp_data_point_climate.set_schedule_profile.assert_awaited_once()


# =============================================================================
# Test: Climate Devices - Weekday Service → CCU Data
# =============================================================================


class TestClimateScheduleWeekdayEndToEnd:
    """Test climate schedule weekday services end-to-end."""

    @pytest.mark.asyncio
    async def test_get_schedule_weekday_returns_ccu_data(self, mock_wp_data_point_climate: MagicMock) -> None:
        """Test that get_schedule_weekday returns CCU weekday data."""
        from custom_components.homematicip_local.services import (
            ATTR_PROFILE,
            ATTR_WEEKDAY,
            _async_service_get_schedule_weekday,
        )

        ccu_weekday_data = {
            "base_temperature": 17.0,
            "periods": [
                {"starttime": "06:00", "endtime": "08:00", "temperature": 21.0},
                {"starttime": "16:00", "endtime": "22:00", "temperature": 21.0},
            ],
        }
        mock_wp_data_point_climate.get_schedule_weekday = AsyncMock(return_value=ccu_weekday_data)

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_data_point_climate
        mock_device.name = "Living Room Thermostat"

        mock_service = MagicMock()
        mock_service.data = {ATTR_PROFILE: "P1", ATTR_WEEKDAY: "MONDAY"}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            result = await _async_service_get_schedule_weekday(hass=MagicMock(), service=mock_service)

        mock_wp_data_point_climate.get_schedule_weekday.assert_awaited_once()
        assert result == ccu_weekday_data

    @pytest.mark.asyncio
    async def test_set_schedule_weekday_sends_data_to_ccu(self, mock_wp_data_point_climate: MagicMock) -> None:
        """Test that set_schedule_weekday sends weekday data to CCU."""
        from custom_components.homematicip_local.services import (
            ATTR_BASE_TEMPERATURE,
            ATTR_PROFILE,
            ATTR_SIMPLE_WEEKDAY_LIST,
            ATTR_WEEKDAY,
            _async_service_set_schedule_weekday,
        )

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_data_point_climate
        mock_device.name = "Living Room Thermostat"

        mock_service = MagicMock()
        mock_service.data = {
            ATTR_PROFILE: "P1",
            ATTR_WEEKDAY: "MONDAY",
            ATTR_BASE_TEMPERATURE: 17.0,
            ATTR_SIMPLE_WEEKDAY_LIST: [
                {"starttime": "06:00", "endtime": "08:00", "temperature": 21.0},
                {"starttime": "16:00", "endtime": "22:00", "temperature": 21.0},
            ],
        }

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            await _async_service_set_schedule_weekday(hass=MagicMock(), service=mock_service)

        mock_wp_data_point_climate.set_schedule_weekday.assert_awaited_once()


# =============================================================================
# Test: Copy Schedule Service → CCU Data
# =============================================================================


class TestCopyScheduleEndToEnd:
    """Test copy_schedule service end-to-end."""

    @pytest.mark.asyncio
    async def test_copy_schedule_between_devices(self, mock_wp_data_point_climate: MagicMock) -> None:
        """Test that copy_schedule copies from source to target device."""
        from custom_components.homematicip_local.services import ATTR_TARGET_DEVICE_ID, _async_service_copy_schedule

        target_wp_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)

        source_device = MagicMock()
        source_device.week_profile_data_point = mock_wp_data_point_climate
        source_device.name = "Source Thermostat"

        target_device = MagicMock()
        target_device.week_profile_data_point = target_wp_dp
        target_device.name = "Target Thermostat"

        mock_service = MagicMock()
        mock_service.data = {ATTR_TARGET_DEVICE_ID: "target_device_id"}

        with (
            patch(
                "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
                return_value=source_device,
            ),
            patch(
                "custom_components.homematicip_local.services._asnyc_get_hm_device_by_id",
                return_value=target_device,
            ),
        ):
            await _async_service_copy_schedule(hass=MagicMock(), service=mock_service)

        mock_wp_data_point_climate.copy_schedule.assert_awaited_once_with(target_data_point=target_wp_dp)

    @pytest.mark.asyncio
    async def test_copy_schedule_profile_within_device(self, mock_wp_data_point_climate: MagicMock) -> None:
        """Test that copy_schedule_profile copies between profiles on the same device."""
        from custom_components.homematicip_local.services import (
            ATTR_SOURCE_PROFILE,
            ATTR_TARGET_PROFILE,
            _async_service_copy_schedule_profile,
        )

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_data_point_climate
        mock_device.name = "Living Room Thermostat"

        mock_service = MagicMock()
        mock_service.data = {ATTR_SOURCE_PROFILE: "P1", ATTR_TARGET_PROFILE: "P2"}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            await _async_service_copy_schedule_profile(hass=MagicMock(), service=mock_service)

        mock_wp_data_point_climate.copy_schedule_profile.assert_awaited_once()
