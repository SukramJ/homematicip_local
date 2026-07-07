"""Test the Homematic(IP) Local for OpenCCU init."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from aiohomematic.const import IDENTIFIER_SEPARATOR, CentralState, DeviceTriggerEventType
from aiohomematic.exceptions import AuthFailure
import custom_components.homematicip_local
from custom_components.homematicip_local import (
    _aiohomematic_restored_unique_id,
    _async_migrate_aiohomematic_hub_unique_ids,
    _async_reanchor_hub_unique_ids_on_serial_change,
    _async_restore_aiohomematic_unique_ids,
    _loom_migrated_unique_id,
)
from custom_components.homematicip_local.config_flow import DomainConfigFlow
from custom_components.homematicip_local.const import (
    BACKEND_CCU,
    BACKEND_LOOM,
    CONF_ADVANCED_CONFIG,
    CONF_OPTIONAL_SETTINGS,
    DOMAIN as HMIP_DOMAIN,
)
from custom_components.homematicip_local.control_unit import ControlUnit
from custom_components.homematicip_local.support import realign_hub_unique_id
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from tests import const


class TestSetupEntry:
    """Tests for setup entry functionality."""

    async def test_setup_entry(
        self,
        hass: HomeAssistant,
        mock_config_entry_v2: MockConfigEntry,
        mock_control_unit: ControlUnit,
    ) -> None:
        """Test setup entry."""
        # no config_entry exists
        assert len(hass.config_entries.async_entries(HMIP_DOMAIN)) == 0
        assert not hass.data.get(HMIP_DOMAIN)

        with (
            patch("custom_components.homematicip_local.find_free_port", return_value=8765),
            patch(
                "custom_components.homematicip_local.control_unit.ControlConfig.create_control_unit",
                return_value=mock_control_unit,
            ),
        ):
            mock_config_entry_v2.add_to_hass(hass)
            await hass.config_entries.async_setup(mock_config_entry_v2.entry_id)
            await hass.async_block_till_done()
            config_entries = hass.config_entries.async_entries(HMIP_DOMAIN)
            assert len(config_entries) == 1
            config_entry = config_entries[0]
            assert config_entry.state == ConfigEntryState.LOADED

    async def test_setup_entry_auth_failure(
        self,
        hass: HomeAssistant,
        mock_config_entry_v2: MockConfigEntry,
        mock_control_unit: ControlUnit,
    ) -> None:
        """Test setup entry with authentication failure triggers reauth."""
        # Configure mock to raise AuthFailure during start_central
        mock_control_unit.start_central = AsyncMock(side_effect=AuthFailure("Invalid credentials"))

        with (
            patch("custom_components.homematicip_local.find_free_port", return_value=8765),
            patch(
                "custom_components.homematicip_local.control_unit.ControlConfig.create_control_unit",
                return_value=mock_control_unit,
            ),
        ):
            mock_config_entry_v2.add_to_hass(hass)

            # Setup should fail with auth error
            result = await hass.config_entries.async_setup(mock_config_entry_v2.entry_id)
            await hass.async_block_till_done()

            # Verify setup failed and entry is in SETUP_ERROR state
            assert result is False
            assert mock_config_entry_v2.state == ConfigEntryState.SETUP_ERROR

            # Verify a reauth flow was triggered via the repair issue
            from homeassistant.helpers import issue_registry as ir

            issue_reg = ir.async_get(hass)
            issue = issue_reg.async_get_issue(
                domain="homeassistant",
                issue_id=f"config_entry_reauth_{HMIP_DOMAIN}_{mock_config_entry_v2.entry_id}",
            )
            assert issue is not None
            assert issue.translation_key == "config_entry_reauth"


class TestCheckMinVersion:
    """Tests for minimum version check."""

    async def test_check_min_version(
        self,
        hass: HomeAssistant,
        mock_config_entry_v2: MockConfigEntry,
        mock_control_unit: ControlUnit,
    ) -> None:
        """Test check_min_version."""
        # no config_entry exists

        orig_version = custom_components.homematicip_local.HMIP_LOCAL_MIN_HA_VERSION
        custom_components.homematicip_local.HMIP_LOCAL_MIN_HA_VERSION = "2099.1.1"
        mock_config_entry_v2.add_to_hass(hass)
        assert await hass.config_entries.async_setup(mock_config_entry_v2.entry_id) is False
        custom_components.homematicip_local.HMIP_LOCAL_MIN_HA_VERSION = orig_version


class TestMigrateEntry:
    """Tests for entry migration."""

    async def test_migrate_entry(
        self,
        hass: HomeAssistant,
        mock_config_entry_v1: MockConfigEntry,
        mock_control_unit: ControlUnit,
    ) -> None:
        """Test setup entry."""
        # no config_entry exists
        assert len(hass.config_entries.async_entries(HMIP_DOMAIN)) == 0
        assert not hass.data.get(HMIP_DOMAIN)

        with (
            patch("custom_components.homematicip_local.find_free_port", return_value=8765),
            patch(
                "custom_components.homematicip_local.control_unit.ControlConfig.create_control_unit",
                return_value=mock_control_unit,
            ),
        ):
            mock_config_entry_v1.add_to_hass(hass)
            await hass.config_entries.async_setup(mock_config_entry_v1.entry_id)
            await hass.async_block_till_done()
            config_entries = hass.config_entries.async_entries(HMIP_DOMAIN)
            assert len(config_entries) == 1
            config_entry = config_entries[0]
            assert config_entry.state == ConfigEntryState.LOADED
            assert config_entry.version == DomainConfigFlow.VERSION
            assert config_entry.data[CONF_ADVANCED_CONFIG] == {
                "command_throttle_interval": 0.1,
                "enable_system_notifications": True,
                "program_scan_enabled": False,
                "sysvar_scan_enabled": False,
                "sysvar_scan_interval": 30,
                "un_ignore": [],
            }

    async def test_migrate_entry_v14_removes_deprecated_optional_settings(
        self,
        hass: HomeAssistant,
        mock_control_unit: ControlUnit,
    ) -> None:
        """Test migration from v14 removes deprecated OptionalSettings values."""
        # Create a v14 config entry with deprecated optional settings
        entry_data = {
            "instance_name": const.INSTANCE_NAME,
            "host": const.HOST,
            "username": const.USERNAME,
            "password": const.PASSWORD,
            "tls": False,
            "verify_tls": False,
            "interface": {"HmIP-RF": {"port": 2010}},
            "advanced_config": {
                "enable_system_notifications": True,
                "sysvar_scan_enabled": False,
                "sysvar_scan_interval": 30,
                "program_scan_enabled": False,
                "un_ignore": [],
                # Deprecated values that should be removed
                "optional_settings": [
                    "ENABLE_LINKED_ENTITY_CLIMATE_ACTIVITY",
                    "USE_INTERFACE_CLIENT",
                    "SR_DISABLE_RANDOMIZED_OUTPUT",  # Valid - should be kept
                ],
            },
        }

        mock_config_entry_v14 = MockConfigEntry(
            entry_id=const.CONFIG_ENTRY_ID,
            version=14,
            domain=HMIP_DOMAIN,
            title=const.INSTANCE_NAME,
            data=entry_data,
            options={},
            pref_disable_new_entities=False,
            pref_disable_polling=False,
            source="user",
            unique_id=const.CONFIG_ENTRY_UNIQUE_ID,
            disabled_by=None,
        )

        with (
            patch("custom_components.homematicip_local.find_free_port", return_value=8765),
            patch(
                "custom_components.homematicip_local.control_unit.ControlConfig.create_control_unit",
                return_value=mock_control_unit,
            ),
        ):
            mock_config_entry_v14.add_to_hass(hass)
            await hass.config_entries.async_setup(mock_config_entry_v14.entry_id)
            await hass.async_block_till_done()
            config_entries = hass.config_entries.async_entries(HMIP_DOMAIN)
            assert len(config_entries) == 1
            config_entry = config_entries[0]
            assert config_entry.state == ConfigEntryState.LOADED
            assert config_entry.version == DomainConfigFlow.VERSION

            # Check that deprecated values were removed and valid ones kept
            optional_settings = config_entry.data[CONF_ADVANCED_CONFIG].get(CONF_OPTIONAL_SETTINGS, [])
            assert "ENABLE_LINKED_ENTITY_CLIMATE_ACTIVITY" not in optional_settings
            assert "USE_INTERFACE_CLIENT" not in optional_settings
            assert "SR_DISABLE_RANDOMIZED_OUTPUT" in optional_settings


class TestUnloadEntry:
    """Tests for unload entry functionality."""

    async def test_unload_entry(self, hass: HomeAssistant, mock_loaded_config_entry: MockConfigEntry) -> None:
        """Test unload entry."""
        assert hass.data[HMIP_DOMAIN]
        assert mock_loaded_config_entry.state == ConfigEntryState.LOADED
        assert await hass.config_entries.async_unload(mock_loaded_config_entry.entry_id) is True
        assert mock_loaded_config_entry.state == ConfigEntryState.NOT_LOADED
        await hass.async_block_till_done()

    # assert HMIP_DOMAIN not in hass.data
    # retry possible?
    # assert await hass.config_entries.async_unload(mock_loaded_config_entry.entry_id) is False


async def test_remove_entry(hass: HomeAssistant, mock_loaded_config_entry: MockConfigEntry) -> None:
    """Test unload entry."""
    assert hass.data[HMIP_DOMAIN]
    assert mock_loaded_config_entry.state == ConfigEntryState.LOADED
    await hass.config_entries.async_remove(mock_loaded_config_entry.entry_id)
    assert mock_loaded_config_entry.state == ConfigEntryState.NOT_LOADED
    await hass.async_block_till_done()
    # assert HMIP_DOMAIN not in hass.data


async def test_reload_entry(hass: HomeAssistant, mock_loaded_config_entry: MockConfigEntry) -> None:
    """Test unload entry."""
    assert mock_loaded_config_entry.title == const.INSTANCE_NAME
    assert hass.data[HMIP_DOMAIN]
    hass.config_entries.async_update_entry(mock_loaded_config_entry, title="Reload")
    await hass.async_block_till_done()
    assert hass.data[HMIP_DOMAIN]
    assert mock_loaded_config_entry.title == "Reload"


def _build_orphan_sweep_self(
    hass: HomeAssistant,
    entry_id: str,
    *,
    state: CentralState = CentralState.RUNNING,
    data_point_unique_ids: tuple[str, ...] = (),
    hub_unique_ids: tuple[str, ...] = (),
    event_group_unique_ids: tuple[str, ...] = (),
    alarm_messages_unique_id: str | None = None,
    service_messages_unique_id: str | None = None,
    inbox_unique_id: str | None = None,
    update_unique_id: str | None = None,
    metrics_unique_ids: tuple[str, str, str] | None = None,
    connectivity_unique_ids: tuple[str, ...] = (),
    install_mode_unique_ids: tuple[tuple[str, str], ...] = (),
    known_device_addresses: tuple[str, ...] = (),
    backend: str = BACKEND_CCU,
    central_id: str = "11a0001234",
) -> SimpleNamespace:
    """Build a minimal ControlUnit-shaped self for _async_cleanup_orphaned_entity_registry_entries."""
    central = MagicMock()
    central.state = state
    central.device_coordinator.devices = tuple(SimpleNamespace(address=address) for address in known_device_addresses)
    central.query_facade.get_data_points.return_value = tuple(
        SimpleNamespace(unique_id=uid) for uid in data_point_unique_ids
    )
    central.hub_coordinator.get_hub_data_points.return_value = tuple(
        SimpleNamespace(unique_id=uid) for uid in hub_unique_ids
    )
    central.hub_coordinator.alarm_messages_dp = (
        SimpleNamespace(unique_id=alarm_messages_unique_id) if alarm_messages_unique_id else None
    )
    central.hub_coordinator.service_messages_dp = (
        SimpleNamespace(unique_id=service_messages_unique_id) if service_messages_unique_id else None
    )
    central.hub_coordinator.inbox_dp = SimpleNamespace(unique_id=inbox_unique_id) if inbox_unique_id else None
    central.hub_coordinator.update_dp = SimpleNamespace(unique_id=update_unique_id) if update_unique_id else None
    if metrics_unique_ids is None:
        central.hub_coordinator.metrics_dps = None
    else:
        sh, cl, le = metrics_unique_ids
        central.hub_coordinator.metrics_dps = SimpleNamespace(
            system_health=SimpleNamespace(unique_id=sh),
            connection_latency=SimpleNamespace(unique_id=cl),
            last_event_age=SimpleNamespace(unique_id=le),
        )
    central.hub_coordinator.connectivity_dps = {
        uid: SimpleNamespace(sensor=SimpleNamespace(unique_id=uid)) for uid in connectivity_unique_ids
    }
    central.hub_coordinator.install_mode_dps = {
        button_uid: SimpleNamespace(
            button=SimpleNamespace(unique_id=button_uid),
            sensor=SimpleNamespace(unique_id=sensor_uid),
        )
        for button_uid, sensor_uid in install_mode_unique_ids
    }
    central.query_facade.get_event_groups.return_value = tuple(
        SimpleNamespace(unique_id=uid) for uid in event_group_unique_ids
    )
    return SimpleNamespace(
        _hass=hass,
        _entry_id=entry_id,
        _central=central,
        _config=SimpleNamespace(backend=backend, central_id=central_id),
    )


async def test_cleanup_orphan_entries_removes_disabled_entity_without_data_point(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """Disabled entity without a corresponding data point is removed."""
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    alive_entity = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_alive_dp",
        config_entry=mock_config_entry_v2,
    )
    orphan_disabled = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_orphan_dp",
        config_entry=mock_config_entry_v2,
        disabled_by=er.RegistryEntryDisabler.USER,
    )
    assert orphan_disabled.disabled

    fake_self = _build_orphan_sweep_self(hass, entry_id, data_point_unique_ids=("alive_dp",))
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    assert entity_registry.async_get(alive_entity.entity_id) is not None
    assert entity_registry.async_get(orphan_disabled.entity_id) is None


async def test_cleanup_orphan_entries_skipped_on_loom_backend(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """The sweep is skipped for the loom backend (partial hub-coordinator surface)."""
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    orphan_disabled = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_orphan_dp",
        config_entry=mock_config_entry_v2,
        disabled_by=er.RegistryEntryDisabler.USER,
    )

    # No data points reported: on the CCU backend this would orphan the entry,
    # but the loom backend must skip the sweep entirely and leave it untouched.
    fake_self = _build_orphan_sweep_self(hass, entry_id, backend=BACKEND_LOOM)
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    assert entity_registry.async_get(orphan_disabled.entity_id) is not None


async def test_cleanup_orphan_entries_recognizes_hub_and_event_unique_ids(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """Hub data points and event groups must protect their entries from cleanup."""
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    sysvar_entity = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_sysvar_dp",
        config_entry=mock_config_entry_v2,
        disabled_by=er.RegistryEntryDisabler.USER,
    )
    event_entity = entity_registry.async_get_or_create(
        domain="event",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_event_group_dp",
        config_entry=mock_config_entry_v2,
    )

    fake_self = _build_orphan_sweep_self(
        hass,
        entry_id,
        hub_unique_ids=("sysvar_dp",),
        event_group_unique_ids=("event_group_dp",),
    )
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    assert entity_registry.async_get(sysvar_entity.entity_id) is not None
    assert entity_registry.async_get(event_entity.entity_id) is not None
    # get_event_groups must have been queried for every DeviceTriggerEventType
    assert fake_self._central.query_facade.get_event_groups.call_count == len(list(DeviceTriggerEventType))


async def test_cleanup_orphan_entries_skipped_when_central_not_running(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """No cleanup when central is not RUNNING (avoids deleting entries during degraded startup)."""
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_some_dp",
        config_entry=mock_config_entry_v2,
        disabled_by=er.RegistryEntryDisabler.USER,
    )

    fake_self = _build_orphan_sweep_self(hass, entry_id, state=CentralState.DEGRADED)
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    # Entry survives because the sweep bailed out early
    assert entity_registry.async_get(entry.entity_id) is not None
    fake_self._central.query_facade.get_data_points.assert_not_called()


async def test_cleanup_orphan_entries_ignores_other_platforms(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """Entries from other platforms must not be touched even with matching config entry."""
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    foreign_entry = entity_registry.async_get_or_create(
        domain="sensor",
        platform="some_other_integration",
        unique_id="foreign_uid",
        config_entry=mock_config_entry_v2,
        disabled_by=er.RegistryEntryDisabler.USER,
    )

    fake_self = _build_orphan_sweep_self(hass, entry_id)
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    assert entity_registry.async_get(foreign_entry.entity_id) is not None


async def test_cleanup_orphan_entries_keeps_native_backup_button(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """The integration-native backup button has no data point but must never be swept."""
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    backup_button = entity_registry.async_get_or_create(
        domain="button",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_openccu_create_backup",
        config_entry=mock_config_entry_v2,
    )

    # No data points reported at all -> without the guard the backup button would orphan.
    fake_self = _build_orphan_sweep_self(hass, entry_id)
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    assert entity_registry.async_get(backup_button.entity_id) is not None


async def test_cleanup_orphan_entries_keeps_central_id_drift(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """A hub entry on a stale central-id anchor whose data point still exists must not be deleted."""
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    # Registry anchored on a stale central id; the live data point uses the current one.
    drifted = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_w78v4413eq_sysvar_x",
        config_entry=mock_config_entry_v2,
        disabled_by=er.RegistryEntryDisabler.USER,
    )

    fake_self = _build_orphan_sweep_self(
        hass,
        entry_id,
        central_id="11a0001234",
        hub_unique_ids=("11a0001234_sysvar_x",),
    )
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    # The drifted entry stays (the setup-time realign migration owns re-anchoring it),
    # rather than being permanently deleted.
    assert entity_registry.async_get(drifted.entity_id) is not None


async def test_cleanup_orphan_entries_recognizes_all_hub_data_point_sources(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """Singleton/mapping hub data points (inbox, update, alarm/service messages, metrics, connectivity, install_mode) must protect their entries."""
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    hub_unique_ids = (
        "hub_inbox",
        "hub_system-update",
        "hub_alarm-messages",
        "hub_service-messages",
        "hub_system-health",
        "hub_connection-latency",
        "hub_last-event-age",
        "hub_connectivity-hmip-rf",
        "install_mode_hmip-button",
        "install_mode_hmip",
    )
    created = [
        entity_registry.async_get_or_create(
            domain="sensor",
            platform=HMIP_DOMAIN,
            unique_id=f"{HMIP_DOMAIN}_{uid}",
            config_entry=mock_config_entry_v2,
        )
        for uid in hub_unique_ids
    ]

    fake_self = _build_orphan_sweep_self(
        hass,
        entry_id,
        inbox_unique_id="hub_inbox",
        update_unique_id="hub_system-update",
        alarm_messages_unique_id="hub_alarm-messages",
        service_messages_unique_id="hub_service-messages",
        metrics_unique_ids=("hub_system-health", "hub_connection-latency", "hub_last-event-age"),
        connectivity_unique_ids=("hub_connectivity-hmip-rf",),
        install_mode_unique_ids=(("install_mode_hmip-button", "install_mode_hmip"),),
    )
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    for entry in created:
        assert entity_registry.async_get(entry.entity_id) is not None, f"{entry.entity_id} was unexpectedly removed"


async def test_cleanup_orphan_entries_skipped_when_data_load_incomplete(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """
    A near-total wipe must be refused (regression for #3215).

    The central can report RUNNING (all clients connected) while the device
    descriptions failed to load (e.g. transient auth error during a CCU restore).
    ``get_data_points()`` then returns only the few devices that did load, which
    would make almost every registry entry look orphaned. Deleting them is
    permanent and breaks dashboards/automations, so the sweep must bail out.
    """
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    created = [
        entity_registry.async_get_or_create(
            domain="sensor",
            platform=HMIP_DOMAIN,
            unique_id=f"{HMIP_DOMAIN}_dp_{index}",
            config_entry=mock_config_entry_v2,
        )
        for index in range(10)
    ]

    # Only one of ten data points loaded -> 9/10 would be orphaned (90% > threshold).
    fake_self = _build_orphan_sweep_self(hass, entry_id, data_point_unique_ids=("dp_0",))
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    for entry in created:
        assert entity_registry.async_get(entry.entity_id) is not None, (
            f"{entry.entity_id} was deleted despite an incomplete device load"
        )


def _create_alive_entities(
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    count: int,
) -> tuple[str, ...]:
    """Create ``count`` entities whose data points are reported alive; return their unique_id stems."""
    stems = tuple(f"alive_{index}" for index in range(count))
    for stem in stems:
        entity_registry.async_get_or_create(
            domain="sensor",
            platform=HMIP_DOMAIN,
            unique_id=f"{HMIP_DOMAIN}_{stem}",
            config_entry=mock_config_entry,
        )
    return stems


async def test_cleanup_orphan_entries_keeps_entry_of_not_yet_loaded_device(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """
    A device entry whose device is not (yet) loaded must be kept, not swept.

    When the central reports RUNNING before every device is materialised (e.g. a
    paramset-cache rebuild on upgrade), the device's data points are missing from
    ``get_data_points()``. Deleting the (disabled) entry would re-create the entity
    disabled and under a fresh entity_id, breaking dashboards/automations/history.
    The device-presence guard keeps it because the backing device is still known to
    HA but absent from the central's loaded devices.
    """
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    device_registry = dr.async_get(hass)
    alive = _create_alive_entities(entity_registry, mock_config_entry_v2, count=3)

    device = device_registry.async_get_or_create(
        config_entry_id=entry_id,
        identifiers={(HMIP_DOMAIN, f"ABC0000001{IDENTIFIER_SEPARATOR}CCU-Homematic")},
    )
    calculated_disabled = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_calculated_abc0000001_1_dew_point",
        config_entry=mock_config_entry_v2,
        device_id=device.id,
        disabled_by=er.RegistryEntryDisabler.USER,
    )

    # Device ABC0000001 is NOT among the central's loaded devices -> not-yet-loaded.
    fake_self = _build_orphan_sweep_self(hass, entry_id, data_point_unique_ids=alive)
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    assert entity_registry.async_get(calculated_disabled.entity_id) is not None


async def test_cleanup_orphan_entries_removes_entry_when_device_loaded_but_data_point_gone(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """A device entry whose device IS loaded but whose data point is gone stays sweepable.

    This is the genuine-orphan case (e.g. un_ignore / profile change removed the
    data point while the device itself is present), which must still be cleaned up.
    """
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    device_registry = dr.async_get(hass)
    alive = _create_alive_entities(entity_registry, mock_config_entry_v2, count=3)

    device = device_registry.async_get_or_create(
        config_entry_id=entry_id,
        identifiers={(HMIP_DOMAIN, f"ABC0000001{IDENTIFIER_SEPARATOR}CCU-Homematic")},
    )
    orphan_disabled = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_abc0000001_1_gone_parameter",
        config_entry=mock_config_entry_v2,
        device_id=device.id,
        disabled_by=er.RegistryEntryDisabler.USER,
    )

    # Device ABC0000001 IS loaded, but its data point is not reported -> real orphan.
    fake_self = _build_orphan_sweep_self(
        hass, entry_id, data_point_unique_ids=alive, known_device_addresses=("ABC0000001",)
    )
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    assert entity_registry.async_get(orphan_disabled.entity_id) is None


async def test_cleanup_orphan_entries_removes_hub_anchored_entry_regardless_of_devices(
    hass: HomeAssistant,
    mock_config_entry_v2: MockConfigEntry,
) -> None:
    """A hub-anchored orphan is still swept: the guard only shields real device entries.

    Hub / program / sysvar entries hang off the central pseudo-device, whose
    identifier carries no ``IDENTIFIER_SEPARATOR``, so the device-presence guard must
    not shield them even when no devices are loaded.
    """
    mock_config_entry_v2.add_to_hass(hass)
    entry_id = mock_config_entry_v2.entry_id

    entity_registry = er.async_get(hass)
    device_registry = dr.async_get(hass)
    alive = _create_alive_entities(entity_registry, mock_config_entry_v2, count=3)

    hub_device = device_registry.async_get_or_create(
        config_entry_id=entry_id,
        identifiers={(HMIP_DOMAIN, "CCU-Homematic")},
    )
    hub_orphan = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_deleted_sysvar",
        config_entry=mock_config_entry_v2,
        device_id=hub_device.id,
        disabled_by=er.RegistryEntryDisabler.USER,
    )

    fake_self = _build_orphan_sweep_self(hass, entry_id, data_point_unique_ids=alive)
    ControlUnit._async_cleanup_orphaned_entity_registry_entries(fake_self)

    assert entity_registry.async_get(hub_orphan.entity_id) is None


class TestLoomUniqueIdMigration:
    """``_loom_migrated_unique_id`` maps legacy keys to the loom/serial scheme."""

    _ENTRY_SUFFIX = "a1b2c3d4e5"  # legacy entry_id[-10:] hub prefix
    _SERIAL_SUFFIX = "11a0001234"  # new serial[-10:]
    _D = HMIP_DOMAIN  # "homematicip_local"

    @pytest.mark.parametrize(
        "unique_id",
        [
            f"{_D}_loom_vcu1234567_1_state",  # already migrated → idempotent
            f"{_D}_home_create_backup",  # synthetic backup button
            f"{_D}_event_group_keypress_vcu1234567_1",  # event group (loom n/a yet)
            "other_integration_xyz",  # not ours
        ],
    )
    def test_left_untouched(self, unique_id: str) -> None:
        assert (
            _loom_migrated_unique_id(unique_id, entry_suffix=self._ENTRY_SUFFIX, serial_suffix=self._SERIAL_SUFFIX)
            is None
        )

    @pytest.mark.parametrize(
        ("old", "expected"),
        [
            # Device data point — no central prefix, just the loom_ namespace.
            (f"{_D}_vcu1234567_1_state", f"{_D}_loom_vcu1234567_1_state"),
            # Custom DP / channel — no parameter, still no prefix.
            (f"{_D}_vcu1234567_1", f"{_D}_loom_vcu1234567_1"),
            # Hub key — entry_id prefix swapped for the serial suffix.
            (
                f"{_D}_a1b2c3d4e5_sysvar_aussen-temperatur",
                f"{_D}_loom_11a0001234_sysvar_aussen-temperatur",
            ),
            # Internal address — same prefix swap.
            (f"{_D}_a1b2c3d4e5_int0001234_1_level", f"{_D}_loom_11a0001234_int0001234_1_level"),
        ],
    )
    def test_rewrites(self, old: str, expected: str) -> None:
        assert (
            _loom_migrated_unique_id(old, entry_suffix=self._ENTRY_SUFFIX, serial_suffix=self._SERIAL_SUFFIX)
            == expected
        )


class TestAioHomematicUniqueIdRestore:
    """``_aiohomematic_restored_unique_id`` strips the loom_ namespace."""

    _D = HMIP_DOMAIN  # "homematicip_local"

    @pytest.mark.parametrize(
        "unique_id",
        [
            f"{_D}_vcu1234567_1_state",  # already aiohomematic-scheme → idempotent
            f"{_D}_11a0001234_sysvar_aussen-temperatur",  # serial hub key, no loom_ namespace
            f"{_D}_home_create_backup",  # synthetic backup button (never loom-keyed)
            "other_integration_xyz",  # not ours
        ],
    )
    def test_left_untouched(self, unique_id: str) -> None:
        assert _aiohomematic_restored_unique_id(unique_id) is None

    @pytest.mark.parametrize(
        ("old", "expected"),
        [
            # Device data point — only the loom_ namespace is stripped.
            (f"{_D}_loom_vcu1234567_1_state", f"{_D}_vcu1234567_1_state"),
            # Custom DP / channel — no parameter, still just strips loom_.
            (f"{_D}_loom_vcu1234567_1", f"{_D}_vcu1234567_1"),
            # Hub key — the serial-anchored slot is already correct, strip loom_.
            (
                f"{_D}_loom_11a0001234_sysvar_aussen-temperatur",
                f"{_D}_11a0001234_sysvar_aussen-temperatur",
            ),
            # Internal address — same plain strip.
            (f"{_D}_loom_11a0001234_int0001234_1_level", f"{_D}_11a0001234_int0001234_1_level"),
        ],
    )
    def test_rewrites(self, old: str, expected: str) -> None:
        assert _aiohomematic_restored_unique_id(old) == expected

    @pytest.mark.parametrize(
        "original",
        [
            f"{_D}_vcu1234567_1_state",
            f"{_D}_vcu1234567_1",
            # Hub keys are serial-anchored on both backends, so they round-trip.
            f"{_D}_11a0001234_sysvar_aussen-temperatur",
            f"{_D}_11a0001234_int0001234_1_level",
            f"{_D}_11a0001234_bidcos_rf_1_press_short",
        ],
    )
    def test_round_trip(self, original: str) -> None:
        """Round-trip aiohomematic → loom → aiohomematic restores the serial key."""
        loom = _loom_migrated_unique_id(original, entry_suffix="a1b2c3d4e5", serial_suffix="11a0001234")
        assert loom is not None
        assert _aiohomematic_restored_unique_id(loom) == original


class TestRealignedHubUniqueId:
    """``_realigned_hub_unique_id`` forces the hub central-id slot onto the live anchor."""

    _D = HMIP_DOMAIN
    _NEW = "11a0001234"  # the live central id (serial[-10:])

    def test_already_aligned_is_noop(self) -> None:
        assert realign_hub_unique_id(f"{self._D}_11a0001234_sysvar_x", central_id="11a0001234") is None

    @pytest.mark.parametrize(
        "unique_id",
        [
            f"{_D}_vcu1234567_1_state",  # device key — no central slot
            f"{_D}_loom_a1b2c3d4e5_sysvar_x",  # loom-namespaced — not ours here
            f"{_D}_11a0001234_sysvar_x",  # already on the live anchor
            f"{_D}_openccu_create_backup",  # synthetic native button — not a routing key
            f"{_D}_event_group_keypress_0008dd8997b338_1",  # device event group — no central slot
            "other_integration_xyz",  # not ours
        ],
    )
    def test_left_untouched(self, unique_id: str) -> None:
        assert self._realign(unique_id) is None

    @pytest.mark.parametrize(
        ("old", "expected"),
        [
            # Any stale slot value is rewritten onto the live anchor, regardless of
            # whether it was a legacy entry_id, an old serial or a re-add leftover.
            (f"{_D}_a1b2c3d4e5_sysvar_x", f"{_D}_11a0001234_sysvar_x"),
            (f"{_D}_w78v4413eq_hub_system-update", f"{_D}_11a0001234_hub_system-update"),
            (f"{_D}_w78v4413eq_install_mode_hmip", f"{_D}_11a0001234_install_mode_hmip"),
            (f"{_D}_a1b2c3d4e5_program_my-prog", f"{_D}_11a0001234_program_my-prog"),
            (f"{_D}_a1b2c3d4e5_int0001234_1_level", f"{_D}_11a0001234_int0001234_1_level"),
            (f"{_D}_a1b2c3d4e5_bidcos_rf_1_press_short", f"{_D}_11a0001234_bidcos_rf_1_press_short"),
            (f"{_D}_w78v4413eq_hmip_rcv_1_9_press_long", f"{_D}_11a0001234_hmip_rcv_1_9_press_long"),
            # Virtual-remote event groups keep their event_group_<type>_ prefix.
            (
                f"{_D}_event_group_keypress_w78v4413eq_bidcos_rf_1",
                f"{_D}_event_group_keypress_11a0001234_bidcos_rf_1",
            ),
        ],
    )
    def test_rewrites(self, old: str, expected: str) -> None:
        assert self._realign(old) == expected

    def _realign(self, unique_id: str) -> str | None:
        return realign_hub_unique_id(unique_id, central_id=self._NEW)


async def test_async_restore_aiohomematic_unique_ids_rewrites_registry(hass: HomeAssistant) -> None:
    """The registry rewrite strips loom_ from device and hub keys alike."""
    serial = "3014F711A0001234"
    entry = MockConfigEntry(domain=HMIP_DOMAIN, unique_id=serial)
    entry.add_to_hass(hass)
    serial_suffix = serial[-10:].lower()

    entity_registry = er.async_get(hass)
    device = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_loom_vcu1234567_1_state",
        config_entry=entry,
    )
    hub = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_loom_{serial_suffix}_sysvar_aussen-temperatur",
        config_entry=entry,
    )

    await _async_restore_aiohomematic_unique_ids(hass, entry)

    assert entity_registry.async_get(device.entity_id).unique_id == f"{HMIP_DOMAIN}_vcu1234567_1_state"
    assert (
        entity_registry.async_get(hub.entity_id).unique_id == f"{HMIP_DOMAIN}_{serial_suffix}_sysvar_aussen-temperatur"
    )


async def test_async_migrate_aiohomematic_hub_unique_ids_reanchors_onto_serial(hass: HomeAssistant) -> None:
    """Legacy entry_id-prefixed hub keys are re-anchored onto the CCU serial."""
    serial = "3014F711A0001234"
    entry = MockConfigEntry(domain=HMIP_DOMAIN, unique_id=serial)
    entry.add_to_hass(hass)
    serial_suffix = serial[-10:].lower()
    entry_suffix = entry.entry_id[-10:]

    entity_registry = er.async_get(hass)
    hub = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_{entry_suffix}_sysvar_aussen-temperatur",
        config_entry=entry,
    )
    device = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_vcu1234567_1_state",
        config_entry=entry,
    )

    await _async_migrate_aiohomematic_hub_unique_ids(hass, entry)

    assert (
        entity_registry.async_get(hub.entity_id).unique_id == f"{HMIP_DOMAIN}_{serial_suffix}_sysvar_aussen-temperatur"
    )
    # device keys carry no central prefix → untouched
    assert entity_registry.async_get(device.entity_id).unique_id == f"{HMIP_DOMAIN}_vcu1234567_1_state"


async def test_async_migrate_aiohomematic_hub_unique_ids_without_serial_uses_entry_id(hass: HomeAssistant) -> None:
    """Without a serial the live anchor is ``entry_id[-10:]``; a key already there is a no-op."""
    entry = MockConfigEntry(domain=HMIP_DOMAIN, unique_id=None)
    entry.add_to_hass(hass)
    entry_suffix = entry.entry_id[-10:].lower()  # the live anchor when no serial is known

    entity_registry = er.async_get(hass)
    hub = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_{entry_suffix}_sysvar_x",
        config_entry=entry,
    )

    await _async_migrate_aiohomematic_hub_unique_ids(hass, entry)

    assert entity_registry.async_get(hub.entity_id).unique_id == f"{HMIP_DOMAIN}_{entry_suffix}_sysvar_x"


async def test_async_migrate_aiohomematic_hub_unique_ids_realigns_stale_anchor(hass: HomeAssistant) -> None:
    """A stale central-id slot (not the live anchor) is realigned, not left to orphan.

    Regression for the disappearing hub / virtual-remote entities: after #1166 the
    live central anchors these keys on the CCU serial. A registry left on an
    unrelated slot (e.g. a prior entry_id from a delete + re-add, or a stale
    serial) fell through the entry_id-only migration and was then permanently
    deleted by the orphan-cleanup sweep. The realign must rewrite whatever slot is
    present onto the live serial — for plain hub keys, virtual-remote keys and the
    virtual-remote event groups alike.
    """
    serial = "3014F711A0001234"
    entry = MockConfigEntry(domain=HMIP_DOMAIN, unique_id=serial)
    entry.add_to_hass(hass)
    serial_suffix = serial[-10:].lower()  # 11a0001234
    stale = "w78v4413eq"  # neither entry_id[-10:] nor the serial suffix
    assert stale not in (entry.entry_id[-10:].lower(), serial_suffix)

    entity_registry = er.async_get(hass)
    hub = entity_registry.async_get_or_create(
        domain="update",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_{stale}_hub_system-update",
        config_entry=entry,
    )
    vremote = entity_registry.async_get_or_create(
        domain="button",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_{stale}_bidcos_rf_9_press_long",
        config_entry=entry,
    )
    event_group = entity_registry.async_get_or_create(
        domain="event",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_event_group_keypress_{stale}_bidcos_rf_1",
        config_entry=entry,
    )
    device = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_0008dd8997b338_1_state",
        config_entry=entry,
    )

    await _async_migrate_aiohomematic_hub_unique_ids(hass, entry)

    assert entity_registry.async_get(hub.entity_id).unique_id == f"{HMIP_DOMAIN}_{serial_suffix}_hub_system-update"
    assert (
        entity_registry.async_get(vremote.entity_id).unique_id
        == f"{HMIP_DOMAIN}_{serial_suffix}_bidcos_rf_9_press_long"
    )
    assert (
        entity_registry.async_get(event_group.entity_id).unique_id
        == f"{HMIP_DOMAIN}_event_group_keypress_{serial_suffix}_bidcos_rf_1"
    )
    # device keys carry no central slot -> untouched
    assert entity_registry.async_get(device.entity_id).unique_id == f"{HMIP_DOMAIN}_0008dd8997b338_1_state"


async def test_async_migrate_aiohomematic_hub_unique_ids_skips_on_collision(hass: HomeAssistant) -> None:
    """A stale key whose live-anchored target already exists is left as-is (no crash)."""
    serial = "3014F711A0001234"
    entry = MockConfigEntry(domain=HMIP_DOMAIN, unique_id=serial)
    entry.add_to_hass(hass)
    serial_suffix = serial[-10:].lower()
    stale = "w78v4413eq"

    entity_registry = er.async_get(hass)
    live = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_{serial_suffix}_sysvar_x",
        config_entry=entry,
    )
    stale_entry = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_{stale}_sysvar_x",
        config_entry=entry,
    )

    await _async_migrate_aiohomematic_hub_unique_ids(hass, entry)

    # No collision crash: the pre-existing live entry keeps the target id and the
    # stale duplicate is left untouched (the sweep can retire it later).
    assert entity_registry.async_get(live.entity_id).unique_id == f"{HMIP_DOMAIN}_{serial_suffix}_sysvar_x"
    assert entity_registry.async_get(stale_entry.entity_id).unique_id == f"{HMIP_DOMAIN}_{stale}_sysvar_x"


async def test_async_reanchor_on_serial_change_rewrites_and_updates_entry(hass: HomeAssistant) -> None:
    """A changed CCU serial re-anchors hub keys and updates the entry unique_id."""
    old_serial = "3014F711A0001234"  # suffix 11a0001234
    new_serial = "3014F711B0009999"  # suffix 11b0009999
    entry = MockConfigEntry(domain=HMIP_DOMAIN, unique_id=old_serial)
    entry.add_to_hass(hass)

    entity_registry = er.async_get(hass)
    hub = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_{old_serial[-10:].lower()}_sysvar_x",
        config_entry=entry,
    )

    control = MagicMock()
    control.central.system_information.serial = new_serial

    await _async_reanchor_hub_unique_ids_on_serial_change(hass, entry, control)

    assert entry.unique_id == new_serial
    assert entity_registry.async_get(hub.entity_id).unique_id == f"{HMIP_DOMAIN}_{new_serial[-10:].lower()}_sysvar_x"


@pytest.mark.parametrize("connected", [None, "unknown", "3014F711A0001234"])
async def test_async_reanchor_on_serial_change_noop(hass: HomeAssistant, connected: str | None) -> None:
    """No re-anchor when the serial is unknown or unchanged."""
    serial = "3014F711A0001234"
    entry = MockConfigEntry(domain=HMIP_DOMAIN, unique_id=serial)
    entry.add_to_hass(hass)

    entity_registry = er.async_get(hass)
    hub = entity_registry.async_get_or_create(
        domain="sensor",
        platform=HMIP_DOMAIN,
        unique_id=f"{HMIP_DOMAIN}_{serial[-10:].lower()}_sysvar_x",
        config_entry=entry,
    )

    control = MagicMock()
    control.central.system_information.serial = connected

    await _async_reanchor_hub_unique_ids_on_serial_change(hass, entry, control)

    assert entry.unique_id == serial
    assert entity_registry.async_get(hub.entity_id).unique_id == f"{HMIP_DOMAIN}_{serial[-10:].lower()}_sysvar_x"
