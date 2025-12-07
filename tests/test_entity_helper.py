"""Test the AioHomematic entity helper."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers import REGISTRY


class TestEntityHelper:
    """Tests for entity helper functions."""

    def test_registry_defaults(self) -> None:
        """Test that defaults are returned when no rule matches."""
        # SWITCH should have a default
        description = REGISTRY.find(
            category=DataPointCategory.SWITCH,
            parameter="UNKNOWN_PARAM",
            device_model="UNKNOWN_DEVICE",
        )

        assert description is not None
        assert description.key == "switch_default"

    def test_registry_find_binary_sensor(self) -> None:
        """Test finding a binary sensor description."""
        description = REGISTRY.find(
            category=DataPointCategory.BINARY_SENSOR,
            parameter="MOTION",
        )

        assert description is not None
        assert description.key == "MOTION"

    def test_registry_find_cover(self) -> None:
        """Test finding a cover description."""
        description = REGISTRY.find(
            category=DataPointCategory.COVER,
            device_model="HmIP-BBL",
        )

        assert description is not None
        assert description.key == "BLIND"

    def test_registry_find_sensor(self) -> None:
        """Test finding a sensor description."""
        description = REGISTRY.find(
            category=DataPointCategory.SENSOR,
            parameter="TEMPERATURE",
        )

        assert description is not None
        assert description.key == "TEMPERATURE"

    def test_registry_find_with_device_override(self) -> None:
        """Test that device-specific overrides work."""
        # Generic frequency should use Hz
        generic_desc = REGISTRY.find(
            category=DataPointCategory.SENSOR,
            parameter="FREQUENCY",
            device_model="HmIP-GENERIC",
        )
        assert generic_desc is not None
        assert generic_desc.native_unit_of_measurement == "Hz"

        # HMW-IO-12-Sw14-DR should use mHz
        device_desc = REGISTRY.find(
            category=DataPointCategory.SENSOR,
            parameter="FREQUENCY",
            device_model="HMW-IO-12-Sw14-DR",
        )
        assert device_desc is not None
        assert device_desc.native_unit_of_measurement == "mHz"

    def test_registry_has_rules(self) -> None:
        """Test that the registry has rules registered."""
        stats = REGISTRY.get_stats()

        # Verify we have rules for the expected categories
        assert "SENSOR" in stats
        assert "BINARY_SENSOR" in stats
        assert "BUTTON" in stats
        assert "COVER" in stats
        assert "SWITCH" in stats
        assert "NUMBER" in stats

        # Verify we have a reasonable number of rules
        assert stats["SENSOR"] > 50
        assert stats["BINARY_SENSOR"] > 10
        assert stats["BUTTON"] > 0
