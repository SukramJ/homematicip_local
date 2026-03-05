"""Number platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any, Final, override

from aiohomematic.const import DataPointCategory, HubValueType, ParameterType
from aiohomematic.interfaces import CombinedDataPointProtocol
from aiohomematic.model.combined.timer import CombinedDpTimerAction
from aiohomematic.model.generic import BaseDpActionNumber, BaseDpNumber
from aiohomematic.model.hub import SysvarDpNumber
from homeassistant.components.number import NumberEntity, NumberMode, RestoreNumber
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.storage import Store

from . import HomematicConfigEntry
from .const import CONF_ACTION_NUMBER_VALUES, DP_ACTION_NUMBER_WHITELIST, HmEntityState
from .control_unit import ControlUnit, signal_new_data_point
from .entity_helpers import HmNumberEntityDescription
from .generic_entity import (
    ATTR_VALUE_STATE,
    AioHomematicGenericEntity,
    AioHomematicGenericRestoreEntity,
    AioHomematicGenericSysvarEntity,
)
from .support import handle_homematic_errors

_LOGGER = logging.getLogger(__name__)

# Storage constants for action number persistence
ACTION_NUMBER_STORAGE_VERSION: Final = 1
ACTION_NUMBER_STORAGE_KEY_PREFIX: Final = "homematicip_local.action_number"


class ActionNumberStore:
    """Store for persisting action number values without triggering config entry reload."""

    def __init__(self, *, hass: HomeAssistant, entry_id: str) -> None:
        """Initialize the store."""
        self._store: Store[dict[str, dict[str, float]]] = Store(
            hass,
            ACTION_NUMBER_STORAGE_VERSION,
            f"{ACTION_NUMBER_STORAGE_KEY_PREFIX}.{entry_id}",
        )
        self._data: dict[str, dict[str, float]] = {}

    async def async_load(self) -> None:
        """Load persisted action number values."""
        if (data := await self._store.async_load()) is not None:
            self._data = data

    async def async_migrate_from_config_entry(self, *, data: Mapping[str, Any]) -> bool:
        """Migrate existing values from config entry data to storage file."""
        if CONF_ACTION_NUMBER_VALUES not in data:
            return False

        migrated_data: dict[str, dict[str, float]] = data[CONF_ACTION_NUMBER_VALUES]
        if not migrated_data:
            return False

        self._data = migrated_data
        await self.async_save()
        _LOGGER.info("Migrated %d action number entries to storage file", len(migrated_data))
        return True

    async def async_save(self) -> None:
        """Save current action number values."""
        await self._store.async_save(self._data)

    async def async_set_value(self, *, channel_address: str, parameter: str, value: float) -> None:
        """Set and persist value for a channel/parameter combination."""
        if channel_address not in self._data:
            self._data[channel_address] = {}
        self._data[channel_address][parameter] = value
        await self.async_save()

    def get_value(self, *, channel_address: str, parameter: str) -> float | None:
        """Get persisted value for a channel/parameter combination."""
        if channel_address in self._data:
            return self._data[channel_address].get(parameter)
        return None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU number platform."""
    control_unit: ControlUnit = entry.runtime_data

    # Initialize action number store (does not trigger config entry reload)
    action_number_store = ActionNumberStore(hass=hass, entry_id=entry.entry_id)
    await action_number_store.async_load()

    # Migrate from config entry data if needed (one-time migration)
    await action_number_store.async_migrate_from_config_entry(data=entry.data)

    @callback
    def async_add_number(data_points: tuple[BaseDpNumber[float | int | None], ...]) -> None:
        """Add number from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_NUMBER: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicNumber(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    @callback
    def async_add_hub_number(data_points: tuple[SysvarDpNumber, ...]) -> None:
        """Add sysvar number from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_HUB_NUMBER: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicSysvarNumber(control_unit=control_unit, data_point=data_point) for data_point in data_points
        ]:
            async_add_entities(entities)

    @callback
    def async_add_action_number(data_points: tuple[BaseDpActionNumber[Any], ...]) -> None:
        """Add action number from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_ACTION_NUMBER: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicActionNumber(
                control_unit=control_unit,
                data_point=data_point,
                store=action_number_store,
            )
            for data_point in data_points
            if data_point.parameter in DP_ACTION_NUMBER_WHITELIST
        ]:
            async_add_entities(entities)

    @callback
    def async_add_combined_number(data_points: tuple[Any, ...]) -> None:
        """Add combined number from Homematic(IP) Local for OpenCCU."""
        combined_dps = [dp for dp in data_points if isinstance(dp, CombinedDataPointProtocol)]
        if not combined_dps:
            return
        _LOGGER.debug("ASYNC_ADD_COMBINED_NUMBER: Adding %i data points", len(combined_dps))

        if entities := [
            AioHomematicCombinedNumber(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in combined_dps
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.NUMBER),
            target=async_add_number,
        )
    )

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.HUB_NUMBER),
            target=async_add_hub_number,
        )
    )

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.ACTION_NUMBER),
            target=async_add_action_number,
        )
    )

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.ACTION_NUMBER),
            target=async_add_combined_number,
        )
    )

    async_add_number(data_points=control_unit.get_new_data_points(data_point_type=BaseDpNumber))

    async_add_hub_number(data_points=control_unit.get_new_hub_data_points(data_point_type=SysvarDpNumber))

    async_add_action_number(data_points=control_unit.get_new_data_points(data_point_type=BaseDpActionNumber))

    async_add_combined_number(data_points=control_unit.get_new_data_points(data_point_type=CombinedDpTimerAction))


class AioHomematicNumber(AioHomematicGenericEntity[BaseDpNumber[Any]], RestoreNumber):
    """Representation of the HomematicIP number entity."""

    entity_description: HmNumberEntityDescription
    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX
    _restored_native_value: float | None = None

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: BaseDpNumber[Any],
    ) -> None:
        """Initialize the number entity."""
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
        self._attr_native_min_value = data_point.min * self._multiplier
        self._attr_native_max_value = data_point.max * self._multiplier
        self._attr_native_step = 1.0 if data_point.hmtype == "INTEGER" else 0.01 * self._multiplier
        if not hasattr(self, "entity_description") and data_point.unit:
            self._attr_native_unit_of_measurement = data_point.unit

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
    def native_value(self) -> float | None:
        """Return the current value."""
        if self._data_point.is_valid and self._data_point.value is not None:
            return float(self._data_point.value * self._multiplier)
        if self.is_restored:
            return self._restored_native_value
        return None

    @override
    async def async_added_to_hass(self) -> None:
        """Check, if state needs to be restored."""
        await super().async_added_to_hass()
        if not self._data_point.is_valid and (restored_sensor_data := await self.async_get_last_number_data()):
            self._restored_native_value = restored_sensor_data.native_value

    @override
    @handle_homematic_errors
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._data_point.send_value(value=value / self._multiplier)


class AioHomematicSysvarNumber(AioHomematicGenericSysvarEntity[SysvarDpNumber], NumberEntity):
    """Representation of the HomematicIP hub number entity."""

    _attr_mode = NumberMode.BOX

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: SysvarDpNumber,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(control_unit=control_unit, data_point=data_point)
        if data_point.min:
            self._attr_native_min_value = float(data_point.min)
        if data_point.max:
            self._attr_native_max_value = float(data_point.max)
        if data_point.unit:
            self._attr_native_unit_of_measurement = data_point.unit
        elif data_point.data_type in (
            HubValueType.FLOAT,
            HubValueType.INTEGER,
        ):
            self._attr_native_unit_of_measurement = " "

    @property
    @override
    def native_value(self) -> float | None:
        """Return the current value."""
        if (value := self._data_point.value) is not None and isinstance(value, (int, float)):
            return float(value)
        return None

    @override
    @handle_homematic_errors
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._data_point.send_variable(value=value)


class AioHomematicActionNumber(AioHomematicGenericRestoreEntity[BaseDpActionNumber[Any]], RestoreNumber):
    """Representation of the HomematicIP action number entity (InputHelper-like)."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX

    def __init__(
        self,
        *,
        control_unit: ControlUnit,
        data_point: BaseDpActionNumber[Any],
        store: ActionNumberStore,
    ) -> None:
        """Initialize action number entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        self._store = store
        self._multiplier: float = data_point.multiplier
        self._attr_native_min_value = data_point.min * self._multiplier
        # Disabled, because we recalculate this with a correct unit in aiohomematic
        # self._attr_native_max_value = data_point.max * self._multiplier
        self._attr_native_step = 1.0 if data_point.hmtype == ParameterType.INTEGER else 0.01 * self._multiplier
        if data_point.unit:
            self._attr_native_unit_of_measurement = data_point.unit

    @property
    @override
    def native_value(self) -> float | None:
        """Return the current value."""
        # Priority: 1. DP value, 2. Restored, 3. Default
        if self._data_point.value is not None:
            return float(self._data_point.value * self._multiplier)

        if (
            self.is_restored
            and self._restored_state
            and self._restored_state.state not in (None, "unknown", "unavailable")
        ):
            try:
                return float(self._restored_state.state)
            except (ValueError, TypeError):
                pass

        if (default := self._data_point.default) is not None:
            return float(default * self._multiplier)

        return None

    @override
    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass."""
        await super().async_added_to_hass()
        self._load_persisted_value()

    @override
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value (store locally in DP, don't send to device)."""
        # Store in aiohomematic DP (local only, not sent to device)
        self._data_point.value = value / self._multiplier

        # Persist in storage file (does not trigger config entry reload)
        await self._store.async_set_value(
            channel_address=self._data_point.channel.address,
            parameter=self._data_point.parameter,
            value=value,
        )

        _LOGGER.debug(
            "Persisted value '%s' for %s:%s in storage file",
            value,
            self._data_point.channel.address,
            self._data_point.parameter,
        )

        # Update HA state
        self.async_write_ha_state()

    def _load_persisted_value(self) -> None:
        """Load persisted value from storage file on startup."""
        channel_address = self._data_point.channel.address
        parameter = self._data_point.parameter

        if (value := self._store.get_value(channel_address=channel_address, parameter=parameter)) is not None:
            self._data_point.value = value / self._multiplier
            _LOGGER.debug(
                "Loaded persisted value '%s' for %s:%s from storage file",
                value,
                channel_address,
                parameter,
            )
        elif (default := self._data_point.default) is not None:
            # Use default if no persisted value
            self._data_point.value = default
            _LOGGER.debug(
                "Using default value '%s' for %s:%s",
                default,
                channel_address,
                parameter,
            )


class AioHomematicCombinedNumber(AioHomematicGenericEntity[CombinedDataPointProtocol], NumberEntity):
    """Representation of the HomematicIP combined number entity."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: CombinedDataPointProtocol,
    ) -> None:
        """Initialize the combined number entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        if data_point.min is not None:
            self._attr_native_min_value = float(data_point.min)
        if data_point.max is not None:
            self._attr_native_max_value = float(data_point.max)
        self._attr_native_step = 1.0
        if data_point.unit:
            self._attr_native_unit_of_measurement = data_point.unit

    @property
    @override
    def native_value(self) -> float | None:
        """Return the current value."""
        if (value := self._data_point.value) is not None:
            return float(value)
        return None

    @override
    @handle_homematic_errors
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._data_point.send_value(value=value)
