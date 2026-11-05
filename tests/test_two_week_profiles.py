"""Tests for devices with a switch schedule and a climate schedule, like HmIP-WGT."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiohomematic.const import DataPointCategory, DataPointUsage
from aiohomematic.interfaces import (
    ClimateWeekProfileDataPointProtocol,
    CustomDataPointProtocol,
    WeekProfileDataPointProtocol,
)
from aiohomematic.model.custom import BaseCustomDpClimate
from custom_components.homematicip_local.climate import AioHomematicClimate
from custom_components.homematicip_local.generic_entity import ATTR_SCHEDULE_DATA, AioHomematicGenericEntity
from custom_components.homematicip_local.sensor import AioHomematicWeekProfileSensor
from custom_components.homematicip_local.services import (
    ATTR_PROFILE,
    _async_service_get_schedule,
    _async_service_get_schedule_profile,
)

SWITCH_SCHEDULE = {"entries": {"1": "switch"}}
CLIMATE_SCHEDULE = {"P1": "climate"}


@pytest.fixture(autouse=True)
def patch_get_data_point() -> Generator[None]:
    """Let the entities take the mock data point as it is."""
    with patch(
        "custom_components.homematicip_local.generic_entity.get_data_point",
        side_effect=lambda data_point: data_point,
    ):
        yield


def _make_device() -> MagicMock:
    """Return a device with both schedules."""
    switch_dp = MagicMock(spec=WeekProfileDataPointProtocol)
    switch_dp.get_schedule = AsyncMock(return_value=SWITCH_SCHEDULE)
    switch_dp.schedule = SWITCH_SCHEDULE
    climate_dp = MagicMock(spec=ClimateWeekProfileDataPointProtocol)
    climate_dp.get_schedule_profile = AsyncMock(return_value=CLIMATE_SCHEDULE)
    climate_dp.schedule = CLIMATE_SCHEDULE
    device = MagicMock()
    device.name = "Glass thermostat"
    device.week_profile_data_point = switch_dp
    device.climate_week_profile_data_point = climate_dp
    device.week_profile_data_points = (switch_dp, climate_dp)
    return device


class TestServices:
    """The services pick the schedule they are about."""

    @pytest.mark.asyncio
    async def test_climate_service_uses_the_climate_schedule(self) -> None:
        """A climate service works although week_profile_data_point is the switch schedule."""
        device = _make_device()
        service = MagicMock()
        service.data = {ATTR_PROFILE: "P1"}
        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=device,
        ):
            result = await _async_service_get_schedule_profile(hass=MagicMock(), service=service)
        assert result == CLIMATE_SCHEDULE

    @pytest.mark.asyncio
    async def test_get_schedule_stays_on_the_switch_schedule(self) -> None:
        """The generic service keeps its target, as existing automations rely on it."""
        device = _make_device()
        with patch(
            "custom_components.homematicip_local.services._async_get_hm_device_by_service_data",
            return_value=device,
        ):
            result = await _async_service_get_schedule(hass=MagicMock(), service=MagicMock())
        assert result == SWITCH_SCHEDULE


class TestEntities:
    """The entities show the schedule that belongs to them."""

    def test_climate_entity_binds_the_climate_schedule(self) -> None:
        """The thermostat gets its profiles and schedule from the climate schedule."""
        device = _make_device()
        data_point = MagicMock(spec=BaseCustomDpClimate)
        data_point.device = device
        data_point.target_temperature_step = 0.5
        entity = AioHomematicClimate(control_unit=MagicMock(), data_point=data_point)
        assert entity._week_profile_data_point is device.climate_week_profile_data_point

    @pytest.mark.parametrize(
        ("category", "schedule"),
        [
            (DataPointCategory.CLIMATE, CLIMATE_SCHEDULE),
            (DataPointCategory.LIGHT, SWITCH_SCHEDULE),
        ],
    )
    def test_schedule_attribute_follows_the_category(self, category: DataPointCategory, schedule: dict) -> None:
        """A primary custom entity shows the schedule of its own kind."""
        data_point = MagicMock(spec=CustomDataPointProtocol)
        data_point.device = _make_device()
        data_point.category = category
        data_point.usage = DataPointUsage.CDP_PRIMARY
        data_point.additional_information = {}
        entity = AioHomematicGenericEntity(control_unit=MagicMock(), data_point=data_point)
        assert entity.extra_state_attributes[ATTR_SCHEDULE_DATA] == schedule

    @pytest.mark.parametrize(
        ("is_climate", "schedule_count", "translation_key"),
        [
            (True, 2, "climate_week_profile"),
            (False, 2, "week_profile"),
            (True, 1, "week_profile"),
        ],
    )
    def test_sensor_name_tells_two_schedules_apart(
        self, is_climate: bool, schedule_count: int, translation_key: str
    ) -> None:
        """Only next to a switch schedule does the climate sensor need a name of its own."""
        data_point = MagicMock(spec=ClimateWeekProfileDataPointProtocol if is_climate else WeekProfileDataPointProtocol)
        data_point.device = MagicMock()
        data_point.device.week_profile_data_points = tuple(MagicMock() for _ in range(schedule_count))
        entity = AioHomematicWeekProfileSensor(control_unit=MagicMock(), data_point=data_point)
        assert entity.translation_key == translation_key
