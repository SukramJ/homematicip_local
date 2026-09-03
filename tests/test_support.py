"""
Unit tests for custom_components.homematicip_local.support.

Covered functions:
- cleanup_click_event_data: transforms keys and removes channel/parameter.
- is_valid_event: returns True on valid schema, False and logs on invalid.
- CLICK_EVENT_SCHEMA: accepts what cleanup_click_event_data produces.
- get_device_identifier: builds the backend-neutral device identifier.
- get_device_address_from_identifiers: parses identifier tuple set.
- get_data_point: passthrough helper for easier mocking.
- get_aiohomematic_version: parses requirement versions from manifest.
"""

from __future__ import annotations

from types import SimpleNamespace

import voluptuous as vol

from aiohomematic.const import IDENTIFIER_SEPARATOR, Interface
from custom_components.homematicip_local.const import (
    EVENT_ADDRESS,
    EVENT_CHANNEL_NO,
    EVENT_DEVICE_ID,
    EVENT_INTERFACE_ID,
    EVENT_MODEL,
    EVENT_NAME,
    EVENT_PARAMETER,
    EVENT_VALUE,
)
from custom_components.homematicip_local.support import (
    CLICK_EVENT_SCHEMA,
    cleanup_click_event_data,
    cleanup_instance_name,
    get_aiohomematic_version,
    get_data_point,
    get_device_address_from_identifiers,
    get_device_identifier,
    is_valid_event,
    validate_device_address,
)


class TestCleanupClickEventData:
    """Tests for cleanup_click_event_data function."""

    def test_transforms_and_removes(self) -> None:
        """It should lower parameter into type, copy channel_no into subtype, and drop original keys."""
        raw = {
            EVENT_PARAMETER: "SHORT_PRESS",
            EVENT_CHANNEL_NO: 2,
            "other": 1,
        }
        cleaned = cleanup_click_event_data(raw)

        assert cleaned["type"] == "short_press"
        assert cleaned["subtype"] == 2
        # Originals removed
        assert EVENT_PARAMETER not in cleaned
        assert EVENT_CHANNEL_NO not in cleaned
        # Pass-through of unrelated keys
        assert cleaned["other"] == 1


class TestClickEventSchema:
    """Tests for CLICK_EVENT_SCHEMA."""

    @staticmethod
    def _device_trigger_event_data() -> dict[str, object]:
        """Return an event payload shaped like ControlUnit._on_device_trigger builds it."""
        return {
            EVENT_INTERFACE_ID: "Otto-HmIP-RF",
            EVENT_ADDRESS: "000B58A9A77B85",
            EVENT_CHANNEL_NO: 1,
            EVENT_MODEL: "HmIP-WRC6",
            EVENT_PARAMETER: "PRESS_SHORT",
            EVENT_VALUE: True,
            EVENT_DEVICE_ID: "3f1c2e9a4b5d6e7f8a9b0c1d2e3f4a5b",
            EVENT_NAME: "Wandtaster WZ",
        }

    def test_accepts_cleaned_click_event(self) -> None:
        """
        The schema must accept what cleanup_click_event_data produces.

        Both halves were covered in isolation before, so nothing caught that the
        schema still required the ``channel_no`` the cleanup had just dropped.
        A rejected event is never fired, which leaves every keypress automation
        without a trigger.
        """
        cleaned = cleanup_click_event_data(self._device_trigger_event_data())

        assert is_valid_event(event_data=cleaned, schema=CLICK_EVENT_SCHEMA) is True

    def test_rejects_event_without_device_id(self) -> None:
        """An event whose device is missing from the registry must not validate."""
        event_data = self._device_trigger_event_data()
        del event_data[EVENT_DEVICE_ID]

        assert is_valid_event(event_data=cleanup_click_event_data(event_data), schema=CLICK_EVENT_SCHEMA) is False

    def test_subtype_stays_an_int(self) -> None:
        """The channel number must survive as an int; blueprints compare it numerically."""
        cleaned = CLICK_EVENT_SCHEMA(cleanup_click_event_data(self._device_trigger_event_data()))

        assert cleaned["subtype"] == 1
        assert cleaned["type"] == "press_short"


class TestIsValidEvent:
    """Tests for is_valid_event function."""

    def test_true_and_false(self) -> None:
        """It should validate against a provided voluptuous schema and return boolean."""
        schema = vol.Schema({"a": int})
        assert is_valid_event({"a": 1}, schema) is True
        assert is_valid_event({"a": "x"}, schema) is False


class TestGetDeviceIdentifier:
    """Tests for get_device_identifier function."""

    def test_applies_the_same_cleanup_as_the_central_name(self) -> None:
        """A slash in the instance name must not split the two paths apart.

        ``ControlConfig`` strips slashes before the name reaches the central,
        so an identifier built from the running central and one built from the
        raw config entry — which is what the registry migration reads — would
        otherwise disagree, and the migration would write a key no platform
        ever produces.
        """
        assert get_device_identifier(
            instance_name="Otto/Dev", address="ABC123", interface="HmIP-RF"
        ) == get_device_identifier(
            instance_name=cleanup_instance_name(instance_name="Otto/Dev"), address="ABC123", interface="HmIP-RF"
        )

    def test_builds_from_instance_name_and_interface(self) -> None:
        """The identifier carries the HA instance name, not a backend's interface id."""
        assert (
            get_device_identifier(instance_name="OttoDev", address="ABC123", interface="HmIP-RF")
            == f"ABC123{IDENTIFIER_SEPARATOR}OttoDev-HmIP-RF"
        )

    def test_matches_the_aiohomematic_identifier(self) -> None:
        """On the direct-CCU backend the result equals what aiohomematic composes itself.

        aiohomematic builds its interface id as ``<central_name>-<interface>``
        and its device identifier as ``<address>@<interface_id>``, so nothing
        moves for a direct-CCU installation. That is the whole reason this
        migration is a no-op there.
        """
        interface_id = f"OttoDev-{Interface.HMIP_RF}"
        assert (
            get_device_identifier(instance_name="OttoDev", address="ABC123", interface=str(Interface.HMIP_RF))
            == f"ABC123{IDENTIFIER_SEPARATOR}{interface_id}"
        )

    def test_returns_none_for_unknown_interface(self) -> None:
        """A loom device stub carries the wire id here until its detail arrives."""
        assert get_device_identifier(instance_name="OttoDev", address="ABC123", interface="Otto-HmIP-RF") is None


class TestGetDeviceAddressFromIdentifiers:
    """Tests for get_device_address_from_identifiers function."""

    def test_parses_regular_device(self) -> None:
        """Extract the address from a regular device identifier."""
        sep = IDENTIFIER_SEPARATOR
        good = ("homematicip_local", f"ABC123{sep}OttoDev-HmIP-RF")
        other = ("homematicip_local", "NOSEP")
        assert get_device_address_from_identifiers({good, other}) == "ABC123"

    def test_parses_schedule_device(self) -> None:
        """Same for the schedule device."""
        sep = IDENTIFIER_SEPARATOR
        assert (
            get_device_address_from_identifiers({("homematicip_local", f"000A1B2C3D{sep}OttoDev-BidCos-RF-schedule")})
            == "000A1B2C3D"
        )

    def test_parses_sub_device(self) -> None:
        """A sub-device suffix sits behind the separator and needs no handling."""
        sep = IDENTIFIER_SEPARATOR
        assert get_device_address_from_identifiers({("homematicip_local", f"ABC123{sep}OttoDev-HmIP-RF-1")}) == "ABC123"

    def test_returns_none_without_separator(self) -> None:
        """Return None when no identifier contains the separator."""
        assert get_device_address_from_identifiers({("homematicip_local", "NOSEPARATOR")}) is None


class TestValidateDeviceAddress:
    """Tests for validate_device_address function."""

    def test_channel_address_extracts_device_part(self) -> None:
        """Extract device part from a channel address."""
        assert validate_device_address("FED00000123:3") == "FED00000123"
        assert validate_device_address("ABC1234567:0") == "ABC1234567"
        assert validate_device_address("HmIP-RF-12345:12") == "HmIP-RF-12345"

    def test_invalid_format_raises(self) -> None:
        """Reject values that are neither device nor channel address."""
        import pytest

        with pytest.raises(vol.Invalid, match="Invalid device address format"):
            validate_device_address("invalid!")
        with pytest.raises(vol.Invalid, match="must be a string"):
            validate_device_address(12345)

    def test_valid_device_address(self) -> None:
        """Accept a plain device address."""
        assert validate_device_address("FED00000123") == "FED00000123"


class TestGetDataPoint:
    """Tests for get_data_point function."""

    def test_passthrough(self) -> None:
        """It should just return the same object provided, to allow easy mocking in higher layers."""
        obj = object()
        assert get_data_point(obj) is obj


class TestGetAiohomematicVersion:
    """Tests for get_aiohomematic_version function."""

    async def test_parses_manifest(self, hass) -> None:
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

        async def _fake_get_integration(_hass, _domain):
            return integration

        # Patch the async_get_integration symbol used inside the module under test
        from custom_components.homematicip_local import support as hm_support

        hm_support.async_get_integration = _fake_get_integration  # type: ignore[assignment]

        version = await get_aiohomematic_version(hass, domain="homematicip_local", package_name="aiohomematic")
        assert version == "2025.10.5"

        # Non-existing package returns fallback None/0.0.0 behavior handled by caller
        version_none = await get_aiohomematic_version(hass, domain="homematicip_local", package_name="doesnotexist")
        assert version_none is None
