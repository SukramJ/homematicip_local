"""Tests for update entities of homematicip_local."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from aiohomematic.const import CCUType
from aiohomematic.exceptions import BaseHomematicException
from custom_components.homematicip_local.update import (
    ATTR_FIRMWARE_UPDATE_STATE,
    AioHomematicHubUpdate,
    AioHomematicUpdate,
    async_setup_entry,
)
from homeassistant.components.update import UpdateEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError


def create_mock_update(
    *,
    available: bool = True,
    in_progress: bool | None = False,
    firmware: str | None = "1.0.0",
    latest_firmware: str | None = "1.1.0",
    name: str = "Test Device Update",
    firmware_update_state: str = "UPDATE_AVAILABLE",
    unique_id: str = "test_update_123",
    device_identifier: str = "test_device_123",
    full_name: str = "Test Device Update",
) -> AioHomematicUpdate:
    """Create a mock update entity with patched initialization."""
    # Create mock data point
    mock_data_point = MagicMock()
    mock_data_point.available = available
    mock_data_point.in_progress = in_progress
    mock_data_point.firmware = firmware
    mock_data_point.latest_firmware = latest_firmware
    mock_data_point.name = name
    mock_data_point.unique_id = unique_id
    mock_data_point.full_name = full_name
    mock_data_point.update_firmware = AsyncMock()
    mock_data_point.refresh_firmware_data = AsyncMock()
    mock_data_point.subscribe_to_data_point_updated = Mock(return_value=Mock())
    mock_data_point.subscribe_to_device_removed = Mock(return_value=Mock())

    # Create mock device
    mock_device = MagicMock()
    mock_device.identifier = device_identifier
    mock_device.firmware_update_state = firmware_update_state
    mock_data_point.device = mock_device

    # Create mock control unit
    mock_cu = MagicMock()

    # Create update instance bypassing __init__
    update = object.__new__(AioHomematicUpdate)
    update._cu = mock_cu
    update._data_point = mock_data_point
    update._attr_unique_id = f"homematicip_local_{unique_id}"
    update._attr_device_info = {"identifiers": {("homematicip_local", device_identifier)}}
    update._attr_extra_state_attributes = {ATTR_FIRMWARE_UPDATE_STATE: firmware_update_state}
    update._unsubscribe_callbacks = []

    return update


def create_mock_hub_update(
    *,
    available: bool = True,
    in_progress: bool | None = False,
    current_firmware: str | None = "2.0.0",
    available_firmware: str | None = "2.1.0",
    name: str = "CCU Update",
    unique_id: str = "test_hub_update_123",
    ccu_type: CCUType = CCUType.OPENCCU,
    full_name: str = "CCU Update",
    backup_directory: str = "backups",  # noqa: S108
) -> AioHomematicHubUpdate:
    """Create a mock hub update entity with patched initialization."""
    # Create mock data point
    mock_data_point = MagicMock()
    mock_data_point.available = available
    mock_data_point.in_progress = in_progress
    mock_data_point.current_firmware = current_firmware
    mock_data_point.available_firmware = available_firmware
    mock_data_point.name = name
    mock_data_point.unique_id = unique_id
    mock_data_point.full_name = full_name
    mock_data_point.install = AsyncMock()
    mock_data_point.subscribe_to_data_point_updated = Mock(return_value=Mock())
    mock_data_point.subscribe_to_device_removed = Mock(return_value=Mock())

    # Create mock central
    mock_central = MagicMock()
    mock_central.system_information.ccu_type = ccu_type
    mock_central.create_backup_and_download = AsyncMock()

    # Create mock control unit
    mock_cu = MagicMock()
    mock_cu.central = mock_central
    mock_cu.device_info = {"identifiers": {("homematicip_local", "hub")}}
    mock_cu.backup_directory = backup_directory

    # Calculate supported features based on ccu_type
    if ccu_type == CCUType.OPENCCU:
        supported_features = UpdateEntityFeature.BACKUP | UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS
    else:
        supported_features = UpdateEntityFeature.INSTALL

    # Create hub update instance bypassing __init__
    hub_update = object.__new__(AioHomematicHubUpdate)
    hub_update._cu = mock_cu
    hub_update._data_point = mock_data_point
    hub_update._attr_unique_id = f"homematicip_local_{unique_id}"
    hub_update._attr_device_info = mock_cu.device_info
    hub_update._attr_supported_features = supported_features
    hub_update._unsubscribe_callbacks = []

    return hub_update


class TestAioHomematicUpdateProperties:
    """Tests for AioHomematicUpdate properties."""

    def test_available_false(self) -> None:
        """Test available returns False when data point is unavailable."""
        update = create_mock_update(available=False)
        assert update.available is False

    def test_available_true(self) -> None:
        """Test available returns True when data point is available."""
        update = create_mock_update(available=True)
        assert update.available is True

    def test_in_progress_false(self) -> None:
        """Test in_progress returns False when no update in progress."""
        update = create_mock_update(in_progress=False)
        assert update.in_progress is False

    def test_in_progress_none(self) -> None:
        """Test in_progress returns None when unknown."""
        update = create_mock_update(in_progress=None)
        assert update.in_progress is None

    def test_in_progress_true(self) -> None:
        """Test in_progress returns True when update is in progress."""
        update = create_mock_update(in_progress=True)
        assert update.in_progress is True

    def test_installed_version(self) -> None:
        """Test installed_version returns firmware."""
        update = create_mock_update(firmware="1.2.3")
        assert update.installed_version == "1.2.3"

    def test_installed_version_none(self) -> None:
        """Test installed_version returns None when no firmware."""
        update = create_mock_update(firmware=None)
        assert update.installed_version is None

    def test_latest_version(self) -> None:
        """Test latest_version returns latest_firmware."""
        update = create_mock_update(latest_firmware="2.0.0")
        assert update.latest_version == "2.0.0"

    def test_latest_version_none(self) -> None:
        """Test latest_version returns None when no latest firmware."""
        update = create_mock_update(latest_firmware=None)
        assert update.latest_version is None

    def test_name(self) -> None:
        """Test name property."""
        update = create_mock_update(name="My Device Update")
        assert update.name == "My Device Update"


class TestAioHomematicUpdateMethods:
    """Tests for AioHomematicUpdate methods."""

    @pytest.mark.asyncio
    async def test_async_added_to_hass(self) -> None:
        """Test async_added_to_hass registers callbacks."""
        update = create_mock_update()
        await update.async_added_to_hass()

        assert len(update._unsubscribe_callbacks) == 2
        update._data_point.subscribe_to_data_point_updated.assert_called_once()
        update._data_point.subscribe_to_device_removed.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_install(self) -> None:
        """Test async_install calls update_firmware."""
        update = create_mock_update()
        await update.async_install(version="1.1.0", backup=False)

        update._data_point.update_firmware.assert_called_once_with(refresh_after_update_intervals=(10, 60))

    @pytest.mark.asyncio
    async def test_async_install_ignores_version(self) -> None:
        """Test async_install ignores version parameter."""
        update = create_mock_update()
        await update.async_install(version=None, backup=True)

        update._data_point.update_firmware.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_update(self) -> None:
        """Test async_update refreshes firmware data."""
        update = create_mock_update()
        await update.async_update()

        update._data_point.refresh_firmware_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_will_remove_from_hass(self) -> None:
        """Test async_will_remove_from_hass unsubscribes callbacks."""
        update = create_mock_update()
        mock_unsubscribe1 = Mock()
        mock_unsubscribe2 = Mock()
        update._unsubscribe_callbacks = [mock_unsubscribe1, mock_unsubscribe2]

        await update.async_will_remove_from_hass()

        mock_unsubscribe1.assert_called_once()
        mock_unsubscribe2.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_will_remove_from_hass_handles_none(self) -> None:
        """Test async_will_remove_from_hass handles None callbacks."""
        update = create_mock_update()
        mock_unsubscribe = Mock()
        update._unsubscribe_callbacks = [mock_unsubscribe, None]

        await update.async_will_remove_from_hass()

        mock_unsubscribe.assert_called_once()


class TestAioHomematicUpdateCallbacks:
    """Tests for AioHomematicUpdate callback methods."""

    def test_async_device_removed_device_not_in_registry(self, hass: HomeAssistant) -> None:
        """Test _async_device_removed when device not in registry."""
        update = create_mock_update()
        update.hass = hass
        update.async_remove = Mock()

        mock_registry_entry = MagicMock()
        mock_registry_entry.device_id = "device_123"
        update.registry_entry = mock_registry_entry

        mock_device_registry = MagicMock()
        mock_device_registry.devices = {}  # Device not in registry

        with (
            patch.object(hass, "async_create_task"),
            patch(
                "custom_components.homematicip_local.update.dr.async_get",
                return_value=mock_device_registry,
            ),
        ):
            update._async_device_removed()

        mock_device_registry.async_remove_device.assert_not_called()

    def test_async_device_removed_no_registry_entry(self, hass: HomeAssistant) -> None:
        """Test _async_device_removed when no registry entry."""
        update = create_mock_update()
        update.hass = hass
        update.async_remove = Mock()
        update.registry_entry = None

        with patch.object(hass, "async_create_task") as mock_create_task:
            update._async_device_removed()

        mock_create_task.assert_called_once()

    def test_async_device_removed_with_device_id(self, hass: HomeAssistant) -> None:
        """Test _async_device_removed with device ID."""
        update = create_mock_update()
        update.hass = hass
        update.async_remove = Mock()

        mock_registry_entry = MagicMock()
        mock_registry_entry.device_id = "device_123"
        update.registry_entry = mock_registry_entry

        mock_device_registry = MagicMock()
        mock_device_registry.devices = {"device_123": MagicMock()}

        with (
            patch.object(hass, "async_create_task"),
            patch(
                "custom_components.homematicip_local.update.dr.async_get",
                return_value=mock_device_registry,
            ),
        ):
            update._async_device_removed()

        mock_device_registry.async_remove_device.assert_called_once_with("device_123")

    def test_async_entity_changed_disabled(self, hass: HomeAssistant) -> None:
        """Test _async_entity_changed when entity is disabled."""
        update = create_mock_update()
        update.hass = hass
        update._attr_entity_id = "update.test"
        update.async_schedule_update_ha_state = Mock()

        # Mock enabled property
        with patch.object(type(update), "enabled", property(lambda self: False)):
            update._async_entity_changed()

        update.async_schedule_update_ha_state.assert_not_called()

    def test_async_entity_changed_enabled(self, hass: HomeAssistant) -> None:
        """Test _async_entity_changed when entity is enabled."""
        update = create_mock_update()
        update.hass = hass
        update._attr_entity_id = "update.test"
        update.async_schedule_update_ha_state = Mock()

        # Mock enabled property
        with patch.object(type(update), "enabled", property(lambda self: True)):
            update._async_entity_changed()

        update.async_schedule_update_ha_state.assert_called_once()


class TestAioHomematicUpdateInit:
    """Tests for AioHomematicUpdate initialization."""

    def test_has_entity_name(self) -> None:
        """Test has_entity_name attribute."""
        update = create_mock_update()
        assert update._attr_has_entity_name is True

    def test_init(self) -> None:
        """Test AioHomematicUpdate initialization."""
        mock_data_point = MagicMock()
        mock_data_point.unique_id = "test_123"
        mock_data_point.full_name = "Test Device"
        mock_data_point.device.identifier = "device_456"
        mock_data_point.device.firmware_update_state = "UP_TO_DATE"

        mock_cu = MagicMock()

        with patch("custom_components.homematicip_local.update._LOGGER"):
            update = AioHomematicUpdate(control_unit=mock_cu, data_point=mock_data_point)

        assert update._cu == mock_cu
        assert update._data_point == mock_data_point
        assert update._attr_unique_id == "homematicip_local_test_123"
        assert ATTR_FIRMWARE_UPDATE_STATE in update._attr_extra_state_attributes
        assert update._unsubscribe_callbacks == []

    def test_should_poll(self) -> None:
        """Test should_poll attribute."""
        update = create_mock_update()
        assert update._attr_should_poll is False

    def test_supported_features(self) -> None:
        """Test supported features."""
        update = create_mock_update()
        expected = UpdateEntityFeature.PROGRESS | UpdateEntityFeature.INSTALL
        assert update._attr_supported_features == expected


class TestAioHomematicHubUpdateProperties:
    """Tests for AioHomematicHubUpdate properties."""

    def test_available_false(self) -> None:
        """Test available returns False when data point is unavailable."""
        hub_update = create_mock_hub_update(available=False)
        assert hub_update.available is False

    def test_available_true(self) -> None:
        """Test available returns True when data point is available."""
        hub_update = create_mock_hub_update(available=True)
        assert hub_update.available is True

    def test_in_progress_false(self) -> None:
        """Test in_progress returns False when no update in progress."""
        hub_update = create_mock_hub_update(in_progress=False)
        assert hub_update.in_progress is False

    def test_in_progress_true(self) -> None:
        """Test in_progress returns True when update is in progress."""
        hub_update = create_mock_hub_update(in_progress=True)
        assert hub_update.in_progress is True

    def test_installed_version(self) -> None:
        """Test installed_version returns current_firmware."""
        hub_update = create_mock_hub_update(current_firmware="3.0.0")
        assert hub_update.installed_version == "3.0.0"

    def test_latest_version_with_available(self) -> None:
        """Test latest_version returns available_firmware when present."""
        hub_update = create_mock_hub_update(available_firmware="3.1.0", current_firmware="3.0.0")
        assert hub_update.latest_version == "3.1.0"

    def test_latest_version_without_available(self) -> None:
        """Test latest_version returns current_firmware when no available."""
        hub_update = create_mock_hub_update(available_firmware=None, current_firmware="3.0.0")
        assert hub_update.latest_version == "3.0.0"

    def test_name(self) -> None:
        """Test name property."""
        hub_update = create_mock_hub_update(name="Hub Update")
        assert hub_update.name == "Hub Update"


class TestAioHomematicHubUpdateSupportedFeatures:
    """Tests for AioHomematicHubUpdate supported features."""

    def test_supported_features_ccu(self) -> None:
        """Test supported features for regular CCU."""
        hub_update = create_mock_hub_update(ccu_type=CCUType.CCU)
        expected = UpdateEntityFeature.INSTALL
        assert hub_update._attr_supported_features == expected

    def test_supported_features_openccu(self) -> None:
        """Test supported features for OpenCCU."""
        hub_update = create_mock_hub_update(ccu_type=CCUType.OPENCCU)
        expected = UpdateEntityFeature.BACKUP | UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS
        assert hub_update._attr_supported_features == expected

    def test_supported_features_unknown(self) -> None:
        """Test supported features for unknown CCU type."""
        hub_update = create_mock_hub_update(ccu_type=CCUType.UNKNOWN)
        expected = UpdateEntityFeature.INSTALL
        assert hub_update._attr_supported_features == expected


class TestAioHomematicHubUpdateMethods:
    """Tests for AioHomematicHubUpdate methods."""

    @pytest.mark.asyncio
    async def test_async_added_to_hass(self) -> None:
        """Test async_added_to_hass registers callbacks."""
        hub_update = create_mock_hub_update()
        await hub_update.async_added_to_hass()

        assert len(hub_update._unsubscribe_callbacks) == 2
        hub_update._data_point.subscribe_to_data_point_updated.assert_called_once()
        hub_update._data_point.subscribe_to_device_removed.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_install_backup_exception(self, hass: HomeAssistant) -> None:
        """Test async_install raises error on backup exception."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass
        hub_update._cu.central.create_backup_and_download.side_effect = BaseHomematicException("Backup failed")

        with pytest.raises(HomeAssistantError, match="Failed to create backup"):
            await hub_update.async_install(version="3.1.0", backup=True)

    @pytest.mark.asyncio
    async def test_async_install_backup_returns_none(self, hass: HomeAssistant) -> None:
        """Test async_install raises error when backup returns None."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass
        hub_update._cu.central.create_backup_and_download.return_value = None

        with pytest.raises(HomeAssistantError, match="Failed to create backup"):
            await hub_update.async_install(version="3.1.0", backup=True)

    @pytest.mark.asyncio
    async def test_async_install_with_backup(self, hass: HomeAssistant) -> None:
        """Test async_install with backup."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass

        # Mock backup data
        mock_backup_data = MagicMock()
        mock_backup_data.filename = "backup_2024.tar.gz"
        mock_backup_data.content = b"backup content"
        hub_update._cu.central.create_backup_and_download.return_value = mock_backup_data

        with patch.object(Path, "mkdir"), patch.object(Path, "write_bytes"):
            await hub_update.async_install(version="3.1.0", backup=True)

        hub_update._cu.central.create_backup_and_download.assert_called_once()
        hub_update._data_point.install.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_install_without_backup(self) -> None:
        """Test async_install without backup."""
        hub_update = create_mock_hub_update()
        await hub_update.async_install(version="3.1.0", backup=False)

        hub_update._data_point.install.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_update_does_nothing(self) -> None:
        """Test async_update does nothing (empty implementation)."""
        hub_update = create_mock_hub_update()
        # Should not raise
        await hub_update.async_update()

    @pytest.mark.asyncio
    async def test_async_will_remove_from_hass(self) -> None:
        """Test async_will_remove_from_hass unsubscribes callbacks."""
        hub_update = create_mock_hub_update()
        mock_unsubscribe1 = Mock()
        mock_unsubscribe2 = Mock()
        hub_update._unsubscribe_callbacks = [mock_unsubscribe1, mock_unsubscribe2]

        await hub_update.async_will_remove_from_hass()

        mock_unsubscribe1.assert_called_once()
        mock_unsubscribe2.assert_called_once()


class TestAioHomematicHubUpdateCallbacks:
    """Tests for AioHomematicHubUpdate callback methods."""

    def test_async_device_removed_no_registry_entry(self, hass: HomeAssistant) -> None:
        """Test _async_device_removed when no registry entry."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass
        hub_update.async_remove = Mock()
        hub_update.registry_entry = None

        with patch.object(hass, "async_create_task"):
            hub_update._async_device_removed()

    def test_async_device_removed_with_device_id(self, hass: HomeAssistant) -> None:
        """Test _async_device_removed with device ID."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass
        hub_update.async_remove = Mock()

        mock_registry_entry = MagicMock()
        mock_registry_entry.device_id = "hub_device_123"
        hub_update.registry_entry = mock_registry_entry

        mock_device_registry = MagicMock()
        mock_device_registry.devices = {"hub_device_123": MagicMock()}

        with (
            patch.object(hass, "async_create_task"),
            patch(
                "custom_components.homematicip_local.update.dr.async_get",
                return_value=mock_device_registry,
            ),
        ):
            hub_update._async_device_removed()

        mock_device_registry.async_remove_device.assert_called_once_with("hub_device_123")

    def test_async_entity_changed_disabled(self, hass: HomeAssistant) -> None:
        """Test _async_entity_changed when entity is disabled."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass
        hub_update._attr_entity_id = "update.hub"
        hub_update.async_schedule_update_ha_state = Mock()

        with patch.object(type(hub_update), "enabled", property(lambda self: False)):
            hub_update._async_entity_changed()

        hub_update.async_schedule_update_ha_state.assert_not_called()

    def test_async_entity_changed_enabled(self, hass: HomeAssistant) -> None:
        """Test _async_entity_changed when entity is enabled."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass
        hub_update._attr_entity_id = "update.hub"
        hub_update.async_schedule_update_ha_state = Mock()

        with patch.object(type(hub_update), "enabled", property(lambda self: True)):
            hub_update._async_entity_changed()

        hub_update.async_schedule_update_ha_state.assert_called_once()


class TestAioHomematicHubUpdateInit:
    """Tests for AioHomematicHubUpdate initialization."""

    def test_init_ccu(self) -> None:
        """Test AioHomematicHubUpdate initialization for regular CCU."""
        mock_data_point = MagicMock()
        mock_data_point.unique_id = "hub_123"
        mock_data_point.full_name = "Hub Update"

        mock_cu = MagicMock()
        mock_cu.central.system_information.ccu_type = CCUType.CCU
        mock_cu.device_info = {"identifiers": {("homematicip_local", "hub")}}

        with patch("custom_components.homematicip_local.update._LOGGER"):
            hub_update = AioHomematicHubUpdate(control_unit=mock_cu, data_point=mock_data_point)

        assert hub_update._attr_supported_features == UpdateEntityFeature.INSTALL

    def test_init_openccu(self) -> None:
        """Test AioHomematicHubUpdate initialization for OpenCCU."""
        mock_data_point = MagicMock()
        mock_data_point.unique_id = "hub_123"
        mock_data_point.full_name = "Hub Update"

        mock_cu = MagicMock()
        mock_cu.central.system_information.ccu_type = CCUType.OPENCCU
        mock_cu.device_info = {"identifiers": {("homematicip_local", "hub")}}

        with patch("custom_components.homematicip_local.update._LOGGER"):
            hub_update = AioHomematicHubUpdate(control_unit=mock_cu, data_point=mock_data_point)

        assert hub_update._cu == mock_cu
        assert hub_update._data_point == mock_data_point
        assert hub_update._attr_unique_id == "homematicip_local_hub_123"
        expected_features = UpdateEntityFeature.BACKUP | UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS
        assert hub_update._attr_supported_features == expected_features


class TestAsyncSetupEntry:
    """Tests for async_setup_entry function."""

    @pytest.mark.asyncio
    async def test_async_setup_entry(self, hass: HomeAssistant) -> None:
        """Test async_setup_entry sets up the platform."""
        mock_control_unit = MagicMock()
        mock_control_unit.get_new_data_points.return_value = ()

        mock_entry = MagicMock()
        mock_entry.runtime_data = mock_control_unit
        mock_entry.entry_id = "test_entry_id"
        mock_entry.async_on_unload = MagicMock()

        mock_async_add_entities = MagicMock()

        with patch("custom_components.homematicip_local.update.async_dispatcher_connect") as mock_dispatcher:
            await async_setup_entry(hass, mock_entry, mock_async_add_entities)

        # Should register two dispatcher connects (UPDATE and HUB_UPDATE)
        assert mock_dispatcher.call_count == 2
        assert mock_entry.async_on_unload.call_count == 2
        mock_control_unit.get_new_data_points.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_setup_entry_hub_update_callback(self, hass: HomeAssistant) -> None:
        """Test async_add_hub_update callback is registered."""
        mock_control_unit = MagicMock()
        mock_control_unit.get_new_data_points.return_value = ()
        mock_control_unit.device_info = {"identifiers": {("homematicip_local", "hub")}}
        mock_control_unit.central.system_information.ccu_type = CCUType.OPENCCU

        mock_entry = MagicMock()
        mock_entry.runtime_data = mock_control_unit
        mock_entry.entry_id = "test_entry_id"
        mock_entry.async_on_unload = MagicMock()

        mock_async_add_entities = MagicMock()
        captured_callbacks = {}

        def capture_dispatcher(hass, signal, target):
            captured_callbacks[signal] = target
            return MagicMock()

        with patch(
            "custom_components.homematicip_local.update.async_dispatcher_connect",
            side_effect=capture_dispatcher,
        ):
            await async_setup_entry(hass, mock_entry, mock_async_add_entities)

        # Verify both callbacks are registered
        assert len(captured_callbacks) == 2

        # Find the hub update callback
        hub_update_signal = None
        for signal in captured_callbacks:
            if "hub_update" in str(signal):
                hub_update_signal = signal
                break

        assert hub_update_signal is not None, "Hub update callback not registered"

        # Verify the callback is callable
        assert callable(captured_callbacks[hub_update_signal])

        # Invoke the callback with a mock hub data point to cover lines 56-65
        mock_hub_data_point = MagicMock()
        mock_hub_data_point.unique_id = "hub_update_123"
        mock_hub_data_point.full_name = "Hub Update Test"

        # Call the callback - this covers async_add_hub_update
        captured_callbacks[hub_update_signal]((mock_hub_data_point,))

        # Verify async_add_entities was called (only for hub update since initial setup had empty data)
        assert mock_async_add_entities.call_count == 1

    @pytest.mark.asyncio
    async def test_async_setup_entry_hub_update_callback_empty(self, hass: HomeAssistant) -> None:
        """Test async_add_hub_update callback with empty data points."""
        mock_control_unit = MagicMock()
        mock_control_unit.get_new_data_points.return_value = ()

        mock_entry = MagicMock()
        mock_entry.runtime_data = mock_control_unit
        mock_entry.entry_id = "test_entry_id"
        mock_entry.async_on_unload = MagicMock()

        mock_async_add_entities = MagicMock()
        captured_callbacks = {}

        def capture_dispatcher(hass, signal, target):
            captured_callbacks[signal] = target
            return MagicMock()

        with patch(
            "custom_components.homematicip_local.update.async_dispatcher_connect",
            side_effect=capture_dispatcher,
        ):
            await async_setup_entry(hass, mock_entry, mock_async_add_entities)

        # Find the hub update callback
        hub_update_signal = None
        for signal in captured_callbacks:
            if "hub_update" in str(signal):
                hub_update_signal = signal
                break

        # Call with empty tuple - should not add entities
        captured_callbacks[hub_update_signal](())

        # Should not be called at all since both initial setup and hub update have empty data
        assert mock_async_add_entities.call_count == 0

    @pytest.mark.asyncio
    async def test_async_setup_entry_with_data_points(self, hass: HomeAssistant) -> None:
        """Test async_setup_entry with existing data points."""
        mock_data_point = MagicMock()

        mock_control_unit = MagicMock()
        mock_control_unit.get_new_data_points.return_value = (mock_data_point,)

        mock_entry = MagicMock()
        mock_entry.runtime_data = mock_control_unit
        mock_entry.entry_id = "test_entry_id"
        mock_entry.async_on_unload = MagicMock()

        mock_async_add_entities = MagicMock()

        with (
            patch("custom_components.homematicip_local.update.async_dispatcher_connect"),
            patch("custom_components.homematicip_local.update.AioHomematicUpdate") as mock_update_class,
        ):
            mock_update_instance = MagicMock()
            mock_update_class.return_value = mock_update_instance

            await async_setup_entry(hass, mock_entry, mock_async_add_entities)

        mock_async_add_entities.assert_called_once()


class TestAioHomematicHubUpdateBackup:
    """Tests for backup functionality in AioHomematicHubUpdate."""

    @pytest.mark.asyncio
    async def test_create_backup_exception(self, hass: HomeAssistant) -> None:
        """Test _async_create_backup handles BaseHomematicException."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass
        hub_update._cu.central.create_backup_and_download.side_effect = BaseHomematicException("Network error")

        with pytest.raises(HomeAssistantError, match="Failed to create backup"):
            await hub_update._async_create_backup()

    @pytest.mark.asyncio
    async def test_create_backup_none_result(self, hass: HomeAssistant) -> None:
        """Test _async_create_backup raises error on None result."""
        hub_update = create_mock_hub_update()
        hub_update.hass = hass
        hub_update._cu.central.create_backup_and_download.return_value = None

        with pytest.raises(HomeAssistantError, match="Failed to create backup"):
            await hub_update._async_create_backup()

    @pytest.mark.asyncio
    async def test_create_backup_success(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test _async_create_backup success."""
        hub_update = create_mock_hub_update(backup_directory=str(tmp_path))
        hub_update.hass = hass

        mock_backup_data = MagicMock()
        mock_backup_data.filename = "backup_test.tar.gz"
        mock_backup_data.content = b"test backup content"
        hub_update._cu.central.create_backup_and_download.return_value = mock_backup_data

        await hub_update._async_create_backup()

        hub_update._cu.central.create_backup_and_download.assert_called_once()
