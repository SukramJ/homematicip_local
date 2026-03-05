"""Sensor platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import logging
from typing import Any, Final, cast, override

from aiohomematic.const import DEFAULT_MULTIPLIER, DataPointCategory, HubValueType, ParameterType
from aiohomematic.interfaces import (
    CalculatedDataPointProtocol,
    ClimateWeekProfileDataPointProtocol,
    CombinedDataPointProtocol,
    GenericDataPointProtocol,
)
from aiohomematic.model.generic import DpSensor
from aiohomematic.model.hub import SysvarDpSensor
from aiohomematic.model.week_profile_data_point import WeekProfileDataPoint
from homeassistant.components.sensor import RestoreSensor, SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import ATTR_CONFIG_ENTRY_ID
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import HomematicConfigEntry
from .const import CLIMATE_SCHEDULE_API_VERSION, SCHEDULE_API_VERSION, HmEntityState
from .control_unit import ControlUnit, signal_new_data_point
from .entity_helpers import HmSensorEntityDescription
from .generic_entity import (
    ATTR_SCHEDULE_DATA,
    ATTR_VALUE_STATE,
    AioHomematicGenericEntity,
    AioHomematicGenericSysvarEntity,
)

ATTR_CURRENT_SCHEDULE_PROFILE: Final = "active_profile"
ATTR_AVAILABLE_PROFILES: Final = "available_profiles"
ATTR_AVAILABLE_TARGET_CHANNELS: Final = "available_target_channels"
ATTR_DEVICE_ACTIVE_PROFILE_INDEX: Final = "device_active_profile_index"
ATTR_MAX_ENTRIES: Final = "max_entries"
ATTR_MAX_TEMP: Final = "max_temp"
ATTR_MIN_TEMP: Final = "min_temp"
ATTR_SCHEDULE_API_VERSION: Final = "schedule_api_version"
ATTR_SCHEDULE_CHANNEL_ADDRESS: Final = "schedule_channel_address"
ATTR_SCHEDULE_DOMAIN: Final = "schedule_domain"
ATTR_SCHEDULE_TYPE: Final = "schedule_type"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU sensor platform."""
    control_unit: ControlUnit = entry.runtime_data

    @callback
    def async_add_sensor(
        data_points: tuple[
            GenericDataPointProtocol[Any] | CalculatedDataPointProtocol | CombinedDataPointProtocol, ...
        ],
    ) -> None:
        """Add sensor from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_SENSOR: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicSensor(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
            if not isinstance(data_point, CombinedDataPointProtocol)
        ]:
            async_add_entities(entities)

    @callback
    def async_add_hub_sensor(data_points: tuple[SysvarDpSensor, ...]) -> None:
        """Add sysvar sensor from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_HUB_SENSOR: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicSysvarSensor(control_unit=control_unit, data_point=data_point) for data_point in data_points
        ]:
            async_add_entities(entities)

    @callback
    def async_add_week_profile_sensor(data_points: tuple[WeekProfileDataPoint, ...]) -> None:
        """Add week profile sensor from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_WEEK_PROFILE_SENSOR: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicWeekProfileSensor(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.SENSOR),
            target=async_add_sensor,
        )
    )
    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.HUB_SENSOR),
            target=async_add_hub_sensor,
        )
    )
    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.WEEK_PROFILE),
            target=async_add_week_profile_sensor,
        )
    )

    async_add_sensor(data_points=control_unit.get_new_data_points(data_point_type=DpSensor))

    async_add_hub_sensor(data_points=control_unit.get_new_hub_data_points(data_point_type=SysvarDpSensor))

    async_add_week_profile_sensor(data_points=control_unit.get_new_data_points(data_point_type=WeekProfileDataPoint))


class AioHomematicSensor(
    AioHomematicGenericEntity[GenericDataPointProtocol[Any] | CalculatedDataPointProtocol], RestoreSensor
):
    """Representation of the HomematicIP sensor entity."""

    entity_description: HmSensorEntityDescription
    _restored_native_value: Any = None

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: GenericDataPointProtocol[Any] | CalculatedDataPointProtocol,
    ) -> None:
        """Initialize the sensor entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        self._multiplier: float = (
            self.entity_description.multiplier
            if hasattr(self, "entity_description")
            and self.entity_description
            and self.entity_description.multiplier is not None
            else data_point.multiplier
        )
        if not hasattr(self, "entity_description") and data_point.unit:
            self._attr_native_unit_of_measurement = data_point.unit

        if data_point.values:
            if self.device_class != SensorDeviceClass.ENUM:
                self._attr_device_class = SensorDeviceClass.ENUM
            self._attr_options = [item.lower() for item in data_point.values] if data_point.values else None

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the generic entity."""
        attributes = super().extra_state_attributes
        if self.is_restored:
            attributes[ATTR_VALUE_STATE] = HmEntityState.RESTORED

        return attributes

    @property
    def is_restored(self) -> bool:
        """Return if the state is restored."""
        return not self._data_point.is_valid and self._restored_native_value is not None

    @property
    @override
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the native value of the entity."""
        if self._data_point.is_valid:
            if (
                self._data_point.value is not None
                and self._data_point.hmtype in (ParameterType.FLOAT, ParameterType.INTEGER)
                and self._multiplier != DEFAULT_MULTIPLIER
            ):
                new_value = self._data_point.value * self._multiplier
                return int(new_value) if self._data_point.hmtype == ParameterType.INTEGER else new_value
            # Strings and enums with custom device class must be lowercase
            # to be translatable.
            if self._data_point.value is not None and self._data_point.hmtype in (
                ParameterType.ENUM,
                ParameterType.STRING,
            ):
                return cast(StateType | date | datetime | Decimal, self._data_point.value.lower())
            return cast(StateType | date | datetime | Decimal, self._data_point.value)
        if self.is_restored:
            return cast(StateType | date | datetime | Decimal, self._restored_native_value)
        return None

    @override
    async def async_added_to_hass(self) -> None:
        """Check, if state needs to be restored."""
        await super().async_added_to_hass()
        if not self._data_point.is_valid and (restored_sensor_data := await self.async_get_last_sensor_data()):
            self._restored_native_value = restored_sensor_data.native_value


class AioHomematicSysvarSensor(AioHomematicGenericSysvarEntity[SysvarDpSensor], SensorEntity):
    """Representation of the HomematicIP hub sensor entity."""

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: SysvarDpSensor,
    ) -> None:
        """Initialize the sensor entity."""
        super().__init__(control_unit=control_unit, data_point=data_point)
        if not hasattr(self, "entity_description"):
            if data_point.data_type == HubValueType.LIST:
                self._attr_options = list(data_point.values) if data_point.values else None
                self._attr_device_class = SensorDeviceClass.ENUM
            elif data_point.data_type in (
                HubValueType.FLOAT,
                HubValueType.INTEGER,
            ):
                self._attr_state_class = SensorStateClass.MEASUREMENT
                if unit := data_point.unit:
                    self._attr_native_unit_of_measurement = unit

    @property
    @override
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the native value of the entity."""
        return self._data_point.value  # type: ignore[no-any-return]


class AioHomematicWeekProfileSensor(AioHomematicGenericEntity[WeekProfileDataPoint], SensorEntity):
    """Representation of the HomematicIP week profile sensor entity."""

    _attr_translation_key = "week_profile"

    __no_recored_attributes = AioHomematicGenericEntity.NO_RECORDED_ATTRIBUTES
    __no_recored_attributes.update(
        {
            ATTR_CURRENT_SCHEDULE_PROFILE,
            ATTR_AVAILABLE_PROFILES,
            ATTR_AVAILABLE_TARGET_CHANNELS,
            ATTR_DEVICE_ACTIVE_PROFILE_INDEX,
            ATTR_MAX_ENTRIES,
            ATTR_MAX_TEMP,
            ATTR_MIN_TEMP,
            ATTR_SCHEDULE_API_VERSION,
            ATTR_SCHEDULE_CHANNEL_ADDRESS,
            ATTR_SCHEDULE_DOMAIN,
            ATTR_SCHEDULE_TYPE,
        }
    )
    _unrecorded_attributes = frozenset(__no_recored_attributes)

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the week profile sensor."""
        attributes = super().extra_state_attributes
        attributes[ATTR_CONFIG_ENTRY_ID] = self._cu.entry_id
        attributes[ATTR_SCHEDULE_TYPE] = self._data_point.schedule_type.value
        attributes[ATTR_MAX_ENTRIES] = self._data_point.max_entries
        if schedule_channel_address := self._data_point.schedule_channel_address:
            attributes[ATTR_SCHEDULE_CHANNEL_ADDRESS] = schedule_channel_address
        if isinstance(self._data_point, ClimateWeekProfileDataPointProtocol):
            attributes[ATTR_AVAILABLE_PROFILES] = [profile.value for profile in self._data_point.available_profiles]
            attributes[ATTR_CURRENT_SCHEDULE_PROFILE] = self._data_point.current_schedule_profile
            attributes[ATTR_DEVICE_ACTIVE_PROFILE_INDEX] = self._data_point.device_active_profile_index
            attributes[ATTR_SCHEDULE_API_VERSION] = CLIMATE_SCHEDULE_API_VERSION
            if self._data_point.min_temp is not None:
                attributes[ATTR_MIN_TEMP] = self._data_point.min_temp
            if self._data_point.max_temp is not None:
                attributes[ATTR_MAX_TEMP] = self._data_point.max_temp
            if schedule := self._data_point.current_profile_schedule:
                attributes[ATTR_SCHEDULE_DATA] = schedule
        elif schedule := self._data_point.schedule:
            attributes[ATTR_SCHEDULE_API_VERSION] = SCHEDULE_API_VERSION
            if schedule_domain := self._data_point.schedule_domain:
                attributes[ATTR_SCHEDULE_DOMAIN] = schedule_domain
            if target_channels := self._data_point.available_target_channels:
                attributes[ATTR_AVAILABLE_TARGET_CHANNELS] = target_channels
            attributes[ATTR_SCHEDULE_DATA] = schedule

        return attributes

    @property
    def native_value(self) -> int:
        """Return the number of active schedule entries."""
        return self._data_point.value
