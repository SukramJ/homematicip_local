"""HomematicIP Local repairs support."""

from __future__ import annotations

from collections.abc import Callable
import contextlib
import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.repairs import RepairsFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.issue_registry import async_delete_issue

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Per-issue fix callbacks for repairs UI
REPAIR_CALLBACKS: dict[str, Callable] = {}


async def async_create_fix_flow(hass: HomeAssistant, issue_id: str, data: dict[str, Any]) -> RepairsFlow:
    """Create a fix flow for issues created by this integration."""
    return _DevicesDelayedFixFlow(hass, issue_id)


class _DevicesDelayedFixFlow(RepairsFlow):
    """Minimal fix flow: confirm and run the registered fix callback (if any), then close the issue."""

    def __init__(self, hass: HomeAssistant, issue_id: str) -> None:
        self.hass = hass
        self._issue_id = issue_id
        # Issue id format: devices_delayed-<interface_id>-<address>
        self._interface_id: str | None = None
        self._address: str | None = None
        parts = issue_id.split("|", 2)
        if len(parts) >= 3:
            self._interface_id = parts[1] or None
            self._address = parts[2] or None

    async def async_step_confirm(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the confirmation to trigger the manual device add and close the issue."""
        # Execute best-effort fix callback if present
        cb = REPAIR_CALLBACKS.pop(self._issue_id, None)
        if cb is not None:
            with contextlib.suppress(Exception):
                await cb()

        # Close the issue
        async_delete_issue(hass=self.hass, domain=DOMAIN, issue_id=self._issue_id)

        # Let the frontend use the translation for success message
        return self.async_create_entry(title="", data={})

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:  # noqa: D401
        # Always show the confirm form first
        return self.async_show_form(
            step_id="confirm",
            data_schema=vol.Schema({}),
            description_placeholders={
                "issue_id": self._issue_id,
                "interface_id": self._interface_id or "",
                "address": self._address or "",
            },
        )
