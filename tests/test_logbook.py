"""
Tests for logbook module to achieve 100% coverage.

This suite validates:
- Event descriptions are registered for the integration domain and correct event types.
- Valid device error event produces the expected name/message for both error and resolved states.
- Invalid event data yields an empty dict from the describe callback.
- Optimistic rollback event produces the expected name/message.
"""

from __future__ import annotations

from collections.abc import Callable

from aiohomematic.const import DeviceTriggerEventType
from custom_components.homematicip_local.const import (
    DOMAIN as HMIP_DOMAIN,
    EVENT_ADDRESS,
    EVENT_AGE_SECONDS,
    EVENT_CHANNEL_NO,
    EVENT_DEVICE_ID,
    EVENT_ERROR,
    EVENT_ERROR_VALUE,
    EVENT_IDENTIFIER,
    EVENT_INTERFACE_ID,
    EVENT_MESSAGE,
    EVENT_MODEL,
    EVENT_NAME,
    EVENT_PARAMETER,
    EVENT_REASON,
    EVENT_RESTORED_VALUE,
    EVENT_ROLLED_BACK_VALUE,
    EVENT_TITLE,
)
from custom_components.homematicip_local.control_unit import EVENT_TYPE_OPTIMISTIC_ROLLBACK
from custom_components.homematicip_local.logbook import async_describe_events
from homeassistant.components.logbook import LOGBOOK_ENTRY_MESSAGE, LOGBOOK_ENTRY_NAME
from homeassistant.core import Event


def _collect_describers() -> list[tuple[str, str, Callable[[Event], dict[str, str]]]]:
    """Collect all describers that async_describe_events registers with HA."""
    captured: list[tuple[str, str, Callable[[Event], dict[str, str]]]] = []

    def register(domain: str, event_type: str, describer: Callable[[Event], dict[str, str]]) -> None:
        captured.append((domain, event_type, describer))

    async_describe_events(None, register)
    return captured


def _get_describer(
    event_type: str,
) -> tuple[str, str, Callable[[Event], dict[str, str]]]:
    """Return the describer for a specific event type."""
    for domain, et, describer in _collect_describers():
        if et == event_type:
            return domain, et, describer
    raise ValueError(f"No describer registered for event type: {event_type}")


class TestAsyncDescribeEvents:
    """Tests for async_describe_events function."""

    def test_registers_device_error_describer(self) -> None:
        """It should register the device error event describer with correct domain and type."""
        domain, event_type, _describer = _get_describer(DeviceTriggerEventType.DEVICE_ERROR.value)

        assert domain == HMIP_DOMAIN
        assert event_type == DeviceTriggerEventType.DEVICE_ERROR.value

    def test_registers_optimistic_rollback_describer(self) -> None:
        """It should register the optimistic rollback event describer with correct domain and type."""
        domain, event_type, _describer = _get_describer(EVENT_TYPE_OPTIMISTIC_ROLLBACK)

        assert domain == HMIP_DOMAIN
        assert event_type == EVENT_TYPE_OPTIMISTIC_ROLLBACK

    def test_registers_two_describers(self) -> None:
        """It should register exactly two event describers."""
        describers = _collect_describers()
        assert len(describers) == 2


class TestDeviceErrorDescriber:
    """Tests for device error event describer callback."""

    def test_returns_empty_dict_for_invalid_payload(self) -> None:
        """It should return an empty dict when event data does not validate against schema."""
        _, event_type, describer = _get_describer(DeviceTriggerEventType.DEVICE_ERROR.value)

        # Missing required name field makes the schema invalid
        event = Event(event_type, data={EVENT_PARAMETER: "low_bat", EVENT_ERROR: True, EVENT_ERROR_VALUE: 1})

        assert describer(event) == {}

    def test_returns_expected_message_for_error_and_resolved(self) -> None:
        """It should format message correctly for error occurred and resolved cases."""
        domain, event_type, describer = _get_describer(DeviceTriggerEventType.DEVICE_ERROR.value)
        assert domain == HMIP_DOMAIN and event_type == DeviceTriggerEventType.DEVICE_ERROR.value

        # Error occurred
        event = Event(
            event_type,
            data={
                # Required base event schema fields
                EVENT_ADDRESS: "ABC0001",
                EVENT_CHANNEL_NO: 1,
                EVENT_MODEL: "XYZ",
                EVENT_INTERFACE_ID: "if1",
                # Parameter specific
                EVENT_PARAMETER: "low_bat",
                # Extended device error schema
                EVENT_NAME: "Kitchen Sensor",
                EVENT_IDENTIFIER: "dev-1",
                EVENT_TITLE: "Device Error",
                EVENT_MESSAGE: "Something happened",
                EVENT_DEVICE_ID: "device-123",
                EVENT_ERROR_VALUE: 1,
                EVENT_ERROR: True,
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
                EVENT_ADDRESS: "ABC0001",
                EVENT_CHANNEL_NO: 1,
                EVENT_MODEL: "XYZ",
                EVENT_INTERFACE_ID: "if1",
                # Parameter specific
                EVENT_PARAMETER: "low_bat",
                # Extended device error schema
                EVENT_NAME: "Kitchen Sensor",
                EVENT_IDENTIFIER: "dev-1",
                EVENT_TITLE: "Device Error",
                EVENT_MESSAGE: "Something happened",
                EVENT_DEVICE_ID: "device-123",
                EVENT_ERROR_VALUE: 0,
                EVENT_ERROR: False,
            },
        )
        result = describer(event)
        assert result[LOGBOOK_ENTRY_MESSAGE] == "Low Bat resolved"


class TestOptimisticRollbackDescriber:
    """Tests for optimistic rollback event describer callback."""

    def test_falls_back_to_address_when_name_missing(self) -> None:
        """It should use device address as fallback when name is not available."""
        _, event_type, describer = _get_describer(EVENT_TYPE_OPTIMISTIC_ROLLBACK)

        event = Event(
            event_type,
            data={
                EVENT_ADDRESS: "VCU0000001",
                EVENT_PARAMETER: "STATE",
                EVENT_REASON: "send_error",
                EVENT_ROLLED_BACK_VALUE: True,
                EVENT_RESTORED_VALUE: False,
                EVENT_AGE_SECONDS: 0.5,
                EVENT_INTERFACE_ID: "BidCos-RF",
            },
        )
        result = describer(event)
        assert result[LOGBOOK_ENTRY_NAME] == "VCU0000001"
        assert result[LOGBOOK_ENTRY_MESSAGE] == "Optimistic update rolled back for STATE (reason: send_error)"

    def test_handles_missing_fields_gracefully(self) -> None:
        """It should use defaults when optional fields are missing."""
        _, event_type, describer = _get_describer(EVENT_TYPE_OPTIMISTIC_ROLLBACK)

        event = Event(event_type, data={})
        result = describer(event)
        assert result[LOGBOOK_ENTRY_NAME] == "unknown"
        assert result[LOGBOOK_ENTRY_MESSAGE] == "Optimistic update rolled back for unknown (reason: unknown)"

    def test_returns_expected_message_with_name(self) -> None:
        """It should format rollback message with device name and reason."""
        _, event_type, describer = _get_describer(EVENT_TYPE_OPTIMISTIC_ROLLBACK)

        event = Event(
            event_type,
            data={
                EVENT_NAME: "Living Room Light",
                EVENT_ADDRESS: "VCU0000001",
                EVENT_PARAMETER: "LEVEL",
                EVENT_REASON: "timeout",
                EVENT_ROLLED_BACK_VALUE: 0.5,
                EVENT_RESTORED_VALUE: 0.0,
                EVENT_AGE_SECONDS: 30.1,
                EVENT_INTERFACE_ID: "HmIP-RF",
            },
        )
        result = describer(event)
        assert result[LOGBOOK_ENTRY_NAME] == "Living Room Light"
        assert result[LOGBOOK_ENTRY_MESSAGE] == "Optimistic update rolled back for LEVEL (reason: timeout)"
