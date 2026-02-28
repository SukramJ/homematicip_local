"""Homematic(IP) Local for OpenCCU is a Python 3 module for Home Assistant and Homematic(IP) devices."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
import logging
import time
from typing import Any, TypeAlias

from awesomeversion import AwesomeVersion

from aiohomematic import __version__ as HAHM_VERSION
from aiohomematic.const import (
    DEFAULT_ENABLE_SYSVAR_SCAN,
    DEFAULT_UN_IGNORES,
    IntegrationIssueType,
    OptionalSettings,
    is_interface_default_port,
)
from aiohomematic.exceptions import AuthFailure
from aiohomematic.store.persistent import cleanup_files
from aiohomematic.support import find_free_port
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT, EVENT_HOMEASSISTANT_STOP, __version__ as HA_VERSION_STR
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr, entity_registry as er, issue_registry as ir
from homeassistant.helpers.entity_registry import async_migrate_entries
from homeassistant.helpers.issue_registry import async_delete_issue
from homeassistant.util.hass_dict import HassKey

from .backup import async_notify_backup_listeners
from .const import (
    CONF_ACTION_SELECT_VALUES,
    CONF_ADVANCED_CONFIG,
    CONF_CALLBACK_PORT_XML_RPC,
    CONF_COMMAND_THROTTLE_INTERVAL,
    CONF_CUSTOM_PORTS,
    CONF_ENABLE_CONFIG_PANEL,
    CONF_ENABLE_PROGRAM_SCAN,
    CONF_ENABLE_SYSTEM_NOTIFICATIONS,
    CONF_ENABLE_SYSVAR_SCAN,
    CONF_INSTANCE_NAME,
    CONF_INTERFACE,
    CONF_OPTIONAL_SETTINGS,
    CONF_SYS_SCAN_INTERVAL,
    CONF_UN_IGNORES,
    DEFAULT_AUTO_CONFIRM_NEW_DEVICES_TIMEOUT,
    DEFAULT_COMMAND_THROTTLE_INTERVAL,
    DEFAULT_ENABLE_CONFIG_PANEL,
    DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS,
    DEFAULT_SYS_SCAN_INTERVAL,
    DOMAIN,
    HMIP_LOCAL_MIN_HA_VERSION,
    HMIP_LOCAL_PLATFORMS,
)
from .control_unit import ControlConfig, ControlUnit, get_storage_directory
from .device_icon import ICON_VIEW_REGISTERED_KEY, DeviceIconView
from .panel import async_register_panel, async_unregister_panel
from .services import async_get_loaded_config_entries, async_setup_services, async_unload_services
from .support import get_aiohomematic_version, get_device_address_at_interface_from_identifiers
from .websocket_api import async_register_websocket_commands

HA_VERSION = AwesomeVersion(HA_VERSION_STR)
HomematicConfigEntry: TypeAlias = ConfigEntry[ControlUnit]


@dataclass(kw_only=True, slots=True)
class HomematicData:
    """Common data for shared Homematic ip local data."""

    default_callback_port_xml_rpc: int | None = None


HM_KEY: HassKey[HomematicData] = HassKey(DOMAIN)
_LOGGER = logging.getLogger(__name__)

# Issue types that should be cleared on startup as they are transient
# and not relevant after a restart
_STALE_ISSUE_TYPES: tuple[str, ...] = (
    IntegrationIssueType.PING_PONG_MISMATCH,
    IntegrationIssueType.FETCH_DATA_FAILED,
    IntegrationIssueType.INCOMPLETE_DEVICE_DATA,
    # Legacy issue types (may still exist from previous sessions)
    "pending_pong_mismatch",
    "unknown_pong_mismatch",
    "interface_not_reachable",
    "xmlrpc_server_receives_no_events",
)


def _cleanup_stale_issues(*, hass: HomeAssistant, entry_id: str) -> None:
    """Delete stale issues from previous sessions for this config entry."""
    issue_registry = ir.async_get(hass)
    for (domain, issue_id), _issue in list(issue_registry.issues.items()):
        if domain != DOMAIN or not issue_id.startswith(entry_id):
            continue
        # Check if stale issue type is part of issue_id
        # (issue_id format: {entry_id}_{issue_type}_{interface_id})
        # Note: translation_key is not persisted in the issue registry storage
        if any(f"_{issue_type}_" in issue_id for issue_type in _STALE_ISSUE_TYPES):
            async_delete_issue(hass=hass, domain=DOMAIN, issue_id=issue_id)
            _LOGGER.debug("Deleted stale issue %s on startup", issue_id)


def _any_entry_has_panel_enabled(*, hass: HomeAssistant) -> bool:
    """Return True if any loaded config entry has the config panel enabled."""
    return any(
        entry.data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_ENABLE_CONFIG_PANEL, DEFAULT_ENABLE_CONFIG_PANEL)
        for entry in hass.config_entries.async_entries(domain=DOMAIN, include_ignore=False, include_disabled=False)
    )


async def async_setup_entry(hass: HomeAssistant, entry: HomematicConfigEntry) -> bool:
    """Set up Homematic(IP) Local for OpenCCU from a config entr11y."""
    expected_version = await get_aiohomematic_version(hass=hass, domain=entry.domain, package_name="aiohomematic")
    if AwesomeVersion(expected_version) != AwesomeVersion(HAHM_VERSION):
        _LOGGER.error(
            "This release of Homematic(IP) Local for OpenCCU requires aiohomematic version %s, but found version %s. "
            "Looks like HA has a problem with dependency management. "
            "This is NOT an issue of the integration.",
            expected_version,
            HAHM_VERSION,
        )
        _LOGGER.warning("Homematic(IP) Local for OpenCCU setup blocked")
        return False
    _LOGGER.debug(
        "Homematic(IP) Local for OpenCCU setup with aiohomematic version %s",
        HAHM_VERSION,
    )

    if AwesomeVersion(HMIP_LOCAL_MIN_HA_VERSION) > HA_VERSION:
        _LOGGER.warning(
            "This release of Homematic(IP) Local for OpenCCU requires HA version %s and above",
            HMIP_LOCAL_MIN_HA_VERSION,
        )
        _LOGGER.warning("HHomematic(IP) Local for OpenCCU setup blocked")
        return False

    # Clean up stale issues from previous sessions
    _cleanup_stale_issues(hass=hass, entry_id=entry.entry_id)

    hass.data.setdefault(HM_KEY, HomematicData())
    if (default_callback_port_xml_rpc := hass.data[HM_KEY].default_callback_port_xml_rpc) is None:
        default_callback_port_xml_rpc = find_free_port()
        hass.data[HM_KEY].default_callback_port_xml_rpc = default_callback_port_xml_rpc

    # Check if this is an initial setup (no devices exist for this entry)
    # If so, enable auto-confirm for new devices during a time window
    device_registry = dr.async_get(hass)
    existing_devices = dr.async_entries_for_config_entry(device_registry, entry.entry_id)
    auto_confirm_until: float | None = None
    if len(existing_devices) == 0:
        auto_confirm_until = time.time() + DEFAULT_AUTO_CONFIRM_NEW_DEVICES_TIMEOUT
        _LOGGER.debug(
            "Initial setup detected for %s. Auto-confirming new devices for %s seconds",
            entry.data.get(CONF_INSTANCE_NAME),
            DEFAULT_AUTO_CONFIRM_NEW_DEVICES_TIMEOUT,
        )

    control = await ControlConfig(
        hass=hass,
        entry_id=entry.entry_id,
        data=entry.data,
        auto_confirm_until=auto_confirm_until,
        default_callback_port_xml_rpc=default_callback_port_xml_rpc,
    ).create_control_unit()
    entry.runtime_data = control
    await hass.config_entries.async_forward_entry_setups(entry, HMIP_LOCAL_PLATFORMS)
    try:
        await control.start_central()
    except AuthFailure as err:
        _LOGGER.warning(
            "Authentication failed for %s. Triggering reauthentication flow",
            entry.data.get(CONF_INSTANCE_NAME),
        )
        raise ConfigEntryAuthFailed("Authentication failed") from err
    await async_setup_services(hass)

    # Register WebSocket commands once (HA raises on duplicate registration)
    if not hass.data.get("homematicip_local_ws_registered"):
        async_register_websocket_commands(hass)
        hass.data["homematicip_local_ws_registered"] = True

    # Register device icon proxy view once
    if not hass.data.get(ICON_VIEW_REGISTERED_KEY):
        hass.http.register_view(DeviceIconView)
        hass.data[ICON_VIEW_REGISTERED_KEY] = True

    # Register or unregister panel based on config entry settings.
    # Only unregister if no loaded config entry has the panel enabled.
    if _any_entry_has_panel_enabled(hass=hass):
        await async_register_panel(hass)
    else:
        async_unregister_panel(hass)

    # Register on HA stop event to gracefully shutdown Homematic(IP) Local connection
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, control.stop_central)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    async_notify_backup_listeners(hass)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: HomematicConfigEntry) -> bool:
    """Unload a config entry."""
    await async_unload_services(hass)
    # First unload platforms so entities can unsubscribe from events
    # (async_will_remove_from_hass is called for each entity)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, HMIP_LOCAL_PLATFORMS)
    # Then stop the central unit
    if hasattr(entry, "runtime_data") and (control := entry.runtime_data):
        await control.stop_central()
    if len(async_get_loaded_config_entries(hass=hass)) == 0:
        async_unregister_panel(hass)
        del hass.data[HM_KEY]
    async_notify_backup_listeners(hass)
    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: HomematicConfigEntry) -> None:
    """Handle removal of an entry."""
    cleanup_files(central_name=entry.data[CONF_INSTANCE_NAME], storage_directory=get_storage_directory(hass=hass))


async def async_remove_config_entry_device(
    hass: HomeAssistant, entry: HomematicConfigEntry, device_entry: dr.DeviceEntry
) -> bool:
    """Remove a config entry from a device."""

    if (address_data := get_device_address_at_interface_from_identifiers(identifiers=device_entry.identifiers)) is None:
        return False

    device_address: str = address_data[0]
    interface_id: str = address_data[1]

    if interface_id and device_address and (control_unit := entry.runtime_data):
        await control_unit.central.device_coordinator.delete_device(
            interface_id=interface_id, device_address=device_address
        )
        _LOGGER.debug(
            "Called delete_device: %s, %s",
            interface_id,
            device_address,
        )
    return True


async def update_listener(hass: HomeAssistant, entry: HomematicConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_migrate_event_entity_unique_ids(hass: HomeAssistant, entry: HomematicConfigEntry) -> None:
    """Migrate event entity unique_ids from channel-based to event_group-based format."""

    @callback
    def update_event_entity_unique_id(entity_entry: er.RegistryEntry) -> dict[str, str] | None:
        """Update unique ID of event entity entry."""
        # Only migrate event platform entities
        if entity_entry.domain != "event":
            return None
        # Check if this is an old-format unique_id (doesn't contain "event_group_")
        if "event_group_" in entity_entry.unique_id:
            return None
        # Extract the channel unique_id part after the domain prefix
        prefix = f"{DOMAIN}_"
        if not entity_entry.unique_id.startswith(prefix):
            return None
        channel_unique_id = entity_entry.unique_id[len(prefix) :]
        # Create new unique_id with event_group format (default to keypress)
        new_unique_id = f"{DOMAIN}_event_group_keypress_{channel_unique_id}"
        _LOGGER.debug(
            "Migrating event entity unique_id: %s -> %s",
            entity_entry.unique_id,
            new_unique_id,
        )
        return {"new_unique_id": new_unique_id}

    await async_migrate_entries(hass, entry.entry_id, update_event_entity_unique_id)


def _migrate_v11_extract_custom_ports(*, data: dict[str, Any]) -> dict[str, Any]:
    """Extract custom (non-default) ports from v11 config entry data."""
    custom_ports: dict[str, int] = {}
    if interfaces := data.get(CONF_INTERFACE):
        for interface_key, interface_config in interfaces.items():
            if isinstance(interface_config, dict) and CONF_PORT in interface_config:
                port = interface_config[CONF_PORT]
                # Get interface name - could be enum or string key
                interface_name = interface_key.value if hasattr(interface_key, "value") else str(interface_key)
                # Check if port is non-default (custom)
                if not is_interface_default_port(interface=interface_name, port=port):
                    custom_ports[interface_name] = port
    # Only add CONF_CUSTOM_PORTS if there are custom ports
    if custom_ports:
        data[CONF_CUSTOM_PORTS] = custom_ports
    return data


def _migrate_v14_remove_deprecated_optional_settings(*, data: dict[str, Any]) -> dict[str, Any]:
    """Remove deprecated OptionalSettings values from v14 config entry data."""
    # Remove deprecated OptionalSettings values that were removed in aiohomematic 2026.1.44
    # - ENABLE_LINKED_ENTITY_CLIMATE_ACTIVITY (now always enabled)
    # - USE_INTERFACE_CLIENT (legacy client removed)
    if CONF_ADVANCED_CONFIG in data and CONF_OPTIONAL_SETTINGS in data[CONF_ADVANCED_CONFIG]:
        valid_settings = {str(s) for s in OptionalSettings}
        current_settings = data[CONF_ADVANCED_CONFIG][CONF_OPTIONAL_SETTINGS]
        filtered_settings = [s for s in current_settings if s in valid_settings]
        if filtered_settings != current_settings:
            data[CONF_ADVANCED_CONFIG] = dict(data[CONF_ADVANCED_CONFIG])
            data[CONF_ADVANCED_CONFIG][CONF_OPTIONAL_SETTINGS] = filtered_settings
    return data


async def async_migrate_entry(hass: HomeAssistant, entry: HomematicConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", entry.version)

    if entry.version == 1:
        data = dict(entry.data)
        data.update({CONF_ENABLE_SYSTEM_NOTIFICATIONS: True})
        hass.config_entries.async_update_entry(entry, version=2, data=data)
    if entry.version == 2:

        @callback
        def update_entity_unique_id(entity_entry: er.RegistryEntry) -> dict[str, str] | None:
            """Update unique ID of entity entry."""
            if entity_entry.unique_id.startswith(f"{DOMAIN}_bidcos_wir"):
                return {
                    "new_unique_id": entity_entry.unique_id.replace(
                        f"{DOMAIN}_bidcos_wir",
                        f"{DOMAIN}_{entry.unique_id}_bidcos_wir",
                    )
                }
            return None

        await async_migrate_entries(hass, entry.entry_id, update_entity_unique_id)

        hass.config_entries.async_update_entry(entry, version=3)
    if entry.version == 3:
        data = dict(entry.data)
        data.update({CONF_UN_IGNORES: []})
        hass.config_entries.async_update_entry(entry, version=4, data=data)
    if entry.version == 4:
        data = dict(entry.data)

        advanced_config = {
            CONF_ENABLE_SYSVAR_SCAN: data.get(CONF_ENABLE_SYSVAR_SCAN, DEFAULT_ENABLE_SYSVAR_SCAN),
            CONF_SYS_SCAN_INTERVAL: data.get(CONF_SYS_SCAN_INTERVAL, DEFAULT_SYS_SCAN_INTERVAL),
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: data.get(
                CONF_ENABLE_SYSTEM_NOTIFICATIONS, DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS
            ),
            CONF_UN_IGNORES: data.get(CONF_UN_IGNORES, DEFAULT_UN_IGNORES),
        }
        default_advanced_config = {
            CONF_ENABLE_SYSVAR_SCAN: DEFAULT_ENABLE_SYSVAR_SCAN,
            CONF_SYS_SCAN_INTERVAL: DEFAULT_SYS_SCAN_INTERVAL,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS,
            CONF_UN_IGNORES: DEFAULT_UN_IGNORES,
        }
        data[CONF_ADVANCED_CONFIG] = {} if advanced_config == default_advanced_config else advanced_config

        def del_param(name: str) -> None:
            with contextlib.suppress(Exception):
                del data[name]

        del_param(name=CONF_ENABLE_SYSVAR_SCAN)
        del_param(name=CONF_SYS_SCAN_INTERVAL)
        del_param(name=CONF_ENABLE_SYSTEM_NOTIFICATIONS)
        del_param(name=CONF_UN_IGNORES)

        cleanup_files(central_name=entry.data[CONF_INSTANCE_NAME], storage_directory=get_storage_directory(hass=hass))
        hass.config_entries.async_update_entry(entry, version=5, data=data)
    if entry.version == 5:
        data = dict(entry.data)
        cleanup_files(central_name=entry.data[CONF_INSTANCE_NAME], storage_directory=get_storage_directory(hass=hass))
        hass.config_entries.async_update_entry(entry, version=6, data=data)
    if entry.version == 6:
        data = dict(entry.data)
        if data.get(CONF_ADVANCED_CONFIG):
            data[CONF_ADVANCED_CONFIG][CONF_ENABLE_PROGRAM_SCAN] = data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SYSVAR_SCAN]
        hass.config_entries.async_update_entry(entry, version=7, data=data)
    if entry.version == 7:
        data = dict(entry.data)
        cleanup_files(central_name=entry.data[CONF_INSTANCE_NAME], storage_directory=get_storage_directory(hass=hass))
        hass.config_entries.async_update_entry(entry, version=8, data=data)
    if entry.version == 8:
        data = dict(entry.data)
        cleanup_files(central_name=entry.data[CONF_INSTANCE_NAME], storage_directory=get_storage_directory(hass=hass))
        hass.config_entries.async_update_entry(entry, version=9, data=data)
    if entry.version == 9:
        data = dict(entry.data)
        if callback_port_xml_rpc := data.get("callback_port"):
            with contextlib.suppress(Exception):
                del data["callback_port"]
            data[CONF_CALLBACK_PORT_XML_RPC] = callback_port_xml_rpc
        hass.config_entries.async_update_entry(entry, version=10, data=data)
    if entry.version == 10:
        data = dict(entry.data)
        # Remove delay_new_device_creation from advanced config (now always True)
        if CONF_ADVANCED_CONFIG in data:
            with contextlib.suppress(Exception):
                del data[CONF_ADVANCED_CONFIG]["delay_new_device_creation"]
        hass.config_entries.async_update_entry(entry, version=11, data=data)
    if entry.version == 11:
        data = _migrate_v11_extract_custom_ports(data=dict(entry.data))
        hass.config_entries.async_update_entry(entry, version=12, data=data)
    if entry.version == 12:
        data = dict(entry.data)
        # Remove action_select_values from config entry data
        # Values are now stored in separate storage file to avoid triggering config entry reload
        with contextlib.suppress(Exception):
            del data[CONF_ACTION_SELECT_VALUES]
        hass.config_entries.async_update_entry(entry, version=13, data=data)
    if entry.version == 13:
        # Migrate event entity unique_ids from channel-based to event_group-based format
        await _async_migrate_event_entity_unique_ids(hass=hass, entry=entry)
        hass.config_entries.async_update_entry(entry, version=14)
    if entry.version == 14:
        data = _migrate_v14_remove_deprecated_optional_settings(data=dict(entry.data))
        hass.config_entries.async_update_entry(entry, version=15, data=data)
    if entry.version == 15:
        data = dict(entry.data)
        if CONF_ADVANCED_CONFIG in data:
            data[CONF_ADVANCED_CONFIG][CONF_COMMAND_THROTTLE_INTERVAL] = DEFAULT_COMMAND_THROTTLE_INTERVAL
        hass.config_entries.async_update_entry(entry, version=16, data=data)
    _LOGGER.info("Migration to version %s successful", entry.version)
    return True
