"""Permission helpers for granular non-admin access control."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, Final

from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import Unauthorized

SCOPE_SCHEDULE_EDIT: Final = "schedule_edit"
SCOPE_DEVICE_CONFIG: Final = "device_config"
SCOPE_DEVICE_LINKS: Final = "device_links"
SCOPE_SYSTEM_ADMIN: Final = "system_admin"

ALL_SCOPES: Final[list[str]] = [
    SCOPE_SCHEDULE_EDIT,
    SCOPE_DEVICE_CONFIG,
    SCOPE_DEVICE_LINKS,
    SCOPE_SYSTEM_ADMIN,
]

CONF_NON_ADMIN_PERMISSIONS: Final = "non_admin_permissions"


def _check_user_scope(
    *,
    hass: HomeAssistant,
    user_is_admin: bool,
    user_is_owner: bool,
    entry_id: str,
    required_scope: str,
) -> None:
    """Check whether a user holds the required scope. Raise Unauthorized if not."""
    if user_is_admin or user_is_owner:
        return

    if required_scope == SCOPE_SYSTEM_ADMIN:
        raise Unauthorized

    entry = hass.config_entries.async_get_entry(entry_id)
    if entry is None:
        raise Unauthorized

    allowed_scopes: list[str] = entry.options.get(CONF_NON_ADMIN_PERMISSIONS, [])
    if required_scope not in allowed_scopes:
        raise Unauthorized


async def check_service_permission(
    *,
    hass: HomeAssistant,
    entry_id: str,
    user_id: str | None,
    required_scope: str,
) -> None:
    """Check permission for a service call context."""
    # System call (automation, script) — always permitted
    if user_id is None:
        return

    user = await hass.auth.async_get_user(user_id)
    if user is None:
        raise Unauthorized

    _check_user_scope(
        hass=hass,
        user_is_admin=user.is_admin,
        user_is_owner=user.is_owner,
        entry_id=entry_id,
        required_scope=required_scope,
    )


def check_ws_permission(
    *,
    hass: HomeAssistant,
    entry_id: str,
    connection: ActiveConnection,
    required_scope: str,
) -> None:
    """Check permission for a WebSocket connection."""
    _check_user_scope(
        hass=hass,
        user_is_admin=connection.user.is_admin,
        user_is_owner=connection.user.is_owner,
        entry_id=entry_id,
        required_scope=required_scope,
    )


def require_scope(
    scope: str,
) -> Callable[
    [Callable[..., Any]],
    Callable[..., Any],
]:
    """
    Decorate a WebSocket handler to require a permission scope.

    This decorator must be synchronous (like HA's @require_admin) because
    the websocket dispatcher calls handlers synchronously. The actual async
    handler is invoked by @async_response further down the decorator chain.
    """

    def decorator(
        func: Callable[..., Any],
    ) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(
            hass: HomeAssistant,
            connection: ActiveConnection,
            msg: dict[str, Any],
        ) -> None:
            """Check scope before calling the handler."""
            try:
                check_ws_permission(
                    hass=hass,
                    entry_id=msg["entry_id"],
                    connection=connection,
                    required_scope=scope,
                )
            except Unauthorized:
                connection.send_error(msg["id"], "unauthorized", "Insufficient permissions")
                return
            func(hass, connection, msg)

        return wrapper

    return decorator
