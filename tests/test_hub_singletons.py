"""The hub singletons reach Home Assistant by announcement, not by enumeration."""

from __future__ import annotations

from unittest.mock import patch

from custom_components.homematicip_local.const import DOMAIN as HMIP_DOMAIN
from custom_components.homematicip_local.control_unit import ControlUnit
from homeassistant.helpers import entity_registry as er

from tests import helper

TEST_DEVICES: dict[str, str] = {"VCU2128127": "HmIP-BSM"}


def _singleton_unique_ids(control: ControlUnit) -> dict[str, str]:
    """Return ``{label: registry unique_id}`` for every hub singleton the coordinator holds.

    Read off the coordinator rather than hard-coded, so a singleton added later
    is covered the day it appears instead of the day someone remembers to list
    it here.
    """
    hub_coordinator = control.central.hub_coordinator
    found: dict[str, str] = {}
    for label in ("alarm_messages_dp", "service_messages_dp", "inbox_dp", "update_dp"):
        if (data_point := getattr(hub_coordinator, label, None)) is not None:
            found[label] = f"{HMIP_DOMAIN}_{data_point.unique_id}"
    if (metrics := hub_coordinator.metrics_dps) is not None:
        for label in ("system_health", "connection_latency", "last_event_age"):
            found[label] = f"{HMIP_DOMAIN}_{getattr(metrics, label).unique_id}"
    for interface_id, connectivity in hub_coordinator.connectivity_dps.items():
        found[f"connectivity:{interface_id}"] = f"{HMIP_DOMAIN}_{connectivity.sensor.unique_id}"
    for interface, install_mode in hub_coordinator.install_mode_dps.items():
        found[f"install_mode_button:{interface}"] = f"{HMIP_DOMAIN}_{install_mode.button.unique_id}"
        found[f"install_mode_sensor:{interface}"] = f"{HMIP_DOMAIN}_{install_mode.sensor.unique_id}"
    return found


class TestHubSingletonsBecomeEntities:
    """The gap that let #1275 drop every announced entity while the suite stayed green.

    `hub_coordinator.get_hub_data_points()` returns programs and sysvars only
    (`aiohomematic/central/coordinators/hub.py:380-384`), and that is the only
    hub query the platforms enumerate in their setup tails. The metrics,
    connectivity and install-mode data points arrive solely through
    `DataPointsCreatedEvent` → `signal_new_data_point`
    (`aiohomematic/central/coordinators/event.py:524-537`), so they become
    entities only if the platforms are already listening when the central
    starts — which in production they are, because `start_central()` runs after
    `async_forward_entry_setups`.

    The default test harness starts the central *before* setting the entry up,
    which is exactly the ordering that loses them. So these entities never
    existed in any test, and a change that stopped them existing in production
    could not fail anything. `start_central_before_setup=False` puts the
    harness in the production order; without it the first test below fails on
    every singleton.
    """

    async def test_every_singleton_the_coordinator_holds_has_a_registry_entry(
        self, factory_ccu: helper.Factory
    ) -> None:
        """Announced entities exist when the platforms are up before the central starts."""
        with patch("custom_components.homematicip_local._async_reanchor_hub_unique_ids_on_serial_change"):
            # Patched, not worked around: the harness cannot know the CCU serial
            # before the central runs, so the entry's unique_id is still the
            # placeholder when setup begins and the re-anchor would re-key
            # everything and reload mid-test. It is covered on its own elsewhere
            # and has nothing to do with what this asserts.
            hass, control = await factory_ccu.setup_environment(TEST_DEVICES, start_central_before_setup=False)

        expected = _singleton_unique_ids(control)
        assert expected, "the coordinator holds no singletons — this asserts nothing"

        entity_registry = er.async_get(hass)
        present = {
            entry.unique_id
            for entry in er.async_entries_for_config_entry(entity_registry, factory_ccu.mock_config_entry.entry_id)
        }
        missing = {label: unique_id for label, unique_id in expected.items() if unique_id not in present}
        assert missing == {}, (
            "hub singletons the coordinator holds never became entities — they are announced, "
            f"not enumerated, so the platforms were not listening when the central started: {missing}"
        )

    async def test_the_default_harness_order_is_the_one_that_loses_them(self, factory_ccu: helper.Factory) -> None:
        """Pin why the suite was blind, so nobody 'fixes' the flag away.

        Negative control for the test above: with the central started before the
        entry, the very same singletons are absent. That is the harness being
        unlike production, not a product defect — and it is the reason the
        first test has to ask for the other order.
        """
        hass, control = await factory_ccu.setup_environment(TEST_DEVICES)

        expected = _singleton_unique_ids(control)
        assert expected, "the coordinator holds no singletons — this asserts nothing"

        entity_registry = er.async_get(hass)
        present = {
            entry.unique_id
            for entry in er.async_entries_for_config_entry(entity_registry, factory_ccu.mock_config_entry.entry_id)
        }
        assert not (set(expected.values()) & present), (
            "the default harness order now spawns singletons too — if that is intended, "
            "the first test no longer needs start_central_before_setup=False"
        )
