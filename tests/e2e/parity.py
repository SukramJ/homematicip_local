"""Scrape + normalize + diff helpers for the three-way parity e2e test.

A *snapshot* of one plane is the set of Home Assistant entities (and their
backing devices) that one config entry produced, reduced to a
backend-agnostic shape so the three planes can be compared key-for-key.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
import re
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

# Card-relevant state attributes worth comparing across planes, by domain.
# Anything volatile (timestamps, signal strength) is deliberately excluded.
_COMPARE_ATTRS: dict[str, tuple[str, ...]] = {
    "climate": ("hvac_modes", "min_temp", "max_temp", "target_temp_step", "supported_features"),
    "cover": ("device_class", "supported_features"),
    "light": ("supported_color_modes", "supported_features"),
    "switch": ("device_class",),
    "binary_sensor": ("device_class",),
    "sensor": ("device_class", "state_class", "unit_of_measurement"),
    "number": ("min", "max", "step", "mode"),
    "select": ("options",),
}


@dataclass(slots=True)
class EntitySnap:
    """One entity reduced to its parity-relevant fields."""

    domain: str
    unique_key: str
    friendly_name: str | None
    state: str | None
    attrs: dict[str, Any]
    raw_unique_id: str
    entity_id: str


@dataclass(slots=True)
class Snapshot:
    """A whole plane's parity-relevant output, keyed by normalized id."""

    plane: str
    entities: dict[str, EntitySnap] = field(default_factory=dict)
    device_keys: set[str] = field(default_factory=set)


def normalize_unique_id(raw: str, *, strip_tokens: tuple[str, ...]) -> str:
    """Reduce a backend-specific unique_id to a comparable key.

    Backend prefixes, the per-run config-entry/instance/central/serial tokens
    and the mqtt instance hash are removed so the same logical entity collapses
    to one key across all three planes.
    """
    out = raw.lower()
    out = re.sub(r"^homematicip_local_", "", out)
    out = re.sub(r"^(openccu-)?loom_", "", out)
    # mqtt discovery prefixes a short hex instance hash.
    out = re.sub(r"^[0-9a-f]{8,12}_", "", out)
    for token in sorted((t.lower() for t in strip_tokens if t), key=len, reverse=True):
        out = out.replace(token + "_", "").replace("_" + token, "").replace(token, "")
    return re.sub(r"_{2,}", "_", out).strip("_")


def scrape(
    hass: HomeAssistant, *, plane: str, config_entry_id: str, platform: str, strip_tokens: tuple[str, ...]
) -> Snapshot:
    """Build a Snapshot from one config entry's registered entities."""
    ent_reg = er.async_get(hass)
    dev_reg = dr.async_get(hass)
    snap = Snapshot(plane=plane)
    for entry in ent_reg.entities.values():
        if entry.config_entry_id != config_entry_id or entry.platform != platform:
            continue
        domain = entry.entity_id.split(".", 1)[0]
        key = f"{domain}:{normalize_unique_id(entry.unique_id, strip_tokens=strip_tokens)}"
        state_obj = hass.states.get(entry.entity_id)
        attrs: dict[str, Any] = {}
        friendly = None
        state_val = None
        if state_obj is not None:
            state_val = state_obj.state
            friendly = state_obj.attributes.get("friendly_name")
            for attr in _COMPARE_ATTRS.get(domain, ()):  # only stable card attrs
                if attr in state_obj.attributes:
                    attrs[attr] = state_obj.attributes[attr]
        snap.entities[key] = EntitySnap(
            domain=domain,
            unique_key=key,
            friendly_name=friendly,
            state=state_val,
            attrs=attrs,
            raw_unique_id=entry.unique_id,
            entity_id=entry.entity_id,
        )
        if entry.device_id and (device := dev_reg.async_get(entry.device_id)) is not None:
            snap.device_keys.add(device.name or device.id)
    return snap


async def wait_until_settled(
    hass: HomeAssistant,
    *,
    predicate: Callable[[], Any],
    timeout: float = 120.0,
    stable_for: float = 3.0,
    poll: float = 0.5,
) -> None:
    """Wait until predicate() has held a stable value for stable_for seconds.

    predicate() should return a comparable snapshot of progress (e.g. an entity
    count). The wait resolves once it stops changing for stable_for seconds, or
    raises TimeoutError after timeout.
    """
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    last_value: Any = object()
    stable_since = loop.time()
    while loop.time() < deadline:
        await hass.async_block_till_done()
        value = predicate()
        now = loop.time()
        if value != last_value:
            last_value = value
            stable_since = now
        elif value and (now - stable_since) >= stable_for:
            return
        await asyncio.sleep(poll)
    raise TimeoutError(f"plane did not settle within {timeout}s (last value: {last_value})")


def diff_snapshots(snaps: Mapping[str, Snapshot]) -> dict[str, Any]:
    """Return a structured diff across the given plane snapshots.

    The first plane (by insertion order) is the reference; every other plane is
    compared against it for missing/extra keys, name and attribute drift.
    """
    planes = list(snaps)
    ref_name = planes[0]
    ref = snaps[ref_name]
    report: dict[str, Any] = {"reference": ref_name, "planes": {p: len(snaps[p].entities) for p in planes}}
    for other_name in planes[1:]:
        other = snaps[other_name]
        ref_keys = set(ref.entities)
        other_keys = set(other.entities)
        name_drift = []
        attr_drift = []
        for key in ref_keys & other_keys:
            r, o = ref.entities[key], other.entities[key]
            if (r.friendly_name or "") != (o.friendly_name or ""):
                name_drift.append((key, r.friendly_name, o.friendly_name))
            if r.attrs != o.attrs:
                attr_drift.append((key, r.attrs, o.attrs))
        report[other_name] = {
            "missing_vs_ref": sorted(ref_keys - other_keys),
            "extra_vs_ref": sorted(other_keys - ref_keys),
            "name_drift": name_drift,
            "attr_drift": attr_drift,
        }
    return report
