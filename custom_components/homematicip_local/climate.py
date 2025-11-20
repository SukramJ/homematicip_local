"""Climate platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timedelta
import logging
from typing import Any, Final, cast

from aiohomematic.const import (
    CLIMATE_PROFILE_DICT,
    CLIMATE_SIMPLE_PROFILE_DICT,
    CLIMATE_SIMPLE_WEEKDAY_DATA,
    CLIMATE_WEEKDAY_DICT,
    DataPointCategory,
    ScheduleProfile,
    WeekdayStr,
)
from aiohomematic.model.custom import (
    PROFILE_PREFIX,
    BaseCustomDpClimate,
    ClimateActivity,
    ClimateMode,
    ClimateProfile,
    CustomDpIpThermostat,
)
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ATTR_CURRENT_HUMIDITY,
    ATTR_CURRENT_TEMPERATURE,
    ATTR_PRESET_MODE,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_NONE,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, STATE_UNAVAILABLE, STATE_UNKNOWN, UnitOfTemperature
from homeassistant.core import HomeAssistant, ServiceResponse, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HomematicConfigEntry
from .control_unit import ControlUnit, signal_new_data_point
from .generic_entity import ATTR_SCHEDULE_DATA, AioHomematicGenericEntity, AioHomematicGenericRestoreEntity

_LOGGER = logging.getLogger(__name__)

ATTR_OPTIMUM_START_STOP: Final = "optimum_start_stop"
ATTR_TEMPERATURE_OFFSET: Final = "temperature_offset"
ATTR_ACTIVE_PROFILE: Final = "active_profile"
ATTR_AVAILABLE_PROFILES: Final = "available_profiles"
ATTR_SIMPLE_SCHEDULE_DATA: Final = "simple_schedule_data"

SUPPORTED_HA_PRESET_MODES: Final = [
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_NONE,
]

HM_TO_HA_HVAC_MODE: Mapping[ClimateMode, HVACMode] = {
    ClimateMode.AUTO: HVACMode.AUTO,
    ClimateMode.COOL: HVACMode.COOL,
    ClimateMode.HEAT: HVACMode.HEAT,
    ClimateMode.OFF: HVACMode.OFF,
}

HA_TO_HM_HVAC_MODE: Mapping[HVACMode, ClimateMode] = {v: k for k, v in HM_TO_HA_HVAC_MODE.items()}

HM_TO_HA_ACTION: Mapping[ClimateActivity, HVACAction] = {
    ClimateActivity.COOL: HVACAction.COOLING,
    ClimateActivity.HEAT: HVACAction.HEATING,
    ClimateActivity.IDLE: HVACAction.IDLE,
    ClimateActivity.OFF: HVACAction.OFF,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU climate platform."""
    control_unit: ControlUnit = entry.runtime_data

    @callback
    def async_add_climate(data_points: tuple[BaseCustomDpClimate, ...]) -> None:
        """Add climate from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_CLIMATE: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicClimate(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.CLIMATE),
            target=async_add_climate,
        )
    )

    async_add_climate(data_points=control_unit.get_new_data_points(data_point_type=BaseCustomDpClimate))


class AioHomematicClimate(AioHomematicGenericRestoreEntity[BaseCustomDpClimate], ClimateEntity):
    """Representation of the HomematicIP climate entity."""

    _attr_translation_key = "hmip_climate"
    _enable_turn_on_off_backwards_compatibility: bool = False
    __no_recored_attributes = AioHomematicGenericEntity.NO_RECORDED_ATTRIBUTES
    __no_recored_attributes.update(
        {ATTR_AVAILABLE_PROFILES, ATTR_OPTIMUM_START_STOP, ATTR_TEMPERATURE_OFFSET, ATTR_SIMPLE_SCHEDULE_DATA}
    )
    _unrecorded_attributes = frozenset(__no_recored_attributes)

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: BaseCustomDpClimate,
    ) -> None:
        """Initialize the climate entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_target_temperature_step = data_point.target_temperature_step
        # Schedule attributes (only for entities that support schedules)
        self._current_profile: ScheduleProfile = ScheduleProfile.P1

    @property
    def current_humidity(self) -> int | None:
        """Return the current humidity."""
        if self._data_point.is_valid:
            return self._data_point.current_humidity
        if self.is_restored and self._restored_state:
            return self._restored_state.attributes.get(ATTR_CURRENT_HUMIDITY)
        return None

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if self._data_point.is_valid:
            return self._data_point.current_temperature
        if self.is_restored and self._restored_state:
            return self._restored_state.attributes.get(ATTR_CURRENT_TEMPERATURE)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the climate entity."""
        attributes = super().extra_state_attributes
        if (
            hasattr(self._data_point, "temperature_offset")
            and (temperature_offset := self._data_point.temperature_offset) is not None
        ):
            attributes[ATTR_TEMPERATURE_OFFSET] = temperature_offset
        if (
            hasattr(self._data_point, "optimum_start_stop")
            and (optimum_start_stop := self._data_point.optimum_start_stop) is not None
        ):
            attributes[ATTR_OPTIMUM_START_STOP] = optimum_start_stop

        # Add schedule attributes if this entity supports schedules
        if self._data_point.supports_schedule:
            attributes[ATTR_ACTIVE_PROFILE] = self._current_profile.value
            attributes[ATTR_AVAILABLE_PROFILES] = [
                profile.value for profile in self._data_point.available_schedule_profiles
            ]
            if schedule_data := self._data_point.schedule.get(self._current_profile):
                attributes[ATTR_SCHEDULE_DATA] = schedule_data
            if simple_schedule_data := self._data_point.simple_schedule.get(self._current_profile):
                attributes[ATTR_SIMPLE_SCHEDULE_DATA] = simple_schedule_data

        return attributes

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the hvac action."""
        if self._data_point.activity and self._data_point.activity in HM_TO_HA_ACTION:
            return HM_TO_HA_ACTION[self._data_point.activity]
        if isinstance(self._data_point, CustomDpIpThermostat) and (
            getattr(self.data_point, "_peer_level_dp") is not None
            or getattr(self.data_point, "_peer_state_dp") is not None
        ):
            return HVACAction.IDLE
        return None

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return hvac mode."""
        if self._data_point.is_valid:
            if self._data_point.mode in HM_TO_HA_HVAC_MODE:
                return HM_TO_HA_HVAC_MODE[self._data_point.mode]
            return HVACMode.OFF
        if (
            self.is_restored
            and self._restored_state
            and (restored_state := self._restored_state.state)
            not in (
                STATE_UNKNOWN,
                STATE_UNAVAILABLE,
            )
        ):
            return HVACMode(value=restored_state)
        return None

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """Return the list of available hvac modes."""
        return [HM_TO_HA_HVAC_MODE[mode] for mode in self._data_point.modes if mode in HM_TO_HA_HVAC_MODE]

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        return self._data_point.max_temp

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        return self._data_point.min_temp

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode."""
        if (
            self._data_point.is_valid
            and self._data_point.profile in SUPPORTED_HA_PRESET_MODES
            or str(self._data_point.profile).startswith(PROFILE_PREFIX)
        ):
            return self._data_point.profile
        if self.is_restored and self._restored_state:
            return self._restored_state.attributes.get(ATTR_PRESET_MODE)
        return None

    @property
    def preset_modes(self) -> list[str]:
        """Return a list of available preset modes incl. hmip profiles."""
        preset_modes = []
        for profile in self._data_point.profiles:
            if profile in SUPPORTED_HA_PRESET_MODES:
                preset_modes.append(profile.value)
            if str(profile).startswith(PROFILE_PREFIX):
                preset_modes.append(profile.value)
        return preset_modes

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Return the list of supported features."""
        supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_OFF | ClimateEntityFeature.TURN_ON
        )
        if self._data_point.supports_profiles:
            supported_features |= ClimateEntityFeature.PRESET_MODE
        return supported_features

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        if self._data_point.is_valid:
            return self._data_point.target_temperature
        if self.is_restored and self._restored_state:
            return self._restored_state.attributes.get(ATTR_TEMPERATURE)
        return None

    async def async_copy_schedule(self, source_entity_id: str) -> None:
        """Copy a schedule from this entity to another."""
        if source_climate_data_point := cast(
            BaseCustomDpClimate,
            self._data_point.device.data_point_provider.get_data_point_by_custom_id(custom_id=source_entity_id),
        ):
            await source_climate_data_point.copy_schedule(target_climate_data_point=self._data_point)

    async def async_copy_schedule_profile(
        self, source_profile: ScheduleProfile, target_profile: ScheduleProfile, source_entity_id: str | None = None
    ) -> None:
        """Copy a schedule profile."""
        if source_entity_id and (
            source_climate_data_point := cast(
                BaseCustomDpClimate,
                self._data_point.device.data_point_provider.get_data_point_by_custom_id(custom_id=source_entity_id),
            )
        ):
            await source_climate_data_point.copy_schedule_profile(
                source_profile=source_profile,
                target_profile=target_profile,
                target_climate_data_point=self._data_point,
            )
        else:
            await self._data_point.copy_schedule_profile(source_profile=source_profile, target_profile=target_profile)

    async def async_disable_away_mode(self) -> None:
        """Disable the away mode on thermostat."""
        await self._data_point.disable_away_mode()

    async def async_enable_away_mode_by_calendar(
        self,
        end: datetime,
        away_temperature: float,
        start: datetime | None = None,
    ) -> None:
        """Enable the away mode by calendar on thermostat."""
        start = start or datetime.now() - timedelta(minutes=10)
        await self._data_point.enable_away_mode_by_calendar(start=start, end=end, away_temperature=away_temperature)

    async def async_enable_away_mode_by_duration(self, hours: int, away_temperature: float) -> None:
        """Enable the away mode by duration on thermostat."""
        await self._data_point.enable_away_mode_by_duration(hours=hours, away_temperature=away_temperature)

    async def async_get_schedule_profile(self, profile: str | ScheduleProfile) -> ServiceResponse:
        """Get a schedule profile."""
        try:
            schedule_profile = profile if isinstance(profile, ScheduleProfile) else ScheduleProfile(profile)
            if profile_data := await self._data_point.get_schedule_profile(profile=schedule_profile):
                return cast(ServiceResponse, profile_data)
        except Exception as err:
            _LOGGER.error(
                "Failed to get schedule profile %s for %s: %s",
                profile,
                self._data_point.custom_id,
                err,
            )
        return None

    async def async_get_schedule_weekday(
        self, profile: str | ScheduleProfile, weekday: str | WeekdayStr
    ) -> ServiceResponse:
        """Get a schedule profile weekday."""
        try:
            schedule_profile = profile if isinstance(profile, ScheduleProfile) else ScheduleProfile(profile)
            schedule_weekday = weekday if isinstance(weekday, WeekdayStr) else WeekdayStr(weekday)
            if weekday_data := await self._data_point.get_schedule_weekday(
                profile=schedule_profile, weekday=schedule_weekday
            ):
                return cast(ServiceResponse, weekday_data)
        except Exception as err:
            _LOGGER.error(
                "Failed to get schedule profile weekday %s/%s for %s: %s",
                profile,
                weekday,
                self._data_point.custom_id,
                err,
            )
        return None

    async def async_set_active_profile(self, profile: str | ScheduleProfile) -> None:
        """Set the active profile."""
        try:
            schedule_profile = profile if isinstance(profile, ScheduleProfile) else ScheduleProfile(profile)
            profile_key = schedule_profile.value
            self._current_profile = schedule_profile

            self.async_write_ha_state()

            _LOGGER.debug(
                "Set active profile %s for %s",
                profile_key,
                self._data_point.custom_id,
            )
        except Exception as err:
            _LOGGER.error(
                "Failed to set active profile %s for %s: %s",
                profile,
                self._data_point.custom_id,
                err,
            )

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode not in HA_TO_HM_HVAC_MODE:
            _LOGGER.warning("Hvac mode %s is not supported by integration", hvac_mode)
            return
        await self._data_point.set_mode(mode=HA_TO_HM_HVAC_MODE[hvac_mode])

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        if preset_mode not in self.preset_modes:
            _LOGGER.warning(
                "Preset mode %s is not supported in hvac_mode %s",
                preset_mode,
                self.hvac_mode,
            )
            return
        await self._data_point.set_profile(profile=ClimateProfile(preset_mode))

    async def async_set_schedule_profile(
        self, profile: str | ScheduleProfile, profile_data: CLIMATE_PROFILE_DICT
    ) -> None:
        """Set a schedule profile."""
        try:
            schedule_profile = profile if isinstance(profile, ScheduleProfile) else ScheduleProfile(profile)
            # Convert string keys to WeekdayStr if needed
            converted_data = {}
            for weekday_key, weekday_value in profile_data.items():
                if isinstance(weekday_key, str):
                    weekday_key = WeekdayStr(weekday_key)
                converted_data[weekday_key] = weekday_value

            await self._data_point.set_schedule_profile(profile=schedule_profile, profile_data=converted_data)

            _LOGGER.debug(
                "Set schedule profile %s for %s",
                schedule_profile.value,
                self._data_point.custom_id,
            )
        except Exception as err:
            _LOGGER.error(
                "Failed to set schedule profile %s for %s: %s",
                profile,
                self._data_point.custom_id,
                err,
            )

    async def async_set_schedule_simple_profile(
        self, profile: ScheduleProfile, simple_profile_data: CLIMATE_SIMPLE_PROFILE_DICT
    ) -> None:
        """Set the schedule simple profile."""
        await self._data_point.set_simple_schedule_profile(
            profile=profile,
            simple_profile_data=simple_profile_data,
        )

    async def async_set_schedule_simple_weekday(
        self,
        profile: ScheduleProfile,
        weekday: WeekdayStr,
        simple_weekday_data: CLIMATE_SIMPLE_WEEKDAY_DATA,
    ) -> None:
        """Set the schedule simple profile weekday."""
        await self._data_point.set_simple_schedule_weekday(
            profile=profile,
            weekday=weekday,
            simple_weekday_data=simple_weekday_data,
        )

    async def async_set_schedule_weekday(
        self, profile: str | ScheduleProfile, weekday: str | WeekdayStr, weekday_data: CLIMATE_WEEKDAY_DICT
    ) -> None:
        """Set a schedule profile weekday."""
        try:
            schedule_profile = profile if isinstance(profile, ScheduleProfile) else ScheduleProfile(profile)
            schedule_weekday = weekday if isinstance(weekday, WeekdayStr) else WeekdayStr(weekday)

            await self._data_point.set_schedule_weekday(
                profile=schedule_profile,
                weekday=schedule_weekday,
                weekday_data=weekday_data,
            )

            _LOGGER.debug(
                "Set schedule profile weekday %s/%s for %s",
                schedule_profile.value,
                weekday,
                self._data_point.custom_id,
            )
        except Exception as err:
            _LOGGER.error(
                "Failed to set schedule profile weekday %s/%s for %s: %s",
                profile,
                weekday,
                self._data_point.custom_id,
                err,
            )

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        await self._data_point.set_temperature(temperature=temperature)
