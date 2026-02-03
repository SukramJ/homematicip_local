"""Tests for climate schedule profile services."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.homematicip_local.climate import AioHomematicClimate
from custom_components.homematicip_local.const import DOMAIN


@pytest.fixture
def mock_climate_entity() -> AioHomematicClimate:
    """Create a mock climate entity for testing."""
    entity = MagicMock(spec=AioHomematicClimate)
    entity._data_point = MagicMock()
    entity._data_point.get_schedule_profile = AsyncMock(return_value={"mock": "profile_data"})
    entity._data_point.get_schedule_weekday = AsyncMock(return_value={"mock": "weekday_data"})
    entity._data_point.set_schedule_profile = AsyncMock()
    entity._data_point.set_schedule_weekday = AsyncMock()
    return entity


class TestClimateScheduleProfileServices:
    """Test climate schedule profile service methods."""

    @pytest.mark.asyncio
    async def test_async_get_schedule_profile(self, mock_climate_entity: AioHomematicClimate) -> None:
        """Test async_get_schedule_profile method."""
        # Create a real entity instance but patch handle_homematic_errors
        with patch("custom_components.homematicip_local.climate.handle_homematic_errors", lambda f: f):
            entity = AioHomematicClimate(
                control_unit=MagicMock(),
                data_point=mock_climate_entity._data_point,
            )

            # Call the method
            result = await entity.async_get_schedule_profile(profile="P1")

            # Verify the data_point method was called correctly
            mock_climate_entity._data_point.get_schedule_profile.assert_awaited_once_with(profile="P1", force_load=True)

            # Verify the result
            assert result == {"mock": "profile_data"}

    @pytest.mark.asyncio
    async def test_async_get_schedule_weekday(self, mock_climate_entity: AioHomematicClimate) -> None:
        """Test async_get_schedule_weekday method."""
        with patch("custom_components.homematicip_local.climate.handle_homematic_errors", lambda f: f):
            entity = AioHomematicClimate(
                control_unit=MagicMock(),
                data_point=mock_climate_entity._data_point,
            )

            # Call the method
            result = await entity.async_get_schedule_weekday(profile="P1", weekday="MONDAY")

            # Verify the data_point method was called correctly
            mock_climate_entity._data_point.get_schedule_weekday.assert_awaited_once_with(
                profile="P1", weekday="MONDAY", force_load=True
            )

            # Verify the result
            assert result == {"mock": "weekday_data"}

    @pytest.mark.asyncio
    async def test_async_set_schedule_profile(self, mock_climate_entity: AioHomematicClimate) -> None:
        """Test async_set_schedule_profile method."""
        with patch("custom_components.homematicip_local.climate.handle_homematic_errors", lambda f: f):
            entity = AioHomematicClimate(
                control_unit=MagicMock(),
                data_point=mock_climate_entity._data_point,
            )

            # Mock the ClimateProfileSchedule model
            profile_data_mock = MagicMock()
            profile_data_mock.model_dump.return_value = {"base_temperature": 20.0, "periods": []}

            # Call the method
            await entity.async_set_schedule_profile(profile="P1", simple_profile_data=profile_data_mock)

            # Verify the data_point method was called correctly
            mock_climate_entity._data_point.set_schedule_profile.assert_awaited_once_with(
                profile="P1",
                profile_data={"base_temperature": 20.0, "periods": []},
            )

    @pytest.mark.asyncio
    async def test_async_set_schedule_weekday(self, mock_climate_entity: AioHomematicClimate) -> None:
        """Test async_set_schedule_weekday method."""
        # Import the actual Pydantic models
        from custom_components.homematicip_local.climate import ClimateSchedulePeriod

        with patch("custom_components.homematicip_local.climate.handle_homematic_errors", lambda f: f):
            entity = AioHomematicClimate(
                control_unit=MagicMock(),
                data_point=mock_climate_entity._data_point,
            )

            # Create a proper Pydantic model instance
            period = ClimateSchedulePeriod(starttime="06:00", endtime="22:00", temperature=21.0)

            # Call the method
            await entity.async_set_schedule_weekday(
                profile="P1",
                weekday="MONDAY",
                base_temperature=17.0,
                simple_weekday_list=[period],
            )

            # Verify the data_point method was called
            assert mock_climate_entity._data_point.set_schedule_weekday.await_count == 1

            # Get the call arguments
            call_args = mock_climate_entity._data_point.set_schedule_weekday.call_args
            assert call_args.kwargs["profile"] == "P1"
            assert call_args.kwargs["weekday"] == "MONDAY"

            # Verify the weekday_data structure
            weekday_data = call_args.kwargs["weekday_data"]
            assert isinstance(weekday_data, dict)
            assert "base_temperature" in weekday_data
            assert weekday_data["base_temperature"] == 17.0
            assert "periods" in weekday_data
            assert len(weekday_data["periods"]) == 1


class TestClimateScheduleServiceRegistration:
    """Test that climate schedule services are properly registered."""

    @pytest.mark.asyncio
    async def test_schedule_profile_services_registered(self, hass: Any) -> None:
        """Test that schedule profile services are registered with correct method names."""
        # This test verifies that the service registrations in services.py
        # correctly reference the renamed methods (without "simple" in the name)

        # Import here to avoid circular dependencies

        from custom_components.homematicip_local.services import async_setup_services

        # Setup services
        await async_setup_services(hass)

        # Verify services exist (they should be registered for climate domain)
        # Note: The actual service names still contain "simple" for backward compatibility
        assert hass.services.has_service(DOMAIN, "get_schedule_simple_profile")
        assert hass.services.has_service(DOMAIN, "get_schedule_simple_weekday")
        assert hass.services.has_service(DOMAIN, "set_schedule_simple_profile")
        assert hass.services.has_service(DOMAIN, "set_schedule_simple_weekday")


class TestClimateScheduleMethodNaming:
    """Test that the method renames are consistent."""

    def test_method_names_without_simple(self) -> None:
        """Verify that climate entity methods no longer contain 'simple' in their names."""
        # Verify the new method names exist
        assert hasattr(AioHomematicClimate, "async_get_schedule_profile")
        assert hasattr(AioHomematicClimate, "async_get_schedule_weekday")
        assert hasattr(AioHomematicClimate, "async_set_schedule_profile")
        assert hasattr(AioHomematicClimate, "async_set_schedule_weekday")

        # Verify the old method names do NOT exist
        assert not hasattr(AioHomematicClimate, "async_get_schedule_simple_profile")
        assert not hasattr(AioHomematicClimate, "async_get_schedule_simple_weekday")
        assert not hasattr(AioHomematicClimate, "async_set_schedule_simple_profile")
        assert not hasattr(AioHomematicClimate, "async_set_schedule_simple_weekday")
