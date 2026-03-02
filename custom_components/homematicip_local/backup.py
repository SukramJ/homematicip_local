"""Backup platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable, Coroutine
import json
import logging
from pathlib import Path
from typing import Any, Final

from aiohomematic.central import CentralUnit
from aiohomematic.exceptions import BaseHomematicException
from homeassistant.components.backup import AgentBackup, BackupAgent, BackupAgentError, BackupNotFound
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


def _meta_filename(*, backup_id: str) -> str:
    """Return the metadata filename for a backup."""
    return f"{backup_id}_meta.json"


class CcuLocalBackupAgent(BackupAgent):
    """Backup agent storing CCU backups alongside HA backup metadata."""

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
        self._backups: dict[str, tuple[AgentBackup, str | None]] = {}
        self._loaded_backups = False

    async def async_delete_backup(self, backup_id: str, **kwargs: Any) -> None:
        """Delete a backup's metadata and associated CCU backup file."""
        if not self._loaded_backups:
            await self._load_backups()
        if backup_id not in self._backups:
            raise BackupNotFound(f"Backup {backup_id} not found")
        meta_path = self._backup_dir / _meta_filename(backup_id=backup_id)
        _, ccu_filename = self._backups[backup_id]
        try:
            await self._hass.async_add_executor_job(meta_path.unlink, True)
            if ccu_filename:
                ccu_path = self._backup_dir / ccu_filename
                await self._hass.async_add_executor_job(ccu_path.unlink, True)
        except OSError as err:
            raise BackupAgentError(f"Failed to delete backup {backup_id}: {err}") from err
        _LOGGER.debug("Deleted backup %s", backup_id)
        self._backups.pop(backup_id)

    async def async_download_backup(
        self,
        backup_id: str,
        **kwargs: Any,
    ) -> AsyncIterator[bytes]:
        """
        Download a backup file.

        Not supported - this agent only stores CCU backups, not HA backup data.
        HA restore uses the local or cloud backup agent.
        """
        raise BackupAgentError("Download not supported: this agent only stores CCU backups")

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
        backup, ccu_filename = self._backups[backup_id]
        if ccu_filename:
            ccu_path = self._backup_dir / ccu_filename
            if not await self._hass.async_add_executor_job(ccu_path.exists):
                _LOGGER.debug(
                    "Removing tracked backup (%s) - CCU file %s does not exist",
                    backup.backup_id,
                    ccu_filename,
                )
                self._backups.pop(backup_id)
                raise BackupNotFound(f"Backup {backup_id} not found")
        return backup

    async def async_list_backups(self, **kwargs: Any) -> list[AgentBackup]:
        """List backups."""
        if not self._loaded_backups:
            await self._load_backups()
        return [backup for backup, _ in self._backups.values()]

    async def async_upload_backup(
        self,
        *,
        open_stream: Callable[[], Coroutine[Any, Any, AsyncIterator[bytes]]],
        backup: AgentBackup,
        **kwargs: Any,
    ) -> None:
        """
        Upload a backup.

        Create a CCU backup and persist metadata linking it to the HA backup.
        The HA backup tar is managed by HA core and not stored by this agent.
        """
        await self._hass.async_add_executor_job(self._backup_dir.mkdir, 0o777, True, True)

        ccu_filename = await self._async_create_ccu_backup()

        meta_path = self._backup_dir / _meta_filename(backup_id=backup.backup_id)
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
        self._backups[backup.backup_id] = (backup, ccu_filename)

    async def _async_create_ccu_backup(self) -> str | None:
        """Create a CCU backup and save it to the backup directory."""
        if not self._central.available:
            raise BackupAgentError(f"CCU {self._central.name} is not available, cannot create CCU backup")
        try:
            backup_data = await self._central.create_backup_and_download()
            if backup_data is None:
                raise BackupAgentError(f"Failed to create backup from CCU {self._central.name}: no data returned")
            self._backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = self._backup_dir / backup_data.filename
            await self._hass.async_add_executor_job(backup_path.write_bytes, backup_data.content)
            _LOGGER.info(
                "CCU backup saved to %s (%d bytes)",
                backup_path,
                len(backup_data.content),
            )
        except BaseHomematicException as err:
            raise BackupAgentError(f"Failed to create CCU backup for {self._central.name}: {err}") from err
        return backup_data.filename

    def _cleanup_ccu_backup(self, *, ccu_filename: str | None) -> None:
        """Remove CCU backup file on rollback."""
        if ccu_filename:
            ccu_path = self._backup_dir / ccu_filename
            ccu_path.unlink(missing_ok=True)

    async def _load_backups(self) -> None:
        """Load backup metadata from disk."""
        backups = await self._hass.async_add_executor_job(self._read_backups)
        _LOGGER.debug("Loaded %s CCU backups for %s", len(backups), self.name)
        self._backups = backups
        self._loaded_backups = True

    def _read_backups(self) -> dict[str, tuple[AgentBackup, str | None]]:
        """Read backup metadata files from disk."""
        backups: dict[str, tuple[AgentBackup, str | None]] = {}
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
                if ccu_filename and (self._backup_dir / ccu_filename).exists():
                    backups[backup.backup_id] = (backup, ccu_filename)
                elif ccu_filename is None:
                    _LOGGER.warning(
                        "Backup metadata %s has no CCU backup file, removing metadata",
                        meta_path,
                    )
                    meta_path.unlink(missing_ok=True)
                else:
                    _LOGGER.warning(
                        "CCU backup file missing for metadata %s, removing metadata",
                        meta_path,
                    )
                    meta_path.unlink(missing_ok=True)
            except (OSError, json.JSONDecodeError, KeyError) as err:
                _LOGGER.warning("Unable to read backup metadata %s: %s", meta_path, err)
        return backups
