"""
Relay openccu-loom's device editor component to the configuration panel.

On the loom backend the panel hosts the daemon's own device editor, the
``<loom-device-editor>`` web component (openccu-loom ADR 0089). The component
makes no network call of its own: the panel hands it a transport, and that
transport is this module. Every REST call the editor makes travels as the
``homematicip_local/loom/editor/request`` WebSocket command and is forwarded
with the entry's stored credential, so the browser never reaches the daemon and
no daemon address or token reaches the browser. The module itself is served
from Home Assistant's origin by :class:`LoomEditorModuleView`.

The HTTP shape of the relay — route check, header filtering, the daemon's
``?central=`` binding, the ``X-On-Behalf-Of`` label — belongs to
``openccu_loom_client`` (``control.central.editor``). This module maps the
integration's concepts onto it: which config entry, which daemon central (by
the CCU serial), which Home Assistant user.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import hashlib
import logging
import re
from typing import TYPE_CHECKING, Any, Final, cast

from aiohttp import web
import probatio as vol
from pydantic import ValidationError

from homeassistant.components.http import KEY_HASS
from homeassistant.components.websocket_api import ERR_NOT_FOUND, ERR_NOT_SUPPORTED
from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.components.websocket_api.decorators import async_response, require_admin, websocket_command
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.http import HomeAssistantView
from homeassistant.util.hass_dict import HassKey

from .const import BACKEND_LOOM, CONF_BACKEND
from .control_unit import signal_central_state_changed

if TYPE_CHECKING:
    from openccu_loom_client.compat.aiohomematic.central.adapter import LoomCentralAdapter
    from openccu_loom_client.operations import EditorOperations, EditorRelayResponse
    from openccu_loom_client.wire.rest import EditorComponentManifest

    from .control_unit import ControlUnit

_LOGGER: Final = logging.getLogger(__name__)

LOOM_EDITORS_KEY: HassKey[dict[str, LoomEditorRelay]] = HassKey("homematicip_local_loom_editors")
LOOM_EDITOR_VIEW_REGISTERED_KEY: HassKey[bool] = HassKey("homematicip_local_loom_editor_view_registered")

# Where Home Assistant serves the module: one URL per entry and module hash, so
# a daemon update yields a new URL and an immutable cache entry never goes stale.
_MODULE_URL: Final = "/homematicip_local/loom-editor/{entry_id}/{module_hash}.js"

# The manifest's ``hash`` is the hex SHA-256 of the module's bytes
# (``EditorComponentManifest.hash``). It becomes part of a URL, so anything
# else is refused rather than embedded.
_SHA256_HEX_RE: Final = re.compile(r"[0-9a-fA-F]{64}")

# The query parameter the daemon binds a device call to its central with
# (``openccu_loom_client.transport.http.DEVICE_CENTRAL_QUERY``).
_CENTRAL_QUERY: Final = "central"

# WebSocket error codes of the relay, besides Home Assistant's own.
ERR_ROUTE_REFUSED: Final = "route_refused"
ERR_CENTRAL_UNRESOLVED: Final = "central_unresolved"
ERR_CENTRAL_MISMATCH: Final = "central_mismatch"
ERR_EDITOR_UNAVAILABLE: Final = "editor_unavailable"
ERR_UNAVAILABLE: Final = "unavailable"
ERR_DAEMON_ERROR: Final = "daemon_error"

_CACHE_HEADERS: Final = {"Cache-Control": "public, max-age=31536000, immutable"}


class LoomEditorModuleIntegrityError(Exception):
    """The module the daemon sent does not match the manifest's hash."""


class LoomEditorUnavailableError(Exception):
    """The daemon offers no editor component this integration can host."""


class LoomEditorCentralMismatchError(Exception):
    """An editor call named a daemon central other than the entry's own."""


class LoomEditorRelay:
    """
    Hold one loom entry's editor state: manifest, daemon central and module.

    Everything is read lazily, on the first authenticated WebSocket call, and
    dropped whenever the entry's central changes state — a reconnect to the
    daemon may reach an updated daemon with another module hash, or a daemon
    that now serves the CCU under another central name.
    """

    __slots__ = (
        "_central",
        "_control",
        "_generation",
        "_manifest",
        "_manifest_read",
        "_module",
        "_module_lock",
        "_serial",
        "_unsubscribe",
    )

    def __init__(self, *, hass: HomeAssistant, entry_id: str, control: ControlUnit, serial: str | None) -> None:
        """Bind the relay to one entry's control unit and follow its central's state."""
        self._control: Final = control
        self._serial: Final = serial or ""
        self._manifest: EditorComponentManifest | None = None
        self._manifest_read = False
        self._central: str | None = None
        self._module: tuple[str, bytes] | None = None
        self._module_lock: Final = asyncio.Lock()
        # Bumped by every invalidation, so a read that was in flight across a
        # reconnect does not store what the previous daemon answered.
        self._generation = 0
        self._unsubscribe: Callable[[], None] = async_dispatcher_connect(
            hass, signal_central_state_changed(entry_id=entry_id), self.invalidate
        )

    @property
    def _editor(self) -> EditorOperations:
        """Return the client's editor operations of this entry's central."""
        return cast("LoomCentralAdapter", self._control.central).editor

    @property
    def control(self) -> ControlUnit:
        """Return the control unit this relay belongs to."""
        return self._control

    @callback
    def close(self) -> None:
        """Stop following the central's state."""
        self._unsubscribe()

    async def get_central(self) -> str:
        """Return the daemon central of the entry's CCU, resolved by serial once per connection."""
        if self._central is not None:
            return self._central
        generation = self._generation
        central = await self._editor.resolve_central(serial=self._serial)
        if generation == self._generation:
            self._central = central
        return central

    async def get_manifest(self) -> EditorComponentManifest | None:
        """
        Return the daemon's editor manifest, read once per connection.

        ``None`` when the daemon has no editor component this integration can
        host: a 404 (a build without the bundle, or a daemon older than the
        editor) or a manifest of an older shape (route strings instead of
        method + prefix, before openccu-loom REST API 19.0.0).
        """
        if self._manifest_read:
            return self._manifest
        generation = self._generation
        manifest = await self._editor.manifest()
        if manifest is not None and not _SHA256_HEX_RE.fullmatch(manifest.hash):
            _LOGGER.warning(
                "The openccu-loom daemon names an editor module hash that is not SHA-256: %r", manifest.hash
            )
            manifest = None
        if generation == self._generation:
            self._manifest = manifest
            self._manifest_read = True
        return manifest

    async def get_module(self, *, module_hash: str) -> bytes | None:
        """
        Return the module's bytes when ``module_hash`` is the current manifest's hash.

        Never reads the manifest: only a hash an authenticated manifest call
        has already put into the cache is served, so an unauthenticated
        request cannot make the integration talk to the daemon on its own.
        Raises :class:`LoomEditorModuleIntegrityError` when the bytes do not
        hash to ``module_hash``.
        """
        if (manifest := self._manifest) is None or manifest.hash != module_hash:
            return None
        async with self._module_lock:
            if self._module is not None and self._module[0] == module_hash:
                return self._module[1]
            data = await self._editor.fetch_module(module_url=manifest.module_url)
            if hashlib.sha256(data).hexdigest() != module_hash.lower():
                raise LoomEditorModuleIntegrityError(
                    f"editor module {manifest.module_url} does not hash to the manifest's {module_hash}"
                )
            self._module = (module_hash, data)
            return data

    @callback
    def invalidate(self) -> None:
        """Forget the manifest and the central; both are read again on the next call."""
        self._generation += 1
        self._manifest = None
        self._manifest_read = False
        self._central = None

    async def relay(
        self,
        *,
        method: str,
        path: str,
        query: dict[str, str],
        headers: dict[str, str],
        body: Any,
        on_behalf_of: str | None,
    ) -> EditorRelayResponse:
        """
        Forward one call of the editor to the entry's daemon central.

        Raises :class:`LoomEditorUnavailableError` without a usable manifest,
        :class:`LoomEditorCentralMismatchError` when ``query`` names another
        central, and passes the client's refusals and transport errors on.
        """
        if (manifest := await self.get_manifest()) is None:
            raise LoomEditorUnavailableError("the openccu-loom daemon offers no editor component")
        central = await self.get_central()
        if (named := query.get(_CENTRAL_QUERY)) is not None and named != central:
            raise LoomEditorCentralMismatchError(f"the editor call names central {named!r}, the entry is {central!r}")
        return await self._editor.relay(
            routes=manifest.routes,
            method=method,
            path=path,
            query=query,
            headers=headers,
            body=body,
            central=central,
            on_behalf_of=on_behalf_of,
        )


class LoomEditorModuleView(HomeAssistantView):
    """
    Serve the editor module of a loom entry from Home Assistant's origin.

    No authentication: a browser's module import carries no auth header, and
    the daemon serves the same module without a session. What is served is
    bounded by the cache — only the module whose hash an authenticated
    manifest call returned, verified against that hash.
    """

    url = _MODULE_URL
    name = "homematicip_local:loom_editor_module"
    requires_auth = False

    async def get(self, request: web.Request, entry_id: str, module_hash: str) -> web.Response:
        """Return the module, or 404 for anything not known from a manifest."""
        hass = request.app[KEY_HASS]
        if (relay := hass.data.get(LOOM_EDITORS_KEY, {}).get(entry_id)) is None:
            raise web.HTTPNotFound
        entry = hass.config_entries.async_get_entry(entry_id)
        if entry is None or not _is_loom(entry=entry) or getattr(entry, "runtime_data", None) is not relay.control:
            raise web.HTTPNotFound
        try:
            data = await relay.get_module(module_hash=module_hash)
        except LoomEditorModuleIntegrityError as err:
            _LOGGER.error("Refusing to serve the openccu-loom editor module: %s", err)
            raise web.HTTPBadGateway from err
        except _base_loom_error() as err:
            _LOGGER.warning("Fetching the openccu-loom editor module failed: %s", err)
            raise web.HTTPBadGateway from err
        if data is None:
            raise web.HTTPNotFound
        return web.Response(body=data, content_type="application/javascript", headers=_CACHE_HEADERS)


@callback
def async_register_loom_editor_view(*, hass: HomeAssistant) -> None:
    """Register the module view once per Home Assistant process; aiohttp cannot remove a route."""
    if hass.data.get(LOOM_EDITOR_VIEW_REGISTERED_KEY):
        return
    hass.http.register_view(LoomEditorModuleView)
    hass.data[LOOM_EDITOR_VIEW_REGISTERED_KEY] = True


def module_url(*, entry_id: str, module_hash: str) -> str:
    """Return the Home Assistant URL of an entry's editor module."""
    return _MODULE_URL.format(entry_id=entry_id, module_hash=module_hash)


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/loom/editor/manifest",
        vol.Required("entry_id"): str,
    }
)
@require_admin
@async_response
async def ws_loom_editor_manifest(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return whether the entry's daemon offers the editor and where its module is served."""
    if (relay := _get_relay(hass=hass, connection=connection, msg=msg)) is None:
        return
    try:
        manifest = await relay.get_manifest()
    except ValidationError as err:
        _LOGGER.info("The openccu-loom daemon's editor manifest is of an older shape: %s", err)
        manifest = None
    except _transport_error() as err:
        connection.send_error(msg["id"], ERR_UNAVAILABLE, str(err))
        return
    except _base_loom_error() as err:
        connection.send_error(msg["id"], ERR_DAEMON_ERROR, str(err))
        return
    if manifest is None:
        connection.send_result(msg["id"], {"available": False, "module_url": None})
        return
    connection.send_result(
        msg["id"],
        {"available": True, "module_url": module_url(entry_id=msg["entry_id"], module_hash=manifest.hash)},
    )


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/loom/editor/request",
        vol.Required("entry_id"): str,
        vol.Required("method"): str,
        vol.Required("path"): str,
        vol.Optional("query", default={}): {str: str},
        vol.Optional("headers", default={}): {str: str},
        # Decoded JSON of an arbitrary editor route, forwarded undecided.
        vol.Optional("body"): object,
    }
)
@require_admin
@async_response
async def ws_loom_editor_request(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Forward one REST call of the editor component and return the daemon's status and body."""
    if (relay := _get_relay(hass=hass, connection=connection, msg=msg)) is None:
        return
    from openccu_loom_client import (  # noqa: PLC0415  # pylint: disable=import-outside-toplevel
        LoomEditorCentralUnresolvedError,
        LoomEditorRouteRefusedError,
        LoomTransportError,
        on_behalf_of_label,
    )
    from openccu_loom_client.exceptions import BaseLoomException  # noqa: PLC0415  # pylint: disable=import-outside-toplevel

    user = connection.user
    try:
        response = await relay.relay(
            method=msg["method"],
            path=msg["path"],
            query=msg["query"],
            headers=msg["headers"],
            body=msg.get("body"),
            on_behalf_of=on_behalf_of_label(name=user.name or "", user_id=f"ha:{user.id}"),
        )
    except ValidationError as err:
        connection.send_error(msg["id"], ERR_EDITOR_UNAVAILABLE, f"unsupported editor manifest: {err}")
    except LoomEditorUnavailableError as err:
        connection.send_error(msg["id"], ERR_EDITOR_UNAVAILABLE, str(err))
    except LoomEditorCentralMismatchError as err:
        connection.send_error(msg["id"], ERR_CENTRAL_MISMATCH, str(err))
    except LoomEditorRouteRefusedError as err:
        connection.send_error(msg["id"], ERR_ROUTE_REFUSED, str(err))
    except LoomEditorCentralUnresolvedError as err:
        connection.send_error(msg["id"], ERR_CENTRAL_UNRESOLVED, str(err))
    except LoomTransportError as err:
        connection.send_error(msg["id"], ERR_UNAVAILABLE, str(err))
    except BaseLoomException as err:
        connection.send_error(msg["id"], ERR_DAEMON_ERROR, str(err))
    else:
        connection.send_result(msg["id"], {"status": response.status, "body": response.body})


def _base_loom_error() -> type[Exception]:
    """Return the loom client's base error; imported lazily like every loom-client reference."""
    from openccu_loom_client.exceptions import BaseLoomException  # noqa: PLC0415  # pylint: disable=import-outside-toplevel

    return cast("type[Exception]", BaseLoomException)


def _get_relay(*, hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any]) -> LoomEditorRelay | None:
    """Return the entry's editor relay, or send the error that says why there is none."""
    entry = hass.config_entries.async_get_entry(msg["entry_id"])
    if entry is None or not getattr(entry, "runtime_data", None):
        connection.send_error(msg["id"], ERR_NOT_FOUND, "Config entry not found")
        return None
    if not _is_loom(entry=entry):
        connection.send_error(msg["id"], ERR_NOT_SUPPORTED, "The editor relay serves openccu-loom entries only")
        return None
    control: ControlUnit = entry.runtime_data
    relays = hass.data.setdefault(LOOM_EDITORS_KEY, {})
    if (relay := relays.get(entry.entry_id)) is not None and relay.control is control:
        return relay
    if relay is not None:
        relay.close()
    relay = LoomEditorRelay(hass=hass, entry_id=entry.entry_id, control=control, serial=entry.unique_id)
    relays[entry.entry_id] = relay

    @callback
    def _drop() -> None:
        """Release the relay together with the entry's control unit."""
        if relays.get(entry.entry_id) is relay:
            del relays[entry.entry_id]
        relay.close()

    entry.async_on_unload(_drop)
    return relay


def _is_loom(*, entry: ConfigEntry) -> bool:
    """Return True for an entry on the openccu-loom backend."""
    return bool(entry.data.get(CONF_BACKEND) == BACKEND_LOOM)


def _transport_error() -> type[Exception]:
    """Return the loom client's transport error; imported lazily like every loom-client reference."""
    from openccu_loom_client import LoomTransportError  # noqa: PLC0415  # pylint: disable=import-outside-toplevel

    return cast("type[Exception]", LoomTransportError)
