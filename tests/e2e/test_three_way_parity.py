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

from aiohomematic.exceptions import BaseHomematicException
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

from .actions import ActionResult, probe_config_surface, run_action_probes
from .enforced_models import ENFORCED_MODELS
from .parity import Snapshot, diff_snapshots, entity_model, per_model_entity_set_report, scrape, wait_until_settled
from .stack import CCU_DEVICES, CCU_PASSWORD, CCU_USERNAME, DAEMON_TOKEN, BackendStack

pytestmark = pytest.mark.e2e

# The godevccu serial both homematicip_local backends key their entities to.
# godevccu configures "GODEVCCU0001" but reports CCU-semantics serials (the
# trailing 10 characters) since 0.1.8+ — the entry unique_id must match the
# *reported* serial or the integration re-anchors and reloads mid-setup.
SERIAL = "DEVCCU0001"

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
    backend: BackendStack,
    action_results: dict[str, Any],
    probe_config: bool = False,
) -> Snapshot:
    """Set up an entry, settle, scrape, run the action probes, unload cleanly."""
    # aiohomematic persists device/paramset caches under the integration storage
    # dir; the HCC config dir is reused across runs, so a stale cache would pin
    # the plane to an earlier (possibly partial) device set. Start each plane from
    # a clean cache so it re-fetches the full set from godevccu.
    shutil.rmtree(Path(hass.config.path(DOMAIN)), ignore_errors=True)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id), f"{plane}: setup failed"
    # Every device materializes at least one entity, so a plane with fewer
    # entities than godevccu parent devices is still loading — the floor
    # bridges aiohomematic's minutes-long silent paramset-fetch gap that a
    # fixed stability window cannot.
    expected_devices = backend.parent_device_count()
    await wait_until_settled(
        hass,
        predicate=lambda: _entities_for(hass, config_entry_id=entry.entry_id, platform=platform),
        timeout=900.0,
        # Bridge the gap between the hub-entity burst and the device-entity burst
        # while aiohomematic fetches all paramset descriptions up front.
        stable_for=_SETTLE_STABLE,
        floor=lambda: _entities_for(hass, config_entry_id=entry.entry_id, platform=platform) >= expected_devices,
    )
    # The config-entry id (its last 10 chars are the central_id) and instance
    # name are random/per-plane and leak into hub/program/sysvar unique_ids.
    tokens = (*strip_tokens, entry.entry_id[-10:], SERIAL, SERIAL[-10:])
    snap = scrape(hass, plane=plane, config_entry_id=entry.entry_id, platform=platform, strip_tokens=tokens)
    # Behavioral parity: identical service calls + a CCU-side push, while the
    # entry is live. Every probe restores the state it found so the shared
    # godevccu is unchanged for the next plane.
    action_results[plane] = await run_action_probes(hass, snap=snap, control_port=backend.ccu_control_port)
    if probe_config and (switch := next((k for k in sorted(snap.entities) if k.startswith("switch:vcu")), None)):
        action_results[f"{plane}:config"] = await probe_config_surface(control=entry.runtime_data, key=switch)
    try:
        await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()
    except BaseHomematicException as bhexc:
        # Tolerate live-backend teardown races (e.g. aiohomematic 2026.7.11
        # raises InvalidStateTransitionError on a second stop request while a
        # client is already STOPPING). The suite asserts parity, not unload
        # hygiene, and every plane runs in its own Home Assistant instance.
        print(f"{plane}: unload raced ({bhexc!r}) — continuing")
    return snap


def _dump(snap: Snapshot) -> None:
    """Print a plane's normalized keys + raw unique_ids for inspection."""
    print(f"\n=== plane {snap.plane}: {len(snap.entities)} entities, {len(snap.device_keys)} devices ===")
    for key in sorted(snap.entities):
        e = snap.entities[key]
        print(f"  {key:<55} | name={e.friendly_name!r} state={e.state!r} raw={e.raw_unique_id}")


async def test_plane_aiohomematic(
    hass: HomeAssistant,
    enable_custom_integrations: Any,
    backend: BackendStack,
    parity_results: dict[str, Any],
    action_results: dict[str, Any],
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
    snap = await _setup_settle_scrape(
        hass,
        entry=entry,
        plane="ccu",
        platform=DOMAIN,
        strip_tokens=("e2eccu",),
        backend=backend,
        action_results=action_results,
        probe_config=True,
    )
    _dump(snap)
    parity_results["ccu"] = snap
    assert snap.entities


async def test_plane_loom(
    hass: HomeAssistant,
    enable_custom_integrations: Any,
    backend: BackendStack,
    parity_results: dict[str, Any],
    action_results: dict[str, Any],
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
        hass,
        entry=entry,
        plane="loom",
        platform=DOMAIN,
        strip_tokens=("e2eloom", "ccu-e2e", "ccu_e2e"),
        backend=backend,
        action_results=action_results,
        probe_config=True,
    )
    _dump(snap)
    parity_results["loom"] = snap
    assert snap.entities


async def test_plane_mqtt(
    hass: HomeAssistant,
    enable_custom_integrations: Any,
    backend: BackendStack,
    parity_results: dict[str, Any],
    action_results: dict[str, Any],
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
        hass,
        entry=entry,
        plane="mqtt",
        platform="mqtt",
        strip_tokens=("ccu-e2e", "ccu_e2e"),
        backend=backend,
        action_results=action_results,
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
    per-plane counts) so a contributor can see exactly where the backends
    drift, plus the ratchet summary — which models are clean and promotable
    into ``ENFORCED_MODELS`` and which enforced models regressed. Strict
    entity-for-entity equality is asserted separately.
    """
    import json

    ordered = _ordered_results(parity_results)
    report = diff_snapshots(ordered)
    clean, dirty = per_model_entity_set_report(
        ordered, is_by_design_residual=lambda plane, key: _is_by_design_residual(plane=plane, key=key)
    )
    report["enforced_models"] = sorted(ENFORCED_MODELS)
    report["promotable_models"] = sorted(clean - ENFORCED_MODELS)
    report["regressed_enforced_models"] = sorted(dirty & ENFORCED_MODELS)
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

    In the default 4-device run every entity is enforced. In a widened run
    (``GODEVCCU_E2E_DEVICES`` set) the ratchet applies: entities of models in
    ``ENFORCED_MODELS`` — and all hub/central entities, which carry no device
    model — must be clean, while the long tail of not-yet-promoted models is
    tracked by ``test_parity_report`` only. See tests/e2e/enforced_models.py
    for the promotion workflow.
    """
    results = _ordered_results(parity_results)
    widened = bool(CCU_DEVICES)
    problems: list[str] = []
    for plane in ("loom", "mqtt"):
        report = diff_snapshots({"ccu": results["ccu"], plane: results[plane]})[plane]
        for field_name, label in (("missing_vs_ref", "missing on"), ("extra_vs_ref", "extra on")):
            residual = [k for k in report[field_name] if not _is_by_design_residual(plane=plane, key=k)]
            if widened:
                residual = [
                    k for k in residual if (model := entity_model(results, key=k)) is None or model in ENFORCED_MODELS
                ]
            if residual:
                problems.append(f"{plane} {label} {field_name}: {residual}")
    assert not problems, "entity-set drift vs ccu reference: " + " | ".join(problems)


def test_action_parity(parity_results: dict[str, Any], action_results: dict[str, Any]) -> None:
    """Identical HA service calls and CCU-side pushes behave identically on every plane.

    Each plane ran the same probe sequence against the same godevccu (switch
    toggle + CCU push, cover position, climate target temperature), restoring
    every value it changed. The traces must match step for step — a timeout on
    one plane while another converged is a behavioral parity break (e.g. a
    command path that silently drops writes, or a push pipeline that never
    reaches the entity).
    """
    _ordered_results(parity_results)  # ensure all planes ran
    traces: dict[str, list[ActionResult]] = {p: action_results[p] for p in ("ccu", "loom", "mqtt")}
    for plane, trace in traces.items():
        assert trace, f"plane {plane} produced no action trace"
        timeouts = [f"{r.step}@{r.key}" for r in trace if r.outcome == "timeout"]
        assert not timeouts, f"plane {plane} probes timed out: {timeouts}"
    reference = traces["ccu"]
    for plane in ("loom", "mqtt"):
        assert traces[plane] == reference, (
            f"action trace of plane {plane} differs from ccu reference:\n"
            f"  ccu:  {reference}\n  {plane}: {traces[plane]}"
        )


def test_config_surface_parity(action_results: dict[str, Any]) -> None:
    """Both homematicip_local backends serve the same paramset description.

    The config panel is driven by ``get_paramset_description`` — sync+cached
    on the aiohomematic backend, REST-served by the daemon on the loom
    backend. For the probed switch channel both must expose the same VALUES
    parameter set, otherwise the device config UI differs per backend.
    """
    ccu = action_results.get("ccu:config")
    loom = action_results.get("loom:config")
    assert ccu, "ccu plane produced no config-surface trace"
    assert loom, "loom plane produced no config-surface trace"
    assert ccu == loom, f"config surface differs:\n  ccu:  {ccu}\n  loom: {loom}"


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
