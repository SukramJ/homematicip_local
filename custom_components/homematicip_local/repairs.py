"""HomematicIP Local repairs support."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
import logging
from typing import Any, Final

import probatio as vol

from homeassistant.components.repairs import RepairsFlow, RepairsFlowResult
from homeassistant.core import HomeAssistant
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

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> RepairsFlowResult:
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

    async def async_step_set_name(self, user_input: dict[str, Any] | None = None) -> RepairsFlowResult:
        """Handle the name input and trigger the device addition."""
        if user_input is None:
            return await self.async_step_init()

        device_name = user_input.get(CONF_DEVICE_NAME, "").strip() if user_input else ""

        # Execute the fix callback with the device name (empty string skips rename)
        cb = REPAIR_CALLBACKS.pop(self._issue_id, None)
        error: str | None = None
        if cb is not None:
            try:
                await cb(device_name=device_name)
            except Exception as err:  # noqa: BLE001 - every backend failure is shown, not swallowed
                # Reporting success here would hide a device the backend has
                # not finished adding; the openccu-loom backend, for one,
                # leaves it accepted but unreleased when the release fails.
                _LOGGER.warning("Adding delayed device %s failed: %s", self._address, err)
                error = str(err) or type(err).__name__

        # Close the issue
        async_delete_issue(hass=self.hass, domain=DOMAIN, issue_id=self._issue_id)

        if error is not None:
            return self.async_abort(
                reason="device_add_failed",
                description_placeholders={"address": self._address or "", "error": error},
            )
        return self.async_create_entry(title="", data={})
