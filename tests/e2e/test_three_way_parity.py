"""Three-way godevccu parity: aiohomematic vs loom-client vs loom-MQTT.

A single godevccu backend feeds three north-bound surfaces; this suite
asserts Home Assistant produces the same devices, entities, names and
card attributes across all three. Opt-in: ``pytest -m e2e -p no:xdist``.
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
from .stack import CCU_PASSWORD, CCU_USERNAME, DAEMON_TOKEN, BackendStack

pytestmark = pytest.mark.e2e

# The godevccu serial both homematicip_local backends key their entities to.
SERIAL = "GODEVCCU0001"


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


# By-design entity-set residuals between the two homematicip_local backends.
# The daemon always exposes a hub system-update entity; the aiohomematic backend
# only creates one when godevccu actually advertises an available firmware.
_LOOM_SET_ALLOWLIST = frozenset({"update:system"})


def test_loom_backend_entity_set_parity(parity_results: dict[str, Any]) -> None:
    """The two homematicip_local backends expose the same set of entities.

    This is the core enforced parity claim: aiohomematic (direct CCU) and the
    openccu-loom-client backend, fed by the same godevccu, must materialize the
    same entities (a single documented hub-update residual aside).
    """
    results = _ordered_results(parity_results)
    report = diff_snapshots({"ccu": results["ccu"], "loom": results["loom"]})["loom"]
    missing = set(report["missing_vs_ref"]) - _LOOM_SET_ALLOWLIST
    extra = set(report["extra_vs_ref"]) - _LOOM_SET_ALLOWLIST
    assert not missing, f"entities on aiohomematic but missing on loom: {sorted(missing)}"
    assert not extra, f"entities on loom but missing on aiohomematic: {sorted(extra)}"


@pytest.mark.xfail(
    reason=(
        "Residual naming/scheme drift, not entity-set drift: the loom-client emits some "
        "calculated-DP names as raw parameter names (e.g. DEW_POINT) instead of the translated "
        "name, and channel/virtual-receiver markers differ; the mqtt discovery layer uses its own "
        "naming and unique-id scheme for schedules, events, sysvars/programs and labels firmware "
        "updates 'Firmware' vs 'Update'. Tracked for the loom-client / daemon naming layers."
    ),
    strict=False,
)
def test_full_entity_parity(parity_results: dict[str, Any]) -> None:
    """Assert the three planes expose an identical set of entities, names and attrs."""
    ordered = _ordered_results(parity_results)
    report = diff_snapshots(ordered)
    problems: list[str] = []
    for plane in ("loom", "mqtt"):
        section = report[plane]
        problems += [
            f"{plane}.{field_name}={len(section[field_name])}"
            for field_name in ("missing_vs_ref", "extra_vs_ref", "name_drift", "attr_drift")
            if section[field_name]
        ]
    assert not problems, "parity drift vs ccu reference: " + ", ".join(problems)
