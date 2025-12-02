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
ISSUE_ID_PREFIX_DEVICES_DELAYED: Final = "devices_delayed"
ISSUE_ID_PREFIX_INBOX_DEVICE: Final = "inbox_device"

# Per-issue fix callbacks for repairs UI
REPAIR_CALLBACKS: dict[str, Callable[..., Awaitable[Any]]] = {}

# Per-issue data for inbox device repairs (stores InboxDeviceData)
INBOX_DEVICE_DATA: dict[str, dict[str, Any]] = {}


async def async_create_fix_flow(hass: HomeAssistant, issue_id: str, data: dict[str, Any]) -> RepairsFlow:
    """Create a fix flow for issues created by this integration."""
    if issue_id.startswith(ISSUE_ID_PREFIX_INBOX_DEVICE):
        return _InboxDeviceFixFlow(hass, issue_id)
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


class _InboxDeviceFixFlow(RepairsFlow):
    """Fix flow for inbox devices: allows naming the device before accepting it."""

    def __init__(self, hass: HomeAssistant, issue_id: str) -> None:
        """Initialize the inbox device fix flow."""
        self.hass = hass
        self._issue_id = issue_id
        # Issue id format: inbox_device|<entry_id>|<address>
        self._entry_id: str | None = None
        self._address: str | None = None
        self._device_type: str | None = None
        self._default_name: str | None = None
        parts = issue_id.split("|", 2)
        if len(parts) >= 3:
            self._entry_id = parts[1] or None
            self._address = parts[2] or None
        # Get stored device data
        if device_data := INBOX_DEVICE_DATA.get(issue_id):
            self._device_type = device_data.get("device_type")
            self._default_name = device_data.get("name")

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Show the form to enter a device name."""
        return self.async_show_form(
            step_id="set_name",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_DEVICE_NAME, default=self._default_name or ""): str,
                }
            ),
            description_placeholders={
                "address": self._address or "",
                "device_type": self._device_type or "",
            },
        )

    async def async_step_set_name(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the name input and trigger the device acceptance."""
        if user_input is None:
            return await self.async_step_init()

        device_name = user_input.get(CONF_DEVICE_NAME, "").strip() if user_input else ""

        # Execute the fix callback with the device name (empty string skips rename)
        cb = REPAIR_CALLBACKS.pop(self._issue_id, None)
        if cb is not None:
            with contextlib.suppress(Exception):
                await cb(device_name=device_name)

        # Clean up stored device data
        INBOX_DEVICE_DATA.pop(self._issue_id, None)

        # Close the issue
        async_delete_issue(hass=self.hass, domain=DOMAIN, issue_id=self._issue_id)

        return self.async_create_entry(title="", data={})
