"""
Functional tests for device-based schedule services.

Tests the actual behavior of the schedule services including:
- Service registration
- Handler invocation via device lookup
- Error handling
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiohomematic.interfaces import ClimateWeekProfileDataPointProtocol, WeekProfileDataPointProtocol
from custom_components.homematicip_local.const import DOMAIN, HmipLocalServices
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError


class TestScheduleServiceRegistration:
    """Test schedule service registration."""

    @pytest.mark.asyncio
    async def test_device_based_schedule_services_registered(self, hass: HomeAssistant) -> None:
        """Test that device-based schedule services are registered."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        assert hass.services.has_service(DOMAIN, HmipLocalServices.GET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.GET_SCHEDULE_PROFILE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.GET_SCHEDULE_WEEKDAY)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SET_SCHEDULE_PROFILE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SET_SCHEDULE_WEEKDAY)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.COPY_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.COPY_SCHEDULE_PROFILE)

    @pytest.mark.asyncio
    async def test_old_entity_based_services_not_registered(self, hass: HomeAssistant) -> None:
        """Test that old entity-based schedule services are no longer registered."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        assert not hass.services.has_service(DOMAIN, "cover_get_schedule")
        assert not hass.services.has_service(DOMAIN, "cover_set_schedule")
        assert not hass.services.has_service(DOMAIN, "light_get_schedule")
        assert not hass.services.has_service(DOMAIN, "light_set_schedule")
        assert not hass.services.has_service(DOMAIN, "switch_get_schedule")
        assert not hass.services.has_service(DOMAIN, "switch_set_schedule")
        assert not hass.services.has_service(DOMAIN, "valve_get_schedule")
        assert not hass.services.has_service(DOMAIN, "valve_set_schedule")


class TestGetScheduleHandler:
    """Test _async_service_get_schedule handler."""

    @pytest.mark.asyncio
    async def test_get_schedule_calls_wp_dp(self) -> None:
        """Test get_schedule calls week_profile_data_point.get_schedule."""
        from custom_components.homematicip_local.services import _async_service_get_schedule

        mock_wp_dp = MagicMock(spec=WeekProfileDataPointProtocol)
        mock_wp_dp.get_schedule = AsyncMock(return_value={"MONDAY": [{"start": "06:00"}]})

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Device"

        mock_service = MagicMock()

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            result = await _async_service_get_schedule(hass=MagicMock(), service=mock_service)

        mock_wp_dp.get_schedule.assert_awaited_once_with(force_load=True)
        assert result == {"MONDAY": [{"start": "06:00"}]}

    @pytest.mark.asyncio
    async def test_get_schedule_raises_if_no_wp_dp(self) -> None:
        """Test get_schedule raises HomeAssistantError if no week_profile_data_point."""
        from custom_components.homematicip_local.services import _async_service_get_schedule

        mock_device = MagicMock()
        mock_device.week_profile_data_point = None
        mock_device.name = "Test Device"

        mock_service = MagicMock()

        with (
            patch(
                "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
                return_value=mock_device,
            ),
            pytest.raises(HomeAssistantError, match="does not support schedules"),
        ):
            await _async_service_get_schedule(hass=MagicMock(), service=mock_service)


class TestSetScheduleHandler:
    """Test _async_service_set_schedule handler."""

    @pytest.mark.asyncio
    async def test_set_schedule_calls_wp_dp(self) -> None:
        """Test set_schedule calls week_profile_data_point.set_schedule."""
        from custom_components.homematicip_local.services import ATTR_SCHEDULE_DATA, _async_service_set_schedule

        mock_wp_dp = MagicMock(spec=WeekProfileDataPointProtocol)
        mock_wp_dp.set_schedule = AsyncMock()

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Device"

        schedule_data = {"MONDAY": [{"start": "06:00", "level": 1.0}]}

        mock_service = MagicMock()
        mock_service.data = {ATTR_SCHEDULE_DATA: schedule_data}

        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=mock_device,
        ):
            await _async_service_set_schedule(hass=MagicMock(), service=mock_service)

        mock_wp_dp.set_schedule.assert_awaited_once_with(schedule_data=schedule_data)

    @pytest.mark.asyncio
    async def test_set_schedule_raises_if_no_wp_dp(self) -> None:
        """Test set_schedule raises HomeAssistantError if no week_profile_data_point."""
        from custom_components.homematicip_local.services import ATTR_SCHEDULE_DATA, _async_service_set_schedule

        mock_device = MagicMock()
        mock_device.week_profile_data_point = None
        mock_device.name = "Test Device"

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
    async def test_set_schedule_wraps_backend_exception(self) -> None:
        """Test that backend exceptions are wrapped in HomeAssistantError."""
        from aiohomematic.exceptions import BaseHomematicException
        from custom_components.homematicip_local.services import ATTR_SCHEDULE_DATA, _async_service_set_schedule

        mock_wp_dp = MagicMock(spec=WeekProfileDataPointProtocol)
        mock_wp_dp.set_schedule = AsyncMock(side_effect=BaseHomematicException("Test error"))

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Device"

        mock_service = MagicMock()
        mock_service.data = {ATTR_SCHEDULE_DATA: {}}

        with (
            patch(
                "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
                return_value=mock_device,
            ),
            pytest.raises(HomeAssistantError),
        ):
            await _async_service_set_schedule(hass=MagicMock(), service=mock_service)

    @pytest.mark.asyncio
    async def test_set_schedule_wraps_validation_error(self) -> None:
        """Test that Pydantic ValidationError is wrapped in HomeAssistantError."""
        from pydantic import ValidationError
        from pydantic_core import InitErrorDetails, PydanticCustomError

        from custom_components.homematicip_local.services import ATTR_SCHEDULE_DATA, _async_service_set_schedule

        error = PydanticCustomError("value_error", "Invalid level value")
        errors: list[InitErrorDetails] = [{"type": error, "loc": ("level",), "input": 2.0}]
        validation_error = ValidationError.from_exception_data("SimpleScheduleEntry", errors)

        mock_wp_dp = MagicMock(spec=WeekProfileDataPointProtocol)
        mock_wp_dp.set_schedule = AsyncMock(side_effect=validation_error)

        mock_device = MagicMock()
        mock_device.week_profile_data_point = mock_wp_dp
        mock_device.name = "Test Device"

        mock_service = MagicMock()
        mock_service.data = {ATTR_SCHEDULE_DATA: {"invalid": "data"}}

        with (
            patch(
                "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
                return_value=mock_device,
            ),
            pytest.raises(HomeAssistantError, match="Invalid schedule data"),
        ):
            await _async_service_set_schedule(hass=MagicMock(), service=mock_service)


class TestCopyScheduleHandler:
    """Test _async_service_copy_schedule handler."""

    @pytest.mark.asyncio
    async def test_copy_schedule_calls_source_dp(self) -> None:
        """Test copy_schedule calls source data point's copy_schedule."""
        from custom_components.homematicip_local.services import ATTR_TARGET_DEVICE_ID, _async_service_copy_schedule

        source_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
        source_dp.copy_schedule = AsyncMock()

        target_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)

        source_device = MagicMock()
        source_device.week_profile_data_point = source_dp
        source_device.name = "Source Device"

        target_device = MagicMock()
        target_device.week_profile_data_point = target_dp
        target_device.name = "Target Device"

        mock_service = MagicMock()
        mock_service.data = {ATTR_TARGET_DEVICE_ID: "target_id"}

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

        source_dp.copy_schedule.assert_awaited_once_with(target_data_point=target_dp)
