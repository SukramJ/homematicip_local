"""
Tests for logbook module to achieve 100% coverage.

This suite validates:
- Event description is registered for the integration domain and device error event type.
- Valid device error event produces the expected name/message for both error and resolved states.
- Invalid event data yields an empty dict from the describe callback.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aiohomematic.const import DeviceTriggerEventType
from custom_components.homematicip_local.const import DOMAIN as HMIP_DOMAIN, EventKey
from custom_components.homematicip_local.logbook import async_describe_events
from homeassistant.components.logbook import LOGBOOK_ENTRY_MESSAGE, LOGBOOK_ENTRY_NAME
from homeassistant.core import Event


def _collect_describer() -> tuple[str, str, Callable[[Event], dict[str, str]]]:
    """Collect the describer that async_describe_events registers with HA."""
    captured: dict[str, Any] = {}

    def register(domain: str, event_type: str, describer: Callable[[Event], dict[str, str]]) -> None:
        captured["domain"] = domain
        captured["event_type"] = event_type
        captured["describer"] = describer

    async_describe_events(None, register)
    return captured["domain"], captured["event_type"], captured["describer"]


class TestAsyncDescribeEvents:
    """Tests for async_describe_events function."""

    def test_registers_device_error_describer(self) -> None:
        """It should register the device error event describer with correct domain and type."""
        domain, event_type, _describer = _collect_describer()

        assert domain == HMIP_DOMAIN
        assert event_type == DeviceTriggerEventType.DEVICE_ERROR.value


class TestDescriber:
    """Tests for event describer callback."""

    def test_returns_empty_dict_for_invalid_payload(self) -> None:
        """It should return an empty dict when event data does not validate against schema."""
        _, event_type, describer = _collect_describer()

        # Missing required name field makes the schema invalid
        event = Event(event_type, data={EventKey.PARAMETER: "low_bat", EventKey.ERROR: True, EventKey.ERROR_VALUE: 1})

        assert describer(event) == {}

    def test_returns_expected_message_for_error_and_resolved(self) -> None:
        """It should format message correctly for error occurred and resolved cases."""
        domain, event_type, describer = _collect_describer()
        assert domain == HMIP_DOMAIN and event_type == DeviceTriggerEventType.DEVICE_ERROR.value

        # Error occurred
        event = Event(
            event_type,
            data={
                # Required base event schema fields
                str(EventKey.ADDRESS): "ABC0001",
                str(EventKey.CHANNEL_NO): 1,
                str(EventKey.MODEL): "XYZ",
                str(EventKey.INTERFACE_ID): "if1",
                # Parameter specific
                str(EventKey.PARAMETER): "low_bat",
                # Extended device error schema
                EventKey.NAME: "Kitchen Sensor",
                EventKey.IDENTIFIER: "dev-1",
                EventKey.TITLE: "Device Error",
                EventKey.MESSAGE: "Something happened",
                EventKey.DEVICE_ID: "device-123",
                EventKey.ERROR_VALUE: 1,
                EventKey.ERROR: True,
            },
        )
        result = describer(event)
        assert result[LOGBOOK_ENTRY_NAME] == "Kitchen Sensor"
        assert result[LOGBOOK_ENTRY_MESSAGE] == "Low Bat 1 occurred"

        # Error resolved
        event = Event(
            event_type,
            data={
                # Required base event schema fields
                str(EventKey.ADDRESS): "ABC0001",
                str(EventKey.CHANNEL_NO): 1,
                str(EventKey.MODEL): "XYZ",
                str(EventKey.INTERFACE_ID): "if1",
                # Parameter specific
                EventKey.PARAMETER: "low_bat",
                # Extended device error schema
                EventKey.NAME: "Kitchen Sensor",
                EventKey.IDENTIFIER: "dev-1",
                EventKey.TITLE: "Device Error",
                EventKey.MESSAGE: "Something happened",
                EventKey.DEVICE_ID: "device-123",
                EventKey.ERROR_VALUE: 0,
                EventKey.ERROR: False,
            },
        )
        result = describer(event)
        assert result[LOGBOOK_ENTRY_MESSAGE] == "Low Bat resolved"
