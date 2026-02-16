"""WebSocket API for device configuration panel."""

from __future__ import annotations

from datetime import UTC, datetime
import logging
from typing import TYPE_CHECKING, Any, Final

import voluptuous as vol

from aiohomematic.ccu_translations import get_channel_type_translation
from aiohomematic.const import LINKABLE_INTERFACES, ParamsetKey
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.parameter_tools import is_parameter_internal, is_parameter_visible, is_parameter_writable
from aiohomematic.support.address import get_device_address
from aiohomematic_config import ConfigSession, FormSchemaGenerator, export_configuration, import_configuration
from homeassistant.components.websocket_api import async_register_command
from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.components.websocket_api.decorators import async_response, require_admin, websocket_command
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.storage import Store
from homeassistant.util.hass_dict import HassKey

if TYPE_CHECKING:
    from .control_unit import ControlUnit

_LOGGER: Final = logging.getLogger(__name__)

SESSIONS_KEY: HassKey[dict[str, ConfigSession]] = HassKey("homematicip_local_config_sessions")
HISTORY_STORE_KEY: Final = "homematicip_local.config_changes"
HISTORY_MAX_ENTRIES: Final = 500

_MAINTENANCE_PARAMS: Final[frozenset[str]] = frozenset(
    {
        "UNREACH",
        "LOW_BAT",
        "RSSI_DEVICE",
        "RSSI_PEER",
        "DUTYCYCLE",
        "CONFIG_PENDING",
    }
)


def _get_session_key(*, entry_id: str, channel_address: str, paramset_key: str) -> str:
    """Return a unique key for a config session."""
    return f"{entry_id}_{channel_address}_{paramset_key}"


def _get_maintenance_data(*, device: Any) -> dict[str, Any]:
    """Return cached maintenance data from device channel 0."""
    result: dict[str, Any] = {}
    for dp in device.generic_data_points:
        if dp.channel.address.endswith(":0") and dp.parameter in _MAINTENANCE_PARAMS:
            result[dp.parameter.lower()] = dp.value
    return result


def _get_history_store(hass: HomeAssistant) -> Store[list[dict[str, Any]]]:
    """Return the change history store."""
    return Store[list[dict[str, Any]]](hass, 1, HISTORY_STORE_KEY)


async def _log_config_change(
    hass: HomeAssistant,
    *,
    entry_id: str,
    interface_id: str,
    channel_address: str,
    device_name: str,
    device_model: str,
    paramset_key: str,
    changes: dict[str, dict[str, Any]],
    source: str,
) -> None:
    """Log a configuration change to persistent storage."""
    store = _get_history_store(hass)
    data: list[dict[str, Any]] = await store.async_load() or []

    entry: dict[str, Any] = {
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "entry_id": entry_id,
        "interface_id": interface_id,
        "channel_address": channel_address,
        "device_name": device_name,
        "device_model": device_model,
        "paramset_key": paramset_key,
        "changes": changes,
        "source": source,
    }
    data.append(entry)

    # FIFO: keep only the most recent entries
    if len(data) > HISTORY_MAX_ENTRIES:
        data = data[-HISTORY_MAX_ENTRIES:]

    await store.async_save(data)


def _build_change_diff(
    *,
    old_values: dict[str, Any],
    new_values: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Build a change diff between old and new paramset values."""
    changes: dict[str, dict[str, Any]] = {}
    for param, new_val in new_values.items():
        old_val = old_values.get(param)
        if old_val != new_val:
            changes[param] = {"old": old_val, "new": new_val}
    return changes


def _get_device_info(
    *,
    control: ControlUnit,
    channel_address: str,
) -> tuple[str, str]:
    """Return device name and model for a channel address."""
    device_address = get_device_address(address=channel_address)
    device = control.central.device_coordinator.get_device(address=device_address)
    if device:
        return device.name or device.address, device.model
    return channel_address, ""


@callback
def async_register_websocket_commands(hass: HomeAssistant) -> None:
    """Register all WebSocket commands for the configuration panel."""
    async_register_command(hass, ws_list_devices)
    async_register_command(hass, ws_get_form_schema)
    async_register_command(hass, ws_get_paramset)
    async_register_command(hass, ws_put_paramset)
    async_register_command(hass, ws_session_open)
    async_register_command(hass, ws_session_set)
    async_register_command(hass, ws_session_undo)
    async_register_command(hass, ws_session_redo)
    async_register_command(hass, ws_session_save)
    async_register_command(hass, ws_session_discard)
    async_register_command(hass, ws_export_paramset)
    async_register_command(hass, ws_import_paramset)
    async_register_command(hass, ws_copy_paramset)
    async_register_command(hass, ws_get_change_history)
    async_register_command(hass, ws_clear_change_history)
    async_register_command(hass, ws_list_device_links)
    async_register_command(hass, ws_get_link_form_schema)
    async_register_command(hass, ws_get_link_paramset)
    async_register_command(hass, ws_put_link_paramset)
    async_register_command(hass, ws_add_link)
    async_register_command(hass, ws_remove_link)
    async_register_command(hass, ws_get_linkable_channels)


def _get_control_unit(hass: HomeAssistant, *, entry_id: str) -> ControlUnit | None:
    """Return the ControlUnit for a config entry."""
    if (entry := hass.config_entries.async_get_entry(entry_id)) is None:
        return None
    if not hasattr(entry, "runtime_data"):
        return None
    control_unit: ControlUnit = entry.runtime_data
    return control_unit


def _get_sessions(hass: HomeAssistant) -> dict[str, ConfigSession]:
    """Return the sessions dict, creating it if needed."""
    if SESSIONS_KEY not in hass.data:
        hass.data[SESSIONS_KEY] = {}
    return hass.data[SESSIONS_KEY]


# ---------------------------------------------------------------------------
# Existing commands
# ---------------------------------------------------------------------------


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/list_devices",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_list_devices(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return all devices with their configurable channels."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    central = control.central
    facade = central.configuration
    locale = hass.config.language
    devices: list[dict[str, Any]] = []

    for device in central.devices:
        try:
            channels = facade.get_configurable_channels(
                interface_id=device.interface_id,
                device_address=device.address,
            )
        except BaseHomematicException:
            continue
        if not channels:
            continue

        channel_list: list[dict[str, Any]] = []
        for ch in channels:
            # Only advertise MASTER if it has writable visible parameters
            effective_keys: list[str] = []
            for pk in ch.paramset_keys:
                if pk == ParamsetKey.MASTER:
                    descriptions = facade.get_paramset_description(
                        interface_id=device.interface_id,
                        channel_address=ch.address,
                        paramset_key=pk,
                    )
                    has_writable = any(
                        is_parameter_visible(parameter_data=pd)
                        and not is_parameter_internal(parameter_data=pd)
                        and is_parameter_writable(parameter_data=pd)
                        for pd in descriptions.values()
                    )
                    if has_writable:
                        effective_keys.append(pk.value)
                else:
                    effective_keys.append(pk.value)

            channel_list.append(
                {
                    "address": ch.address,
                    "channel_type": ch.channel_type,
                    "channel_type_label": get_channel_type_translation(
                        channel_type=ch.channel_type,
                        locale=locale,
                    )
                    or ch.channel_type,
                    "paramset_keys": effective_keys,
                }
            )

        devices.append(
            {
                "address": device.address,
                "interface": str(device.interface),
                "interface_id": device.interface_id,
                "model": device.model,
                "model_description": device.model_description or "",
                "name": device.name or device.address,
                "firmware": device.firmware,
                "channels": channel_list,
                "maintenance": _get_maintenance_data(device=device),
            }
        )

    connection.send_result(msg["id"], {"devices": devices})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_form_schema",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Optional("channel_type", default=""): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_get_form_schema(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return auto-generated form schema for a channel."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    facade = control.central.configuration
    paramset_key = ParamsetKey(msg["paramset_key"])

    descriptions = facade.get_paramset_description(
        interface_id=msg["interface_id"],
        channel_address=msg["channel_address"],
        paramset_key=paramset_key,
    )
    current_values = await facade.get_paramset(
        interface_id=msg["interface_id"],
        channel_address=msg["channel_address"],
        paramset_key=paramset_key,
    )

    device = control.central.device_coordinator.get_device(address=msg["channel_address"])

    generator = FormSchemaGenerator(locale=hass.config.language)
    schema = generator.generate(
        descriptions=descriptions,
        current_values=current_values,
        channel_address=msg["channel_address"],
        channel_type=msg.get("channel_type", ""),
        model=device.model if device else "",
        sub_model=device.sub_model if device else None,
    )

    connection.send_result(msg["id"], schema.model_dump())


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_paramset",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_get_paramset(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return current paramset values for a channel."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    facade = control.central.configuration
    paramset_key = ParamsetKey(msg["paramset_key"])

    try:
        values = await facade.get_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    connection.send_result(msg["id"], {"values": values})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/put_paramset",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Required("values"): dict,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
        vol.Optional("validate", default=True): bool,
    }
)
@async_response
async def ws_put_paramset(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Validate and write paramset values."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    facade = control.central.configuration
    paramset_key = ParamsetKey(msg["paramset_key"])

    # Read old values for change history
    try:
        old_values = await facade.get_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException:
        old_values = {}

    try:
        result = await facade.put_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
            values=msg["values"],
            validate=msg.get("validate", True),
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "write_failed", str(err))
        return

    # Log to change history on success
    if result.success:
        changes = _build_change_diff(old_values=old_values, new_values=msg["values"])
        if changes:
            device_name, device_model = _get_device_info(
                control=control,
                channel_address=msg["channel_address"],
            )
            await _log_config_change(
                hass,
                entry_id=msg["entry_id"],
                interface_id=msg["interface_id"],
                channel_address=msg["channel_address"],
                device_name=device_name,
                device_model=device_model,
                paramset_key=msg["paramset_key"],
                changes=changes,
                source="manual",
            )

    connection.send_result(
        msg["id"],
        {
            "success": result.success,
            "validated": result.validated,
            "validation_errors": dict(result.validation_errors),
        },
    )


# ---------------------------------------------------------------------------
# ConfigSession commands
# ---------------------------------------------------------------------------


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/session_open",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_session_open(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Open a new configuration editing session for a channel."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    facade = control.central.configuration
    paramset_key = ParamsetKey(msg["paramset_key"])

    descriptions = facade.get_paramset_description(
        interface_id=msg["interface_id"],
        channel_address=msg["channel_address"],
        paramset_key=paramset_key,
    )

    try:
        initial_values = await facade.get_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    session = ConfigSession(descriptions=descriptions, initial_values=initial_values)
    session_key = _get_session_key(
        entry_id=msg["entry_id"],
        channel_address=msg["channel_address"],
        paramset_key=msg["paramset_key"],
    )
    sessions = _get_sessions(hass)
    sessions[session_key] = session

    connection.send_result(msg["id"], {"success": True})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/session_set",
        vol.Required("entry_id"): str,
        vol.Required("channel_address"): str,
        vol.Required("parameter"): str,
        vol.Required("value"): vol.Any(str, int, float, bool),
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_session_set(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Set a parameter value in the active session."""
    session_key = _get_session_key(
        entry_id=msg["entry_id"],
        channel_address=msg["channel_address"],
        paramset_key=msg["paramset_key"],
    )
    sessions = _get_sessions(hass)
    session = sessions.get(session_key)
    if session is None:
        connection.send_error(msg["id"], "session_not_found", "No active session for this channel")
        return

    session.set(parameter=msg["parameter"], value=msg["value"])
    validation_errors = session.validate_changes()

    connection.send_result(
        msg["id"],
        {
            "is_dirty": session.is_dirty,
            "can_undo": session.can_undo,
            "can_redo": session.can_redo,
            "validation_errors": {param: vr.reason for param, vr in validation_errors.items()},
        },
    )


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/session_undo",
        vol.Required("entry_id"): str,
        vol.Required("channel_address"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_session_undo(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Undo the last change in the active session."""
    session_key = _get_session_key(
        entry_id=msg["entry_id"],
        channel_address=msg["channel_address"],
        paramset_key=msg["paramset_key"],
    )
    sessions = _get_sessions(hass)
    session = sessions.get(session_key)
    if session is None:
        connection.send_error(msg["id"], "session_not_found", "No active session for this channel")
        return

    performed = session.undo()

    connection.send_result(
        msg["id"],
        {
            "performed": performed,
            "is_dirty": session.is_dirty,
            "can_undo": session.can_undo,
            "can_redo": session.can_redo,
        },
    )


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/session_redo",
        vol.Required("entry_id"): str,
        vol.Required("channel_address"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_session_redo(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Redo the last undone change in the active session."""
    session_key = _get_session_key(
        entry_id=msg["entry_id"],
        channel_address=msg["channel_address"],
        paramset_key=msg["paramset_key"],
    )
    sessions = _get_sessions(hass)
    session = sessions.get(session_key)
    if session is None:
        connection.send_error(msg["id"], "session_not_found", "No active session for this channel")
        return

    performed = session.redo()

    connection.send_result(
        msg["id"],
        {
            "performed": performed,
            "is_dirty": session.is_dirty,
            "can_undo": session.can_undo,
            "can_redo": session.can_redo,
        },
    )


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/session_save",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_session_save(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Validate, write, and close the active session."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    session_key = _get_session_key(
        entry_id=msg["entry_id"],
        channel_address=msg["channel_address"],
        paramset_key=msg["paramset_key"],
    )
    sessions = _get_sessions(hass)
    session = sessions.get(session_key)
    if session is None:
        connection.send_error(msg["id"], "session_not_found", "No active session for this channel")
        return

    # Validate before writing
    validation_errors = session.validate_changes()
    if validation_errors:
        connection.send_result(
            msg["id"],
            {
                "success": False,
                "validated": True,
                "validation_errors": {param: vr.reason for param, vr in validation_errors.items()},
                "changes_applied": 0,
            },
        )
        return

    changes = session.get_changes()
    if not changes:
        # Nothing to write — remove session and return
        sessions.pop(session_key, None)
        connection.send_result(
            msg["id"],
            {
                "success": True,
                "validated": True,
                "validation_errors": {},
                "changes_applied": 0,
            },
        )
        return

    facade = control.central.configuration
    paramset_key = ParamsetKey(msg["paramset_key"])

    # Read old values for change history
    try:
        old_values = await facade.get_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException:
        old_values = {}

    try:
        result = await facade.put_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
            values=changes,
            validate=True,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "write_failed", str(err))
        return

    if result.success:
        # Log to change history and remove session
        change_diff = _build_change_diff(old_values=old_values, new_values=changes)
        if change_diff:
            device_name, device_model = _get_device_info(
                control=control,
                channel_address=msg["channel_address"],
            )
            await _log_config_change(
                hass,
                entry_id=msg["entry_id"],
                interface_id=msg["interface_id"],
                channel_address=msg["channel_address"],
                device_name=device_name,
                device_model=device_model,
                paramset_key=msg["paramset_key"],
                changes=change_diff,
                source="manual",
            )
        sessions.pop(session_key, None)

    connection.send_result(
        msg["id"],
        {
            "success": result.success,
            "validated": result.validated,
            "validation_errors": dict(result.validation_errors),
            "changes_applied": len(changes) if result.success else 0,
        },
    )


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/session_discard",
        vol.Required("entry_id"): str,
        vol.Required("channel_address"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_session_discard(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Discard the active session without saving."""
    session_key = _get_session_key(
        entry_id=msg["entry_id"],
        channel_address=msg["channel_address"],
        paramset_key=msg["paramset_key"],
    )
    sessions = _get_sessions(hass)
    sessions.pop(session_key, None)

    connection.send_result(msg["id"], {"success": True})


# ---------------------------------------------------------------------------
# Export / Import commands
# ---------------------------------------------------------------------------


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/export_paramset",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_export_paramset(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Export a channel paramset as JSON."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    facade = control.central.configuration
    paramset_key = ParamsetKey(msg["paramset_key"])

    try:
        values = await facade.get_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    device_address = get_device_address(address=msg["channel_address"])
    device = control.central.device_coordinator.get_device(address=device_address)
    model = device.model if device else ""
    # Resolve channel type from the device's channel object
    channel_type = ""
    if device:
        channel = device.get_channel(channel_address=msg["channel_address"])
        if channel:
            channel_type = channel.type_name

    json_data = export_configuration(
        device_address=device_address,
        model=model,
        channel_address=msg["channel_address"],
        channel_type=channel_type,
        paramset_key=msg["paramset_key"],
        values=values,
    )

    connection.send_result(msg["id"], {"json_data": json_data})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/import_paramset",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Required("json_data"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_import_paramset(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Import a paramset from JSON and write to a channel."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        imported = import_configuration(json_data=msg["json_data"])
    except (ValueError, TypeError) as err:
        connection.send_error(msg["id"], "invalid_data", str(err))
        return

    if imported.paramset_key != msg["paramset_key"]:
        connection.send_error(
            msg["id"],
            "paramset_key_mismatch",
            f"Imported paramset_key '{imported.paramset_key}' does not match target '{msg['paramset_key']}'",
        )
        return

    # Validate model match
    device_address = get_device_address(address=msg["channel_address"])
    device = control.central.device_coordinator.get_device(address=device_address)
    target_model = device.model if device else ""
    if imported.model and target_model and imported.model != target_model:
        connection.send_error(
            msg["id"],
            "model_mismatch",
            f"Imported model '{imported.model}' does not match target model '{target_model}'",
        )
        return

    facade = control.central.configuration
    paramset_key = ParamsetKey(msg["paramset_key"])

    # Read old values for change history
    try:
        old_values = await facade.get_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException:
        old_values = {}

    try:
        result = await facade.put_paramset(
            interface_id=msg["interface_id"],
            channel_address=msg["channel_address"],
            paramset_key=paramset_key,
            values=imported.values,
            validate=True,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "write_failed", str(err))
        return

    if result.success:
        change_diff = _build_change_diff(old_values=old_values, new_values=imported.values)
        if change_diff:
            device_name, device_model = _get_device_info(
                control=control,
                channel_address=msg["channel_address"],
            )
            await _log_config_change(
                hass,
                entry_id=msg["entry_id"],
                interface_id=msg["interface_id"],
                channel_address=msg["channel_address"],
                device_name=device_name,
                device_model=device_model,
                paramset_key=msg["paramset_key"],
                changes=change_diff,
                source="import",
            )

    connection.send_result(
        msg["id"],
        {
            "success": result.success,
            "validated": result.validated,
            "validation_errors": dict(result.validation_errors),
            "imported_model": imported.model,
            "imported_at": imported.exported_at,
        },
    )


# ---------------------------------------------------------------------------
# Copy paramset command
# ---------------------------------------------------------------------------


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/copy_paramset",
        vol.Required("entry_id"): str,
        vol.Required("source_interface_id"): str,
        vol.Required("source_channel_address"): str,
        vol.Required("target_interface_id"): str,
        vol.Required("target_channel_address"): str,
        vol.Optional("paramset_key", default="MASTER"): vol.In(["MASTER", "VALUES"]),
    }
)
@async_response
async def ws_copy_paramset(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Copy paramset values from one channel to another."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    facade = control.central.configuration
    paramset_key = ParamsetKey(msg["paramset_key"])

    # Read source values
    try:
        source_values = await facade.get_paramset(
            interface_id=msg["source_interface_id"],
            channel_address=msg["source_channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "read_failed", f"Failed to read source: {err}")
        return

    # Read target description to filter writable parameters
    target_descriptions = facade.get_paramset_description(
        interface_id=msg["target_interface_id"],
        channel_address=msg["target_channel_address"],
        paramset_key=paramset_key,
    )

    # Filter: only parameters present in target description AND writable
    filtered_values: dict[str, Any] = {}
    skipped = 0
    for param, value in source_values.items():
        if param in target_descriptions and is_parameter_writable(parameter_data=target_descriptions[param]):
            filtered_values[param] = value
        else:
            skipped += 1

    if not filtered_values:
        connection.send_result(
            msg["id"],
            {
                "success": True,
                "validated": True,
                "validation_errors": {},
                "parameters_copied": 0,
                "parameters_skipped": skipped,
            },
        )
        return

    # Read old target values for change history
    try:
        old_values = await facade.get_paramset(
            interface_id=msg["target_interface_id"],
            channel_address=msg["target_channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException:
        old_values = {}

    try:
        result = await facade.put_paramset(
            interface_id=msg["target_interface_id"],
            channel_address=msg["target_channel_address"],
            paramset_key=paramset_key,
            values=filtered_values,
            validate=True,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "write_failed", str(err))
        return

    if result.success:
        change_diff = _build_change_diff(old_values=old_values, new_values=filtered_values)
        if change_diff:
            device_name, device_model = _get_device_info(
                control=control,
                channel_address=msg["target_channel_address"],
            )
            await _log_config_change(
                hass,
                entry_id=msg["entry_id"],
                interface_id=msg["target_interface_id"],
                channel_address=msg["target_channel_address"],
                device_name=device_name,
                device_model=device_model,
                paramset_key=msg["paramset_key"],
                changes=change_diff,
                source="copy",
            )

    connection.send_result(
        msg["id"],
        {
            "success": result.success,
            "validated": result.validated,
            "validation_errors": dict(result.validation_errors),
            "parameters_copied": len(filtered_values) if result.success else 0,
            "parameters_skipped": skipped,
        },
    )


# ---------------------------------------------------------------------------
# Change history commands
# ---------------------------------------------------------------------------


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_change_history",
        vol.Required("entry_id"): str,
        vol.Optional("channel_address", default=""): str,
        vol.Optional("limit", default=50): vol.All(int, vol.Range(min=1, max=500)),
    }
)
@async_response
async def ws_get_change_history(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return change history entries."""
    store = _get_history_store(hass)
    data: list[dict[str, Any]] = await store.async_load() or []

    # Filter by entry_id
    filtered = [e for e in data if e.get("entry_id") == msg["entry_id"]]

    # Optionally filter by channel_address
    channel_address: str = msg.get("channel_address", "")
    if channel_address:
        filtered = [e for e in filtered if e.get("channel_address") == channel_address]

    total = len(filtered)
    # Return most recent entries first, limited
    limit: int = msg.get("limit", 50)
    entries = list(reversed(filtered[-limit:]))

    connection.send_result(msg["id"], {"entries": entries, "total": total})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/clear_change_history",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_clear_change_history(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Clear all change history entries for an entry."""
    store = _get_history_store(hass)
    data: list[dict[str, Any]] = await store.async_load() or []

    original_count = len(data)
    data = [e for e in data if e.get("entry_id") != msg["entry_id"]]
    cleared = original_count - len(data)

    await store.async_save(data)

    connection.send_result(msg["id"], {"success": True, "cleared": cleared})


# ---------------------------------------------------------------------------
# Direct link commands
# ---------------------------------------------------------------------------


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/list_device_links",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("device_address"): str,
    }
)
@async_response
async def ws_list_device_links(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return all direct links for a device."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    central = control.central
    device = central.device_coordinator.get_device(address=msg["device_address"])
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    if device.interface not in LINKABLE_INTERFACES:
        connection.send_result(msg["id"], {"links": []})
        return

    links: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for channel in device.channels.values():
        try:
            raw_links: Any = await device.client.get_links(channel_address=channel.address, flags=0)
        except BaseHomematicException:
            continue

        if not isinstance(raw_links, list):
            continue

        for link_info in raw_links:
            sender_addr: str = link_info.get("SENDER", "")
            receiver_addr: str = link_info.get("RECEIVER", "")
            if not sender_addr or not receiver_addr:
                continue

            # Deduplicate
            key = (sender_addr, receiver_addr)
            if key in seen:
                continue
            seen.add(key)

            # Determine direction relative to current device
            is_sender = sender_addr.startswith(msg["device_address"])

            # Resolve peer device
            peer_addr = receiver_addr if is_sender else sender_addr
            peer_device_addr = get_device_address(address=peer_addr)
            peer_device = central.device_coordinator.get_device(address=peer_device_addr)

            links.append(
                {
                    "sender_address": sender_addr,
                    "receiver_address": receiver_addr,
                    "name": link_info.get("NAME", ""),
                    "description": link_info.get("DESCRIPTION", ""),
                    "flags": link_info.get("FLAGS", 0),
                    "sender_device_name": (
                        device.name if is_sender else (peer_device.name if peer_device else peer_device_addr)
                    ),
                    "sender_device_model": (device.model if is_sender else (peer_device.model if peer_device else "")),
                    "receiver_device_name": (
                        device.name if not is_sender else (peer_device.name if peer_device else peer_device_addr)
                    ),
                    "receiver_device_model": (
                        device.model if not is_sender else (peer_device.model if peer_device else "")
                    ),
                    "peer_address": peer_addr,
                    "peer_device_name": peer_device.name if peer_device else peer_device_addr,
                    "peer_device_model": peer_device.model if peer_device else "",
                    "direction": "outgoing" if is_sender else "incoming",
                }
            )

    connection.send_result(msg["id"], {"links": links})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_link_form_schema",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("sender_channel_address"): str,
        vol.Required("receiver_channel_address"): str,
    }
)
@async_response
async def ws_get_link_form_schema(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return form schema for a link paramset."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    facade = control.central.configuration
    sender_addr = msg["sender_channel_address"]
    receiver_addr = msg["receiver_channel_address"]

    # Paramset description for LINK type
    descriptions = facade.get_paramset_description(
        interface_id=msg["interface_id"],
        channel_address=receiver_addr,
        paramset_key=ParamsetKey.LINK,
    )

    # Current values for this specific link (sender address as paramset key)
    device_addr = get_device_address(address=receiver_addr)
    device = control.central.device_coordinator.get_device(address=device_addr)
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Receiver device not found")
        return

    try:
        current_values = await device.client.get_paramset(
            channel_address=receiver_addr,
            paramset_key=sender_addr,
            convert_from_pd=True,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    channel = device.get_channel(channel_address=receiver_addr)
    generator = FormSchemaGenerator(locale=hass.config.language)
    schema = generator.generate(
        descriptions=descriptions,
        current_values=current_values,
        channel_address=receiver_addr,
        channel_type=channel.type_name if channel else "",
        model=device.model,
        sub_model=device.sub_model,
    )

    connection.send_result(msg["id"], schema.model_dump())


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_link_paramset",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("sender_channel_address"): str,
        vol.Required("receiver_channel_address"): str,
    }
)
@async_response
async def ws_get_link_paramset(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return current link paramset values."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    receiver_addr = msg["receiver_channel_address"]
    sender_addr = msg["sender_channel_address"]
    device_addr = get_device_address(address=receiver_addr)
    device = control.central.device_coordinator.get_device(address=device_addr)
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Receiver device not found")
        return

    try:
        values = await device.client.get_paramset(
            channel_address=receiver_addr,
            paramset_key=sender_addr,
            convert_from_pd=True,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    connection.send_result(msg["id"], {"values": values})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/put_link_paramset",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("sender_channel_address"): str,
        vol.Required("receiver_channel_address"): str,
        vol.Required("values"): dict,
    }
)
@async_response
async def ws_put_link_paramset(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Write link paramset values."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    sender_addr = msg["sender_channel_address"]
    receiver_addr = msg["receiver_channel_address"]
    device_addr = get_device_address(address=receiver_addr)
    device = control.central.device_coordinator.get_device(address=device_addr)
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Receiver device not found")
        return

    # Read old values for change history
    try:
        old_values = await device.client.get_paramset(
            channel_address=receiver_addr,
            paramset_key=sender_addr,
            convert_from_pd=True,
        )
    except BaseHomematicException:
        old_values = {}

    try:
        await device.client.put_paramset(
            channel_address=receiver_addr,
            paramset_key_or_link_address=sender_addr,
            values=msg["values"],
            check_against_pd=True,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "write_failed", str(err))
        return

    # Log to change history
    changes = _build_change_diff(old_values=old_values, new_values=msg["values"])
    if changes:
        device_name, device_model = _get_device_info(
            control=control,
            channel_address=receiver_addr,
        )
        await _log_config_change(
            hass,
            entry_id=msg["entry_id"],
            interface_id=msg["interface_id"],
            channel_address=f"{sender_addr} -> {receiver_addr}",
            device_name=device_name,
            device_model=device_model,
            paramset_key="LINK",
            changes=changes,
            source="manual",
        )

    connection.send_result(msg["id"], {"success": True})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/add_link",
        vol.Required("entry_id"): str,
        vol.Required("sender_channel_address"): str,
        vol.Required("receiver_channel_address"): str,
        vol.Optional("name", default=""): str,
        vol.Optional("description", default="created by HA"): str,
    }
)
@async_response
async def ws_add_link(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Create a new direct link between two channels."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    sender_addr = msg["sender_channel_address"]
    receiver_addr = msg["receiver_channel_address"]
    sender_device_addr = get_device_address(address=sender_addr)
    device = control.central.device_coordinator.get_device(address=sender_device_addr)
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Sender device not found")
        return

    name = msg.get("name") or f"{sender_addr} -> {receiver_addr}"
    description = msg.get("description", "created by HA")

    try:
        await device.client.add_link(
            sender_address=sender_addr,
            receiver_address=receiver_addr,
            name=name,
            description=description,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "add_link_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/remove_link",
        vol.Required("entry_id"): str,
        vol.Required("sender_channel_address"): str,
        vol.Required("receiver_channel_address"): str,
    }
)
@async_response
async def ws_remove_link(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Remove a direct link between two channels."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    sender_addr = msg["sender_channel_address"]
    receiver_addr = msg["receiver_channel_address"]
    sender_device_addr = get_device_address(address=sender_addr)
    device = control.central.device_coordinator.get_device(address=sender_device_addr)
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Sender device not found")
        return

    try:
        await device.client.remove_link(
            sender_address=sender_addr,
            receiver_address=receiver_addr,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "remove_link_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_linkable_channels",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Required("role"): vol.In(["sender", "receiver"]),
    }
)
@async_response
async def ws_get_linkable_channels(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return channels compatible for linking with the given channel."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    central = control.central
    interface_id = msg["interface_id"]
    source_channel_addr = msg["channel_address"]
    role = msg["role"]

    candidates: list[dict[str, Any]] = []

    for device in central.devices:
        if device.interface_id != interface_id:
            continue
        if device.interface not in LINKABLE_INTERFACES:
            continue

        for channel in device.channels.values():
            # Skip the source channel itself
            if channel.address == source_channel_addr:
                continue

            # Check if this channel has LINK in its paramset keys
            has_link = any(pk == ParamsetKey.LINK for pk in channel.paramset_keys)
            if not has_link:
                continue

            if role == "sender":
                # Source is sender — look for receivers (channels with target roles)
                if not getattr(channel, "link_peer_target_categories", ()):
                    continue
            elif not getattr(channel, "link_peer_source_categories", ()):
                # Source is receiver — look for senders (channels with source roles)
                continue

            candidates.append(
                {
                    "address": channel.address,
                    "channel_type": channel.type_name,
                    "device_address": device.address,
                    "device_name": device.name or device.address,
                    "device_model": device.model,
                }
            )

    connection.send_result(msg["id"], {"channels": candidates})
