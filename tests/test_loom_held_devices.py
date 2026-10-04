"""Tests for devices the openccu-loom daemon holds back until they are named.

The daemon holds every newly paired device: it is not built and shows up only
on ``GET /inbox`` flagged ``pending_creation``. openccu-loom-client announces
such an address as a ``DeviceLifecycleEvent`` of type ``DELAYED`` and answers
``add_new_devices_manually`` with accept-under-the-name, then release. These
tests drive the integration's side of that exchange end to end: a real loom
compat central on Home Assistant's mocked HTTP client session (the daemon's
REST surface is the mocker), the production ``ControlUnit.start_central``
subscription, Home Assistant's issue registry, and the real repairs flow
manager running this integration's fix flow.

Only the central's network-heavy bring-up (store walk, event stream, hub
reconcile loop) is stubbed, the same set the client's own held-device tests
stub; the inbox read, the ``DELAYED`` announcement, the decline timer and the
accept/release requests are the production code paths.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any
from unittest.mock import patch

from openccu_loom_client.compat.aiohomematic.central import adapter as loom_adapter_module
import openccu_loom_client.compat.aiohomematic.central.held_devices as held_devices_module
from openccu_loom_client.wire import DAEMON_API_VERSION
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker, AiohttpClientMockResponse
from yarl import URL

from custom_components.homematicip_local.const import (
    BACKEND_LOOM,
    CONF_BACKEND,
    CONF_INSTANCE_NAME,
    CONF_LOOM_PORT,
    CONF_LOOM_TOKEN,
    CONF_TLS,
    DOMAIN,
)
from custom_components.homematicip_local.control_unit import ControlConfig, ControlUnit
from homeassistant.components.repairs import repairs_flow_manager
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import device_registry as dr, issue_registry as ir
from homeassistant.setup import async_setup_component

_CU = "custom_components.homematicip_local.control_unit"
_HOST = "loom.test"
_PORT = 8080
_BASE = f"http://{_HOST}:{_PORT}/api/v1"
_CENTRAL = "home"
# The daemon's wire interface id: `<central>-<interface>` (the client's
# `wire_interface_id`), which is what the DELAYED event carries.
_INTERFACE_ID = f"{_CENTRAL}-HmIP-RF"
_ADDRESS = "0001D3C99C3C93"
_ISSUE_ID = f"devices_delayed|{_INTERFACE_ID}|{_ADDRESS}"
_NAME = "Stehlampe Wohnzimmer"

# Shapes taken from the client's own fakes (tests/unit/test_compat_central_adapter.py
# `_INFO` and `_LITE_ENTRY`): the always-on capability set and a ready central.
_INFO = {
    "version": "1.2.3",
    "api_version": DAEMON_API_VERSION,
    "commit": "deadbeef",
    "build_date": "2026-05-24T10:00:00Z",
    "addon_build": False,
    "started_at": "2026-05-24T10:01:00Z",
    "uptime": "PT60S",
    "capabilities": ["rest.v1", "ws.broadcasts.v1", "errors.problem_details.v1"],
    "schema_digest": "sha256:test",
    "config_ui_url": "",
}
_CCU_ENTRY = {
    "name": _CENTRAL,
    "host": "ccu.local",
    "available": True,
    "is_ha_app": False,
    "configured_interfaces": [],
    "serial": "0000DAEMON1234",
    "readiness": {"phase": "ready", "ready": True, "interfaces_loaded": 1, "interfaces_total": 1},
    "system_type": "openccu-lite",
    "model": "openccu-lite",
    "features": {},
}


def _inbox_entry(**flags: bool) -> dict[str, Any]:
    return {"central": _CENTRAL, "address": _ADDRESS, "model": "HmIP-PS", "interface": "HmIP-RF", **flags}


_HELD = _inbox_entry(pending_creation=True)


@dataclass
class _FakeDaemon:
    """The daemon's REST surface as seen through Home Assistant's mocked client session."""

    mock: AiohttpClientMocker
    inbox: list[dict[str, Any]] = field(default_factory=list)

    @property
    def inbox_reads(self) -> int:
        return sum(1 for m, u, _, _ in self.mock.mock_calls if m.upper() == "GET" and u.path.endswith("/inbox"))

    @property
    def writes(self) -> list[tuple[str, str, Any]]:
        """Every non-GET request the daemon received, in order: (method, path, JSON body)."""
        return [(m.upper(), str(u.path), d) for m, u, d, _ in self.mock.mock_calls if m.upper() != "GET"]

    def install(self, *, release_status: HTTPStatus = HTTPStatus.NO_CONTENT) -> None:
        self.mock.get(f"{_BASE}/info", json=_INFO)
        self.mock.get(f"{_BASE}/system/ccu", json=[_CCU_ENTRY])
        self.mock.get(f"{_BASE}/interfaces", json=[])
        # Read at request time, so a test can change what the daemon holds.
        self.mock.get(f"{_BASE}/inbox", side_effect=self._inbox)
        self.mock.post(f"{_BASE}/devices/{_ADDRESS}/accept", status=HTTPStatus.ACCEPTED)
        if release_status >= HTTPStatus.BAD_REQUEST:
            self.mock.post(
                f"{_BASE}/devices/{_ADDRESS}/release",
                status=release_status,
                headers={"Content-Type": "application/problem+json"},
                json={"type": "https://openccu-loom.dev/errors/internal", "title": "boom", "status": release_status},
            )
        else:
            self.mock.post(f"{_BASE}/devices/{_ADDRESS}/release", status=release_status)

    async def _inbox(self, method: str, url: URL, data: Any) -> AiohttpClientMockResponse:
        return AiohttpClientMockResponse(method, url, json=list(self.inbox))


class _Clock:
    """Stands in for the control unit's ``time`` module so the auto-confirm window can close."""

    def __init__(self, now: float) -> None:
        self.now = now

    def time(self) -> float:
        return self.now


@pytest.fixture
def daemon(aioclient_mock: AiohttpClientMocker) -> _FakeDaemon:
    return _FakeDaemon(mock=aioclient_mock)


async def _start(
    hass: HomeAssistant,
    daemon: _FakeDaemon,
    monkeypatch: pytest.MonkeyPatch,
    *,
    auto_confirm_until: float | None = None,
) -> ControlUnit:
    """Build the loom control unit through ControlConfig and run its production start_central."""
    data = {
        CONF_BACKEND: BACKEND_LOOM,
        CONF_INSTANCE_NAME: _CENTRAL,
        CONF_HOST: _HOST,
        CONF_LOOM_PORT: _PORT,
        CONF_TLS: False,
        CONF_LOOM_TOKEN: "tok-123456",
    }
    entry = MockConfigEntry(domain=DOMAIN, data=data)
    entry.add_to_hass(hass)
    control_unit = await ControlUnit.async_create(
        control_config=ControlConfig(
            hass=hass, entry_id=entry.entry_id, data=data, auto_confirm_until=auto_confirm_until
        )
    )
    central: Any = control_unit.central
    assert isinstance(central, loom_adapter_module.LoomCentralAdapter), "the loom backend must build the compat central"

    async def _noop(*_args: Any, **_kwargs: Any) -> None:
        return None

    for target, attr in (
        (central.client_coordinator, "refresh"),
        (central._client, "wait_until_ready"),
        (central._client, "start_events"),
        (central, "_bootstrap_model"),
        (central.query_facade, "prefetch_un_ignore_candidates"),
        (central, "_emit_data_points_created"),
        (central, "_hub_reconcile_loop"),
    ):
        monkeypatch.setattr(target, attr, _noop)
    await control_unit.start_central()
    await hass.async_block_till_done()
    # start_central logs and swallows a failed start; a stopped central would
    # make every "nothing happened" assertion below vacuous.
    assert central.available, "the loom central must have started"
    return control_unit


@pytest.fixture
async def stop_units() -> AsyncIterator[list[ControlUnit]]:
    units: list[ControlUnit] = []
    yield units
    for unit in units:
        await unit.stop_central()


def _issue(hass: HomeAssistant) -> ir.IssueEntry | None:
    return ir.async_get(hass).async_get_issue(DOMAIN, _ISSUE_ID)


def _device_created(hass: HomeAssistant) -> bool:
    return any(_ADDRESS in identifier for device in dr.async_get(hass).devices for _, identifier in device.identifiers)


async def _wait_until(hass: HomeAssistant, predicate: Callable[[], bool], *, rounds: int = 200) -> bool:
    """Let the event loop run (the client's decline timer is a plain asyncio task) until ``predicate`` holds."""
    for _ in range(rounds):
        await hass.async_block_till_done()
        if predicate():
            return True
        await asyncio.sleep(0.01)
    return predicate()


async def _fix_repair(hass: HomeAssistant, *, name: str) -> dict[str, Any]:
    """Run the issue's fix flow the way the repairs UI does: init, then submit the name."""
    # The repairs platform is looked up only for a loaded integration, which a
    # running entry always is; this test builds its control unit without
    # setting the whole entry up.
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "repairs", {})
    manager = repairs_flow_manager(hass)
    assert manager is not None
    form = await manager.async_init(DOMAIN, context={"issue_id": _ISSUE_ID})
    assert form["type"] is FlowResultType.FORM
    assert form["step_id"] == "set_name"
    return dict(await manager.async_configure(form["flow_id"], {"device_name": name}))


class TestHeldDeviceOutsideAutoConfirmWindow:
    """After the auto-confirm window a held device becomes a fixable repair issue."""

    async def test_fixing_the_repair_accepts_under_the_name_then_releases(
        self, hass: HomeAssistant, daemon: _FakeDaemon, monkeypatch: pytest.MonkeyPatch, stop_units: list[ControlUnit]
    ) -> None:
        daemon.inbox = [_HELD]
        daemon.install()
        stop_units.append(await _start(hass, daemon, monkeypatch))
        assert _issue(hass) is not None

        result = await _fix_repair(hass, name=_NAME)

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert daemon.writes == [
            ("POST", f"/api/v1/devices/{_ADDRESS}/accept", {"name": _NAME}),
            ("POST", f"/api/v1/devices/{_ADDRESS}/release", None),
        ], "the entered name must travel in the accept body, followed by the release"
        assert _issue(hass) is None

    async def test_held_device_raises_repair_issue_and_creates_nothing(
        self, hass: HomeAssistant, daemon: _FakeDaemon, monkeypatch: pytest.MonkeyPatch, stop_units: list[ControlUnit]
    ) -> None:
        daemon.inbox = [_HELD]
        daemon.install()
        stop_units.append(await _start(hass, daemon, monkeypatch))

        issue = _issue(hass)
        assert issue is not None, "a held device must surface as a devices_delayed repair issue"
        assert issue.is_fixable
        assert issue.translation_placeholders == {
            "instance_name": _CENTRAL,
            "interface_id": _INTERFACE_ID,
            "address": _ADDRESS,
        }
        assert not _device_created(hass)
        assert daemon.writes == []

    async def test_release_failure_is_not_reported_as_success(
        self, hass: HomeAssistant, daemon: _FakeDaemon, monkeypatch: pytest.MonkeyPatch, stop_units: list[ControlUnit]
    ) -> None:
        daemon.inbox = [_HELD]
        daemon.install(release_status=HTTPStatus.INTERNAL_SERVER_ERROR)
        stop_units.append(await _start(hass, daemon, monkeypatch))

        result = await _fix_repair(hass, name=_NAME)

        assert [path for _, path, _ in daemon.writes] == [
            f"/api/v1/devices/{_ADDRESS}/accept",
            f"/api/v1/devices/{_ADDRESS}/release",
        ], "the failure under test is the release after a successful accept"
        assert result["type"] is FlowResultType.ABORT, "a failed release must not finish the fix flow as a success"
        assert result["reason"] == "device_add_failed"
        assert "stays awaiting release" in result["description_placeholders"]["error"]
        assert result["description_placeholders"]["address"] == _ADDRESS


class TestHeldDeviceInsideAutoConfirmWindow:
    """A held device is never accepted without a name, not even by the setup-time auto-confirm."""

    async def test_auto_confirm_sends_nothing_to_the_daemon(
        self, hass: HomeAssistant, daemon: _FakeDaemon, monkeypatch: pytest.MonkeyPatch, stop_units: list[ControlUnit]
    ) -> None:
        clock = _Clock(now=1_000.0)
        daemon.inbox = [_HELD]
        daemon.install()
        with patch(f"{_CU}.time", clock):
            unit = await _start(hass, daemon, monkeypatch, auto_confirm_until=1_600.0)
            stop_units.append(unit)

        # The integration's nameless auto-confirm reached the client — which
        # declined it and armed its re-sync — and nothing went to the daemon.
        assert unit.central._held_devices.resync_pending, "the nameless auto-confirm must have been declined"  # type: ignore[attr-defined]
        assert daemon.writes == []
        assert _issue(hass) is None
        assert not _device_created(hass)

    async def test_issue_follows_once_the_window_closes(
        self, hass: HomeAssistant, daemon: _FakeDaemon, monkeypatch: pytest.MonkeyPatch, stop_units: list[ControlUnit]
    ) -> None:
        monkeypatch.setattr(held_devices_module, "HELD_RESYNC_DELAY_SECONDS", 0.05)
        clock = _Clock(now=1_000.0)
        daemon.inbox = [_HELD]
        daemon.install()
        with patch(f"{_CU}.time", clock):
            unit = await _start(hass, daemon, monkeypatch, auto_confirm_until=1_600.0)
            stop_units.append(unit)
            assert _issue(hass) is None

            # The window closes; the client's delayed re-sync announces the
            # device again and this time it becomes a repair issue.
            clock.now = 1_700.0
            assert await _wait_until(hass, lambda: _issue(hass) is not None), (
                "the re-announced device must raise an issue"
            )

        assert daemon.writes == [], "no accept or release without a name"
        assert not _device_created(hass)


class TestNotHeldInboxEntries:
    """Negative control: inbox entries the daemon does not hold unbuilt raise nothing and send nothing."""

    @pytest.mark.parametrize(
        "entry",
        [_inbox_entry(), _inbox_entry(awaiting_release=True)],
        ids=["plain-inbox-entry", "awaiting-release"],
    )
    async def test_no_issue_and_no_request(
        self,
        hass: HomeAssistant,
        daemon: _FakeDaemon,
        monkeypatch: pytest.MonkeyPatch,
        stop_units: list[ControlUnit],
        entry: dict[str, Any],
    ) -> None:
        daemon.inbox = [entry]
        daemon.install()
        stop_units.append(await _start(hass, daemon, monkeypatch))

        assert daemon.inbox_reads >= 1, "the inbox must have been read for this to mean anything"
        assert _issue(hass) is None
        assert daemon.writes == []
