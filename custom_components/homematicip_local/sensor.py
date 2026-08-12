"""Sensor platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import logging
from typing import TYPE_CHECKING, Any, Final, cast, override

from aiohomematic.const import DEFAULT_MULTIPLIER, DataPointCategory, DataPointType, HubValueType, ParameterType
from aiohomematic.interfaces import (
    CalculatedDataPointProtocol,
    ClimateWeekProfileDataPointProtocol,
    CombinedDataPointProtocol,
    GenericDataPointProtocol,
)
from aiohomematic.model.hub import SysvarDpSensor
from aiohomematic.model.week_profile_data_point import WeekProfileDataPoint
from homeassistant.components.sensor import RestoreSensor, SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import ATTR_CONFIG_ENTRY_ID, EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType, UndefinedType

from . import HomematicConfigEntry
from .backend_types import LOOM_DP_ALARM_CONTROL_PANEL
from .const import CLIMATE_SCHEDULE_API_VERSION, DOMAIN, SCHEDULE_API_VERSION, HmEntityState
from .control_unit import ControlUnit, signal_new_data_point
from .entity_helpers import HmSensorEntityDescription
from .generic_entity import (
    ATTR_SCHEDULE_DATA,
    ATTR_VALUE_STATE,
    AioHomematicAlarmEntity,
    AioHomematicGenericEntity,
    AioHomematicGenericHubEntity,
    AioHomematicGenericSysvarEntity,
    get_schedule_name,
)

if TYPE_CHECKING:
    # Typing-only: the loom twin is absent on a CCU-only install, where the
    # dispatch tuple is empty and this entity is never constructed.
    from openccu_loom_client.compat.aiohomematic.model.alarm_panel import LoomDpAlarmControlPanel

    from aiohomematic.interfaces.model import GenericHubDataPointProtocol

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
ATTR_SCHEDULE_ENABLED: Final = "schedule_enabled"
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

    @callback
    def async_add_alarm_triggered_motion_sensor(data_points: tuple[Any, ...]) -> None:
        """Add a latched-detector counter per alarm panel (openccu-loom only)."""
        _LOGGER.debug("ASYNC_ADD_ALARM_TRIGGERED_MOTION_SENSOR: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicAlarmTriggeredMotionSensor(control_unit=control_unit, data_point=data_point)
            for data_point in data_points
            # Loom-only surface: the tuple is empty on a CCU-only install.
            if isinstance(data_point, LOOM_DP_ALARM_CONTROL_PANEL)
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
    # The counter rides the alarm panel data point, so it spawns off the same
    # announce a panel does — including a zone created at runtime.
    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.ALARM_CONTROL_PANEL),
            target=async_add_alarm_triggered_motion_sensor,
        )
    )

    async_add_sensor(
        data_points=control_unit.get_new_data_points(
            data_point_type=DataPointType.SENSOR, category=DataPointCategory.SENSOR
        )
    )

    async_add_hub_sensor(data_points=control_unit.get_new_hub_data_points(data_point_type=SysvarDpSensor))

    async_add_week_profile_sensor(
        data_points=control_unit.get_new_data_points(
            data_point_type=DataPointType.SENSOR, category=DataPointCategory.WEEK_PROFILE
        )
    )

    async_add_alarm_triggered_motion_sensor(
        data_points=control_unit.get_new_data_points(data_point_type=DataPointType.ALARM_CONTROL_PANEL)
    )


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
        # An enum sensor (data_point.values) must not carry a unit of measurement;
        # Home Assistant rejects a unit on the non-numeric "enum" device class.
        if not hasattr(self, "entity_description") and data_point.unit and not data_point.values:
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

    _unrecorded_attributes = frozenset(
        AioHomematicGenericHubEntity.NO_RECORDED_ATTRIBUTES
        | {f"alarm_{i}" for i in range(1, 100)}
        | {f"message_{i}" for i in range(1, 200)}
    )

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
            ATTR_SCHEDULE_ENABLED,
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
            if (schedule_enabled := self._data_point.schedule_enabled) is not None:
                attributes[ATTR_SCHEDULE_ENABLED] = schedule_enabled
            attributes[ATTR_SCHEDULE_DATA] = schedule

        return attributes

    @property
    @override
    def name(self) -> str | UndefinedType | None:
        """Return the name of the entity."""
        if self._cu.enable_sub_devices:
            # Sub-device is "Schedule"/"Zeitplan", sensor is the main entity
            return None
        # Without sub-devices, use the schedule translation as entity name
        return get_schedule_name(locale=self._data_point.device.config_provider.config.locale)

    @property
    def native_value(self) -> int:
        """Return the number of active schedule entries."""
        return self._data_point.value


class AioHomematicAlarmTriggeredMotionSensor(AioHomematicAlarmEntity, SensorEntity):
    """
    Counts the latched detectors a motion reset would clear (openccu-loom).

    The number beside the reset button, and the answer to "why will this
    zone not arm": a detector holding its ``MOTION`` flag reads as open
    and blocks arming until the flag clears. The master panel's counter
    covers every zone, which is the scope its aggregate reset writes.

    Diagnostic on purpose — unlike the button next to it, this reports
    rather than acts. The count and the reset come from one daemon-side
    predicate, so it can never name a detector the button would skip.
    """

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "alarm_triggered_motion"

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: LoomDpAlarmControlPanel,
    ) -> None:
        """Initialize the latched-detector counter."""
        super().__init__(
            control_unit=control_unit,
            # Same structural-satisfaction cast the panel platform makes:
            # only the enum homes differ nominally.
            data_point=cast("GenericHubDataPointProtocol", data_point),
        )
        # The base keys the unique id on the data point alone, which the
        # panel entity already claims — this rides the same data point.
        self._attr_unique_id = f"{DOMAIN}_{data_point.unique_id}_triggered_motion"
        # One device holds every zone, so the zone has to be in the entity
        # name or the counters are indistinguishable. Only used when the
        # daemon's own name is unavailable — see `name`.
        self._attr_translation_placeholders = {"zone": data_point.name}

    @property
    def _panel(self) -> LoomDpAlarmControlPanel:
        """Return the data point as its concrete loom type."""
        return cast("LoomDpAlarmControlPanel", self._data_point)

    @property
    @override
    def name(self) -> str | UndefinedType | None:
        """
        Return the daemon's name for this counter, else compose one here.

        Same naming authority as the button beside it — see
        `AioHomematicAlarmMotionResetButton.name` for why the daemon's
        copy wins, why the local translation is the fallback rather than
        the rule, and why the panel's own resolved name is not used.
        """
        if isinstance(daemon_name := self._panel.triggered_motion_name, str) and daemon_name:
            return daemon_name
        return super(AioHomematicGenericHubEntity, self).name

    @property
    @override
    def native_value(self) -> int:
        """Return how many detectors are currently latched."""
        return self._panel.triggered_motion_count
