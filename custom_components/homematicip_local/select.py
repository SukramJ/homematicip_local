"""Select platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from copy import deepcopy
import logging

from aiohomematic.const import DataPointCategory
from aiohomematic.model.generic import DpActionSelect, DpSelect
from aiohomematic.model.hub import SysvarDpSelect
from homeassistant.components.select import SelectEntity
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN, EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HomematicConfigEntry
from .const import CONF_ACTION_SELECT_VALUES, DP_ACTION_SELECT_WHITELIST
from .control_unit import ControlUnit, signal_new_data_point
from .generic_entity import AioHomematicGenericRestoreEntity, AioHomematicGenericSysvarEntity
from .support import handle_homematic_errors

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU select platform."""
    control_unit: ControlUnit = entry.runtime_data

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
            if data_point.parameter in DP_ACTION_SELECT_WHITELIST
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
            )
            for data_point in data_points
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
    def options(self) -> list[str]:
        """Return the options."""
        if options := self._data_point.values:
            return [option.lower() for option in options]
        return []

    @handle_homematic_errors
    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        await self._data_point.send_value(value=option.upper())


class AioHomematicSysvarSelect(AioHomematicGenericSysvarEntity[SysvarDpSelect], SelectEntity):
    """Representation of the HomematicIP hub select entity."""

    @property
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        return self._data_point.value  # type: ignore[no-any-return]

    @property
    def options(self) -> list[str]:
        """Return the options."""
        if options := self._data_point.values:
            return list(options)
        return []

    @handle_homematic_errors
    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        await self._data_point.send_variable(value=option)


class AioHomematicActionSelect(AioHomematicGenericRestoreEntity[DpActionSelect], SelectEntity):
    """Representation of the HomematicIP action select entity (InputHelper-like)."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: DpActionSelect,
    ) -> None:
        """Initialize action select entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )

    @property
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
    def options(self) -> list[str]:
        """Return the available options from values."""
        if values := self._data_point.values:
            return [option.lower() for option in values]
        return []

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass."""
        await super().async_added_to_hass()
        # Load persisted value after hass is available
        self._load_persisted_value()

    async def async_select_option(self, option: str) -> None:
        """
        Select an option (store locally in DP, don't send to device).

        This stores the value in the DpActionSelect instance and persists it
        in the config entry data for retrieval across restarts.
        """
        # Store in aiohomematic DP (local only, not sent to device)
        self._data_point.value = option.upper()

        # Persist in config entry
        await self._persist_value(option)

        # Update HA state
        self.async_write_ha_state()

    def _load_persisted_value(self) -> None:
        """Load persisted value from config entry data on startup."""
        if not (entry := self.hass.config_entries.async_get_entry(self._cu._entry_id)):  # pylint: disable=protected-access
            return

        # Get device address and parameter name
        channel_address = self._data_point.channel.address
        parameter = self._data_point.parameter

        # Load value from nested structure: {channel_address: {parameter: value}}
        if (
            CONF_ACTION_SELECT_VALUES in entry.data
            and channel_address in entry.data[CONF_ACTION_SELECT_VALUES]
            and (value := entry.data[CONF_ACTION_SELECT_VALUES][channel_address].get(parameter))
        ):
            self._data_point.value = value.upper()
            _LOGGER.debug(
                "Loaded persisted value '%s' for %s:%s from config entry",
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

    async def _persist_value(self, value: str) -> None:
        """Persist selected value in config entry data."""
        if not (entry := self.hass.config_entries.async_get_entry(self._cu._entry_id)):  # pylint: disable=protected-access
            return

        # Get device address and parameter name
        channel_address = self._data_point.channel.address
        parameter = self._data_point.parameter

        # Deep copy to avoid modifying the original entry.data
        data = deepcopy(dict(entry.data))

        # Initialize nested storage structure: {channel_address: {parameter: value}}
        if CONF_ACTION_SELECT_VALUES not in data:
            data[CONF_ACTION_SELECT_VALUES] = {}

        if channel_address not in data[CONF_ACTION_SELECT_VALUES]:
            data[CONF_ACTION_SELECT_VALUES][channel_address] = {}

        # Store value under channel_address -> parameter
        data[CONF_ACTION_SELECT_VALUES][channel_address][parameter] = value

        # Update config entry
        self.hass.config_entries.async_update_entry(entry, data=data)

        _LOGGER.debug(
            "Persisted value '%s' for %s:%s in config entry",
            value,
            channel_address,
            parameter,
        )
