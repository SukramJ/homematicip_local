"""
Functional tests for schedule services.

Tests the actual behavior of the schedule services including:
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
        """Test that set_schedule services are registered for all domains."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Verify services are registered for all domains
        assert hass.services.has_service(DOMAIN, HmipLocalServices.COVER_SET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.LIGHT_SET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SWITCH_SET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.VALVE_SET_SCHEDULE)


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
        """Test that services are registered and can be called."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Services should be registered and callable for all domains
        assert hass.services.has_service(DOMAIN, HmipLocalServices.COVER_SET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.LIGHT_SET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SWITCH_SET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.VALVE_SET_SCHEDULE)

        # The services are platform-specific, so without actual entities they won't do much
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

    @pytest.mark.asyncio
    async def test_set_schedule_wraps_validation_error(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test that Pydantic ValidationError is wrapped in HomeAssistantError."""
        from pydantic import ValidationError
        from pydantic_core import InitErrorDetails, PydanticCustomError

        # Create a Pydantic ValidationError
        error = PydanticCustomError("value_error", "Invalid level value")
        errors: list[InitErrorDetails] = [{"type": error, "loc": ("level",), "input": 2.0}]
        mock_custom_data_point.set_schedule.side_effect = ValidationError.from_exception_data(
            "SimpleScheduleEntry", errors
        )

        schedule_data = {"1": {"time": "06:00", "level": 2.0}}

        # ValidationError should be wrapped in HomeAssistantError
        with pytest.raises(HomeAssistantError, match="Invalid schedule data"):
            await mock_entity.async_set_schedule(schedule_data=schedule_data)

    @pytest.mark.asyncio
    async def test_set_schedule_wraps_value_error(
        self, mock_entity: AioHomematicGenericEntity, mock_custom_data_point: MagicMock
    ) -> None:
        """Test that ValueError from domain-specific validation is wrapped in HomeAssistantError."""
        # Make set_schedule raise a ValueError (domain-specific validation)
        mock_custom_data_point.set_schedule.side_effect = ValueError("Switch level must be 0.0 or 1.0")

        schedule_data = {"1": {"time": "06:00", "level": 0.5}}

        # ValueError should be wrapped in HomeAssistantError
        with pytest.raises(HomeAssistantError, match="Switch level must be 0.0 or 1.0"):
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
        """Test that get_schedule services are registered for all domains."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Verify services are registered for all domains
        assert hass.services.has_service(DOMAIN, HmipLocalServices.COVER_GET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.LIGHT_GET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SWITCH_GET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.VALVE_GET_SCHEDULE)


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
        """Test that services are registered and can be called."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Services should be registered and callable for all domains
        assert hass.services.has_service(DOMAIN, HmipLocalServices.COVER_GET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.LIGHT_GET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SWITCH_GET_SCHEDULE)
        assert hass.services.has_service(DOMAIN, HmipLocalServices.VALVE_GET_SCHEDULE)

        # The services are platform-specific, so without actual entities they won't do much
        # This test validates registration, not full execution


class TestScheduleSchemaValidation:
    """Test domain-specific Voluptuous schema validation."""

    def test_cover_schema_accepts_level_2(self) -> None:
        """Test cover schema accepts level_2 field."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_COVER_SCHEDULE_DATA

        valid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "08:00",
                    "target_channels": ["1_1"],
                    "level": 0.5,
                    "level_2": 0.3,
                }
            }
        }

        # Should not raise
        result = vol.Schema(SCHEMA_COVER_SCHEDULE_DATA)(valid_data)
        assert result["schedule_data"]["1"]["level_2"] == 0.3

    def test_cover_schema_rejects_duration(self) -> None:
        """Test cover schema rejects duration field."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_COVER_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "08:00",
                    "target_channels": ["1_1"],
                    "level": 0.5,
                    "duration": "30min",  # Not allowed for cover
                }
            }
        }

        with pytest.raises(vol.Invalid, match="extra keys not allowed"):
            vol.Schema(SCHEMA_COVER_SCHEDULE_DATA)(invalid_data)

    def test_light_schema_accepts_ramp_time(self) -> None:
        """Test light schema accepts ramp_time field."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_LIGHT_SCHEDULE_DATA

        valid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 0.8,
                    "duration": "2h",
                    "ramp_time": "10s",
                }
            }
        }

        # Should not raise
        result = vol.Schema(SCHEMA_LIGHT_SCHEDULE_DATA)(valid_data)
        assert result["schedule_data"]["1"]["ramp_time"] == "10s"

    def test_light_schema_rejects_level_2(self) -> None:
        """Test light schema rejects level_2 field."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_LIGHT_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 0.8,
                    "level_2": 0.5,  # Not allowed for light
                }
            }
        }

        with pytest.raises(vol.Invalid, match="extra keys not allowed"):
            vol.Schema(SCHEMA_LIGHT_SCHEDULE_DATA)(invalid_data)

    def test_schema_rejects_invalid_entry_number(self) -> None:
        """Test schema rejects entry number outside 1-24 range."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_SWITCH_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "25": {  # Invalid: must be 1-24
                    "weekdays": ["MONDAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 1.0,
                }
            }
        }

        with pytest.raises(vol.Invalid, match="must be 1-24"):
            vol.Schema(SCHEMA_SWITCH_SCHEDULE_DATA)(invalid_data)

    def test_schema_rejects_invalid_target_channel(self) -> None:
        """Test schema rejects invalid target_channels format."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_SWITCH_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "06:00",
                    "target_channels": ["invalid"],  # Invalid format
                    "level": 1.0,
                }
            }
        }

        with pytest.raises(vol.Invalid, match="Invalid channel format"):
            vol.Schema(SCHEMA_SWITCH_SCHEDULE_DATA)(invalid_data)

    def test_schema_rejects_invalid_time_format(self) -> None:
        """Test schema rejects invalid time format."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_SWITCH_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "25:00",  # Invalid hour
                    "target_channels": ["1_1"],
                    "level": 1.0,
                }
            }
        }

        with pytest.raises(vol.Invalid, match="Invalid time format"):
            vol.Schema(SCHEMA_SWITCH_SCHEDULE_DATA)(invalid_data)

    def test_schema_rejects_invalid_weekday(self) -> None:
        """Test schema rejects invalid weekday values."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_SWITCH_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["INVALID_DAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 1.0,
                }
            }
        }

        with pytest.raises(vol.Invalid, match="Invalid weekday"):
            vol.Schema(SCHEMA_SWITCH_SCHEDULE_DATA)(invalid_data)

    def test_switch_schema_accepts_valid_data(self) -> None:
        """Test switch schema accepts valid schedule data."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_SWITCH_SCHEDULE_DATA

        valid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY", "TUESDAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 1.0,
                    "duration": "30min",
                }
            }
        }

        # Should not raise
        result = vol.Schema(SCHEMA_SWITCH_SCHEDULE_DATA)(valid_data)
        assert result["schedule_data"]["1"]["level"] == 1.0

    def test_switch_schema_rejects_non_binary_level(self) -> None:
        """Test switch schema rejects level values other than 0.0 or 1.0."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_SWITCH_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 0.5,  # Invalid for switch
                }
            }
        }

        with pytest.raises(vol.Invalid, match="Switch level must be 0.0 or 1.0"):
            vol.Schema(SCHEMA_SWITCH_SCHEDULE_DATA)(invalid_data)

    def test_switch_schema_rejects_ramp_time(self) -> None:
        """Test switch schema rejects ramp_time field."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_SWITCH_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 1.0,
                    "ramp_time": "10s",  # Not allowed for switch
                }
            }
        }

        with pytest.raises(vol.Invalid, match="extra keys not allowed"):
            vol.Schema(SCHEMA_SWITCH_SCHEDULE_DATA)(invalid_data)

    def test_valve_schema_accepts_duration(self) -> None:
        """Test valve schema accepts duration field."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_VALVE_SCHEDULE_DATA

        valid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 1.0,
                    "duration": "30min",
                }
            }
        }

        # Should not raise
        result = vol.Schema(SCHEMA_VALVE_SCHEDULE_DATA)(valid_data)
        assert result["schedule_data"]["1"]["duration"] == "30min"

    def test_valve_schema_rejects_level_2(self) -> None:
        """Test valve schema rejects level_2 field."""
        import voluptuous as vol

        from custom_components.homematicip_local.services import SCHEMA_VALVE_SCHEDULE_DATA

        invalid_data = {
            "schedule_data": {
                "1": {
                    "weekdays": ["MONDAY"],
                    "time": "06:00",
                    "target_channels": ["1_1"],
                    "level": 1.0,
                    "level_2": 0.5,  # Not allowed for valve
                }
            }
        }

        with pytest.raises(vol.Invalid, match="extra keys not allowed"):
            vol.Schema(SCHEMA_VALVE_SCHEDULE_DATA)(invalid_data)
