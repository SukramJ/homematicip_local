"""Select platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any, Final, override

from aiohomematic.const import DataPointCategory
from aiohomematic.model.generic import DpActionSelect, DpSelect
from aiohomematic.model.hub import SysvarDpSelect
from homeassistant.components.select import SelectEntity
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN, EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.storage import Store

from . import HomematicConfigEntry
from .const import CONF_ACTION_SELECT_VALUES, DP_ACTION_SELECT_WHITELIST
from .control_unit import ControlUnit, signal_new_data_point
from .generic_entity import AioHomematicGenericRestoreEntity, AioHomematicGenericSysvarEntity
from .support import handle_homematic_errors

_LOGGER = logging.getLogger(__name__)

# Storage constants for action select persistence
STORAGE_VERSION: Final = 1
STORAGE_KEY_PREFIX: Final = "homematicip_local.action_select"


class ActionSelectStore:
    """Store for persisting action select values without triggering config entry reload."""

    def __init__(self, *, hass: HomeAssistant, entry_id: str) -> None:
        """Initialize the store."""
        self._store: Store[dict[str, dict[str, str]]] = Store(
            hass,
            STORAGE_VERSION,
            f"{STORAGE_KEY_PREFIX}.{entry_id}",
        )
        self._data: dict[str, dict[str, str]] = {}

    async def async_load(self) -> None:
        """Load persisted action select values."""
        if (data := await self._store.async_load()) is not None:
            self._data = data

    async def async_migrate_from_config_entry(self, *, data: Mapping[str, Any]) -> bool:
        """Migrate existing values from config entry data to storage file."""
        if CONF_ACTION_SELECT_VALUES not in data:
            return False

        migrated_data: dict[str, dict[str, str]] = data[CONF_ACTION_SELECT_VALUES]
        if not migrated_data:
            return False

        self._data = migrated_data
        await self.async_save()
        _LOGGER.info("Migrated %d action select entries to storage file", len(migrated_data))
        return True

    async def async_save(self) -> None:
        """Save current action select values."""
        await self._store.async_save(self._data)

    async def async_set_value(self, *, channel_address: str, parameter: str, value: str) -> None:
        """Set and persist value for a channel/parameter combination."""
        if channel_address not in self._data:
            self._data[channel_address] = {}
        self._data[channel_address][parameter] = value
        await self.async_save()

    def get_value(self, *, channel_address: str, parameter: str) -> str | None:
        """Get persisted value for a channel/parameter combination."""
        if channel_address in self._data:
            return self._data[channel_address].get(parameter)
        return None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU select platform."""
    control_unit: ControlUnit = entry.runtime_data

    # Initialize action select store (does not trigger config entry reload)
    action_select_store = ActionSelectStore(hass=hass, entry_id=entry.entry_id)
    await action_select_store.async_load()

    # Migrate from config entry data if needed (one-time migration)
    await action_select_store.async_migrate_from_config_entry(data=entry.data)

    @callback
    def async_add_select(data_points: tuple[DpSelect, ...]) -> None:
        """Add select from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_SELECT: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicSelect(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    @callback
    def async_add_hub_select(data_points: tuple[SysvarDpSelect, ...]) -> None:
        """Add sysvar select from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_HUB_SELECT: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicSysvarSelect(control_unit=control_unit, data_point=data_point) for data_point in data_points
        ]:
            async_add_entities(entities)

    @callback
    def async_add_action_select(data_points: tuple[DpActionSelect, ...]) -> None:
        """Add action select from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_ACTION_SELECT: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicActionSelect(
                control_unit=control_unit,
                data_point=data_point,
                store=action_select_store,
            )
            for data_point in data_points
            if data_point.parameter in DP_ACTION_SELECT_WHITELIST
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.SELECT),
            target=async_add_select,
        )
    )

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.HUB_SELECT),
            target=async_add_hub_select,
        )
    )

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.ACTION_SELECT),
            target=async_add_action_select,
        )
    )

    async_add_select(data_points=control_unit.get_new_data_points(data_point_type=DpSelect))

    async_add_hub_select(data_points=control_unit.get_new_hub_data_points(data_point_type=SysvarDpSelect))

    async_add_action_select(data_points=control_unit.get_new_data_points(data_point_type=DpActionSelect))


class AioHomematicSelect(AioHomematicGenericRestoreEntity[DpSelect], SelectEntity):
    """Representation of the HomematicIP select entity."""

    @property
    @override
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        if self._data_point.is_valid:
            value = self._data_point.value
            return value.lower() if isinstance(value, str) else str(value)
        if (
            self.is_restored
            and self._restored_state
            and (restored_state := self._restored_state.state)
            not in (
                STATE_UNKNOWN,
                STATE_UNAVAILABLE,
            )
        ):
            return restored_state
        return None

    @property
    @override
    def options(self) -> list[str]:
        """Return the options."""
        if options := self._data_point.values:
            return [option.lower() for option in options]
        return []

    @override
    @handle_homematic_errors
    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        await self._data_point.send_value(value=option.upper())


class AioHomematicSysvarSelect(AioHomematicGenericSysvarEntity[SysvarDpSelect], SelectEntity):
    """Representation of the HomematicIP hub select entity."""

    @property
    @override
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        return self._data_point.value  # type: ignore[no-any-return]

    @property
    @override
    def options(self) -> list[str]:
        """Return the options."""
        if options := self._data_point.values:
            return list(options)
        return []

    @override
    @handle_homematic_errors
    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        await self._data_point.send_variable(value=option)


class AioHomematicActionSelect(AioHomematicGenericRestoreEntity[DpActionSelect], SelectEntity):
    """Representation of the HomematicIP action select entity (InputHelper-like)."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        *,
        control_unit: ControlUnit,
        data_point: DpActionSelect,
        store: ActionSelectStore,
    ) -> None:
        """Initialize action select entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        self._store = store

    @property
    @override
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        # Priority: 1. aiohomematic value, 2. restored state, 3. default
        if value := self._data_point.value:
            return value.lower() if isinstance(value, str) else str(value)

        if (
            self.is_restored
            and self._restored_state
            and (restored_state := self._restored_state.state) not in (STATE_UNKNOWN, STATE_UNAVAILABLE)
        ):
            return restored_state

        # Return default if available
        if default := self._data_point.default:
            return default.lower() if isinstance(default, str) else str(default)

        return None

    @property
    @override
    def options(self) -> list[str]:
        """Return the available options from values."""
        if values := self._data_point.values:
            return [option.lower() for option in values]
        return []

    @override
    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass."""
        await super().async_added_to_hass()
        # Load persisted value from storage file
        self._load_persisted_value()

    @override
    async def async_select_option(self, option: str) -> None:
        """
        Select an option (store locally in DP, don't send to device).

        This stores the value in the DpActionSelect instance and persists it
        in the storage file for retrieval across restarts.
        """
        # Store in aiohomematic DP (local only, not sent to device)
        self._data_point.value = option.upper()

        # Persist in storage file (does not trigger config entry reload)
        await self._store.async_set_value(
            channel_address=self._data_point.channel.address,
            parameter=self._data_point.parameter,
            value=option,
        )

        _LOGGER.debug(
            "Persisted value '%s' for %s:%s in storage file",
            option,
            self._data_point.channel.address,
            self._data_point.parameter,
        )

        # Update HA state
        self.async_write_ha_state()

    def _load_persisted_value(self) -> None:
        """Load persisted value from storage file on startup."""
        channel_address = self._data_point.channel.address
        parameter = self._data_point.parameter

        if value := self._store.get_value(channel_address=channel_address, parameter=parameter):
            self._data_point.value = value.upper()
            _LOGGER.debug(
                "Loaded persisted value '%s' for %s:%s from storage file",
                value,
                channel_address,
                parameter,
            )
        elif default := self._data_point.default:
            # Use default if no persisted value
            self._data_point.value = default
            _LOGGER.debug(
                "Using default value '%s' for %s:%s",
                default,
                channel_address,
                parameter,
            )
