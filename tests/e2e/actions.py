"""Behavioral (action) parity probes for the three-way e2e suite.

Entity-set parity proves the planes *materialize* the same entities; the
probes here prove they *behave* the same: identical Home Assistant service
calls against the same godevccu must converge to identical states on every
plane, a CCU-side push must reach every plane's entity, and (for the two
homematicip_local backends) the config surface must serve the same paramset
description.

Every probe restores the state it found so the backend is unchanged for the
next plane, and every probe records its outcome as a plain string — the
parity assertion is simply "all planes produced the same trace".
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from inspect import isawaitable
import json
import re
from typing import Any
import urllib.request

from homeassistant.core import HomeAssistant

from .parity import Snapshot

PROBE_TIMEOUT = 30.0
_POLL = 0.25


@dataclass(slots=True, frozen=True)
class ActionResult:
    """One probe step reduced to a cross-plane comparable outcome."""

    key: str
    step: str
    outcome: str


async def _wait_for(hass: HomeAssistant, *, predicate: Callable[[], bool], timeout: float = PROBE_TIMEOUT) -> bool:
    """Poll until predicate() holds; return whether it did within timeout."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while loop.time() < deadline:
        await hass.async_block_till_done()
        if predicate():
            return True
        await asyncio.sleep(_POLL)
    return False


def _pick(snap: Snapshot, *, domain: str) -> tuple[str, str] | None:
    """Return (canonical key, entity_id) of the first device-backed entity of a domain.

    Deterministic across planes: entities are sorted by canonical key, and only
    channel-addressed HmIP entities participate — hub program switches,
    schedule switches and week-profile sensors have no channel address and are
    excluded — so every plane picks the same logical entity.
    """
    for key in sorted(snap.entities):
        entity = snap.entities[key]
        if (
            entity.domain == domain
            and entity.model
            and entity.model.startswith("HmIP-")
            and _channel_address(key) is not None
        ):
            return key, entity.entity_id
    return None


def _channel_address(key: str) -> str | None:
    """Reconstruct the CCU channel address from a canonical entity key.

    godevccu addresses are uppercase ``VCU<digits>``; the canonical key folds
    ``VCU2128127:4`` to ``vcu2128127_4``.
    """
    if match := re.fullmatch(r"[a-z_]+:(vcu\d+)_(\d+)", key):
        return f"{match.group(1).upper()}:{match.group(2)}"
    return None


def _state(hass: HomeAssistant, entity_id: str) -> str | None:
    """Return the current state string of an entity."""
    state = hass.states.get(entity_id)
    return state.state if state else None


def _attr(hass: HomeAssistant, entity_id: str, name: str) -> Any:
    """Return one state attribute of an entity."""
    state = hass.states.get(entity_id)
    return state.attributes.get(name) if state else None


async def _call(hass: HomeAssistant, domain: str, service: str, data: dict[str, Any]) -> None:
    """Invoke a Home Assistant service and flush the event loop."""
    await hass.services.async_call(domain, service, data, blocking=True)
    await hass.async_block_till_done()


async def _probe_switch(hass: HomeAssistant, *, key: str, entity_id: str, out: list[ActionResult]) -> None:
    """Toggle a switch there and back via HA services."""
    initial = _state(hass, entity_id)
    target, restore = ("off", "on") if initial == "on" else ("on", "off")
    for step, want in (("toggle", target), ("restore", restore)):
        await _call(hass, "switch", f"turn_{want}", {"entity_id": entity_id})
        ok = await _wait_for(hass, predicate=lambda want=want: _state(hass, entity_id) == want)
        out.append(ActionResult(key=key, step=f"switch.{step}", outcome=want if ok else "timeout"))


async def _probe_cover(hass: HomeAssistant, *, key: str, entity_id: str, out: list[ActionResult]) -> None:
    """Drive a cover to 50 % and back via HA services."""
    initial = _attr(hass, entity_id, "current_position")
    restore = int(initial) if initial is not None else 0
    target = 50 if restore != 50 else 75
    for step, want in (("set_position", target), ("restore", restore)):
        await _call(hass, "cover", "set_cover_position", {"entity_id": entity_id, "position": want})
        ok = await _wait_for(hass, predicate=lambda want=want: _attr(hass, entity_id, "current_position") == want)
        out.append(ActionResult(key=key, step=f"cover.{step}", outcome=str(want) if ok else "timeout"))


async def _probe_climate(
    hass: HomeAssistant, *, key: str, entity_id: str, control_port: int, out: list[ActionResult]
) -> None:
    """Set a target temperature via the HA service, then restore it CCU-side.

    The restore goes through the godevccu control API because the initial
    HmIP target (4.5 °C) lies below HA's accepted range — the service would
    reject it — and the CCU-side write doubles as a second push-parity check.
    """
    initial = _attr(hass, entity_id, "temperature")
    min_temp = float(_attr(hass, entity_id, "min_temp") or 5.0)
    max_temp = float(_attr(hass, entity_id, "max_temp") or 30.0)
    step_size = float(_attr(hass, entity_id, "target_temp_step") or 0.5)
    # Mid-range is valid on every plane — the advertised min_temp may lie
    # below HA's accepted range (HmIP thermostats report the off-temperature
    # 3.5 °C as minimum while validation starts at 5.0 °C).
    target = round(((min_temp + max_temp) / 2) / step_size) * step_size
    if initial is not None and float(initial) == target:
        target += step_size
    await _call(hass, "climate", "set_temperature", {"entity_id": entity_id, "temperature": target})
    ok = await _wait_for(hass, predicate=lambda: _attr(hass, entity_id, "temperature") == target)
    out.append(ActionResult(key=key, step="climate.set_temperature", outcome=str(target) if ok else "timeout"))
    restore = float(initial) if initial is not None else target
    address = _channel_address(key)
    if address is None:
        out.append(ActionResult(key=key, step="climate.restore", outcome="no-address"))
        return
    await asyncio.to_thread(
        _post_set_value, control_port=control_port, address=address, value_key="SET_POINT_TEMPERATURE", value=restore
    )
    ok = await _wait_for(hass, predicate=lambda: _attr(hass, entity_id, "temperature") == restore)
    out.append(ActionResult(key=key, step="climate.restore", outcome=str(restore) if ok else "timeout"))


def _post_set_value(*, control_port: int, address: str, value_key: str, value: object) -> None:
    """POST a value change to the godevccu control API (blocking, loopback)."""
    body = json.dumps({"address": address, "value_key": value_key, "value": value}).encode()
    request = urllib.request.Request(
        f"http://127.0.0.1:{control_port}/set_value",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5.0):  # noqa: S310 - loopback only
        pass


async def _probe_ccu_push(
    hass: HomeAssistant, *, key: str, entity_id: str, control_port: int, out: list[ActionResult]
) -> None:
    """Drive a CCU-side STATE change and assert the plane sees the push."""
    address = _channel_address(key)
    if address is None:
        out.append(ActionResult(key=key, step="push.state", outcome="no-address"))
        return
    initial = _state(hass, entity_id)
    flipped, restored = ("off", "on") if initial == "on" else ("on", "off")
    for step, want in (("state", flipped), ("restore", restored)):
        await asyncio.to_thread(
            _post_set_value, control_port=control_port, address=address, value_key="STATE", value=want == "on"
        )
        ok = await _wait_for(hass, predicate=lambda want=want: _state(hass, entity_id) == want)
        out.append(ActionResult(key=key, step=f"push.{step}", outcome=want if ok else "timeout"))


async def probe_config_surface(*, control: Any, key: str) -> list[ActionResult]:
    """Fetch the VALUES paramset description for the probed switch channel.

    Runs only on the two homematicip_local planes (the mqtt plane has no
    config surface). The outcome is the sorted parameter-name list — both
    backends must serve the same description for the same channel.
    """
    from aiohomematic.const import ParamsetKey

    address = _channel_address(key)
    if address is None:
        return [ActionResult(key=key, step="config.paramset", outcome="no-address")]
    # get_device takes the DEVICE address; the loom backend resolves strictly
    # (a channel address yields None) while aiohomematic tolerates both.
    device = control.central.device_coordinator.get_device(address=address.split(":")[0])
    if device is None:
        return [ActionResult(key=key, step="config.paramset", outcome="no-device")]
    descriptions = control.central.configuration.get_paramset_description(
        interface_id=device.interface_id,
        channel_address=address,
        paramset_key=ParamsetKey.VALUES,
    )
    if isawaitable(descriptions):
        descriptions = await descriptions
    parameters = ",".join(sorted(descriptions)) if descriptions else "empty"
    return [ActionResult(key=key, step="config.paramset", outcome=parameters)]


async def run_action_probes(hass: HomeAssistant, *, snap: Snapshot, control_port: int) -> list[ActionResult]:
    """Run every service + push probe against one plane and return its trace."""
    out: list[ActionResult] = []
    if switch := _pick(snap, domain="switch"):
        await _probe_switch(hass, key=switch[0], entity_id=switch[1], out=out)
        await _probe_ccu_push(hass, key=switch[0], entity_id=switch[1], control_port=control_port, out=out)
    if cover := _pick(snap, domain="cover"):
        await _probe_cover(hass, key=cover[0], entity_id=cover[1], out=out)
    if climate := _pick(snap, domain="climate"):
        await _probe_climate(hass, key=climate[0], entity_id=climate[1], control_port=control_port, out=out)
    return out
