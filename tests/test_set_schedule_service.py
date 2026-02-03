"""
Functional tests for set_schedule service.

Tests the actual behavior of the set_schedule service including:
- Service call validation
- Entity method invocation
- Error handling
- Schedule data processing
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.homematicip_local.const import DOMAIN, HmipLocalServices
from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError


@pytest.fixture
def mock_control_unit() -> MagicMock:
    """Create a mock ControlUnit."""
    control_unit = MagicMock()
    control_unit.central = MagicMock()
    return control_unit


@pytest.fixture
def mock_custom_data_point() -> MagicMock:
    """Create a mock CustomDataPointProtocol with schedule support."""
    from aiohomematic.interfaces import CustomDataPointProtocol

    data_point = MagicMock(spec=CustomDataPointProtocol)
    data_point.has_schedule = True
    data_point.set_schedule = AsyncMock()
    data_point.get_schedule = AsyncMock(return_value={})

    # Mock device (still needed for other functionality)
    device = MagicMock()
    data_point.device = device
    data_point.name = "TEST_SWITCH"
    data_point.channel_address = "VCU0000001:1"

    return data_point


@pytest.fixture
def mock_entity(mock_control_unit: MagicMock, mock_custom_data_point: MagicMock) -> AioHomematicGenericEntity:
    """Create a mock entity with schedule support."""
    entity = AioHomematicGenericEntity(
        control_unit=mock_control_unit,
        data_point=mock_custom_data_point,
    )
    entity.entity_id = "switch.test_switch"
    entity.hass = MagicMock()
    return entity


class TestSetScheduleServiceRegistration:
    """Test set_schedule service registration."""

    @pytest.mark.asyncio
    async def test_service_registered_for_all_domains(self, hass: HomeAssistant) -> None:
        """Test that set_schedule service is registered."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Verify service is registered
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SET_SCHEDULE)


class TestAsyncSetScheduleMethod:
    """Test async_set_schedule method behavior."""

    @pytest.mark.asyncio
    async def test_set_schedule_calls_data_point_method(
        self, mock_control_unit: MagicMock, mock_custom_data_point: MagicMock
    ) -> None:
        """Test set_schedule calls data_point.set_schedule directly."""
        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=mock_custom_data_point,
        )
        entity.entity_id = "switch.test_switch"

        schedule_data = {"1": {"time": "06:00", "condition": "fixed_time"}}

        # Call set_schedule
        await entity.async_set_schedule(schedule_data=schedule_data)

        # Verify data_point.set_schedule was called
        mock_custom_data_point.set_schedule.assert_awaited_once_with(schedule_data=schedule_data)

    @pytest.mark.asyncio
    async def test_set_schedule_non_custom_data_point(self, mock_control_unit: MagicMock) -> None:
        """Test that set_schedule handles non-CustomDataPointProtocol gracefully."""
        from aiohomematic.interfaces import GenericDataPointProtocol

        # Create entity with GenericDataPointProtocol (not CustomDataPointProtocol)
        generic_data_point = MagicMock(spec=GenericDataPointProtocol)
        generic_data_point.name = "TEST_SENSOR"
        generic_data_point.channel_address = "VCU0000001:1"

        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=generic_data_point,
        )
        entity.entity_id = "sensor.test_sensor"

        schedule_data = {0: {"start": "00:00", "end": "06:00", "value": False}}

        # Should not raise exception, just log warning and return
        await entity.async_set_schedule(schedule_data=schedule_data)

    @pytest.mark.asyncio
    async def test_set_schedule_with_empty_schedule(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test setting an empty schedule."""
        schedule_data: dict[str, dict[Any, Any]] = {}

        await mock_entity.async_set_schedule(schedule_data=schedule_data)

        # Verify data_point.set_schedule was still called
        mock_custom_data_point.set_schedule.assert_awaited_once_with(schedule_data=schedule_data)

    @pytest.mark.asyncio
    async def test_set_schedule_with_valid_data(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test setting schedule with valid schedule data."""
        schedule_data = {
            "1": {
                "weekdays": ["MONDAY", "TUESDAY"],
                "time": "06:00",
                "condition": "fixed_time",
                "target_channels": ["1_1"],
                "level": 1.0,
            },
            "2": {
                "weekdays": ["SATURDAY", "SUNDAY"],
                "time": "08:00",
                "condition": "fixed_time",
                "target_channels": ["1_1"],
                "level": 0.5,
            },
        }

        await mock_entity.async_set_schedule(schedule_data=schedule_data)

        # Verify data_point.set_schedule was called with correct data
        mock_custom_data_point.set_schedule.assert_awaited_once_with(schedule_data=schedule_data)

    @pytest.mark.asyncio
    async def test_set_schedule_without_schedule_support(
        self, mock_control_unit: MagicMock, mock_custom_data_point: MagicMock
    ) -> None:
        """Test set_schedule when entity doesn't support schedules."""
        # Disable schedule support
        mock_custom_data_point.has_schedule = False

        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=mock_custom_data_point,
        )
        entity.entity_id = "switch.test_switch"

        schedule_data = {"1": {"time": "06:00", "condition": "fixed_time"}}

        # Should not raise exception, just log warning and return
        await entity.async_set_schedule(schedule_data=schedule_data)

        # Verify set_schedule was NOT called
        mock_custom_data_point.set_schedule.assert_not_awaited()


class TestSetScheduleServiceIntegration:
    """Test set_schedule service end-to-end integration."""

    @pytest.mark.asyncio
    async def test_service_registered_and_callable(self, hass: HomeAssistant) -> None:
        """Test that service is registered and can be called."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Service should be registered and callable
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SET_SCHEDULE)

        # The service is platform-specific, so without actual entities it won't do much
        # This test validates registration, not full execution


class TestSetScheduleErrorHandling:
    """Test error handling in set_schedule service."""

    @pytest.mark.asyncio
    async def test_set_schedule_wraps_exceptions(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test that exceptions from data_point.set_schedule are wrapped in HomeAssistantError."""
        from aiohomematic.exceptions import BaseHomematicException

        # Make set_schedule raise an exception
        mock_custom_data_point.set_schedule.side_effect = BaseHomematicException("Test error")

        schedule_data = {"1": {"time": "06:00", "condition": "fixed_time"}}

        # Exception should be wrapped in HomeAssistantError by @handle_homematic_errors decorator
        with pytest.raises(HomeAssistantError):
            await mock_entity.async_set_schedule(schedule_data=schedule_data)


class TestSetScheduleDataValidation:
    """Test schedule data validation."""

    @pytest.mark.asyncio
    async def test_set_schedule_with_complex_schedule(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test setting a complex multi-entry schedule."""
        schedule_data = {
            "1": {  # Weekday morning
                "weekdays": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"],
                "time": "06:00",
                "condition": "fixed_time",
                "target_channels": ["1_1"],
                "level": 0.8,
                "duration": "2h",
                "ramp_time": "10s",
            },
            "2": {  # Weekday evening
                "weekdays": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"],
                "time": "18:00",
                "condition": "fixed_time",
                "target_channels": ["1_1"],
                "level": 0.6,
                "duration": "4h",
                "ramp_time": "10s",
            },
            "3": {  # Weekend
                "weekdays": ["SATURDAY", "SUNDAY"],
                "time": "08:00",
                "condition": "fixed_time",
                "target_channels": ["1_1"],
                "level": 0.5,
                "duration": "12h",
                "ramp_time": "10s",
            },
        }

        await mock_entity.async_set_schedule(schedule_data=schedule_data)

        # Verify data_point.set_schedule was called with correct data
        mock_custom_data_point.set_schedule.assert_awaited_once_with(schedule_data=schedule_data)

    @pytest.mark.asyncio
    async def test_set_schedule_with_numeric_values(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test setting schedule with numeric values (e.g., dimmer levels)."""
        schedule_data = {
            "1": {
                "weekdays": ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"],
                "time": "06:00",
                "condition": "fixed_time",
                "target_channels": ["1_1"],
                "level": 0.75,  # 75% brightness
                "duration": "16h",
                "ramp_time": "10s",
            },
            "2": {
                "weekdays": ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"],
                "time": "22:00",
                "condition": "fixed_time",
                "target_channels": ["1_1"],
                "level": 0.25,  # 25% brightness
                "duration": "8h",
                "ramp_time": "10s",
            },
        }

        await mock_entity.async_set_schedule(schedule_data=schedule_data)

        # Verify data_point.set_schedule was called with correct data
        mock_custom_data_point.set_schedule.assert_awaited_once_with(schedule_data=schedule_data)


class TestGetScheduleServiceRegistration:
    """Test get_schedule service registration."""

    @pytest.mark.asyncio
    async def test_service_registered_for_all_domains(self, hass: HomeAssistant) -> None:
        """Test that get_schedule service is registered."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Verify service is registered
        assert hass.services.has_service(DOMAIN, HmipLocalServices.GET_SCHEDULE)


class TestAsyncGetScheduleMethod:
    """Test async_get_schedule method behavior."""

    @pytest.mark.asyncio
    async def test_get_schedule_calls_data_point_method(
        self, mock_control_unit: MagicMock, mock_custom_data_point: MagicMock
    ) -> None:
        """Test get_schedule calls data_point.get_schedule directly."""
        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=mock_custom_data_point,
        )
        entity.entity_id = "switch.test_switch"

        # Call get_schedule
        await entity.async_get_schedule()

        # Verify data_point.get_schedule was called
        mock_custom_data_point.get_schedule.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_schedule_non_custom_data_point(self, mock_control_unit: MagicMock) -> None:
        """Test that get_schedule handles non-CustomDataPointProtocol gracefully."""
        from aiohomematic.interfaces import GenericDataPointProtocol

        # Create entity with GenericDataPointProtocol (not CustomDataPointProtocol)
        generic_data_point = MagicMock(spec=GenericDataPointProtocol)
        generic_data_point.name = "TEST_SENSOR"
        generic_data_point.channel_address = "VCU0000001:1"

        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=generic_data_point,
        )
        entity.entity_id = "sensor.test_sensor"

        # Should return empty dict and log warning
        result = await entity.async_get_schedule()
        assert result == {}

    @pytest.mark.asyncio
    async def test_get_schedule_returns_empty_schedule(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test getting an empty schedule."""
        # Configure data_point.get_schedule to return empty dict
        mock_custom_data_point.get_schedule = AsyncMock(return_value={})

        result = await mock_entity.async_get_schedule()

        # Verify data_point.get_schedule was called
        mock_custom_data_point.get_schedule.assert_awaited_once()

        # Verify result is empty
        assert result == {}

    @pytest.mark.asyncio
    async def test_get_schedule_with_valid_data(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test getting schedule with valid schedule data."""
        expected_schedule = {
            "1": {
                "weekdays": ["MONDAY", "TUESDAY"],
                "time": "06:00",
                "condition": "fixed_time",
                "target_channels": ["1_1"],
                "level": 0.8,
            }
        }

        # Configure data_point.get_schedule to return expected data
        mock_custom_data_point.get_schedule = AsyncMock(return_value=expected_schedule)

        result = await mock_entity.async_get_schedule()

        # Verify data_point.get_schedule was called
        mock_custom_data_point.get_schedule.assert_awaited_once()

        # Verify result matches expected schedule
        assert result == expected_schedule

    @pytest.mark.asyncio
    async def test_get_schedule_without_schedule_support(
        self, mock_control_unit: MagicMock, mock_custom_data_point: MagicMock
    ) -> None:
        """Test get_schedule when entity doesn't support schedules."""
        # Disable schedule support
        mock_custom_data_point.has_schedule = False

        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=mock_custom_data_point,
        )
        entity.entity_id = "switch.test_switch"

        # Should return empty dict and log warning
        result = await entity.async_get_schedule()
        assert result == {}

        # Verify get_schedule was NOT called
        mock_custom_data_point.get_schedule.assert_not_called()


class TestGetScheduleServiceIntegration:
    """Test get_schedule service end-to-end integration."""

    @pytest.mark.asyncio
    async def test_service_registered_and_callable(self, hass: HomeAssistant) -> None:
        """Test that service is registered and can be called."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Service should be registered and callable
        assert hass.services.has_service(DOMAIN, HmipLocalServices.GET_SCHEDULE)

        # The service is platform-specific, so without actual entities it won't do much
        # This test validates registration, not full execution
