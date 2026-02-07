"""Tests for climate schedule profile services (device-based)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiohomematic.interfaces import ClimateWeekProfileDataPointProtocol
from custom_components.homematicip_local.const import HmipLocalServices
from homeassistant.exceptions import HomeAssistantError


class TestGetScheduleProfileHandler:
    """Test _async_service_get_schedule_profile handler."""

    @pytest.mark.asyncio
    async def test_get_schedule_profile_calls_wp_dp(self) -> None:
        """Test get_schedule_profile calls week_profile_data_point.get_schedule_profile."""
        from custom_components.homematicip_local.services import ATTR_PROFILE, _async_service_get_schedule_profile

        mock_wp_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
        mock_wp_dp.get_schedule_profile = AsyncMock(return_value={"MONDAY": [{"start": "06:00", "temp": 21.0}]})

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Climate"

        mock_service = MagicMock()
        mock_service.data = {ATTR_PROFILE: "P1"}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            result = await _async_service_get_schedule_profile(hass=MagicMock(), service=mock_service)

        mock_wp_dp.get_schedule_profile.assert_awaited_once()
        assert result == {"MONDAY": [{"start": "06:00", "temp": 21.0}]}

    @pytest.mark.asyncio
    async def test_get_schedule_profile_raises_if_not_climate(self) -> None:
        """Test get_schedule_profile raises error if device is not climate."""
        from aiohomematic.interfaces import WeekProfileDataPointProtocol
        from custom_components.homematicip_local.services import ATTR_PROFILE, _async_service_get_schedule_profile

        mock_wp_dp = MagicMock(spec=WeekProfileDataPointProtocol)

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Non-Climate Device"

        mock_service = MagicMock()
        mock_service.data = {ATTR_PROFILE: "P1"}

        with (
            patch(
                "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
                return_value=mock_device,
            ),
            pytest.raises(HomeAssistantError, match="does not support climate schedules"),
        ):
            await _async_service_get_schedule_profile(hass=MagicMock(), service=mock_service)


class TestGetScheduleWeekdayHandler:
    """Test _async_service_get_schedule_weekday handler."""

    @pytest.mark.asyncio
    async def test_get_schedule_weekday_calls_wp_dp(self) -> None:
        """Test get_schedule_weekday calls week_profile_data_point.get_schedule_weekday."""
        from custom_components.homematicip_local.services import (
            ATTR_PROFILE,
            ATTR_WEEKDAY,
            _async_service_get_schedule_weekday,
        )

        mock_wp_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
        mock_wp_dp.get_schedule_weekday = AsyncMock(
            return_value={"base_temperature": 17.0, "periods": [{"starttime": "06:00", "temperature": 21.0}]}
        )

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Climate"

        mock_service = MagicMock()
        mock_service.data = {ATTR_PROFILE: "P1", ATTR_WEEKDAY: "MONDAY"}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            result = await _async_service_get_schedule_weekday(hass=MagicMock(), service=mock_service)

        mock_wp_dp.get_schedule_weekday.assert_awaited_once()
        assert "base_temperature" in result


class TestSetScheduleProfileHandler:
    """Test _async_service_set_schedule_profile handler."""

    @pytest.mark.asyncio
    async def test_set_schedule_profile_calls_wp_dp(self) -> None:
        """Test set_schedule_profile calls week_profile_data_point.set_schedule_profile."""
        from custom_components.homematicip_local.services import (
            ATTR_PROFILE,
            ATTR_SIMPLE_PROFILE_DATA,
            _async_service_set_schedule_profile,
        )

        mock_wp_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
        mock_wp_dp.set_schedule_profile = AsyncMock()

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Climate"

        profile_data = {"MONDAY": {"base_temperature": 17.0, "periods": []}}
        mock_service = MagicMock()
        mock_service.data = {ATTR_PROFILE: "P1", ATTR_SIMPLE_PROFILE_DATA: profile_data}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            await _async_service_set_schedule_profile(hass=MagicMock(), service=mock_service)

        mock_wp_dp.set_schedule_profile.assert_awaited_once()


class TestSetScheduleWeekdayHandler:
    """Test _async_service_set_schedule_weekday handler."""

    @pytest.mark.asyncio
    async def test_set_schedule_weekday_calls_wp_dp(self) -> None:
        """Test set_schedule_weekday calls week_profile_data_point.set_schedule_weekday."""
        from custom_components.homematicip_local.services import (
            ATTR_BASE_TEMPERATURE,
            ATTR_PROFILE,
            ATTR_SIMPLE_WEEKDAY_LIST,
            ATTR_WEEKDAY,
            _async_service_set_schedule_weekday,
        )

        mock_wp_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
        mock_wp_dp.set_schedule_weekday = AsyncMock()

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Climate"

        mock_service = MagicMock()
        mock_service.data = {
            ATTR_PROFILE: "P1",
            ATTR_WEEKDAY: "MONDAY",
            ATTR_BASE_TEMPERATURE: 17.0,
            ATTR_SIMPLE_WEEKDAY_LIST: [{"starttime": "06:00", "endtime": "22:00", "temperature": 21.0}],
        }

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            await _async_service_set_schedule_weekday(hass=MagicMock(), service=mock_service)

        mock_wp_dp.set_schedule_weekday.assert_awaited_once()


class TestCopyScheduleProfileHandler:
    """Test _async_service_copy_schedule_profile handler."""

    @pytest.mark.asyncio
    async def test_copy_schedule_profile_within_device(self) -> None:
        """Test copy_schedule_profile within the same device."""
        from custom_components.homematicip_local.services import (
            ATTR_SOURCE_PROFILE,
            ATTR_TARGET_PROFILE,
            _async_service_copy_schedule_profile,
        )

        mock_wp_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
        mock_wp_dp.copy_schedule_profile = AsyncMock()

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Climate"

        mock_service = MagicMock()
        mock_service.data = {ATTR_SOURCE_PROFILE: "P1", ATTR_TARGET_PROFILE: "P2"}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            await _async_service_copy_schedule_profile(hass=MagicMock(), service=mock_service)

        mock_wp_dp.copy_schedule_profile.assert_awaited_once()


class TestScheduleServiceMethodNaming:
    """Test that the schedule service enum values are correct."""

    def test_new_service_names_exist(self) -> None:
        """Verify that new device-based service names exist in HmipLocalServices enum."""
        assert hasattr(HmipLocalServices, "GET_SCHEDULE")
        assert hasattr(HmipLocalServices, "SET_SCHEDULE")
        assert hasattr(HmipLocalServices, "GET_SCHEDULE_PROFILE")
        assert hasattr(HmipLocalServices, "GET_SCHEDULE_WEEKDAY")
        assert hasattr(HmipLocalServices, "SET_SCHEDULE_PROFILE")
        assert hasattr(HmipLocalServices, "SET_SCHEDULE_WEEKDAY")
        assert hasattr(HmipLocalServices, "COPY_SCHEDULE")
        assert hasattr(HmipLocalServices, "COPY_SCHEDULE_PROFILE")
        assert hasattr(HmipLocalServices, "SET_CURRENT_SCHEDULE_PROFILE")

    def test_old_entity_based_service_names_removed(self) -> None:
        """Verify that old entity-based service names are removed."""
        assert not hasattr(HmipLocalServices, "COVER_GET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "COVER_SET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "LIGHT_GET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "LIGHT_SET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "SWITCH_GET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "SWITCH_SET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "VALVE_GET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "VALVE_SET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "GET_SCHEDULE_SIMPLE_PROFILE")
        assert not hasattr(HmipLocalServices, "GET_SCHEDULE_SIMPLE_WEEKDAY")
        assert not hasattr(HmipLocalServices, "SET_SCHEDULE_SIMPLE_PROFILE")
        assert not hasattr(HmipLocalServices, "SET_SCHEDULE_SIMPLE_WEEKDAY")
