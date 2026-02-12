"""WebSocket API for device configuration panel."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Final

import voluptuous as vol

from aiohomematic.ccu_translations import get_channel_type_translation
from aiohomematic.const import ParamsetKey
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.parameter_tools import is_parameter_internal, is_parameter_visible, is_parameter_writable
from aiohomematic_config import FormSchemaGenerator
from homeassistant.components.websocket_api import async_register_command
from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.components.websocket_api.decorators import async_response, require_admin, websocket_command
from homeassistant.core import HomeAssistant, callback

if TYPE_CHECKING:
    from .control_unit import ControlUnit

_LOGGER: Final = logging.getLogger(__name__)


@callback
def async_register_websocket_commands(hass: HomeAssistant) -> None:
    """Register all WebSocket commands for the configuration panel."""
    async_register_command(hass, ws_list_devices)
    async_register_command(hass, ws_get_form_schema)
    async_register_command(hass, ws_get_paramset)
    async_register_command(hass, ws_put_paramset)


def _get_control_unit(hass: HomeAssistant, *, entry_id: str) -> ControlUnit | None:
    """Return the ControlUnit for a config entry."""
    if (entry := hass.config_entries.async_get_entry(entry_id)) is None:
        return None
    if not hasattr(entry, "runtime_data"):
        return None
    control_unit: ControlUnit = entry.runtime_data
    return control_unit


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
                "interface_id": device.interface_id,
                "model": device.model,
                "model_description": device.model_description or "",
                "name": device.name or device.address,
                "firmware": device.firmware,
                "channels": channel_list,
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

    connection.send_result(
        msg["id"],
        {
            "success": result.success,
            "validated": result.validated,
            "validation_errors": dict(result.validation_errors),
        },
    )
