"""Test the Homematic(IP) Local for OpenCCU init."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from aiohomematic.const import CentralState, DeviceTriggerEventType
from aiohomematic.exceptions import AuthFailure
import custom_components.homematicip_local
from custom_components.homematicip_local.config_flow import DomainConfigFlow
from custom_components.homematicip_local.const import (
    CONF_ADVANCED_CONFIG,
    CONF_OPTIONAL_SETTINGS,
    DOMAIN as HMIP_DOMAIN,
)
from custom_components.homematicip_local.control_unit import ControlUnit
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

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
) -> SimpleNamespace:
    """Build a minimal ControlUnit-shaped self for _async_cleanup_orphaned_entity_registry_entries."""
    central = MagicMock()
    central.state = state
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
    return SimpleNamespace(_hass=hass, _entry_id=entry_id, _central=central)


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
