"""Notify platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

import logging
from typing import Any, Final

from aiohomematic.const import DataPointCategory
from aiohomematic.model.custom.text_display import CustomDpTextDisplay
from homeassistant.components.notify import NotifyEntity, NotifyEntityFeature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.storage import Store

from . import HomematicConfigEntry
from .control_unit import ControlUnit, signal_new_data_point
from .generic_entity import AioHomematicGenericEntity
from .support import handle_homematic_errors

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION: Final = 1
STORAGE_KEY_PREFIX: Final = "homematicip_local.text_display"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU notify platform."""
    control_unit: ControlUnit = entry.runtime_data

    @callback
    def async_add_notify(data_points: tuple[CustomDpTextDisplay, ...]) -> None:
        """Add notify entities from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_NOTIFY: Adding %i data points", len(data_points))

        if entities := [
            HmipTextDisplayNotifyEntity(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.TEXT_DISPLAY),
            target=async_add_notify,
        )
    )

    async_add_notify(data_points=control_unit.get_new_data_points(data_point_type=CustomDpTextDisplay))


class TextDisplayStore:
    """Store for persisting text display state."""

    def __init__(self, *, hass: HomeAssistant, unique_id: str) -> None:
        """Initialize the store."""
        self._store: Store[dict[str, Any]] = Store(
            hass,
            STORAGE_VERSION,
            f"{STORAGE_KEY_PREFIX}.{unique_id}",
        )

    async def async_load(self) -> dict[str, Any] | None:
        """Load persisted display state."""
        return await self._store.async_load()

    async def async_save(self, *, state: dict[str, Any]) -> None:
        """Save current display state."""
        await self._store.async_save(state)


class HmipTextDisplayNotifyEntity(AioHomematicGenericEntity[CustomDpTextDisplay], NotifyEntity):
    """Notify entity for HmIP text display devices (e.g., HmIP-WRCD)."""

    _attr_supported_features = NotifyEntityFeature.TITLE

    def __init__(
        self,
        *,
        control_unit: ControlUnit,
        data_point: CustomDpTextDisplay,
    ) -> None:
        """Initialize the notify entity."""
        super().__init__(control_unit=control_unit, data_point=data_point)
        self._store: TextDisplayStore | None = None
        self._current_state: dict[str, Any] = {}

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes for UI/cards."""
        return {
            # Available options from ActionSelects (paramset VALUE_LIST)
            "available_icons": self._data_point.available_icons,
            "available_sounds": self._data_point.available_sounds,
            "available_background_colors": self._data_point.available_background_colors,
            "available_text_colors": self._data_point.available_text_colors,
            "available_alignments": self._data_point.available_alignments,
            # Feature support
            "supports_icons": self._data_point.supports_icons,
            "supports_sounds": self._data_point.supports_sounds,
            # Current state (persisted)
            "current_lines": self._current_state.get("lines", {}),
        }

    async def async_added_to_hass(self) -> None:
        """Restore state when added to hass."""
        await super().async_added_to_hass()
        # Initialize store now that we have access to hass
        self._store = TextDisplayStore(
            hass=self.hass,
            unique_id=self._data_point.unique_id,
        )
        if stored := await self._store.async_load():
            self._current_state = stored

    @handle_homematic_errors
    async def async_clear_text_display(self) -> None:
        """Clear all display lines."""
        # Clear all 3 display lines
        for display_id in range(1, 4):
            await self._data_point.send_text(
                text="",
                display_id=display_id,
                icon="NO_ICON",
            )

        # Clear persisted state
        self._current_state = {"lines": {}}
        if self._store:
            await self._store.async_save(state=self._current_state)

    @handle_homematic_errors
    async def async_send_message(self, message: str, title: str | None = None) -> None:
        """Send message to display."""
        # Build display line from message
        line_id = 1

        # If title is provided, send title on line 1 and message on line 2
        if title:
            await self._data_point.send_text(
                text=title,
                display_id=1,
            )
            line_id = 2
            self._current_state.setdefault("lines", {})[1] = {"text": title}

        # Send message
        await self._data_point.send_text(
            text=message,
            display_id=line_id,
        )
        self._current_state.setdefault("lines", {})[line_id] = {"text": message}

        # Persist state
        if self._store:
            await self._store.async_save(state=self._current_state)

    @handle_homematic_errors
    async def async_send_text_display(
        self,
        *,
        text: str,
        icon: str | None = None,
        background_color: str | None = None,
        text_color: str | None = None,
        alignment: str | None = None,
        display_id: int | None = None,
        sound: str | None = None,
        repeat: int | None = None,
    ) -> None:
        """Send text to display with full control over all parameters."""
        kwargs: dict[str, Any] = {"text": text}
        # Convert string parameters to uppercase (device expects uppercase values)
        if icon is not None:
            kwargs["icon"] = icon.upper()
        if background_color is not None:
            kwargs["background_color"] = background_color.upper()
        if text_color is not None:
            kwargs["text_color"] = text_color.upper()
        if alignment is not None:
            kwargs["alignment"] = alignment.upper()
        if display_id is not None:
            kwargs["display_id"] = display_id
        if sound is not None:
            kwargs["sound"] = sound.upper()
        if repeat is not None:
            kwargs["repeat"] = repeat

        await self._data_point.send_text(**kwargs)

        # Persist state
        line_id = display_id or 1
        self._current_state.setdefault("lines", {})[line_id] = kwargs
        if self._store:
            await self._store.async_save(state=self._current_state)
