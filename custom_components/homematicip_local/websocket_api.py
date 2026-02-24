"""WebSocket API for device configuration panel."""

from __future__ import annotations

import dataclasses
import logging
from typing import TYPE_CHECKING, Any, Final

from pydantic import ValidationError
import voluptuous as vol

from aiohomematic.const import ParamsetKey
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.support.address import get_device_address
from aiohomematic_config import (
    ConfigChangeLog,
    ConfigSession,
    FormSchemaGenerator,
    ProfileStore,
    build_change_diff,
    export_configuration,
    get_climate_schedule,
    get_device_schedule,
    import_configuration,
    list_schedule_devices,
    set_climate_active_profile,
    set_climate_schedule_weekday,
    set_device_schedule,
)
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
PROFILE_STORE_KEY: HassKey[ProfileStore] = HassKey("homematicip_local_profile_store")
CHANGE_LOG_KEY: HassKey[ConfigChangeLog] = HassKey("homematicip_local_change_log")
HISTORY_STORE_KEY: Final = "homematicip_local.config_changes"


def _get_session_key(*, entry_id: str, channel_address: str, paramset_key: str) -> str:
    """Return a unique key for a config session."""
    return f"{entry_id}_{channel_address}_{paramset_key}"


def _get_history_store(hass: HomeAssistant) -> Store[list[dict[str, Any]]]:
    """Return the change history store."""
    return Store[list[dict[str, Any]]](hass, 1, HISTORY_STORE_KEY)


async def _get_change_log(hass: HomeAssistant) -> ConfigChangeLog:
    """Return the shared ConfigChangeLog, loading from store if needed."""
    if CHANGE_LOG_KEY not in hass.data:
        store = _get_history_store(hass)
        data: list[dict[str, Any]] = await store.async_load() or []
        log = ConfigChangeLog()
        log.load_entries(raw_entries=data)
        hass.data[CHANGE_LOG_KEY] = log
    return hass.data[CHANGE_LOG_KEY]


async def _persist_change_log(hass: HomeAssistant, *, log: ConfigChangeLog) -> None:
    """Persist the change log to HA Store."""
    store = _get_history_store(hass)
    await store.async_save(log.to_dicts())


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
    async_register_command(hass, ws_get_link_profiles)
    async_register_command(hass, ws_get_link_paramset)
    async_register_command(hass, ws_put_link_paramset)
    async_register_command(hass, ws_add_link)
    async_register_command(hass, ws_remove_link)
    async_register_command(hass, ws_get_linkable_channels)
    # Schedule commands
    async_register_command(hass, ws_list_schedule_devices)
    async_register_command(hass, ws_get_climate_schedule)
    async_register_command(hass, ws_set_climate_schedule_weekday)
    async_register_command(hass, ws_set_climate_active_profile)
    async_register_command(hass, ws_get_device_schedule)
    async_register_command(hass, ws_set_device_schedule)
    async_register_command(hass, ws_reload_device_config)


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


def _get_profile_store(hass: HomeAssistant) -> ProfileStore:
    """Return the shared ProfileStore instance, creating it if needed."""
    if PROFILE_STORE_KEY not in hass.data:
        hass.data[PROFILE_STORE_KEY] = ProfileStore()
    return hass.data[PROFILE_STORE_KEY]


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

    devices = control.central.configuration.get_configurable_devices(locale=hass.config.language)
    connection.send_result(msg["id"], {"devices": [dataclasses.asdict(d) for d in devices]})


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
        changes = build_change_diff(old_values=old_values, new_values=msg["values"])
        if changes:
            device_name, device_model = _get_device_info(
                control=control,
                channel_address=msg["channel_address"],
            )
            log = await _get_change_log(hass)
            log.add(
                entry_id=msg["entry_id"],
                interface_id=msg["interface_id"],
                channel_address=msg["channel_address"],
                device_name=device_name,
                device_model=device_model,
                paramset_key=msg["paramset_key"],
                changes=changes,
                source="manual",
            )
            await _persist_change_log(hass, log=log)

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
        change_diff = build_change_diff(old_values=old_values, new_values=changes)
        if change_diff:
            device_name, device_model = _get_device_info(
                control=control,
                channel_address=msg["channel_address"],
            )
            log = await _get_change_log(hass)
            log.add(
                entry_id=msg["entry_id"],
                interface_id=msg["interface_id"],
                channel_address=msg["channel_address"],
                device_name=device_name,
                device_model=device_model,
                paramset_key=msg["paramset_key"],
                changes=change_diff,
                source="manual",
            )
            await _persist_change_log(hass, log=log)
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
        change_diff = build_change_diff(old_values=old_values, new_values=imported.values)
        if change_diff:
            device_name, device_model = _get_device_info(
                control=control,
                channel_address=msg["channel_address"],
            )
            log = await _get_change_log(hass)
            log.add(
                entry_id=msg["entry_id"],
                interface_id=msg["interface_id"],
                channel_address=msg["channel_address"],
                device_name=device_name,
                device_model=device_model,
                paramset_key=msg["paramset_key"],
                changes=change_diff,
                source="import",
            )
            await _persist_change_log(hass, log=log)

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

    try:
        result, old_values, copied_values = await facade.copy_paramset(
            source_interface_id=msg["source_interface_id"],
            source_channel_address=msg["source_channel_address"],
            target_interface_id=msg["target_interface_id"],
            target_channel_address=msg["target_channel_address"],
            paramset_key=paramset_key,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    if result.success and copied_values:
        changes = build_change_diff(old_values=old_values, new_values=copied_values)
        if changes:
            device_name, device_model = _get_device_info(
                control=control,
                channel_address=msg["target_channel_address"],
            )
            log = await _get_change_log(hass)
            log.add(
                entry_id=msg["entry_id"],
                interface_id=msg["target_interface_id"],
                channel_address=msg["target_channel_address"],
                device_name=device_name,
                device_model=device_model,
                paramset_key=msg["paramset_key"],
                changes=changes,
                source="copy",
            )
            await _persist_change_log(hass, log=log)

    connection.send_result(msg["id"], dataclasses.asdict(result))


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
    log = await _get_change_log(hass)
    entries, total = log.get_entries(
        entry_id=msg["entry_id"],
        channel_address=msg.get("channel_address", ""),
        limit=msg.get("limit", 50),
    )
    connection.send_result(
        msg["id"],
        {"entries": [dataclasses.asdict(e) for e in entries], "total": total},
    )


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
    log = await _get_change_log(hass)
    cleared = log.clear_by_entry_id(entry_id=msg["entry_id"])
    await _persist_change_log(hass, log=log)
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

    device_links = await control.central.link.get_device_links(
        device_address=msg["device_address"],
        locale=hass.config.language,
    )
    connection.send_result(msg["id"], {"links": [dataclasses.asdict(dl) for dl in device_links]})


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

    sender_addr = msg["sender_channel_address"]
    receiver_addr = msg["receiver_channel_address"]

    device_addr = get_device_address(address=receiver_addr)
    device = control.central.device_coordinator.get_device(address=device_addr)
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Receiver device not found")
        return

    try:
        descriptions = await control.central.configuration.get_link_paramset_description(
            interface_id=msg["interface_id"],
            channel_address=receiver_addr,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    # Current values for this specific link (sender address as paramset key)
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
        require_translation=False,
        enrich_link_metadata=True,
    )

    connection.send_result(msg["id"], schema.model_dump())


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_link_profiles",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("sender_channel_address"): str,
        vol.Required("receiver_channel_address"): str,
    }
)
@async_response
async def ws_get_link_profiles(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return available easymode profiles for a link."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    sender_addr = msg["sender_channel_address"]
    receiver_addr = msg["receiver_channel_address"]

    # Resolve receiver device and channel
    receiver_device_addr = get_device_address(address=receiver_addr)
    receiver_device = control.central.device_coordinator.get_device(address=receiver_device_addr)
    if receiver_device is None:
        connection.send_error(msg["id"], "device_not_found", "Receiver device not found")
        return

    receiver_channel = receiver_device.get_channel(channel_address=receiver_addr)
    receiver_channel_type = receiver_channel.type_name if receiver_channel else ""

    # Resolve sender device and channel
    sender_device_addr = get_device_address(address=sender_addr)
    sender_device = control.central.device_coordinator.get_device(address=sender_device_addr)
    sender_channel = sender_device.get_channel(channel_address=sender_addr) if sender_device else None
    sender_channel_type = sender_channel.type_name if sender_channel else ""

    if not receiver_channel_type or not sender_channel_type:
        connection.send_result(msg["id"], {"profiles": None, "active_profile_id": 0})
        return

    profile_store = _get_profile_store(hass)
    locale = hass.config.language

    profiles = await profile_store.get_profiles(
        receiver_channel_type=receiver_channel_type,
        sender_channel_type=sender_channel_type,
        locale=locale,
    )

    if profiles is None:
        connection.send_result(msg["id"], {"profiles": None, "active_profile_id": 0})
        return

    # Load current values to match active profile
    try:
        current_values = await receiver_device.client.get_paramset(
            channel_address=receiver_addr,
            paramset_key=sender_addr,
            convert_from_pd=True,
        )
    except BaseHomematicException:
        active_profile_id = 0
    else:
        active_profile_id = await profile_store.match_active_profile(
            receiver_channel_type=receiver_channel_type,
            sender_channel_type=sender_channel_type,
            current_values=current_values,
        )

    connection.send_result(
        msg["id"],
        {
            "profiles": [p.model_dump() for p in profiles],
            "active_profile_id": active_profile_id,
        },
    )


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
    changes = build_change_diff(old_values=old_values, new_values=msg["values"])
    if changes:
        device_name, device_model = _get_device_info(
            control=control,
            channel_address=receiver_addr,
        )
        log = await _get_change_log(hass)
        log.add(
            entry_id=msg["entry_id"],
            interface_id=msg["interface_id"],
            channel_address=f"{sender_addr} -> {receiver_addr}",
            device_name=device_name,
            device_model=device_model,
            paramset_key="LINK",
            changes=changes,
            source="manual",
        )
        await _persist_change_log(hass, log=log)

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

    success = await control.central.link.add_link(
        sender_channel_address=msg["sender_channel_address"],
        receiver_channel_address=msg["receiver_channel_address"],
        name=msg.get("name", ""),
        description=msg.get("description", "created by HA"),
    )
    if not success:
        connection.send_error(msg["id"], "add_link_failed", "Failed to add link")
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

    success = await control.central.link.remove_link(
        sender_channel_address=msg["sender_channel_address"],
        receiver_channel_address=msg["receiver_channel_address"],
    )
    if not success:
        connection.send_error(msg["id"], "remove_link_failed", "Failed to remove link")
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

    channels = control.central.link.get_linkable_channels(
        interface_id=msg["interface_id"],
        source_channel_address=msg["channel_address"],
        role=msg["role"],
        locale=hass.config.language,
    )
    connection.send_result(msg["id"], {"channels": [dataclasses.asdict(ch) for ch in channels]})


# ---------------------------------------------------------------------------
# Schedule commands
# ---------------------------------------------------------------------------


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/list_schedule_devices",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_list_schedule_devices(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return all devices with schedule support."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    devices = list_schedule_devices(devices=control.central.device_coordinator.devices)
    connection.send_result(msg["id"], {"devices": [dataclasses.asdict(d) for d in devices]})


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_climate_schedule",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
        vol.Optional("profile"): str,
    }
)
@async_response
async def ws_get_climate_schedule(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return climate schedule data."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    device = control.central.device_coordinator.get_device(address=msg["device_address"])
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    try:
        data = await get_climate_schedule(
            device=device,
            profile=msg.get("profile"),
        )
    except (BaseHomematicException, ValueError, ValidationError) as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    connection.send_result(msg["id"], dataclasses.asdict(data))


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/set_climate_schedule_weekday",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
        vol.Required("profile"): str,
        vol.Required("weekday"): str,
        vol.Required("base_temperature"): vol.Coerce(float),
        vol.Required("simple_weekday_list"): list,
    }
)
@async_response
async def ws_set_climate_schedule_weekday(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Set climate schedule weekday data."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    device = control.central.device_coordinator.get_device(address=msg["device_address"])
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    try:
        await set_climate_schedule_weekday(
            device=device,
            profile=msg["profile"],
            weekday=msg["weekday"],
            base_temperature=msg["base_temperature"],
            simple_weekday_list=msg["simple_weekday_list"],
        )
    except (BaseHomematicException, ValueError, ValidationError) as err:
        connection.send_error(msg["id"], "write_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True})


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/set_climate_active_profile",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
        vol.Required("profile"): str,
    }
)
@async_response
async def ws_set_climate_active_profile(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Set the active climate schedule profile."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    device = control.central.device_coordinator.get_device(address=msg["device_address"])
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    try:
        set_climate_active_profile(device=device, profile=msg["profile"])
    except (ValueError, ValidationError) as err:
        connection.send_error(msg["id"], "write_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True})


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_device_schedule",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
    }
)
@async_response
async def ws_get_device_schedule(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return device schedule data."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    device = control.central.device_coordinator.get_device(address=msg["device_address"])
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    try:
        data = await get_device_schedule(device=device)
    except (BaseHomematicException, ValueError, ValidationError) as err:
        connection.send_error(msg["id"], "read_failed", str(err))
        return

    connection.send_result(msg["id"], dataclasses.asdict(data))


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/set_device_schedule",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
        vol.Required("schedule_data"): dict,
    }
)
@async_response
async def ws_set_device_schedule(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Set device schedule data."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    device = control.central.device_coordinator.get_device(address=msg["device_address"])
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    try:
        await set_device_schedule(
            device=device,
            schedule_data=msg["schedule_data"],
        )
    except (BaseHomematicException, ValueError, ValidationError) as err:
        connection.send_error(msg["id"], "write_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True})


@require_admin
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/reload_device_config",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
    }
)
@async_response
async def ws_reload_device_config(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Reload device configuration from CCU."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    device = control.central.device_coordinator.get_device(address=msg["device_address"])
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    try:
        await device.reload_device_config()
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "reload_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True})
