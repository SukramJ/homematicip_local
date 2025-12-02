"""HomematicIP Local repairs support."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
import contextlib
import logging
from typing import Any, Final

import voluptuous as vol

from homeassistant.components.repairs import RepairsFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.issue_registry import async_delete_issue

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_NAME: Final = "device_name"

# Per-issue fix callbacks for repairs UI
REPAIR_CALLBACKS: dict[str, Callable[..., Awaitable[Any]]] = {}


async def async_create_fix_flow(hass: HomeAssistant, issue_id: str, data: dict[str, Any]) -> RepairsFlow:
    """Create a fix flow for issues created by this integration."""
    return _DevicesDelayedFixFlow(hass, issue_id)


class _DevicesDelayedFixFlow(RepairsFlow):
    """Fix flow for delayed devices: allows naming the device before adding it."""

    def __init__(self, hass: HomeAssistant, issue_id: str) -> None:
        self.hass = hass
        self._issue_id = issue_id
        # Issue id format: devices_delayed|<interface_id>|<address>
        self._interface_id: str | None = None
        self._address: str | None = None
        parts = issue_id.split("|", 2)
        if len(parts) >= 3:
            self._interface_id = parts[1] or None
            self._address = parts[2] or None

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Show the form to enter a device name."""
        return self.async_show_form(
            step_id="set_name",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_DEVICE_NAME, default=""): str,
                }
            ),
            description_placeholders={
                "interface_id": self._interface_id or "",
                "address": self._address or "",
            },
        )

    async def async_step_set_name(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the name input and trigger the device addition."""
        if user_input is None:
            return await self.async_step_init()

        device_name = user_input.get(CONF_DEVICE_NAME, "").strip() if user_input else ""

        # Execute the fix callback with the device name (empty string skips rename)
        cb = REPAIR_CALLBACKS.pop(self._issue_id, None)
        if cb is not None:
            with contextlib.suppress(Exception):
                await cb(device_name=device_name)

        # Close the issue
        async_delete_issue(hass=self.hass, domain=DOMAIN, issue_id=self._issue_id)

        return self.async_create_entry(title="", data={})
