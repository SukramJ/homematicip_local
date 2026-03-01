"""Test the backup platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from collections.abc import Callable
import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiohomematic.exceptions import BaseHomematicException
from custom_components.homematicip_local.backup import (
    CcuLocalBackupAgent,
    async_get_backup_agents,
    async_notify_backup_listeners,
    async_register_backup_agents_listener,
)
from homeassistant.components.backup import AgentBackup, BackupAgentError, BackupNotFound
from homeassistant.core import HomeAssistant


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


def _make_entry(*, control_unit: MagicMock, entry_id: str = "test-entry-id") -> MagicMock:
    """Create mock config entry with runtime_data."""
    entry = MagicMock()
    entry.runtime_data = control_unit
    entry.entry_id = entry_id
    return entry


def _make_agent_backup(
    *,
    backup_id: str = "test-backup-id",
    name: str = "Test Backup",
    date: str = "2026-02-10T12:00:00Z",
    size: int = 1024,
) -> AgentBackup:
    """Create a test AgentBackup."""
    return AgentBackup(
        addons=[],
        backup_id=backup_id,
        date=date,
        database_included=False,
        extra_metadata={},
        folders=[],
        homeassistant_included=True,
        homeassistant_version="2026.2.0",
        name=name,
        protected=False,
        size=size,
    )


class TestAsyncGetBackupAgents:
    """Tests for async_get_backup_agents."""

    async def test_returns_agent_per_entry(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that one agent is returned per loaded config entry."""
        control_unit = _make_control_unit(backup_directory=str(tmp_path))
        entry = _make_entry(control_unit=control_unit)

        with patch.object(hass.config_entries, "async_loaded_entries", return_value=[entry]):
            agents = await async_get_backup_agents(hass)

        assert len(agents) == 1
        assert isinstance(agents[0], CcuLocalBackupAgent)

    async def test_returns_empty_for_no_entries(self, hass: HomeAssistant) -> None:
        """Test that empty list is returned when no entries exist."""
        with patch.object(hass.config_entries, "async_loaded_entries", return_value=[]):
            agents = await async_get_backup_agents(hass)

        assert agents == []


class TestBackupAgentListener:
    """Tests for backup agent listener registration."""

    async def test_notify_without_listeners(self, hass: HomeAssistant) -> None:
        """Test that notification without listeners does not fail."""
        async_notify_backup_listeners(hass)

    async def test_register_and_notify(self, hass: HomeAssistant) -> None:
        """Test listener registration and notification."""
        called: list[bool] = []
        listener: Callable[[], None] = lambda: called.append(True)

        remove = async_register_backup_agents_listener(hass, listener=listener)
        async_notify_backup_listeners(hass)

        assert len(called) == 1

        remove()
        async_notify_backup_listeners(hass)
        assert len(called) == 1  # Not called again after removal


class TestCcuLocalBackupAgent:
    """Tests for CcuLocalBackupAgent."""

    async def test_agent_id(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test agent_id format."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        assert agent.agent_id == "homematicip_local.test-entry-id"

    async def test_delete_backup(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test deleting a backup removes tar and metadata files."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        meta_path = tar_path.parent / (tar_path.stem + "_meta.json")
        assert tar_path.exists()
        assert meta_path.exists()

        await agent.async_delete_backup("test-backup-id")

        assert not tar_path.exists()
        assert not meta_path.exists()
        assert await agent.async_list_backups() == []

    async def test_delete_backup_not_found(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that BackupNotFound is raised when deleting missing backup."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)

        with pytest.raises(BackupNotFound):
            await agent.async_delete_backup("nonexistent")

    async def test_delete_backup_os_error(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that OSError during delete is wrapped in BackupAgentError."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        # Ensure backups are loaded so _load_backups is not called during delete
        await agent.async_list_backups()

        with (
            patch.object(hass, "async_add_executor_job", side_effect=OSError("permission denied")),
            pytest.raises(BackupAgentError, match="Failed to delete backup"),
        ):
            await agent.async_delete_backup("test-backup-id")

    async def test_delete_backup_removes_ccu_file(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test deleting a backup also removes the associated CCU backup file."""
        central = MagicMock()
        central.available = True
        central.name = "TestCCU"
        backup_data = _make_backup_data()
        central.create_backup_and_download = AsyncMock(return_value=backup_data)

        agent = self._make_agent(hass=hass, backup_dir=tmp_path, central=central)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        ccu_path = tmp_path / "backup_2026.tar.gz"
        meta_path = tar_path.parent / (tar_path.stem + "_meta.json")
        assert tar_path.exists()
        assert meta_path.exists()
        assert ccu_path.exists()

        await agent.async_delete_backup("test-backup-id")

        assert not tar_path.exists()
        assert not meta_path.exists()
        assert not ccu_path.exists()

    async def test_delete_backup_with_fresh_agent(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test deleting a backup with a fresh agent instance (simulates HA restart)."""
        backup = _make_agent_backup()

        # Agent 1: handles the upload
        agent1 = self._make_agent(hass=hass, backup_dir=tmp_path)
        tar_path = agent1.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent1.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        meta_path = tar_path.parent / (tar_path.stem + "_meta.json")
        assert tar_path.exists()
        assert meta_path.exists()

        # Agent 2: fresh instance (as if HA restarted), handles the delete
        agent2 = self._make_agent(hass=hass, backup_dir=tmp_path)
        await agent2.async_delete_backup("test-backup-id")

        assert not tar_path.exists()
        assert not meta_path.exists()

    async def test_download_backup_not_implemented(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that download raises NotImplementedError (HA core uses get_backup_path)."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)

        with pytest.raises(NotImplementedError):
            await agent.async_download_backup("test-backup-id")

    async def test_get_backup(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test retrieving a backup by ID."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        result = await agent.async_get_backup("test-backup-id")
        assert result.backup_id == "test-backup-id"

    async def test_get_backup_not_found(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that BackupNotFound is raised for missing backup."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)

        with pytest.raises(BackupNotFound):
            await agent.async_get_backup("nonexistent")

    async def test_get_backup_path(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test get_backup_path returns the correct path."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        result = agent.get_backup_path("test-backup-id")
        assert result == tar_path

    async def test_get_backup_path_not_found(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test get_backup_path raises BackupNotFound for unknown backup."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)

        with pytest.raises(BackupNotFound):
            agent.get_backup_path("nonexistent")

    async def test_get_backup_tar_deleted(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that BackupNotFound is raised when tar file was deleted."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        # Delete the tar file externally
        tar_path.unlink()

        with pytest.raises(BackupNotFound):
            await agent.async_get_backup("test-backup-id")

    async def test_list_backups_empty(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test listing backups from empty directory."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backups = await agent.async_list_backups()
        assert backups == []

    async def test_load_from_disk(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that backups are loaded from existing metadata files on disk."""
        backup = _make_agent_backup()
        tar_name = "Test_Backup_2026-02-10_12.00_00000000.tar"
        meta_name = "Test_Backup_2026-02-10_12.00_00000000_meta.json"

        # Create files on disk before agent starts (new format)
        (tmp_path / tar_name).write_bytes(b"fake-tar")
        (tmp_path / meta_name).write_text(
            json.dumps({"backup": backup.as_dict(), "ccu_backup_filename": "ccu_backup.sbk"}),
            encoding="utf-8",
        )

        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backups = await agent.async_list_backups()

        assert len(backups) == 1
        assert backups[0].backup_id == "test-backup-id"

    async def test_load_from_disk_legacy_format(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that backups with legacy metadata format (without wrapper) are loaded."""
        backup = _make_agent_backup()
        tar_name = "Test_Backup_2026-02-10_12.00_00000000.tar"
        meta_name = "Test_Backup_2026-02-10_12.00_00000000_meta.json"

        # Create files on disk with legacy format (plain AgentBackup dict)
        (tmp_path / tar_name).write_bytes(b"fake-tar")
        (tmp_path / meta_name).write_text(
            json.dumps(backup.as_dict()),
            encoding="utf-8",
        )

        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backups = await agent.async_list_backups()

        assert len(backups) == 1
        assert backups[0].backup_id == "test-backup-id"

    async def test_load_skips_corrupt_metadata(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that corrupt metadata files are skipped gracefully."""
        meta_name = "corrupt_backup_meta.json"
        tar_name = "corrupt_backup.tar"

        (tmp_path / meta_name).write_text("not valid json", encoding="utf-8")
        (tmp_path / tar_name).write_bytes(b"fake-tar")

        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backups = await agent.async_list_backups()

        assert backups == []

    async def test_load_skips_orphaned_metadata(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that metadata without tar file is cleaned up."""
        backup = _make_agent_backup()
        meta_name = "Test_Backup_2026-02-10_12.00_00000000_meta.json"

        # Only create metadata, no tar file
        (tmp_path / meta_name).write_text(
            json.dumps(backup.as_dict()),
            encoding="utf-8",
        )

        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backups = await agent.async_list_backups()

        assert backups == []
        assert not (tmp_path / meta_name).exists()  # Cleaned up

    async def test_nonexistent_directory(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that nonexistent backup directory returns empty list."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path / "nonexistent")
        backups = await agent.async_list_backups()
        assert backups == []

    async def test_upload_and_list(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that uploading creates metadata and backup appears in list."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backup = _make_agent_backup()

        # Simulate manager writing the .tar file
        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")

        # Agent gets notified of the upload
        await agent.async_upload_backup(
            open_stream=AsyncMock(),
            backup=backup,
        )

        # Verify metadata file was written
        meta_path = tar_path.parent / (tar_path.stem + "_meta.json")
        assert meta_path.exists()

        # Verify backup appears in list
        backups = await agent.async_list_backups()
        assert len(backups) == 1
        assert backups[0].backup_id == "test-backup-id"

    async def test_upload_backup_os_error(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that OSError during upload metadata write is wrapped in BackupAgentError."""
        agent = self._make_agent(hass=hass, backup_dir=tmp_path)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")

        original = hass.async_add_executor_job

        async def fail_on_write_text(func: Any, *args: Any) -> Any:
            if hasattr(func, "__self__") and isinstance(func.__self__, Path) and func.__name__ == "write_text":
                raise OSError("disk full")
            return await original(func, *args)

        with (
            patch.object(hass, "async_add_executor_job", side_effect=fail_on_write_text),
            pytest.raises(BackupAgentError, match="Failed to save backup metadata"),
        ):
            await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

    async def test_upload_backup_os_error_cleans_up_ccu_backup(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that CCU backup file is removed when metadata write fails."""
        central = MagicMock()
        central.available = True
        central.name = "TestCCU"
        backup_data = _make_backup_data()
        central.create_backup_and_download = AsyncMock(return_value=backup_data)

        agent = self._make_agent(hass=hass, backup_dir=tmp_path, central=central)
        backup = _make_agent_backup()

        ccu_path = tmp_path / "backup_2026.tar.gz"

        # Wrap async_add_executor_job to let the CCU backup succeed but fail on metadata write
        original = hass.async_add_executor_job

        async def selective_fail(func: Any, *args: Any) -> Any:
            if hasattr(func, "__self__") and isinstance(func.__self__, Path) and func.__name__ == "write_text":
                raise OSError("disk full")
            return await original(func, *args)

        with (
            patch.object(hass, "async_add_executor_job", side_effect=selective_fail),
            pytest.raises(BackupAgentError, match="Failed to save backup metadata"),
        ):
            await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        # CCU backup file should be cleaned up
        assert not ccu_path.exists()

    async def test_upload_ccu_backup_fails(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that CCU backup failure logs warning but metadata is still saved."""
        central = MagicMock()
        central.available = True
        central.name = "TestCCU"
        central.create_backup_and_download = AsyncMock(side_effect=BaseHomematicException("connection lost"))

        agent = self._make_agent(hass=hass, backup_dir=tmp_path, central=central)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        # Metadata was still saved despite CCU backup failure
        backups = await agent.async_list_backups()
        assert len(backups) == 1

    async def test_upload_ccu_backup_returns_none(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that None backup data logs warning but metadata is still saved."""
        central = MagicMock()
        central.available = True
        central.name = "TestCCU"
        central.create_backup_and_download = AsyncMock(return_value=None)

        agent = self._make_agent(hass=hass, backup_dir=tmp_path, central=central)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        # Metadata was still saved despite no CCU backup data
        backups = await agent.async_list_backups()
        assert len(backups) == 1

    async def test_upload_ccu_unavailable(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that unavailable CCU logs warning but metadata is still saved."""
        central = MagicMock()
        central.available = False
        central.name = "TestCCU"
        central.create_backup_and_download = AsyncMock()

        agent = self._make_agent(hass=hass, backup_dir=tmp_path, central=central)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        central.create_backup_and_download.assert_not_awaited()
        # Metadata was still saved
        backups = await agent.async_list_backups()
        assert len(backups) == 1

    async def test_upload_creates_ccu_backup(self, hass: HomeAssistant, tmp_path: Path) -> None:
        """Test that uploading a backup creates a CCU backup first."""
        central = MagicMock()
        central.available = True
        central.name = "TestCCU"
        backup_data = _make_backup_data()
        central.create_backup_and_download = AsyncMock(return_value=backup_data)

        agent = self._make_agent(hass=hass, backup_dir=tmp_path, central=central)
        backup = _make_agent_backup()

        tar_path = agent.get_new_backup_path(backup)
        tar_path.parent.mkdir(parents=True, exist_ok=True)
        tar_path.write_bytes(b"fake-tar-content")
        await agent.async_upload_backup(open_stream=AsyncMock(), backup=backup)

        central.create_backup_and_download.assert_awaited_once()
        assert (tmp_path / "backup_2026.tar.gz").exists()
        assert (tmp_path / "backup_2026.tar.gz").read_bytes() == b"backup-content"

    def _make_agent(
        self,
        *,
        hass: HomeAssistant,
        backup_dir: Path,
        central: MagicMock | None = None,
    ) -> CcuLocalBackupAgent:
        """Create a test backup agent."""
        if central is None:
            central = MagicMock()
            central.available = True
            central.name = "TestCCU"
            central.create_backup_and_download = AsyncMock(return_value=None)
        return CcuLocalBackupAgent(
            hass=hass,
            central=central,
            backup_directory=str(backup_dir),
            name="CCU Test",
            unique_id="test-entry-id",
        )
