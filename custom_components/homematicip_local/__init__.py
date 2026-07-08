"""Homematic(IP) Local for OpenCCU is a Python 3 module for Home Assistant and Homematic(IP) devices."""

from __future__ import annotations

from collections.abc import Callable
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
    BACKEND_LOOM,
    CONF_ACTION_SELECT_VALUES,
    CONF_ADVANCED_CONFIG,
    CONF_BACKEND,
    CONF_CALLBACK_PORT_XML_RPC,
    CONF_COMMAND_THROTTLE_INTERVAL,
    CONF_CUSTOM_PORTS,
    CONF_DISABLE_CONFIG_PANEL,
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
    DEFAULT_DISABLE_CONFIG_PANEL,
    DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS,
    DEFAULT_SYS_SCAN_INTERVAL,
    DOMAIN,
    HMIP_LOCAL_MIN_HA_VERSION,
    HMIP_LOCAL_PLATFORMS,
)
from .control_unit import ControlConfig, ControlUnit, get_storage_directory
from .device_icon import ICON_VIEW_REGISTERED_KEY, DeviceIconView
from .panel import async_register_cards, async_register_panel, async_unregister_cards, async_unregister_panel
from .services import async_get_loaded_config_entries, async_setup_services, async_unload_services
from .support import get_aiohomematic_version, get_device_address_at_interface_from_identifiers, realign_hub_unique_id
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
    for entry in hass.config_entries.async_entries(domain=DOMAIN, include_ignore=False, include_disabled=False):
        if entry.data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_DISABLE_CONFIG_PANEL, DEFAULT_DISABLE_CONFIG_PANEL):
            continue
        if hasattr(entry, "runtime_data") and entry.runtime_data:
            return True
    return False


async def async_setup_entry(hass: HomeAssistant, entry: HomematicConfigEntry) -> bool:
    """Set up Homematic(IP) Local for OpenCCU from a config entr11y."""
    # The openccu-loom backend talks to the daemon via openccu-loom-client
    # and does not depend on the aiohomematic runtime version, so skip the
    # aiohomematic version gate for it.
    is_loom_backend = entry.data.get(CONF_BACKEND) == BACKEND_LOOM
    expected_version = await get_aiohomematic_version(hass=hass, domain=entry.domain, package_name="aiohomematic")
    # Only block when the installed aiohomematic is OLDER than the version this
    # release was built against. A newer (patch) version is fine and must not
    # abort setup - HA/pip can legitimately resolve a newer aiohomematic than
    # the manifest pin via transitive, upper-bound-less dependencies.
    if (
        not is_loom_backend
        and expected_version is not None
        and AwesomeVersion(HAHM_VERSION) < AwesomeVersion(expected_version)
    ):
        _LOGGER.error(
            "This release of Homematic(IP) Local for OpenCCU requires aiohomematic version %s or newer, "
            "but found the older version %s. "
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

    # For the openccu-loom backend, migrate any legacy aiohomematic entity
    # unique_ids to the canonical loom/serial scheme before entities are
    # (re)created, so existing entities keep their identity on cutover.
    if is_loom_backend:
        await _async_migrate_loom_unique_ids(hass, entry)
    else:
        # Switched back from loom: strip the loom_ namespace. Then align any
        # legacy entry_id-anchored hub keys onto the CCU-serial scheme.
        await _async_restore_aiohomematic_unique_ids(hass, entry)
        await _async_migrate_aiohomematic_hub_unique_ids(hass, entry)

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
        # The config entry's HA unique_id is the CCU serial; inject it so
        # the loom backend keys entities identically to the unique_id
        # registry migration above.
        serial=entry.unique_id,
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
    if not is_loom_backend:
        await _async_reanchor_hub_unique_ids_on_serial_change(hass, entry, control)
    await async_setup_services(hass)

    # Register WebSocket commands once (HA raises on duplicate registration)
    if not hass.data.get("homematicip_local_ws_registered"):
        async_register_websocket_commands(hass)
        hass.data["homematicip_local_ws_registered"] = True

    # Register device icon proxy view once
    if not hass.data.get(ICON_VIEW_REGISTERED_KEY):
        hass.http.register_view(DeviceIconView)
        hass.data[ICON_VIEW_REGISTERED_KEY] = True

    # Register or unregister panel based on config entry settings and backend type.
    # Panel is enabled by default for CCU backends only.
    if _any_entry_has_panel_enabled(hass=hass):
        await async_register_panel(hass)
    else:
        async_unregister_panel(hass)

    # Register Lovelace cards (always, independent of panel setting)
    await async_register_cards(hass)

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
        async_unregister_cards(hass)
        del hass.data[HM_KEY]
    elif not _any_entry_has_panel_enabled(hass=hass):
        async_unregister_panel(hass)
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


def _loom_migrated_unique_id(unique_id: str, *, entry_suffix: str, serial_suffix: str) -> str | None:
    """Map a legacy aiohomematic HA ``unique_id`` to the loom/serial scheme.

    HA stores ``{DOMAIN}_<routing-key>``. The openccu-loom backend keys its
    data points with the canonical ``loom_<routing-key>`` (the CCU serial
    suffix fills the central-id slot of hub / internal / virtual-remote
    keys, replacing aiohomematic's ``entry_id[-10:]`` prefix). This rewrites
    the legacy key to the loom one; see openccu-loom
    ``docs/external-clients/ha-unique-id-migration.md``.

    Returns ``None`` when no rewrite applies: already migrated, not one of
    our entities, or a synthetic entity that is not a data-point routing key
    (the per-central backup button, and the legacy event-group entities the
    loom backend does not emit yet — those are out of scope here).
    """
    prefix = f"{DOMAIN}_"
    if not unique_id.startswith(prefix):
        return None
    key = unique_id[len(prefix) :]
    if key.startswith("loom_"):  # idempotent
        return None
    if key.endswith("_create_backup") or key.startswith("event_group_"):
        return None
    # Hub / internal / virtual-remote keys carried the entry_id suffix as
    # their prefix; swap it for the CCU serial suffix. Everything else
    # (devices, channels, custom DPs) carried no central prefix.
    entry_prefix = f"{entry_suffix}_"
    if key.startswith(entry_prefix):
        return f"{prefix}loom_{serial_suffix}_{key[len(entry_prefix) :]}"
    return f"{prefix}loom_{key}"


async def _async_migrate_loom_unique_ids(hass: HomeAssistant, entry: HomematicConfigEntry) -> None:
    """Rewrite legacy entity unique_ids to the loom/serial scheme.

    Runs once, early in setup, for the openccu-loom backend. A config entry
    switched from the CCU backend still holds aiohomematic-era keys in the
    entity registry; the loom backend produces canonical ``loom_`` keys, so
    without this rewrite every entity would orphan (losing history, area and
    customisations). The rewrite is purely string-level, idempotent, and
    scoped to this entry, so it is safe to run on every setup.
    """
    serial = entry.unique_id  # the config entry's HA unique_id is the CCU serial
    if not serial:
        _LOGGER.warning(
            "Skipping loom unique_id migration for %s: config entry has no serial",
            entry.data.get(CONF_INSTANCE_NAME),
        )
        return
    entry_suffix = entry.entry_id[-10:]
    serial_suffix = serial[-10:].lower()

    @callback
    def _migrator(entity_entry: er.RegistryEntry) -> dict[str, str] | None:
        new_unique_id = _loom_migrated_unique_id(
            entity_entry.unique_id,
            entry_suffix=entry_suffix,
            serial_suffix=serial_suffix,
        )
        if new_unique_id is None or new_unique_id == entity_entry.unique_id:
            return None
        _LOGGER.debug(
            "Migrating unique_id to loom scheme: %s -> %s",
            entity_entry.unique_id,
            new_unique_id,
        )
        return {"new_unique_id": new_unique_id}

    await async_migrate_entries(hass, entry.entry_id, _migrator)


def _aiohomematic_restored_unique_id(unique_id: str) -> str | None:
    """Strip the ``loom_`` namespace from an HA ``unique_id``.

    The inverse of :func:`_loom_migrated_unique_id`. Both backends now anchor
    hub / internal / virtual-remote entities on the CCU serial (see
    ``central_id`` in :mod:`.control_unit`), so the two schemes differ only by
    the ``loom_`` namespace and restoring a key is a plain prefix strip — the
    serial-anchored central-id slot is already correct, no swap needed.

    Returns ``None`` when no rewrite applies: not one of our entities, or
    already in the aiohomematic scheme (no ``loom_`` namespace).
    """
    prefix = f"{DOMAIN}_"
    if not unique_id.startswith(prefix):
        return None
    key = unique_id[len(prefix) :]
    if not key.startswith("loom_"):  # idempotent: already aiohomematic-scheme
        return None
    body = key[len("loom_") :]
    return f"{prefix}{body}"


async def _async_restore_aiohomematic_unique_ids(hass: HomeAssistant, entry: HomematicConfigEntry) -> None:
    """Rewrite loom entity unique_ids back to the aiohomematic scheme.

    Runs once, early in setup, for the aiohomematic backend. A config entry
    switched back from the openccu-loom backend still holds canonical
    ``loom_`` keys in the entity registry; aiohomematic produces un-namespaced
    keys, so without this rewrite every entity would orphan (losing history,
    area and customisations). The inverse of
    :func:`_async_migrate_loom_unique_ids`, it is purely string-level,
    idempotent, and scoped to this entry, so it is safe to run on every setup.
    """

    @callback
    def _migrator(entity_entry: er.RegistryEntry) -> dict[str, str] | None:
        new_unique_id = _aiohomematic_restored_unique_id(entity_entry.unique_id)
        if new_unique_id is None or new_unique_id == entity_entry.unique_id:
            return None
        _LOGGER.debug(
            "Restoring unique_id to aiohomematic scheme: %s -> %s",
            entity_entry.unique_id,
            new_unique_id,
        )
        return {"new_unique_id": new_unique_id}

    await async_migrate_entries(hass, entry.entry_id, _migrator)


async def _async_realign_hub_unique_ids(hass: HomeAssistant, entry: HomematicConfigEntry, *, central_id: str) -> None:
    """Force the central-id slot of every hub / virtual-remote registry key onto ``central_id``.

    Entry-scoped, idempotent and collision-safe. Hub / install-mode / program /
    sysvar / internal / virtual-remote keys (and the virtual-remote event groups)
    carry a central-id slot; this rewrites whatever value sits there onto the live
    ``central_id`` regardless of the old value, so a registry inherited from an
    earlier anchor (legacy ``entry_id[-10:]``, a prior serial, or a stale slot from
    a delete + re-add) realigns onto the live key instead of orphaning and being
    deleted by the orphan-cleanup sweep. Device / channel / custom-DP keys carry no
    slot and are left untouched.
    """
    entity_registry = er.async_get(hass)

    @callback
    def _migrator(entity_entry: er.RegistryEntry) -> dict[str, str] | None:
        new_unique_id = realign_hub_unique_id(entity_entry.unique_id, central_id=central_id)
        if new_unique_id is None or new_unique_id == entity_entry.unique_id:
            return None
        # A live-anchored entry may already exist (e.g. created under the live
        # anchor by an earlier setup); HA raises on a duplicate unique_id, so skip
        # rather than abort the whole migration.
        if entity_registry.async_get_entity_id(entity_entry.domain, entity_entry.platform, new_unique_id):
            _LOGGER.debug(
                "Skipping hub unique_id realign, target already exists: %s -> %s",
                entity_entry.unique_id,
                new_unique_id,
            )
            return None
        _LOGGER.debug(
            "Realigning hub unique_id onto the live central id: %s -> %s",
            entity_entry.unique_id,
            new_unique_id,
        )
        return {"new_unique_id": new_unique_id}

    await async_migrate_entries(hass, entry.entry_id, _migrator)


async def _async_migrate_aiohomematic_hub_unique_ids(hass: HomeAssistant, entry: HomematicConfigEntry) -> None:
    """Realign hub / virtual-remote unique_ids onto the live central id.

    aiohomematic anchors hub / sysvar / program / install-mode / internal /
    virtual-remote entities (and their event groups) on the central id — the CCU
    serial when known, else ``entry_id[-10:]`` (see ``central_id`` in
    :mod:`.control_unit`). A registry inherited from a different anchor (legacy
    ``entry_id``-prefixed keys, or a stale slot left by a delete + re-add) would
    otherwise no longer match the live keys, orphan, and be permanently deleted by
    the orphan-cleanup sweep. This one-time, entry-scoped, collision-safe rewrite
    runs early in setup, before entities are (re)created, and is a no-op once
    everything is on the live anchor. Device / channel keys carry no central slot
    and are left untouched.
    """
    central_id = (entry.unique_id or entry.entry_id)[-10:].lower()
    await _async_realign_hub_unique_ids(hass, entry, central_id=central_id)


async def _async_reanchor_hub_unique_ids_on_serial_change(
    hass: HomeAssistant, entry: HomematicConfigEntry, control: ControlUnit
) -> None:
    """Re-anchor hub unique_ids when the connected CCU serial has changed.

    The CCU serial (read from the radio module) anchors hub / sysvar /
    program / install-mode / internal / virtual-remote unique_ids and the
    config-entry identity. It is stable in normal operation but changes on a
    radio-module (Funkmodul) swap. When the freshly-connected serial differs
    from the stored one, this realigns those keys onto the new serial, updates
    the entry's unique_id and reloads so the running central rebuilds on the new
    anchor. A no-op when the serial is unchanged or unknown.
    """
    old_serial = entry.unique_id
    new_serial = control.central.system_information.serial
    if not old_serial or not new_serial or new_serial.lower() == "unknown":
        return
    if new_serial.lower() == old_serial.lower():
        return

    _LOGGER.warning(
        "CCU serial for %s changed (%s -> %s); re-anchoring hub entities and reloading",
        entry.data.get(CONF_INSTANCE_NAME),
        old_serial,
        new_serial,
    )
    await _async_realign_hub_unique_ids(hass, entry, central_id=new_serial[-10:].lower())
    hass.config_entries.async_update_entry(entry, unique_id=new_serial)
    hass.config_entries.async_schedule_reload(entry.entry_id)


def _migrate_v11_extract_custom_ports(data: dict[str, Any]) -> dict[str, Any]:
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


def _migrate_v14_remove_deprecated_optional_settings(data: dict[str, Any]) -> dict[str, Any]:
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


def _migrate_v1_to_v2_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v1 to v2: enable system notifications by default."""
    data[CONF_ENABLE_SYSTEM_NOTIFICATIONS] = True
    return data


def _migrate_v3_to_v4_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v3 to v4: introduce un-ignores list."""
    data[CONF_UN_IGNORES] = []
    return data


def _migrate_v6_to_v7_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v6 to v7: derive program scan from sysvar scan."""
    if data.get(CONF_ADVANCED_CONFIG):
        data[CONF_ADVANCED_CONFIG][CONF_ENABLE_PROGRAM_SCAN] = data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SYSVAR_SCAN]
    return data


def _migrate_v2_unique_id(entry: HomematicConfigEntry) -> Callable[[er.RegistryEntry], dict[str, str] | None]:
    """Return entity-id migration callback used by v2->v3."""

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

    return update_entity_unique_id


def _migrate_v4_to_v5_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v4 to v5: collapse advanced settings and drop legacy keys."""
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

    for key in (CONF_ENABLE_SYSVAR_SCAN, CONF_SYS_SCAN_INTERVAL, CONF_ENABLE_SYSTEM_NOTIFICATIONS, CONF_UN_IGNORES):
        with contextlib.suppress(KeyError):
            del data[key]

    return data


def _migrate_v9_to_v10_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v9 to v10: rename callback_port to CONF_CALLBACK_PORT_XML_RPC."""
    if callback_port_xml_rpc := data.get("callback_port"):
        with contextlib.suppress(KeyError):
            del data["callback_port"]
        data[CONF_CALLBACK_PORT_XML_RPC] = callback_port_xml_rpc
    return data


def _migrate_v10_to_v11_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v10 to v11: drop delay_new_device_creation."""
    if CONF_ADVANCED_CONFIG in data:
        with contextlib.suppress(KeyError):
            del data[CONF_ADVANCED_CONFIG]["delay_new_device_creation"]
    return data


def _migrate_v12_to_v13_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v12 to v13: drop action_select_values from entry data."""
    with contextlib.suppress(KeyError):
        del data[CONF_ACTION_SELECT_VALUES]
    return data


def _migrate_v15_to_v16_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v15 to v16: introduce command throttle interval default."""
    if CONF_ADVANCED_CONFIG in data:
        data[CONF_ADVANCED_CONFIG][CONF_COMMAND_THROTTLE_INTERVAL] = DEFAULT_COMMAND_THROTTLE_INTERVAL
    return data


def _migrate_v16_to_v17_data(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate config entry data from v16 to v17: drop legacy enable_config_panel key."""
    if CONF_ADVANCED_CONFIG in data:
        # Panel is now enabled by default
        data[CONF_ADVANCED_CONFIG].pop("enable_config_panel", None)
    return data


# Dispatch table for pure data-only migrations (no hass / async work).
# Each entry maps from-version -> data transformer. The to-version is always from + 1.
_DATA_MIGRATIONS: dict[int, Callable[[dict[str, Any]], dict[str, Any]]] = {
    1: _migrate_v1_to_v2_data,
    3: _migrate_v3_to_v4_data,
    6: _migrate_v6_to_v7_data,
    9: _migrate_v9_to_v10_data,
    10: _migrate_v10_to_v11_data,
    11: _migrate_v11_extract_custom_ports,
    12: _migrate_v12_to_v13_data,
    14: _migrate_v14_remove_deprecated_optional_settings,
    15: _migrate_v15_to_v16_data,
    16: _migrate_v16_to_v17_data,
}

# Versions whose only side effect is calling cleanup_files() before bumping the version.
_CLEANUP_FILE_VERSIONS = frozenset({5, 7, 8})


async def async_migrate_entry(hass: HomeAssistant, entry: HomematicConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", entry.version)

    while entry.version < 17:
        version = entry.version
        if migrator := _DATA_MIGRATIONS.get(version):
            data = migrator(dict(entry.data))
            hass.config_entries.async_update_entry(entry, version=version + 1, data=data)
        elif version in _CLEANUP_FILE_VERSIONS:
            cleanup_files(
                central_name=entry.data[CONF_INSTANCE_NAME], storage_directory=get_storage_directory(hass=hass)
            )
            hass.config_entries.async_update_entry(entry, version=version + 1, data=dict(entry.data))
        elif version == 2:
            await async_migrate_entries(hass, entry.entry_id, _migrate_v2_unique_id(entry))
            hass.config_entries.async_update_entry(entry, version=3)
        elif version == 4:
            data = _migrate_v4_to_v5_data(data=dict(entry.data))
            cleanup_files(
                central_name=entry.data[CONF_INSTANCE_NAME], storage_directory=get_storage_directory(hass=hass)
            )
            hass.config_entries.async_update_entry(entry, version=5, data=data)
        elif version == 13:
            # Migrate event entity unique_ids from channel-based to event_group-based format
            await _async_migrate_event_entity_unique_ids(hass=hass, entry=entry)
            hass.config_entries.async_update_entry(entry, version=14)
        else:
            break  # Unknown version - stop migrating to avoid infinite loop

    _LOGGER.info("Migration to version %s successful", entry.version)
    return True
