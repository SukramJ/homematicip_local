"""Test the backup platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiohomematic.exceptions import BaseHomematicException
from custom_components.homematicip_local.backup import async_post_backup, async_pre_backup
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError


def _make_backup_data(*, filename: str = "backup_2026.tar.gz", content: bytes = b"backup-content") -> MagicMock:
    """Create mock backup data."""
    backup_data = MagicMock()
    backup_data.filename = filename
    backup_data.content = content
    return backup_data


def _make_control_unit(
    *, available: bool = True, name: str = "TestCCU", backup_directory: str = "backups"
) -> MagicMock:
    """Create mock control unit."""
    control_unit = MagicMock()
    control_unit.central.available = available
    control_unit.central.name = name
    control_unit.backup_directory = backup_directory
    control_unit.central.create_backup_and_download = AsyncMock()
    return control_unit


def _make_entry(*, control_unit: MagicMock) -> MagicMock:
    """Create mock config entry with runtime_data."""
    entry = MagicMock()
    entry.runtime_data = control_unit
    return entry


class TestAsyncPreBackup:
    """Tests for async_pre_backup."""

    async def test_async_pre_backup_backup_returns_none(self, hass: HomeAssistant) -> None:
        """Test that None backup data raises HomeAssistantError."""
        control_unit = _make_control_unit()
        control_unit.central.create_backup_and_download.return_value = None
        entry = _make_entry(control_unit=control_unit)

        with (
            patch.object(hass.config_entries, "async_loaded_entries", return_value=[entry]),
            pytest.raises(HomeAssistantError, match="Failed to create backup from CCU"),
        ):
            await async_pre_backup(hass)

    async def test_async_pre_backup_ccu_unavailable(self, hass: HomeAssistant) -> None:
        """Test that unavailable CCU is skipped with a warning."""
        control_unit = _make_control_unit(available=False)
        entry = _make_entry(control_unit=control_unit)

        with patch.object(hass.config_entries, "async_loaded_entries", return_value=[entry]):
            await async_pre_backup(hass)

        control_unit.central.create_backup_and_download.assert_not_awaited()

    async def test_async_pre_backup_exception(self, hass: HomeAssistant) -> None:
        """Test that BaseHomematicException is wrapped in HomeAssistantError."""
        control_unit = _make_control_unit()
        control_unit.central.create_backup_and_download.side_effect = BaseHomematicException("connection lost")
        entry = _make_entry(control_unit=control_unit)

        with (
            patch.object(hass.config_entries, "async_loaded_entries", return_value=[entry]),
            pytest.raises(HomeAssistantError, match="Failed to create CCU backup for TestCCU"),
        ):
            await async_pre_backup(hass)

    async def test_async_pre_backup_no_entries(self, hass: HomeAssistant) -> None:
        """Test that no config entries results in no error."""
        with patch.object(hass.config_entries, "async_loaded_entries", return_value=[]):
            await async_pre_backup(hass)

    async def test_async_pre_backup_success(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test successful backup creation and file write."""
        backup_dir = tmp_path / "backups"
        control_unit = _make_control_unit(backup_directory=str(backup_dir))
        backup_data = _make_backup_data()
        control_unit.central.create_backup_and_download.return_value = backup_data
        entry = _make_entry(control_unit=control_unit)

        with patch.object(hass.config_entries, "async_loaded_entries", return_value=[entry]):
            await async_pre_backup(hass)

        control_unit.central.create_backup_and_download.assert_awaited_once()
        assert (backup_dir / "backup_2026.tar.gz").exists()
        assert (backup_dir / "backup_2026.tar.gz").read_bytes() == b"backup-content"


class TestAsyncPostBackup:
    """Tests for async_post_backup."""

    async def test_async_post_backup(self, hass: HomeAssistant) -> None:
        """Test that post backup is a no-op."""
        await async_post_backup(hass)
