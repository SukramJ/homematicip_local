"""
Unit tests for custom_components.homematicip_local.support.

Covered functions:
- cleanup_click_event_data: transforms keys and removes channel/parameter.
- is_valid_event: returns True on valid schema, False and logs on invalid.
- get_device_address_at_interface_from_identifiers: parses identifier tuple set.
- get_data_point: passthrough helper for easier mocking.
- get_aiohomematic_version: parses requirement versions from manifest.
"""

from __future__ import annotations

from types import SimpleNamespace

import voluptuous as vol

from aiohomematic.const import IDENTIFIER_SEPARATOR, EventKey
from custom_components.homematicip_local.support import (
    cleanup_click_event_data,
    get_aiohomematic_version,
    get_data_point,
    get_device_address_at_interface_from_identifiers,
    is_valid_event,
)


def test_cleanup_click_event_data_transforms_and_removes() -> None:
    """It should lower parameter into type, copy channel_no into subtype, and drop original keys."""
    raw = {
        EventKey.PARAMETER: "SHORT_PRESS",
        EventKey.CHANNEL_NO: 2,
        "other": 1,
    }
    cleaned = cleanup_click_event_data(raw)

    assert cleaned["type"] == "short_press"
    assert cleaned["subtype"] == 2
    # Originals removed
    assert EventKey.PARAMETER not in cleaned
    assert EventKey.CHANNEL_NO not in cleaned
    # Pass-through of unrelated keys
    assert cleaned["other"] == 1


def test_is_valid_event_true_and_false() -> None:
    """It should validate against a provided voluptuous schema and return boolean."""
    schema = vol.Schema({"a": int})
    assert is_valid_event({"a": 1}, schema) is True
    assert is_valid_event({"a": "x"}, schema) is False


def test_get_device_address_at_interface_from_identifiers_parses() -> None:
    """It should extract the interface and address from identifiers containing the separator."""
    sep = IDENTIFIER_SEPARATOR
    good = ("homematicip_local", f"INTF{sep}ADDRESS")
    other = ("homematicip_local", "NOSEP")
    result = get_device_address_at_interface_from_identifiers({good, other})
    # Function currently returns a list from split; accept either list or tuple shape
    assert tuple(result) == ("INTF", "ADDRESS")


def test_get_data_point_passthrough() -> None:
    """It should just return the same object provided, to allow easy mocking in higher layers."""
    obj = object()
    assert get_data_point(obj) is obj


async def test_get_aiohomematic_version_parses_manifest(hass) -> None:
    """It should parse the version of a package from the integration manifest requirements."""
    # Provide a fake integration object with a minimal manifest
    integration = SimpleNamespace(
        manifest={
            "requirements": [
                "aiohomematic == 2025.10.5",
                "somepkg!=1.0.0",
                "another~=2.0",
            ]
        }
    )

    async def _fake_get_integration(_hass, _domain):  # noqa: ANN001
        return integration

    # Patch the async_get_integration symbol used inside the module under test
    from custom_components.homematicip_local import support as hm_support

    hm_support.async_get_integration = _fake_get_integration  # type: ignore[assignment]

    version = await get_aiohomematic_version(hass, domain="homematicip_local", package_name="aiohomematic")
    assert version == "2025.10.5"

    # Non-existing package returns fallback None/0.0.0 behavior handled by caller
    version_none = await get_aiohomematic_version(hass, domain="homematicip_local", package_name="doesnotexist")
    assert version_none is None
