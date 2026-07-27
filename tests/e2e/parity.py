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
    has_state: bool = True
    model: str | None = None


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
    # calculated/combined DP markers are present on some planes only.
    out = re.sub(r"^(calculated|combined)_", "", out)
    for token in sorted((t.lower() for t in strip_tokens if t), key=len, reverse=True):
        out = out.replace(token + "_", "").replace("_" + token, "").replace(token, "")
    # Unify separators: dashes only differ cosmetically between backends.
    out = out.replace("-", "_")
    return re.sub(r"_{2,}", "_", out).strip("_")


def _canonical_key(raw: str, *, domain: str, strip_tokens: tuple[str, ...]) -> str:
    """Return the cross-plane comparison key for one entity.

    On top of unique-id normalization this drops the ``hub_`` prefix (some
    planes omit it), a trailing ``_<domain>`` suffix (mqtt discovery appends the
    component name) and collapses the event / schedule / week-profile unique-id
    schemes — which differ between the aiohomematic and mqtt-discovery layers
    for the same logical entity — to one shape.
    """
    norm = normalize_unique_id(raw, strip_tokens=strip_tokens)
    norm = re.sub(r"^hub_", "", norm)
    if norm.endswith(f"_{domain}"):
        norm = norm[: -(len(domain) + 1)]
    # event groups: ccu 'event_group_keypress_<addr>_<ch>' vs mqtt '<addr>_<ch>'.
    norm = re.sub(r"^event_group_(?:keypress|impulse|press|device_error)_", "", norm)
    # schedule switch: 'schedule_channel_switch_<addr>_schedule_channel_lock_<a>_<b>'
    # (aiohomematic) vs '<addr>_<ch>_schedule_<a>_<b>' (mqtt) -> 'sched_<addr>_<a>_<b>'.
    if (m := re.match(r"^schedule_channel_switch_([0-9a-z]+)_schedule_channel_lock_(\d+_\d+)$", norm)) or (
        m := re.match(r"^([0-9a-z]+)_\d+_schedule_(\d+_\d+)$", norm)
    ):
        norm = f"sched_{m.group(1)}_{m.group(2)}"
    # week-profile sensor: 'week_profile_<addr>_week_profile' (aiohomematic) vs
    # '<addr>_<ch>_schedule' (mqtt) -> 'wp_<addr>'.
    elif (m := re.match(r"^week_profile_([0-9a-z]+)_week_profile$", norm)) or (
        m := re.match(r"^([0-9a-z]+)_\d+_schedule$", norm)
    ):
        norm = f"wp_{m.group(1)}"
    return f"{domain}:{norm}"


def _canonical_name(name: str | None, *, strip_tokens: tuple[str, ...]) -> str:
    """Return a name with per-plane instance/central tokens removed."""
    if not name:
        return ""
    out = name
    for token in sorted((t for t in strip_tokens if t), key=len, reverse=True):
        out = re.sub(re.escape(token), "", out, flags=re.IGNORECASE)
    # A removed central/instance token can orphan its joining separator
    # (e.g. "Connectivity ccu-e2e-HmIP-RF" -> "Connectivity -HmIP-RF"); drop a
    # separator left dangling after a space without touching real ones (HmIP-RF).
    out = re.sub(r"(?<=\s)[-_]+(?=\S)", "", out)
    return re.sub(r"\s{2,}", " ", out).strip(" -_")


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
        key = _canonical_key(entry.unique_id, domain=domain, strip_tokens=strip_tokens)
        # original_name is the stable, integration-assigned entity name; the live
        # friendly_name depends on a state existing (timing) and prepends the
        # device name, so it drifts on cosmetics the registry name does not.
        name = _canonical_name(entry.original_name, strip_tokens=strip_tokens)
        state_obj = hass.states.get(entry.entity_id)
        attrs: dict[str, Any] = {}
        state_val = None
        if state_obj is not None:
            state_val = state_obj.state
            for attr in _COMPARE_ATTRS.get(domain, ()):  # only stable card attrs
                if attr in state_obj.attributes:
                    attrs[attr] = state_obj.attributes[attr]
        model: str | None = None
        if entry.device_id and (device := dev_reg.async_get(entry.device_id)) is not None:
            snap.device_keys.add(device.name or device.id)
            model = device.model
        snap.entities[key] = EntitySnap(
            domain=domain,
            unique_key=key,
            friendly_name=name,
            state=state_val,
            attrs=attrs,
            raw_unique_id=entry.unique_id,
            entity_id=entry.entity_id,
            has_state=state_obj is not None,
            model=model,
        )
    return snap


async def wait_until_settled(
    hass: HomeAssistant,
    *,
    predicate: Callable[[], Any],
    timeout: float = 120.0,
    stable_for: float = 3.0,
    poll: float = 0.5,
    floor: Callable[[], bool] | None = None,
) -> None:
    """Wait until predicate() has held a stable value for stable_for seconds.

    predicate() should return a comparable snapshot of progress (e.g. an entity
    count). The wait resolves once it stops changing for stable_for seconds, or
    raises TimeoutError after timeout.

    When ``floor`` is given, stability only counts once it returns True. This
    bridges arbitrarily long silent gaps in the load (aiohomematic's up-front
    paramset-description fetch produces no new entities for minutes on a large
    device set) that would otherwise satisfy any fixed stability window while
    the plane is still far from loaded.
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
        elif value and (floor is None or floor()) and (now - stable_since) >= stable_for:
            return
        await asyncio.sleep(poll)
    raise TimeoutError(f"plane did not settle within {timeout}s (last value: {last_value})")


def entity_model(snaps: Mapping[str, Snapshot], *, key: str) -> str | None:
    """Return the device model behind a canonical key, from the first plane that knows it."""
    for snap in snaps.values():
        if (entity := snap.entities.get(key)) is not None and entity.model:
            return entity.model
    return None


def per_model_entity_set_report(
    snaps: Mapping[str, Snapshot],
    *,
    is_by_design_residual: Callable[[str, str], bool],
) -> tuple[set[str], set[str]]:
    """Return (clean, dirty) device models by cross-plane entity-set parity.

    The first plane is the reference. A model is *dirty* when any of its
    entities is missing/extra on another plane (by-design residuals aside);
    every other model seen on the reference plane is *clean*. Entities without
    a device model (hub entities) do not participate — they are always
    enforced directly by the parity test.
    """
    planes = list(snaps)
    reference = snaps[planes[0]]
    dirty: set[str] = set()
    for other in planes[1:]:
        report = diff_snapshots({planes[0]: reference, other: snaps[other]})[other]
        for field_name in ("missing_vs_ref", "extra_vs_ref"):
            for key in report[field_name]:
                if is_by_design_residual(other, key):
                    continue
                if (model := entity_model(snaps, key=key)) is not None:
                    dirty.add(model)
    all_models = {entity.model for entity in reference.entities.values() if entity.model}
    return all_models - dirty, dirty


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
            # Card attributes are only comparable when both sides actually have a
            # state object; a secondary channel that has not reported yet carries
            # no attributes, which is a timing artifact, not a real drift.
            if r.has_state and o.has_state and r.attrs != o.attrs:
                attr_drift.append((key, r.attrs, o.attrs))
        report[other_name] = {
            "missing_vs_ref": sorted(ref_keys - other_keys),
            "extra_vs_ref": sorted(other_keys - ref_keys),
            "name_drift": name_drift,
            "attr_drift": attr_drift,
        }
    return report
