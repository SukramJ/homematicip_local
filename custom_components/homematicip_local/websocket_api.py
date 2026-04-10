"""WebSocket API for device configuration panel."""

from __future__ import annotations

import asyncio
import dataclasses
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

from pydantic import ValidationError
import voluptuous as vol

from aiohomematic.ccu_translations import get_device_icon
from aiohomematic.const import Interface, Parameter, ParamsetKey
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
from aiohomematic_config.master_profile_store import MasterProfileStore
from homeassistant.components.websocket_api import async_register_command
from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.components.websocket_api.decorators import async_response, websocket_command
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.issue_registry import async_delete_issue
from homeassistant.helpers.storage import Store
from homeassistant.util.hass_dict import HassKey

from .const import DOMAIN
from .permissions import (
    ALL_SCOPES,
    CONF_NON_ADMIN_PERMISSIONS,
    SCOPE_DEVICE_CONFIG,
    SCOPE_DEVICE_LINKS,
    SCOPE_SCHEDULE_EDIT,
    SCOPE_SYSTEM_ADMIN,
    require_scope,
)
from .repairs import REPAIR_CALLBACKS

if TYPE_CHECKING:
    from .control_unit import ControlUnit

_LOGGER: Final = logging.getLogger(__name__)


SESSIONS_KEY: HassKey[dict[str, ConfigSession]] = HassKey("homematicip_local_config_sessions")
PROFILE_STORE_KEY: HassKey[ProfileStore] = HassKey("homematicip_local_profile_store")
MASTER_PROFILE_STORE_KEY: HassKey[MasterProfileStore] = HassKey("homematicip_local_master_profile_store")
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
    async_register_command(hass, ws_get_master_profiles)
    async_register_command(hass, ws_get_link_paramset)
    async_register_command(hass, ws_put_link_paramset)
    async_register_command(hass, ws_add_link)
    async_register_command(hass, ws_remove_link)
    async_register_command(hass, ws_get_linkable_channels)
    # Determine parameter
    async_register_command(hass, ws_determine_parameter)
    # Schedule commands
    async_register_command(hass, ws_list_schedule_devices)
    async_register_command(hass, ws_get_climate_schedule)
    async_register_command(hass, ws_set_climate_schedule_weekday)
    async_register_command(hass, ws_set_climate_active_profile)
    async_register_command(hass, ws_get_device_schedule)
    async_register_command(hass, ws_set_device_schedule)
    async_register_command(hass, ws_reload_device_config)
    # Integration tab commands
    async_register_command(hass, ws_get_system_health)
    async_register_command(hass, ws_get_command_throttle_stats)
    async_register_command(hass, ws_get_incidents)
    async_register_command(hass, ws_clear_incidents)
    async_register_command(hass, ws_clear_cache)
    async_register_command(hass, ws_get_device_statistics)
    # OpenCCU tab commands
    async_register_command(hass, ws_get_system_information)
    async_register_command(hass, ws_create_backup)
    async_register_command(hass, ws_get_hub_data)
    async_register_command(hass, ws_get_install_mode_status)
    async_register_command(hass, ws_trigger_install_mode)
    async_register_command(hass, ws_get_signal_quality)
    async_register_command(hass, ws_get_firmware_overview)
    async_register_command(hass, ws_refresh_firmware_data)
    async_register_command(hass, ws_panel_reload_device_config)
    # Firmware update trigger
    async_register_command(hass, ws_update_firmware)
    # Link profile testing
    async_register_command(hass, ws_test_link_profile)
    # User permissions
    async_register_command(hass, ws_get_user_permissions)
    # Inbox, service messages, alarm messages
    async_register_command(hass, ws_get_inbox_devices)
    async_register_command(hass, ws_accept_inbox_device)
    async_register_command(hass, ws_get_service_messages)
    async_register_command(hass, ws_acknowledge_service_message)
    async_register_command(hass, ws_get_alarm_messages)
    async_register_command(hass, ws_acknowledge_alarm_message)


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


def _get_master_profile_store(hass: HomeAssistant) -> MasterProfileStore:
    """Return the shared MasterProfileStore instance, creating it if needed."""
    if MASTER_PROFILE_STORE_KEY not in hass.data:
        hass.data[MASTER_PROFILE_STORE_KEY] = MasterProfileStore()
    return hass.data[MASTER_PROFILE_STORE_KEY]


# ---------------------------------------------------------------------------
# Existing commands
# ---------------------------------------------------------------------------


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
    device_dicts = []
    for d in devices:
        d_dict = dataclasses.asdict(d)
        if icon := get_device_icon(model=d.model):
            d_dict["device_icon"] = icon
        device_dicts.append(d_dict)
    connection.send_result(msg["id"], {"devices": device_dicts})


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
        is_hmip=device.interface == Interface.HMIP_RF if device else False,
    )

    connection.send_result(msg["id"], schema.model_dump())


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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_DEVICE_CONFIG)
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


@require_scope(SCOPE_SYSTEM_ADMIN)
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
        is_hmip=device.interface == Interface.HMIP_RF,
    )

    connection.send_result(msg["id"], schema.model_dump())


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


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_master_profiles",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Required("sender_type"): str,
    }
)
@async_response
async def ws_get_master_profiles(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return available MASTER easymode profiles for a channel."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    channel_addr = msg["channel_address"]
    sender_type = msg["sender_type"]

    # Resolve channel type
    device_addr = get_device_address(address=channel_addr)
    device = control.central.device_coordinator.get_device(address=device_addr)
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    channel = device.get_channel(channel_address=channel_addr)
    channel_type = channel.type_name if channel else ""

    if not channel_type:
        connection.send_result(msg["id"], {"profiles": None, "active_profile_id": 0})
        return

    store = _get_master_profile_store(hass)
    locale = hass.config.language

    profiles = store.get_profiles(
        channel_type=channel_type,
        sender_type=sender_type,
        locale=locale,
    )

    if profiles is None:
        connection.send_result(msg["id"], {"profiles": None, "active_profile_id": 0})
        return

    # Load current LINK paramset values to match active profile
    try:
        current_values = await control.central.configuration.get_paramset(
            interface_id=msg["interface_id"],
            channel_address=channel_addr,
            paramset_key=ParamsetKey.MASTER,
        )
    except BaseHomematicException:
        active_profile_id = 0
    else:
        active_profile_id = store.match_active_profile(
            channel_type=channel_type,
            sender_type=sender_type,
            current_values=current_values,
        )

    connection.send_result(
        msg["id"],
        {
            "profiles": [p.model_dump() for p in profiles],
            "active_profile_id": active_profile_id,
        },
    )


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


@require_scope(SCOPE_DEVICE_LINKS)
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


@require_scope(SCOPE_DEVICE_LINKS)
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


@require_scope(SCOPE_DEVICE_LINKS)
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


@require_scope(SCOPE_SCHEDULE_EDIT)
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


@require_scope(SCOPE_SCHEDULE_EDIT)
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


@require_scope(SCOPE_SCHEDULE_EDIT)
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


@require_scope(SCOPE_SCHEDULE_EDIT)
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


# ---------------------------------------------------------------------------
# Integration tab commands
# ---------------------------------------------------------------------------


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/integration/get_system_health",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_system_health(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return the system health dashboard data."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    connection.send_result(msg["id"], control.central.health.to_dict())


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/integration/get_command_throttle_stats",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_command_throttle_stats(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return command throttle statistics per interface."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    throttle_stats: dict[str, dict[str, Any]] = {
        client.interface_id: {
            "interval": client.command_throttle.interval,
            "is_enabled": client.command_throttle.is_enabled,
            "queue_size": client.command_throttle.queue_size,
            "throttled_count": client.command_throttle.throttled_count,
            "critical_count": client.command_throttle.critical_count,
            "burst_count": client.command_throttle.burst_count,
            "burst_threshold": client.command_throttle.burst_threshold,
            "burst_window": client.command_throttle.burst_window,
        }
        for client in control.central.client_coordinator.clients
    }

    connection.send_result(msg["id"], {"throttle_stats": throttle_stats})


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/integration/get_incidents",
        vol.Required("entry_id"): str,
        vol.Optional("limit", default=50): int,
        vol.Optional("interface_id"): str,
    }
)
@async_response
async def ws_get_incidents(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return incidents from the incident store."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    incident_store = control.central.cache_coordinator.incident_store

    if "interface_id" in msg:
        incidents = await incident_store.get_incidents_by_interface(interface_id=msg["interface_id"])
        incident_list = [i.to_dict() for i in incidents[-msg["limit"] :]]
    else:
        incident_list = await incident_store.get_recent_incidents(limit=msg["limit"])

    diagnostics = await incident_store.get_diagnostics()

    connection.send_result(
        msg["id"],
        {
            "incidents": incident_list,
            "summary": {
                "total_incidents": diagnostics.get("total_incidents", 0),
                "incidents_by_type": diagnostics.get("incidents_by_type", {}),
                "incidents_by_severity": diagnostics.get("incidents_by_severity", {}),
            },
        },
    )


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/integration/clear_incidents",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_clear_incidents(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Clear all incidents from the incident store."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    control.central.cache_coordinator.incident_store.clear_incidents()
    connection.send_result(msg["id"], {"success": True})


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/integration/clear_cache",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_clear_cache(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Clear all caches."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    await control.central.cache_coordinator.clear_all()
    connection.send_result(msg["id"], {"success": True})


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/integration/get_device_statistics",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_device_statistics(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return device statistics grouped by interface."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    by_interface: dict[str, dict[str, int]] = {}
    total_devices = 0
    unreachable_devices = 0
    firmware_updatable_devices = 0

    for device in control.central.device_coordinator.devices:
        iid = device.interface_id
        if iid not in by_interface:
            by_interface[iid] = {"total": 0, "unreachable": 0, "firmware_updatable": 0}

        by_interface[iid]["total"] += 1
        total_devices += 1

        if not device.availability.is_reachable:
            by_interface[iid]["unreachable"] += 1
            unreachable_devices += 1

        if device.firmware_updatable:
            by_interface[iid]["firmware_updatable"] += 1
            firmware_updatable_devices += 1

    connection.send_result(
        msg["id"],
        {
            "total_devices": total_devices,
            "unreachable_devices": unreachable_devices,
            "firmware_updatable_devices": firmware_updatable_devices,
            "by_interface": by_interface,
        },
    )


# ---------------------------------------------------------------------------
# OpenCCU tab commands
# ---------------------------------------------------------------------------


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/get_system_information",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_system_information(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return CCU system information."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    central = control.central
    sys_info = central.system_information

    connection.send_result(
        msg["id"],
        {
            "name": central.name,
            "model": central.model,
            "version": central.version,
            "url": central.url,
            "serial": sys_info.serial,
            "hostname": sys_info.hostname,
            "ccu_type": sys_info.ccu_type.value if sys_info.ccu_type else None,
            "auth_enabled": sys_info.auth_enabled,
            "https_redirect_enabled": sys_info.https_redirect_enabled,
            "available_interfaces": list(sys_info.available_interfaces),
            "has_backup": sys_info.has_backup,
            "has_system_update": sys_info.has_system_update,
        },
    )


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/create_backup",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_create_backup(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Create and download a CCU backup."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        backup_data = await control.central.create_backup_and_download()
        if backup_data is None:
            connection.send_error(msg["id"], "backup_failed", "Failed to create backup from CCU")
            return

        backup_dir = Path(control.backup_directory)
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / backup_data.filename

        await hass.async_add_executor_job(backup_path.write_bytes, backup_data.content)

        _LOGGER.info("CCU backup saved to %s (%d bytes)", backup_path, len(backup_data.content))

        connection.send_result(
            msg["id"],
            {
                "success": True,
                "filename": backup_data.filename,
                "path": str(backup_path),
                "size": len(backup_data.content),
            },
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "backup_failed", str(err))


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/get_hub_data",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_hub_data(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return service and alarm message counts from hub data points."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    hub_coord = control.central.hub_coordinator
    service_messages = hub_coord.service_messages_dp.value if hub_coord.service_messages_dp else None
    alarm_messages = hub_coord.alarm_messages_dp.value if hub_coord.alarm_messages_dp else None

    connection.send_result(
        msg["id"],
        {
            "service_messages": service_messages,
            "alarm_messages": alarm_messages,
        },
    )


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/get_install_mode_status",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_install_mode_status(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return install mode status for HmIP-RF and BidCos-RF."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    install_mode_dps = control.central.hub_coordinator.install_mode_dps
    result: dict[str, dict[str, Any]] = {}

    for interface, label in ((Interface.HMIP_RF, "hmip"), (Interface.BIDCOS_RF, "bidcos")):
        if (im_dp := install_mode_dps.get(interface)) is not None:
            result[label] = {
                "remaining_seconds": im_dp.sensor.value,
                "active": im_dp.sensor.is_active,
                "available": True,
            }
        else:
            result[label] = {
                "remaining_seconds": None,
                "active": False,
                "available": False,
            }

    connection.send_result(msg["id"], result)


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/trigger_install_mode",
        vol.Required("entry_id"): str,
        vol.Required("interface"): vol.In(["hmip", "bidcos"]),
    }
)
@async_response
async def ws_trigger_install_mode(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Trigger install mode for the specified interface."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    interface_map: dict[str, Interface] = {
        "hmip": Interface.HMIP_RF,
        "bidcos": Interface.BIDCOS_RF,
    }
    interface = interface_map[msg["interface"]]

    install_mode_dps = control.central.hub_coordinator.install_mode_dps
    if (im_dp := install_mode_dps.get(interface)) is None:
        connection.send_error(msg["id"], "not_available", f"Install mode not available for {msg['interface']}")
        return

    try:
        await im_dp.button.activate()
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "activate_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True})


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/get_signal_quality",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_signal_quality(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return signal quality data for all devices."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    devices_data: list[dict[str, Any]] = []

    for device in control.central.device_coordinator.devices:
        avail = device.availability

        rssi_device_value: int | None = None
        rssi_peer_value: int | None = None

        if rssi_dp := device.get_generic_data_point(parameter=Parameter.RSSI_DEVICE):
            rssi_device_value = rssi_dp.value
        if rssi_dp := device.get_generic_data_point(parameter=Parameter.RSSI_PEER):
            rssi_peer_value = rssi_dp.value

        devices_data.append(
            {
                "address": device.address,
                "name": device.name,
                "model": device.model,
                "interface_id": device.interface_id,
                "is_reachable": avail.is_reachable,
                "rssi_device": rssi_device_value,
                "rssi_peer": rssi_peer_value,
                "signal_strength": avail.signal_strength,
                "low_battery": avail.low_battery,
            }
        )

    connection.send_result(msg["id"], {"devices": devices_data})


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/get_firmware_overview",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_firmware_overview(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return firmware overview for all devices."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    devices_data: list[dict[str, Any]] = []
    total_devices = 0
    firmware_updatable = 0

    for device in control.central.device_coordinator.devices:
        total_devices += 1
        if device.firmware_updatable:
            firmware_updatable += 1

        devices_data.append(
            {
                "address": device.address,
                "name": device.name,
                "model": device.model,
                "interface_id": device.interface_id,
                "firmware": device.firmware,
                "available_firmware": device.available_firmware,
                "firmware_updatable": device.firmware_updatable,
                "firmware_update_state": device.firmware_update_state.value,
            }
        )

    connection.send_result(
        msg["id"],
        {
            "devices": devices_data,
            "summary": {
                "total_devices": total_devices,
                "firmware_updatable": firmware_updatable,
            },
        },
    )


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/refresh_firmware_data",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_refresh_firmware_data(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Refresh firmware data from the CCU."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        await control.central.device_coordinator.refresh_firmware_data()
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "refresh_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True})


@require_scope(SCOPE_SCHEDULE_EDIT)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/reload_device_config",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
    }
)
@async_response
async def ws_panel_reload_device_config(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Reload device configuration from the CCU."""
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


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/get_inbox_devices",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_inbox_devices(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return inbox devices (not yet accepted)."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        devices = await control.central.json_rpc_client.get_inbox_devices()
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "fetch_failed", str(err))
        return

    connection.send_result(
        msg["id"],
        {
            "devices": [dataclasses.asdict(dev) for dev in devices],
        },
    )


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/accept_inbox_device",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
        vol.Optional("device_name"): str,
        vol.Optional("device_id"): str,
    }
)
@async_response
async def ws_accept_inbox_device(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Accept a device from the CCU inbox."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        success = await control.central.json_rpc_client.accept_device_in_inbox(device_address=msg["device_address"])
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "accept_failed", str(err))
        return

    if not success:
        connection.send_error(msg["id"], "accept_failed", "Failed to accept device")
        return

    if (device_name := msg.get("device_name")) and (device_id := msg.get("device_id")):
        try:
            await control.central.json_rpc_client.rename_device(ise_id=int(device_id), new_name=device_name)
        except BaseHomematicException as err:
            _LOGGER.warning("Failed to rename device %s: %s", msg["device_address"], err)

    # Auto-confirm the repair issue that will be created when the CCU sends
    # the newDevices callback. Wait for the callback to arrive and then
    # execute the repair callback so the device appears in HA immediately.
    device_address = msg["device_address"]
    device_name_for_confirm = msg.get("device_name", "")

    async def _auto_confirm_delayed_device() -> None:
        # Wait for the repair callback to be registered (max 30s)
        for _ in range(60):
            matching = [
                issue_id
                for issue_id in REPAIR_CALLBACKS
                if issue_id.startswith("devices_delayed|") and issue_id.endswith(f"|{device_address}")
            ]
            if matching:
                for issue_id in matching:
                    if cb := REPAIR_CALLBACKS.pop(issue_id, None):
                        try:
                            await cb(device_name=device_name_for_confirm)
                        except Exception:
                            _LOGGER.exception("Failed to auto-confirm device %s", device_address)
                    async_delete_issue(hass=hass, domain=DOMAIN, issue_id=issue_id)
                _LOGGER.info("Auto-confirmed inbox device %s", device_address)
                return
            await asyncio.sleep(0.5)

        _LOGGER.warning("Timeout waiting for delayed device callback for %s", device_address)

    hass.async_create_task(
        _auto_confirm_delayed_device(),
        f"auto_confirm_inbox_{device_address}",
    )

    connection.send_result(msg["id"], {"success": True})


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/get_service_messages",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_service_messages(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return detailed service messages."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        messages = await control.central.json_rpc_client.get_service_messages()
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "fetch_failed", str(err))
        return

    connection.send_result(
        msg["id"],
        {
            "messages": [dataclasses.asdict(m) for m in messages],
        },
    )


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/get_alarm_messages",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_alarm_messages(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return detailed alarm messages."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        alarms = await control.central.json_rpc_client.get_alarm_messages()
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "fetch_failed", str(err))
        return

    connection.send_result(
        msg["id"],
        {
            "alarms": [dataclasses.asdict(a) for a in alarms],
        },
    )


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/acknowledge_service_message",
        vol.Required("entry_id"): str,
        vol.Required("msg_id"): str,
    }
)
@async_response
async def ws_acknowledge_service_message(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Acknowledge (clear) a service message."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        success = await control.central.json_rpc_client.acknowledge_message(message_id=msg["msg_id"])
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "acknowledge_failed", str(err))
        return

    if not success:
        connection.send_error(msg["id"], "acknowledge_failed", "Failed to acknowledge message")
        return

    connection.send_result(msg["id"], {"success": True})


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/acknowledge_alarm_message",
        vol.Required("entry_id"): str,
        vol.Required("alarm_id"): str,
    }
)
@async_response
async def ws_acknowledge_alarm_message(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Acknowledge (clear) an alarm message."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    try:
        success = await control.central.json_rpc_client.acknowledge_message(message_id=msg["alarm_id"])
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "acknowledge_failed", str(err))
        return

    if not success:
        connection.send_error(msg["id"], "acknowledge_failed", "Failed to acknowledge alarm")
        return

    connection.send_result(msg["id"], {"success": True})


# ---------------------------------------------------------------------------
# Determine parameter
# ---------------------------------------------------------------------------


@require_scope(SCOPE_DEVICE_CONFIG)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/determine_parameter",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("channel_address"): str,
        vol.Required("parameter_id"): str,
    }
)
@async_response
async def ws_determine_parameter(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Auto-detect a parameter value from the device."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    device_address = get_device_address(address=msg["channel_address"])
    device = control.central.device_coordinator.get_device(address=device_address)
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    try:
        value = await device.client.determine_parameter(
            channel_address=msg["channel_address"],
            parameter=msg["parameter_id"],
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "determine_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True, "value": value})


# ---------------------------------------------------------------------------
# Firmware update trigger
# ---------------------------------------------------------------------------


@require_scope(SCOPE_SYSTEM_ADMIN)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/ccu/update_firmware",
        vol.Required("entry_id"): str,
        vol.Required("device_address"): str,
    }
)
@async_response
async def ws_update_firmware(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Trigger a firmware update for a device."""
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    device = control.central.device_coordinator.get_device(address=msg["device_address"])
    if device is None:
        connection.send_error(msg["id"], "device_not_found", "Device not found")
        return

    if not device.firmware_updatable:
        connection.send_error(msg["id"], "not_updatable", "Device firmware is not updatable")
        return

    try:
        success = await device.update_firmware(refresh_after_update_intervals=(10, 60))
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "update_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": success})


# ---------------------------------------------------------------------------
# Link profile testing
# ---------------------------------------------------------------------------


@require_scope(SCOPE_DEVICE_LINKS)
@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/test_link_profile",
        vol.Required("entry_id"): str,
        vol.Required("interface_id"): str,
        vol.Required("sender_channel_address"): str,
        vol.Required("receiver_channel_address"): str,
        vol.Required("profile_id"): int,
    }
)
@async_response
async def ws_test_link_profile(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Test a link profile by temporarily applying it.

    This writes the profile's default values to the link paramset so the user
    can observe the effect. The values remain until overwritten.
    """
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    receiver_addr = msg["receiver_channel_address"]
    sender_addr = msg["sender_channel_address"]

    # Resolve devices and channel types
    receiver_device_addr = get_device_address(address=receiver_addr)
    receiver_device = control.central.device_coordinator.get_device(address=receiver_device_addr)
    if receiver_device is None:
        connection.send_error(msg["id"], "device_not_found", "Receiver device not found")
        return

    receiver_channel = receiver_device.get_channel(channel_address=receiver_addr)
    receiver_channel_type = receiver_channel.type_name if receiver_channel else ""

    sender_device_addr = get_device_address(address=sender_addr)
    sender_device = control.central.device_coordinator.get_device(address=sender_device_addr)
    sender_channel = sender_device.get_channel(channel_address=sender_addr) if sender_device else None
    sender_channel_type = sender_channel.type_name if sender_channel else ""

    # Get the profile
    profile_store = _get_profile_store(hass)
    profiles = await profile_store.get_profiles(
        receiver_channel_type=receiver_channel_type,
        sender_channel_type=sender_channel_type,
        locale=hass.config.language,
    )
    if profiles is None:
        connection.send_error(msg["id"], "no_profiles", "No profiles available for this link")
        return

    profile = next((p for p in profiles if p.id == msg["profile_id"]), None)
    if profile is None:
        connection.send_error(msg["id"], "profile_not_found", f"Profile {msg['profile_id']} not found")
        return

    # Build values: merge default_values and fixed_params
    values_to_apply: dict[str, Any] = {}
    values_to_apply.update(profile.fixed_params)
    values_to_apply.update(profile.default_values)

    if not values_to_apply:
        connection.send_error(msg["id"], "no_values", "Profile has no values to apply")
        return

    try:
        await receiver_device.client.put_paramset(
            channel_address=receiver_addr,
            paramset_key_or_link_address=sender_addr,
            values=values_to_apply,
            check_against_pd=True,
        )
    except BaseHomematicException as err:
        connection.send_error(msg["id"], "apply_failed", str(err))
        return

    connection.send_result(msg["id"], {"success": True, "applied_values": values_to_apply})


# ---------------------------------------------------------------------------
# User permissions
# ---------------------------------------------------------------------------


@websocket_command(
    {
        vol.Required("type"): "homematicip_local/config/get_user_permissions",
        vol.Required("entry_id"): str,
    }
)
@async_response
async def ws_get_user_permissions(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return the effective permissions for the current user."""
    user = connection.user
    entry = hass.config_entries.async_get_entry(msg["entry_id"])
    if entry is None:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    if user.is_admin or user.is_owner:
        scopes = list(ALL_SCOPES)
    else:
        scopes = list(entry.options.get(CONF_NON_ADMIN_PERMISSIONS, []))

    backend: str | None = None
    if (control := _get_control_unit(hass, entry_id=msg["entry_id"])) is not None:
        backend = control.central.model

    connection.send_result(
        msg["id"],
        {
            "is_admin": user.is_admin,
            "permissions": scopes,
            "backend": backend,
        },
    )
