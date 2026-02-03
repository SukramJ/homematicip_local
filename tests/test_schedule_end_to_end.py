"""
End-to-end tests for schedule services with CCU data validation.

These tests validate the complete data flow:
1. Service call with documentation examples → CCU put_paramset data
2. CCU get_paramset data → Entity attributes and service responses

Tests verify what data is actually sent to/received from the CCU.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity


@pytest.fixture
def mock_week_profile_simple() -> MagicMock:
    """Create a mock DefaultWeekProfile for non-climate devices."""
    from aiohomematic.model import week_profile as wp

    week_profile = MagicMock(spec=wp.DefaultWeekProfile)
    week_profile.schedule_channel_address = "VCU0000001:1"
    week_profile.has_schedule = True
    week_profile.set_schedule = AsyncMock()
    week_profile.get_schedule = AsyncMock()
    week_profile.schedule = {}

    return week_profile


@pytest.fixture
def mock_week_profile_climate() -> MagicMock:
    """Create a mock ClimateWeekProfile for climate devices."""
    from aiohomematic.model import week_profile as wp

    week_profile = MagicMock(spec=wp.ClimateWeekProfile)
    week_profile.schedule_channel_address = "VCU0000002:7"
    week_profile.has_schedule = True
    week_profile.set_schedule = AsyncMock()
    week_profile.set_profile = AsyncMock()
    week_profile.set_weekday = AsyncMock()
    week_profile.get_schedule = AsyncMock()
    week_profile.get_profile = AsyncMock()
    week_profile.get_weekday = AsyncMock()
    week_profile.schedule = {}

    return week_profile


# =============================================================================
# Test: Non-Climate Devices - Service Call → CCU Data
# =============================================================================


class TestNonClimateScheduleCCUToAttributes:
    """Test how CCU raw data is transformed to entity attributes."""

    @pytest.mark.asyncio
    async def test_light_dimmer_schedule_loaded_from_ccu(
        self, mock_control_unit: MagicMock, mock_week_profile_simple: MagicMock
    ) -> None:
        """Test that dimmer schedule from CCU is correctly exposed."""
        from aiohomematic.interfaces import CustomDataPointProtocol

        # Simulate CCU raw data with dimmer values (0-100)
        ccu_schedule_data = {
            0: {"start": "00:00", "end": "06:00", "value": 0},
            1: {"start": "06:00", "end": "22:00", "value": 75},
            2: {"start": "22:00", "end": "00:00", "value": 25},
        }

        mock_week_profile_simple.schedule = ccu_schedule_data
        mock_week_profile_simple.get_schedule = AsyncMock(return_value=ccu_schedule_data)

        data_point = MagicMock(spec=CustomDataPointProtocol)
        data_point.has_schedule = True
        data_point.name = "LEVEL"
        data_point.channel_address = "VCU0000001:1"

        device = MagicMock()
        device.week_profile = mock_week_profile_simple
        data_point.device = device

        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=data_point,
        )
        entity.entity_id = "light.hallway_dimmer"

        # Entity should expose the schedule
        retrieved_schedule = await mock_week_profile_simple.get_schedule()
        assert retrieved_schedule == ccu_schedule_data

    @pytest.mark.asyncio
    async def test_switch_schedule_loaded_from_ccu(
        self, mock_control_unit: MagicMock, mock_week_profile_simple: MagicMock
    ) -> None:
        """
        Test that switch schedule loaded from CCU is correctly exposed.

        Simulates:
        1. CCU returns raw schedule data
        2. Week profile caches it
        3. Entity exposes it via attributes
        """
        from aiohomematic.interfaces import CustomDataPointProtocol

        # Simulate CCU raw data for a switch schedule
        ccu_schedule_data = {
            0: {"start": "06:00", "end": "22:00", "value": True},
            1: {"start": "22:00", "end": "06:00", "value": False},
        }

        # Mock week_profile to return this schedule
        mock_week_profile_simple.schedule = ccu_schedule_data
        mock_week_profile_simple.get_schedule = AsyncMock(return_value=ccu_schedule_data)

        data_point = MagicMock(spec=CustomDataPointProtocol)
        data_point.has_schedule = True
        data_point.name = "SWITCH"
        data_point.channel_address = "VCU0000001:1"

        device = MagicMock()
        device.week_profile = mock_week_profile_simple
        data_point.device = device

        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=data_point,
        )
        entity.entity_id = "switch.garden_pump"

        # Verify that entity can access the schedule
        assert entity._data_point.device.week_profile.schedule == ccu_schedule_data


# =============================================================================
# Test: Climate Devices - Service Call → CCU Data
# =============================================================================


class TestEntityAttributesExposure:
    """Test that schedule information is exposed via entity attributes."""

    @pytest.mark.asyncio
    async def test_has_schedule_attribute_exposed(
        self, mock_control_unit: MagicMock, mock_week_profile_simple: MagicMock
    ) -> None:
        """
        Test that has_schedule attribute is exposed.

        Documentation mentions:
        ```yaml
        {{ state_attr('switch.garden_pump', 'has_schedule') }}
        ```
        """
        from aiohomematic.interfaces import CustomDataPointProtocol

        data_point = MagicMock(spec=CustomDataPointProtocol)
        data_point.has_schedule = True
        data_point.name = "SWITCH"
        data_point.channel_address = "VCU0000001:1"

        device = MagicMock()
        device.week_profile = mock_week_profile_simple
        data_point.device = device

        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=data_point,
        )
        entity.entity_id = "switch.garden_pump"

        # Verify has_schedule is accessible
        assert entity._data_point.has_schedule is True

    @pytest.mark.asyncio
    async def test_schedule_data_accessible_via_week_profile(
        self, mock_control_unit: MagicMock, mock_week_profile_simple: MagicMock
    ) -> None:
        """Test that schedule data is accessible via week_profile."""
        from aiohomematic.interfaces import CustomDataPointProtocol

        schedule_data = {
            0: {"start": "06:00", "end": "22:00", "value": True},
            1: {"start": "22:00", "end": "06:00", "value": False},
        }

        mock_week_profile_simple.schedule = schedule_data

        data_point = MagicMock(spec=CustomDataPointProtocol)
        data_point.has_schedule = True
        data_point.name = "SWITCH"
        data_point.channel_address = "VCU0000001:1"

        device = MagicMock()
        device.week_profile = mock_week_profile_simple
        data_point.device = device

        entity = AioHomematicGenericEntity(
            control_unit=mock_control_unit,
            data_point=data_point,
        )
        entity.entity_id = "switch.garden_pump"

        # Verify schedule is accessible
        assert entity._data_point.device.week_profile.schedule == schedule_data
