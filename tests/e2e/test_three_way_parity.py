"""Three-way godevccu parity: aiohomematic vs loom-client vs loom-MQTT.

A single godevccu backend feeds three north-bound surfaces; this suite
asserts Home Assistant produces the same devices, entities, names and
card attributes across all three. Opt-in: ``pytest -m e2e -n0``.
"""

from __future__ import annotations

from pathlib import Path
import shutil
from typing import Any

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.homematicip_local.const import (
    CONF_ADVANCED_CONFIG,
    CONF_BACKEND,
    CONF_COMMAND_THROTTLE_INTERVAL,
    CONF_ENABLE_PROGRAM_SCAN,
    CONF_ENABLE_SYSTEM_NOTIFICATIONS,
    CONF_ENABLE_SYSVAR_SCAN,
    CONF_INSTANCE_NAME,
    CONF_INTERFACE,
    CONF_JSON_PORT,
    CONF_LOOM_PORT,
    CONF_LOOM_TOKEN,
    CONF_TLS,
    CONF_VERIFY_TLS,
    DOMAIN,
)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .parity import Snapshot, diff_snapshots, scrape, wait_until_settled
from .stack import CCU_DEVICES, CCU_PASSWORD, CCU_USERNAME, DAEMON_TOKEN, BackendStack

pytestmark = pytest.mark.e2e

# The godevccu serial both homematicip_local backends key their entities to.
SERIAL = "GODEVCCU0001"

# The full ~399-device set loads in big bursts with a long up-front
# paramset-fetch gap on the aiohomematic plane; the fixed 4-device set settles
# almost immediately. Widen the stability window only when the large set is used.
_SETTLE_STABLE = 20.0 if CCU_DEVICES else 5.0


def _entities_for(hass: HomeAssistant, *, config_entry_id: str, platform: str) -> int:
    """Return the number of registered entities for a config entry + platform."""
    ent_reg = er.async_get(hass)
    return sum(1 for e in ent_reg.entities.values() if e.config_entry_id == config_entry_id and e.platform == platform)


async def _setup_settle_scrape(
    hass: HomeAssistant,
    *,
    entry: MockConfigEntry,
    plane: str,
    platform: str,
    strip_tokens: tuple[str, ...],
) -> Snapshot:
    """Set up an entry, wait for entities to settle, scrape, unload cleanly."""
    # aiohomematic persists device/paramset caches under the integration storage
    # dir; the HCC config dir is reused across runs, so a stale cache would pin
    # the plane to an earlier (possibly partial) device set. Start each plane from
    # a clean cache so it re-fetches the full set from godevccu.
    shutil.rmtree(Path(hass.config.path(DOMAIN)), ignore_errors=True)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id), f"{plane}: setup failed"
    await wait_until_settled(
        hass,
        predicate=lambda: _entities_for(hass, config_entry_id=entry.entry_id, platform=platform),
        timeout=900.0,
        # Bridge the gap between the hub-entity burst and the device-entity burst
        # while aiohomematic fetches all paramset descriptions up front.
        stable_for=_SETTLE_STABLE,
    )
    # The config-entry id (its last 10 chars are the central_id) and instance
    # name are random/per-plane and leak into hub/program/sysvar unique_ids.
    tokens = (*strip_tokens, entry.entry_id[-10:], SERIAL, SERIAL[-10:])
    snap = scrape(hass, plane=plane, config_entry_id=entry.entry_id, platform=platform, strip_tokens=tokens)
    await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    return snap


def _dump(snap: Snapshot) -> None:
    """Print a plane's normalized keys + raw unique_ids for inspection."""
    print(f"\n=== plane {snap.plane}: {len(snap.entities)} entities, {len(snap.device_keys)} devices ===")
    for key in sorted(snap.entities):
        e = snap.entities[key]
        print(f"  {key:<55} | name={e.friendly_name!r} state={e.state!r} raw={e.raw_unique_id}")


async def test_plane_aiohomematic(
    hass: HomeAssistant, enable_custom_integrations: Any, backend: BackendStack, parity_results: dict[str, Any]
) -> None:
    """Scrape the aiohomematic backend talking directly to godevccu."""
    data = {
        CONF_INSTANCE_NAME: "E2eCcu",
        CONF_HOST: "127.0.0.1",
        CONF_USERNAME: CCU_USERNAME,
        CONF_PASSWORD: CCU_PASSWORD,
        CONF_TLS: False,
        CONF_VERIFY_TLS: False,
        CONF_JSON_PORT: backend.ccu_json_rpc_port,
        CONF_INTERFACE: {"HmIP-RF": {CONF_PORT: backend.ccu_xml_rpc_port}},
        CONF_ADVANCED_CONFIG: {
            CONF_ENABLE_SYSVAR_SCAN: True,
            CONF_ENABLE_PROGRAM_SCAN: True,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: True,
            # Drop the 0.1 s inter-command throttle: against a local godevccu
            # with the full ~399-device set the throttled paramset fetch would
            # otherwise take many minutes before any device entity appears.
            CONF_COMMAND_THROTTLE_INTERVAL: 0.0,
        },
    }
    entry = MockConfigEntry(domain=DOMAIN, data=data, version=17, unique_id=SERIAL, title="E2eCcu")
    snap = await _setup_settle_scrape(hass, entry=entry, plane="ccu", platform=DOMAIN, strip_tokens=("e2eccu",))
    _dump(snap)
    parity_results["ccu"] = snap
    assert snap.entities


async def test_plane_loom(
    hass: HomeAssistant, enable_custom_integrations: Any, backend: BackendStack, parity_results: dict[str, Any]
) -> None:
    """Scrape the openccu-loom-client backend talking to the daemon."""
    data = {
        CONF_BACKEND: "loom",
        CONF_INSTANCE_NAME: "E2eLoom",
        CONF_HOST: "127.0.0.1",
        CONF_LOOM_PORT: backend.daemon_rest_port,
        CONF_LOOM_TOKEN: DAEMON_TOKEN,
        CONF_TLS: False,
        CONF_VERIFY_TLS: False,
        CONF_ADVANCED_CONFIG: {},
    }
    entry = MockConfigEntry(domain=DOMAIN, data=data, version=17, unique_id=SERIAL, title="E2eLoom")
    # The loom backend keys central/connectivity entities by the daemon's
    # central name (ccu-e2e), not the HA instance name.
    snap = await _setup_settle_scrape(
        hass, entry=entry, plane="loom", platform=DOMAIN, strip_tokens=("e2eloom", "ccu-e2e", "ccu_e2e")
    )
    _dump(snap)
    parity_results["loom"] = snap
    assert snap.entities


async def test_plane_mqtt(
    hass: HomeAssistant, enable_custom_integrations: Any, backend: BackendStack, parity_results: dict[str, Any]
) -> None:
    """Scrape Home Assistant's mqtt entities from the daemon's discovery."""
    # HA's mqtt integration reads configuration.yaml during setup; the HCC
    # testing_config dir has none, so provide an empty one.
    from pathlib import Path

    Path(hass.config.path("configuration.yaml")).write_text("", encoding="utf-8")
    entry = MockConfigEntry(
        domain="mqtt",
        data={"broker": "127.0.0.1", CONF_PORT: backend.mqtt_port},
        version=1,
        title="E2eMqtt",
    )
    snap = await _setup_settle_scrape(
        hass, entry=entry, plane="mqtt", platform="mqtt", strip_tokens=("ccu-e2e", "ccu_e2e")
    )
    _dump(snap)
    parity_results["mqtt"] = snap
    assert snap.entities


def _ordered_results(parity_results: dict[str, Any]) -> dict[str, Snapshot]:
    """Return the three plane snapshots in reference-first order."""
    assert set(parity_results) == {"ccu", "loom", "mqtt"}, "all three planes must have produced a snapshot"
    return {p: parity_results[p] for p in ("ccu", "loom", "mqtt")}


def test_parity_report(parity_results: dict[str, Any]) -> None:
    """Emit the three-way diff report; assert every plane produced entities.

    This is the always-on diagnostic: it prints the structured diff (and the
    per-plane counts) so a contributor can see exactly where the backends drift.
    Strict entity-for-entity equality is asserted separately.
    """
    import json

    ordered = _ordered_results(parity_results)
    report = diff_snapshots(ordered)
    print("\n=== PARITY REPORT ===")
    print(json.dumps(report, indent=2, default=str))
    for plane, snap in ordered.items():
        assert snap.entities, f"plane {plane} produced no entities"


def _is_by_design_residual(*, plane: str, key: str) -> bool:
    """Return whether an entity-set difference is an accepted by-design residual.

    * ``update:system`` — the daemon-backed planes always expose a hub
      system-update; the aiohomematic backend only creates one when godevccu
      advertises an available firmware.
    * The mqtt discovery layer deliberately does not surface admin/maintenance
      entities: program *buttons* (it exposes programs as switches), the
      install-mode button + sensor and the backup button.
    """
    if key == "update:system":
        return True
    if plane == "mqtt":
        return key.startswith("button:program_") or key == "button:create_backup" or "install_mode" in key
    return False


def test_entity_set_parity(parity_results: dict[str, Any]) -> None:
    """All three planes expose the same set of entities (by-design residuals aside).

    The core parity claim: one godevccu, fed through the aiohomematic backend,
    the openccu-loom-client backend and the daemon's mqtt discovery, yields the
    same Home Assistant entities. Naming/attribute drift is asserted separately.
    """
    results = _ordered_results(parity_results)
    problems: list[str] = []
    for plane in ("loom", "mqtt"):
        report = diff_snapshots({"ccu": results["ccu"], plane: results[plane]})[plane]
        for field_name, label in (("missing_vs_ref", "missing on"), ("extra_vs_ref", "extra on")):
            residual = [k for k in report[field_name] if not _is_by_design_residual(plane=plane, key=k)]
            if residual:
                problems.append(f"{plane} {label} {field_name}: {residual}")
    assert not problems, "entity-set drift vs ccu reference: " + " | ".join(problems)


@pytest.mark.xfail(
    reason=(
        "Residual naming/attribute drift, not entity-set drift. loom: only the multi-channel "
        "` chN` marker remains — it needs paramset-description-level presence (a parameter defined "
        "on several channels even when active on one), which the daemon's active-data-point model "
        "does not expose; the schedule-switch target-channel names are fixed via api 1.7.0. mqtt: "
        "the discovery layer uses HA-idiomatic naming (sysvar display names, no channel-type/`P `/"
        "`SV ` prefixes, `Firmware` vs `Update`) and sets units/state_class on sysvars. Tracked for "
        "the daemon wire/discovery naming layers."
    ),
    strict=False,
)
def test_full_entity_parity(parity_results: dict[str, Any]) -> None:
    """Assert the three planes expose identical entity names and card attributes."""
    ordered = _ordered_results(parity_results)
    report = diff_snapshots(ordered)
    problems: list[str] = []
    for plane in ("loom", "mqtt"):
        section = report[plane]
        problems += [
            f"{plane}.{field_name}={len(section[field_name])}"
            for field_name in ("name_drift", "attr_drift")
            if section[field_name]
        ]
    assert not problems, "name/attr drift vs ccu reference: " + ", ".join(problems)
