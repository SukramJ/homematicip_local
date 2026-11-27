"""Test the relay of openccu-loom's device editor component."""

from __future__ import annotations

import hashlib
from typing import Any
import unicodedata
from unittest.mock import Mock

from openccu_loom_client import (
    EditorRelayResponse,
    LoomEditorCentralUnresolvedError,
    LoomEditorRouteRefusedError,
    LoomTransportError,
    route_allowed,
)
from openccu_loom_client.wire.rest import EditorComponentManifest, EditorRoute
import pytest
from pytest_homeassistant.common import MockConfigEntry, MockUser

from custom_components.homematicip_local import _any_entry_has_panel_enabled
from custom_components.homematicip_local.const import (
    BACKEND_CCU,
    BACKEND_LOOM,
    CONF_ADVANCED_CONFIG,
    CONF_BACKEND,
    CONF_DISABLE_CONFIG_PANEL,
    DOMAIN,
)
from custom_components.homematicip_local.control_unit import signal_central_state_changed
from custom_components.homematicip_local.loom_editor import (
    LOOM_EDITORS_KEY,
    async_register_loom_editor_view,
    module_url,
)
from custom_components.homematicip_local.websocket_api import async_register_websocket_commands
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

ENTRY_ID = "loom-entry"
SERIAL = "3014F711A0001F5A49A0B3C2"
CENTRAL = "ccu-living"
MODULE = b"customElements.define('loom-device-editor', class extends HTMLElement {});\n"
MODULE_HASH = hashlib.sha256(MODULE).hexdigest()

# A slice of the daemon's editor route list (openccu-loom
# assets/ui/src/component/editor-routes.json): method + prefix.
ROUTES = (
    ("GET", "/devices"),
    ("PUT", "/devices/*/paramsets"),
    ("POST", "/devices/*/paramsets"),
    ("POST", "/sessions/edit"),
)


class FakeEditor:
    """
    Stand in for ``control.central.editor`` of openccu-loom-client.

    The route check is the client's own ``route_allowed``; only the daemon
    I/O is faked, and every call that would have reached the daemon is
    recorded.
    """

    def __init__(self) -> None:
        """Answer with a manifest, one central and a 200 by default."""
        self.manifest_value: EditorComponentManifest | None = EditorComponentManifest(
            module_url=f"/app/component/editor-{MODULE_HASH}.js",
            hash=MODULE_HASH,
            routes=[EditorRoute(method=method, prefix=prefix) for method, prefix in ROUTES],
        )
        self.centrals: dict[str, str] = {SERIAL: CENTRAL}
        self.response = EditorRelayResponse(status=200, body={"ok": True})
        self.relay_error: Exception | None = None
        self.module_bytes = MODULE
        self.manifest_reads = 0
        self.resolve_calls: list[str] = []
        self.sent: list[dict[str, Any]] = []
        self.module_fetches: list[str] = []

    async def fetch_module(self, *, module_url: str) -> bytes:
        """Return the module bytes."""
        self.module_fetches.append(module_url)
        return self.module_bytes

    async def manifest(self) -> EditorComponentManifest | None:
        """Return the manifest, ``None`` standing for the daemon's 404."""
        self.manifest_reads += 1
        return self.manifest_value

    async def relay(
        self,
        *,
        routes: list[EditorRoute],
        method: str,
        path: str,
        query: dict[str, str] | None,
        headers: dict[str, str] | None,
        body: Any,
        central: str,
        on_behalf_of: str | None,
    ) -> EditorRelayResponse:
        """Refuse an uncovered call like the client does, else record it."""
        if not central:
            raise LoomEditorCentralUnresolvedError("no central")
        if not route_allowed(routes=routes, method=method, path=path):
            raise LoomEditorRouteRefusedError(f"{method} {path}")
        if self.relay_error is not None:
            raise self.relay_error
        self.sent.append(
            {
                "method": method,
                "path": path,
                "query": {**(query or {}), "central": central},
                "headers": dict(headers or {}),
                "body": body,
                "on_behalf_of": on_behalf_of,
            }
        )
        return self.response

    async def resolve_central(self, *, serial: str) -> str:
        """Name the central of ``serial``."""
        self.resolve_calls.append(serial)
        if not serial or serial not in self.centrals:
            raise LoomEditorCentralUnresolvedError(f"no central for {serial!r}")
        return self.centrals[serial]


def _add_entry(
    hass: HomeAssistant, *, backend: str = BACKEND_LOOM, serial: str | None = SERIAL, entry_id: str = ENTRY_ID
) -> tuple[MockConfigEntry, FakeEditor]:
    """Add a loaded-looking entry whose control unit carries a fake editor."""
    editor = FakeEditor()
    control = Mock()
    control.central.editor = editor
    entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id=entry_id,
        unique_id=serial,
        data={CONF_BACKEND: backend, "instance_name": "loom", CONF_ADVANCED_CONFIG: {}},
    )
    entry.add_to_hass(hass)
    entry.runtime_data = control
    return entry, editor


@pytest.fixture
def register_commands(hass: HomeAssistant) -> None:
    """Register the integration's WebSocket commands."""
    async_register_websocket_commands(hass)


async def _call(client: Any, **msg: Any) -> dict[str, Any]:
    """Send one command and return its response."""
    _call.counter += 1  # type: ignore[attr-defined]
    await client.send_json({"id": _call.counter, **msg})  # type: ignore[attr-defined]
    response: dict[str, Any] = await client.receive_json()
    return response


_call.counter = 0  # type: ignore[attr-defined]


async def _request(client: Any, **fields: Any) -> dict[str, Any]:
    """Send ``loom/editor/request`` for the test entry."""
    msg: dict[str, Any] = {
        "type": "homematicip_local/loom/editor/request",
        "entry_id": ENTRY_ID,
        "method": "GET",
        "path": "/devices/A:1",
    }
    msg.update(fields)
    return await _call(client, **msg)


async def _manifest(client: Any, *, entry_id: str = ENTRY_ID) -> dict[str, Any]:
    """Send ``loom/editor/manifest``."""
    return await _call(client, type="homematicip_local/loom/editor/manifest", entry_id=entry_id)


@pytest.mark.usefixtures("register_commands")
class TestEditorCommands:
    """The two admin-only WebSocket commands."""

    async def test_a_call_naming_another_central_is_refused(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _, editor = _add_entry(hass)
        client = await hass_ws_client(hass)
        response = await _request(client, query={"central": "ccu-other"})
        assert response["error"]["code"] == "central_mismatch"
        assert editor.sent == []

    async def test_ccu_entry_is_refused(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _, editor = _add_entry(hass, backend=BACKEND_CCU)
        client = await hass_ws_client(hass)
        for response in (await _manifest(client), await _request(client)):
            assert response["success"] is False
            assert response["error"]["code"] == "not_supported"
        assert editor.manifest_reads == 0
        assert LOOM_EDITORS_KEY not in hass.data

    async def test_central_is_the_one_resolved_by_serial(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _, editor = _add_entry(hass)
        editor.centrals = {"OTHER": "ccu-other", SERIAL: CENTRAL}
        client = await hass_ws_client(hass)
        await _request(client)
        await _request(client, query={"central": CENTRAL})
        assert [sent["query"]["central"] for sent in editor.sent] == [CENTRAL, CENTRAL]
        # Resolved once and cached.
        assert editor.resolve_calls == [SERIAL]

    async def test_daemon_unreachable_is_unavailable(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _, editor = _add_entry(hass)
        editor.relay_error = LoomTransportError("connection refused")
        client = await hass_ws_client(hass)
        response = await _request(client)
        assert response["error"]["code"] == "unavailable"

    async def test_entry_without_serial_is_refused(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _, editor = _add_entry(hass, serial=None)
        client = await hass_ws_client(hass)
        response = await _request(client)
        assert response["error"]["code"] == "central_unresolved"
        assert editor.resolve_calls == [""]
        assert editor.sent == []

    async def test_manifest_404_means_unavailable(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _, editor = _add_entry(hass)
        editor.manifest_value = None
        client = await hass_ws_client(hass)
        response = await _manifest(client)
        assert response["result"] == {"available": False, "module_url": None}
        # The relay refuses as well, and nothing reaches the daemon.
        response = await _request(client)
        assert response["error"]["code"] == "editor_unavailable"
        assert editor.sent == []

    async def test_manifest_available(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _add_entry(hass)
        client = await hass_ws_client(hass)
        response = await _manifest(client)
        assert response["success"] is True
        assert response["result"] == {
            "available": True,
            "module_url": f"/homematicip_local/loom-editor/{ENTRY_ID}/{MODULE_HASH}.js",
        }

    async def test_non_admin_is_refused(
        self, hass: HomeAssistant, hass_ws_client: Any, hass_read_only_access_token: str
    ) -> None:
        _, editor = _add_entry(hass)
        client = await hass_ws_client(hass, access_token=hass_read_only_access_token)
        for response in (await _manifest(client), await _request(client)):
            assert response["success"] is False
            assert response["error"]["code"] == "unauthorized"
        assert editor.manifest_reads == 0
        assert editor.sent == []

    @pytest.mark.parametrize("name", ["A" * 200, "Al\x07ex\u200b\n"])
    async def test_on_behalf_of_is_valid_for_any_name(
        self, hass: HomeAssistant, hass_ws_client: Any, hass_admin_user: MockUser, name: str
    ) -> None:
        hass_admin_user.name = name
        _, editor = _add_entry(hass)
        client = await hass_ws_client(hass)
        await _request(client)
        label = editor.sent[0]["on_behalf_of"]
        # The daemon's rule (openccu-loom middleware/audit_actor.go, invalidOnBehalfOf).
        assert label
        assert len(label.encode()) <= 128
        assert all(unicodedata.category(ch) not in {"Cc", "Cf"} for ch in label)
        assert label.endswith(f"(ha:{hass_admin_user.id})")

    async def test_on_behalf_of_names_the_ha_user(
        self, hass: HomeAssistant, hass_ws_client: Any, hass_admin_user: MockUser
    ) -> None:
        _, editor = _add_entry(hass)
        client = await hass_ws_client(hass)
        await _request(client, headers={"X-On-Behalf-Of": "Mallory"})
        (sent,) = editor.sent
        assert sent["on_behalf_of"] == f"{hass_admin_user.name} (ha:{hass_admin_user.id})"

    async def test_reconnect_signal_drops_manifest_and_central(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _, editor = _add_entry(hass)
        client = await hass_ws_client(hass)
        await _manifest(client)
        await _request(client)
        assert (editor.manifest_reads, len(editor.resolve_calls)) == (1, 1)
        await _manifest(client)
        await _request(client)
        assert (editor.manifest_reads, len(editor.resolve_calls)) == (1, 1)

        # A daemon update while disconnected: new module, central renamed.
        new_module = b"// updated\n"
        new_hash = hashlib.sha256(new_module).hexdigest()
        editor.manifest_value = EditorComponentManifest(
            module_url=f"/app/component/editor-{new_hash}.js",
            hash=new_hash,
            routes=editor.manifest_value.routes,  # type: ignore[union-attr]
        )
        editor.centrals[SERIAL] = "ccu-renamed"
        async_dispatcher_send(hass, signal_central_state_changed(entry_id=ENTRY_ID))
        await hass.async_block_till_done()

        response = await _manifest(client)
        assert response["result"]["module_url"].endswith(f"/{new_hash}.js")
        await _request(client)
        assert editor.sent[-1]["query"]["central"] == "ccu-renamed"
        assert (editor.manifest_reads, len(editor.resolve_calls)) == (2, 2)

    @pytest.mark.parametrize(
        ("status", "body"),
        [
            (200, {"address": "A:1"}),
            (204, None),
            (409, {"type": "about:blank", "title": "Conflict", "status": 409}),
            (423, {"title": "Locked", "status": 423}),
        ],
    )
    async def test_request_passes_every_status_through(
        self, hass: HomeAssistant, hass_ws_client: Any, status: int, body: Any
    ) -> None:
        _, editor = _add_entry(hass)
        editor.response = EditorRelayResponse(status=status, body=body)
        client = await hass_ws_client(hass)
        response = await _request(
            client,
            method="PUT",
            path="/devices/A:1/paramsets/MASTER",
            query={"validate": "1"},
            headers={"X-Edit-Token": "tok"},
            body={"LEVEL": 1},
        )
        assert response["success"] is True
        assert response["result"] == {"status": status, "body": body}
        (sent,) = editor.sent
        assert sent["method"] == "PUT"
        assert sent["path"] == "/devices/A:1/paramsets/MASTER"
        assert sent["query"] == {"validate": "1", "central": CENTRAL}
        assert sent["headers"] == {"X-Edit-Token": "tok"}
        assert sent["body"] == {"LEVEL": 1}

    async def test_serial_no_central_reports_is_refused(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        _, editor = _add_entry(hass)
        editor.centrals = {"OTHER": "ccu-other"}
        client = await hass_ws_client(hass)
        response = await _request(client)
        assert response["error"]["code"] == "central_unresolved"
        assert editor.sent == []
        # Not cached: once the central reports the serial, the call goes through.
        editor.centrals[SERIAL] = CENTRAL
        response = await _request(client)
        assert response["success"] is True
        assert editor.sent[0]["query"]["central"] == CENTRAL

    @pytest.mark.parametrize(
        ("method", "path"),
        [
            ("POST", "/devices/A:1/release"),
            ("DELETE", "/devices/A:1"),
            ("GET", "/audit"),
            ("PUT", "/devices//paramsets/MASTER"),
        ],
    )
    async def test_uncovered_route_is_refused_and_nothing_sent(
        self, hass: HomeAssistant, hass_ws_client: Any, method: str, path: str
    ) -> None:
        _, editor = _add_entry(hass)
        client = await hass_ws_client(hass)
        response = await _request(client, method=method, path=path)
        assert response["success"] is False
        assert response["error"]["code"] == "route_refused"
        assert editor.sent == []

    async def test_unknown_entry_is_not_found(self, hass: HomeAssistant, hass_ws_client: Any) -> None:
        client = await hass_ws_client(hass)
        response = await _manifest(client, entry_id="nope")
        assert response["error"]["code"] == "not_found"


@pytest.mark.usefixtures("register_commands")
class TestEditorModuleView:
    """The module served from Home Assistant's origin."""

    async def test_bytes_not_matching_the_hash_are_502(
        self, hass: HomeAssistant, hass_ws_client: Any, hass_client_no_auth: Any
    ) -> None:
        _, editor = _add_entry(hass)
        editor.module_bytes = b"// tampered\n"
        ws = await hass_ws_client(hass)
        async_register_loom_editor_view(hass=hass)
        url = (await _manifest(ws))["result"]["module_url"]
        http = await hass_client_no_auth()
        resp = await http.get(url)
        assert resp.status == 502

    async def test_ccu_entry_is_404(self, hass: HomeAssistant, hass_ws_client: Any, hass_client_no_auth: Any) -> None:
        _, editor = _add_entry(hass, backend=BACKEND_CCU)
        ws = await hass_ws_client(hass)
        async_register_loom_editor_view(hass=hass)
        await _manifest(ws)
        http = await hass_client_no_auth()
        resp = await http.get(module_url(entry_id=ENTRY_ID, module_hash=MODULE_HASH))
        assert resp.status == 404
        assert editor.manifest_reads == 0
        assert editor.module_fetches == []

    async def test_hash_of_a_previous_connection_is_404(
        self, hass: HomeAssistant, hass_ws_client: Any, hass_client_no_auth: Any
    ) -> None:
        _, editor = _add_entry(hass)
        ws = await hass_ws_client(hass)
        async_register_loom_editor_view(hass=hass)
        url = (await _manifest(ws))["result"]["module_url"]
        async_dispatcher_send(hass, signal_central_state_changed(entry_id=ENTRY_ID))
        await hass.async_block_till_done()
        http = await hass_client_no_auth()
        resp = await http.get(url)
        assert resp.status == 404
        assert editor.manifest_reads == 1

    async def test_serves_the_hash_a_manifest_call_returned(
        self, hass: HomeAssistant, hass_ws_client: Any, hass_client_no_auth: Any
    ) -> None:
        _, editor = _add_entry(hass)
        ws = await hass_ws_client(hass)
        async_register_loom_editor_view(hass=hass)
        url = (await _manifest(ws))["result"]["module_url"]
        http = await hass_client_no_auth()
        for _ in range(2):
            resp = await http.get(url)
            assert resp.status == 200
            assert await resp.read() == MODULE
            assert resp.headers["Content-Type"].startswith("application/javascript")
            assert resp.headers["Cache-Control"] == "public, max-age=31536000, immutable"
        # Fetched once, cached afterwards.
        assert editor.module_fetches == [f"/app/component/editor-{MODULE_HASH}.js"]

    async def test_unauthenticated_request_before_a_manifest_call_is_404(
        self, hass: HomeAssistant, hass_ws_client: Any, hass_client_no_auth: Any
    ) -> None:
        _, editor = _add_entry(hass)
        await hass_ws_client(hass)
        async_register_loom_editor_view(hass=hass)
        http = await hass_client_no_auth()
        resp = await http.get(module_url(entry_id=ENTRY_ID, module_hash=MODULE_HASH))
        assert resp.status == 404
        assert editor.manifest_reads == 0
        assert editor.module_fetches == []

    async def test_wrong_hash_is_404(self, hass: HomeAssistant, hass_ws_client: Any, hass_client_no_auth: Any) -> None:
        _, editor = _add_entry(hass)
        ws = await hass_ws_client(hass)
        async_register_loom_editor_view(hass=hass)
        await _manifest(ws)
        http = await hass_client_no_auth()
        resp = await http.get(module_url(entry_id=ENTRY_ID, module_hash="0" * 64))
        assert resp.status == 404
        assert editor.module_fetches == []


class TestPanelEnablement:
    """A loom entry enables the panel now that it hosts the daemon's editor."""

    async def test_loaded_loom_entry_enables_the_panel(self, hass: HomeAssistant) -> None:
        _add_entry(hass)
        assert _any_entry_has_panel_enabled(hass=hass) is True

    async def test_loom_entry_with_panel_disabled_does_not(self, hass: HomeAssistant) -> None:
        entry, _ = _add_entry(hass)
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, CONF_ADVANCED_CONFIG: {CONF_DISABLE_CONFIG_PANEL: True}}
        )
        assert _any_entry_has_panel_enabled(hass=hass) is False
