"""Test the AioHomematic entity helper."""

from __future__ import annotations

import pytest

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers import REGISTRY
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.event import EventDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTime


class TestEntityHelper:
    """Tests for entity helper functions."""

    def test_daemon_and_ccu_latency_do_not_share_a_description(self) -> None:
        """The rule must match the daemon sensor only, not the CCU one beside it."""
        daemon = REGISTRY.find(category=DataPointCategory.HUB_SENSOR, var_name="daemon_latency")
        ccu = REGISTRY.find(category=DataPointCategory.HUB_SENSOR, var_name="connection_latency")
        assert daemon is not None
        assert ccu is not None
        assert daemon.key != ccu.key

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

    def test_registry_find_daemon_connection(self) -> None:
        """
        The openccu-loom daemon-reachability sensor carries CONNECTIVITY.

        It answers the same question as the per-interface connectivity
        sensors one layer up, so it needs the same device class — without
        one Home Assistant renders a bare on/off and cannot tell that
        "off" is the bad state.

        It needs a rule of its own because the interface rule matches the
        ``Connectivity`` name prefix and this singleton is named
        ``daemon_connection``; the one is not a substring of the other.
        """
        description = REGISTRY.find(
            category=DataPointCategory.HUB_BINARY_SENSOR,
            var_name="daemon_connection",
        )

        assert description is not None
        assert description.key == "DAEMON_CONNECTION"
        assert description.device_class == BinarySensorDeviceClass.CONNECTIVITY

    def test_registry_find_daemon_latency(self) -> None:
        """
        The client-to-daemon latency sensor is distinct from the CCU one.

        Two legs with unrelated causes: a slow reverse proxy between Home
        Assistant and the daemon is invisible in the CCU figure, and a
        struggling CCU is invisible in this one. They are therefore two
        sensors, and each needs its own description — without one the entity
        renders with no unit, device class or icon.
        """
        description = REGISTRY.find(
            category=DataPointCategory.HUB_SENSOR,
            var_name="daemon_latency",
        )

        assert description is not None
        assert description.key == "DAEMON_LATENCY"
        assert description.device_class == SensorDeviceClass.DURATION
        assert description.native_unit_of_measurement == UnitOfTime.MILLISECONDS

    @pytest.mark.parametrize("device_model", ["HmIP-DBB", "HmIP-DSD-PCB"])
    def test_registry_find_doorbell_event(self, device_model: str) -> None:
        """Doorbell devices expose their event group with the doorbell device class."""
        description = REGISTRY.find(
            category=DataPointCategory.EVENT_GROUP,
            device_model=device_model,
        )

        assert description is not None
        assert description.key == "event_doorbell"
        assert description.device_class == EventDeviceClass.DOORBELL

    def test_registry_find_event_defaults_to_button(self) -> None:
        """A non-doorbell keypress device keeps the default button device class."""
        description = REGISTRY.find(
            category=DataPointCategory.EVENT_GROUP,
            device_model="HmIP-WRC2",
        )

        assert description is not None
        assert description.key == "event_default"
        assert description.device_class == EventDeviceClass.BUTTON

    def test_registry_find_interface_connectivity(self) -> None:
        """The per-interface sensor keeps its own rule — the two must not collapse."""
        description = REGISTRY.find(
            category=DataPointCategory.HUB_BINARY_SENSOR,
            var_name="Connectivity HmIP-RF",
        )

        assert description is not None
        assert description.key == "CONNECTIVITY_SENSOR"
        assert description.device_class == BinarySensorDeviceClass.CONNECTIVITY

    @pytest.mark.parametrize(
        ("security_class", "device_class"),
        [
            ("smoke", BinarySensorDeviceClass.SMOKE),
            ("water", BinarySensorDeviceClass.MOISTURE),
            ("gas", BinarySensorDeviceClass.GAS),
            ("co", BinarySensorDeviceClass.CO),
            ("tamper", BinarySensorDeviceClass.TAMPER),
            ("battery", BinarySensorDeviceClass.BATTERY),
            ("technical", BinarySensorDeviceClass.PROBLEM),
            ("intrusion", BinarySensorDeviceClass.SAFETY),
            ("panic", BinarySensorDeviceClass.SAFETY),
        ],
    )
    def test_registry_find_security_class(self, security_class: str, device_class: BinarySensorDeviceClass) -> None:
        """
        Each Security & Safety hazard class carries its own device class.

        Without one the sensor is a bare on/off, and "on" — a detector has
        fired — reads as the good state. The table is spelled out rather
        than derived so that changing a mapping has to change a test: a
        loop over the rules would agree with whatever the rules say.
        """
        description = REGISTRY.find(
            category=DataPointCategory.HUB_BINARY_SENSOR,
            var_name=f"security_{security_class}",
        )

        assert description is not None
        assert description.device_class == device_class

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

    def test_registry_security_classes_do_not_shadow_connectivity(self) -> None:
        """
        The security rules must not swallow the connectivity sensors.

        Both families are HUB_BINARY_SENSOR and matched by substring, and
        the first matching rule wins — so a rule matched on a shorter
        fragment would quietly take entities it was never meant to.
        """
        for var_name, expected in (
            ("daemon_connection", "DAEMON_CONNECTION"),
            ("Connectivity HmIP-RF", "CONNECTIVITY_SENSOR"),
        ):
            description = REGISTRY.find(
                category=DataPointCategory.HUB_BINARY_SENSOR,
                var_name=var_name,
            )
            assert description is not None
            assert description.key == expected
