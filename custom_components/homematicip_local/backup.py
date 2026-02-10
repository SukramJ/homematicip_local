"""Backup platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable, Coroutine
import json
import logging
from pathlib import Path
from typing import Any, Final

from aiohomematic.central import CentralUnit
from aiohomematic.exceptions import BaseHomematicException
from homeassistant.components.backup import (
    AgentBackup,
    BackupAgent,
    BackupAgentError,
    BackupNotFound,
    LocalBackupAgent,
    suggested_filename,
)
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
_DATA_BACKUP_AGENT_LISTENERS: Final = f"{DOMAIN}_backup_agent_listeners"


async def async_get_backup_agents(
    hass: HomeAssistant,
    **kwargs: Any,
) -> list[BackupAgent]:
    """Return a list of backup agents."""
    agents: list[BackupAgent] = []
    for entry in hass.config_entries.async_loaded_entries(DOMAIN):
        control_unit = entry.runtime_data
        agents.append(
            CcuLocalBackupAgent(
                hass=hass,
                central=control_unit.central,
                backup_directory=control_unit.backup_directory,
                name=f"CCU {control_unit.central.name}",
                unique_id=entry.entry_id,
            )
        )
    return agents


@callback
def async_register_backup_agents_listener(
    hass: HomeAssistant,
    *,
    listener: Callable[[], None],
    **kwargs: Any,
) -> Callable[[], None]:
    """Register a listener to be called when agents are added or removed."""
    hass.data.setdefault(_DATA_BACKUP_AGENT_LISTENERS, []).append(listener)

    @callback
    def remove_listener() -> None:
        """Remove the listener."""
        hass.data[_DATA_BACKUP_AGENT_LISTENERS].remove(listener)
        if not hass.data[_DATA_BACKUP_AGENT_LISTENERS]:
            del hass.data[_DATA_BACKUP_AGENT_LISTENERS]

    return remove_listener


@callback
def async_notify_backup_listeners(hass: HomeAssistant) -> None:
    """Notify backup agent listeners of config entry changes."""
    for listen in hass.data.get(_DATA_BACKUP_AGENT_LISTENERS, []):
        listen()


def _meta_filename(*, tar_filename: str) -> str:
    """Return the metadata filename for a backup tar file."""
    return tar_filename.rsplit(".", 1)[0] + "_meta.json"


def _tar_filename_from_meta(*, meta_filename: str) -> str:
    """Return the tar filename for a metadata file."""
    return meta_filename.replace("_meta.json", ".tar")


class CcuLocalBackupAgent(LocalBackupAgent):
    """Backup agent storing HA backups in the CCU backup directory."""

    domain = DOMAIN

    def __init__(
        self,
        *,
        hass: HomeAssistant,
        central: CentralUnit,
        backup_directory: str,
        name: str,
        unique_id: str,
    ) -> None:
        """Initialize the backup agent."""
        super().__init__()
        self._hass = hass
        self._central = central
        self._backup_dir = Path(backup_directory)
        self.name = name
        self.unique_id = unique_id
        self._backups: dict[str, tuple[AgentBackup, Path, str | None]] = {}
        self._loaded_backups = False

    async def async_delete_backup(self, backup_id: str, **kwargs: Any) -> None:
        """Delete a backup file, its metadata, and associated CCU backup."""
        if not self._loaded_backups:
            await self._load_backups()
        backup_path = self.get_backup_path(backup_id)
        meta_path = backup_path.parent / _meta_filename(tar_filename=backup_path.name)
        _, _, ccu_filename = self._backups[backup_id]
        try:
            await self._hass.async_add_executor_job(backup_path.unlink, True)
            await self._hass.async_add_executor_job(meta_path.unlink, True)
            if ccu_filename:
                ccu_path = self._backup_dir / ccu_filename
                await self._hass.async_add_executor_job(ccu_path.unlink, True)
        except OSError as err:
            raise BackupAgentError(f"Failed to delete backup {backup_id}: {err}") from err
        _LOGGER.debug("Deleted backup at %s", backup_path)
        self._backups.pop(backup_id)

    async def async_download_backup(
        self,
        backup_id: str,
        **kwargs: Any,
    ) -> AsyncIterator[bytes]:
        """
        Download a backup file.

        Not used for LocalBackupAgent - HA core uses get_backup_path() directly.
        """
        raise NotImplementedError

    async def async_get_backup(
        self,
        backup_id: str,
        **kwargs: Any,
    ) -> AgentBackup:
        """Return a backup."""
        if not self._loaded_backups:
            await self._load_backups()
        if backup_id not in self._backups:
            raise BackupNotFound(f"Backup {backup_id} not found")
        backup, backup_path, _ = self._backups[backup_id]
        if not await self._hass.async_add_executor_job(backup_path.exists):
            _LOGGER.debug(
                "Removing tracked backup (%s) that does not exist at %s",
                backup.backup_id,
                backup_path,
            )
            self._backups.pop(backup_id)
            raise BackupNotFound(f"Backup {backup_id} not found")
        return backup

    async def async_list_backups(self, **kwargs: Any) -> list[AgentBackup]:
        """List backups."""
        if not self._loaded_backups:
            await self._load_backups()
        return [backup for backup, _, _ in self._backups.values()]

    async def async_upload_backup(
        self,
        *,
        open_stream: Callable[[], Coroutine[Any, Any, AsyncIterator[bytes]]],
        backup: AgentBackup,
        **kwargs: Any,
    ) -> None:
        """
        Upload a backup.

        Create a CCU backup first, then persist HA backup metadata.
        The tar file is already written to disk by HA core at get_new_backup_path().
        CCU backup failures are logged but do not block the HA backup.
        """
        ccu_filename = await self._async_create_ccu_backup()
        tar_path = self.get_new_backup_path(backup)
        meta_path = tar_path.parent / _meta_filename(tar_filename=tar_path.name)
        meta_data = {
            "backup": backup.as_dict(),
            "ccu_backup_filename": ccu_filename,
        }
        try:
            await self._hass.async_add_executor_job(
                meta_path.write_text,
                json.dumps(meta_data, ensure_ascii=False),
                "utf-8",
            )
        except OSError as err:
            self._cleanup_ccu_backup(ccu_filename=ccu_filename)
            raise BackupAgentError(f"Failed to save backup metadata: {err}") from err
        self._backups[backup.backup_id] = (backup, tar_path, ccu_filename)

    def get_backup_path(self, backup_id: str) -> Path:
        """Return the local path to an existing backup."""
        try:
            return self._backups[backup_id][1]
        except KeyError as err:
            raise BackupNotFound(f"Backup {backup_id} does not exist") from err

    def get_new_backup_path(self, backup: AgentBackup) -> Path:
        """Return the local path to a new backup."""
        return self._backup_dir / suggested_filename(backup)

    async def _async_create_ccu_backup(self) -> str | None:
        """Create a CCU backup and save it to the backup directory."""
        if not self._central.available:
            _LOGGER.warning(
                "CCU %s is not available, skipping CCU backup",
                self._central.name,
            )
            return None
        try:
            backup_data = await self._central.create_backup_and_download()
            if backup_data is None:
                _LOGGER.warning(
                    "Failed to create backup from CCU %s: no data returned",
                    self._central.name,
                )
                return None
            self._backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = self._backup_dir / backup_data.filename
            await self._hass.async_add_executor_job(backup_path.write_bytes, backup_data.content)
            _LOGGER.info(
                "CCU backup saved to %s (%d bytes)",
                backup_path,
                len(backup_data.content),
            )
        except BaseHomematicException as err:
            _LOGGER.warning(
                "Failed to create CCU backup for %s: %s",
                self._central.name,
                err,
            )
            return None
        return backup_data.filename

    def _cleanup_ccu_backup(self, *, ccu_filename: str | None) -> None:
        """Remove CCU backup file on rollback."""
        if ccu_filename:
            ccu_path = self._backup_dir / ccu_filename
            ccu_path.unlink(missing_ok=True)

    async def _load_backups(self) -> None:
        """Load backup metadata from disk."""
        backups = await self._hass.async_add_executor_job(self._read_backups)
        _LOGGER.debug("Loaded %s HA backups for %s", len(backups), self.name)
        self._backups = backups
        self._loaded_backups = True

    def _read_backups(self) -> dict[str, tuple[AgentBackup, Path, str | None]]:
        """Read backup metadata files from disk."""
        backups: dict[str, tuple[AgentBackup, Path, str | None]] = {}
        if not self._backup_dir.exists():
            return backups
        for meta_path in self._backup_dir.glob("*_meta.json"):
            try:
                meta_data = json.loads(meta_path.read_text(encoding="utf-8"))
                if "backup" in meta_data:
                    backup = AgentBackup.from_dict(meta_data["backup"])
                    ccu_filename: str | None = meta_data.get("ccu_backup_filename")
                else:
                    backup = AgentBackup.from_dict(meta_data)
                    ccu_filename = None
                tar_path = self._backup_dir / _tar_filename_from_meta(meta_filename=meta_path.name)
                if tar_path.exists():
                    backups[backup.backup_id] = (backup, tar_path, ccu_filename)
                else:
                    _LOGGER.warning(
                        "Backup tar file missing for metadata %s, removing metadata",
                        meta_path,
                    )
                    meta_path.unlink(missing_ok=True)
            except (OSError, json.JSONDecodeError, KeyError) as err:
                _LOGGER.warning("Unable to read backup metadata %s: %s", meta_path, err)
        return backups
