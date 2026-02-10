"""Backup platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

import logging
from pathlib import Path

from aiohomematic.exceptions import BaseHomematicException
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_pre_backup(hass: HomeAssistant) -> None:
    """Create CCU backups before a HA backup starts."""
    for entry in hass.config_entries.async_loaded_entries(DOMAIN):
        control_unit = entry.runtime_data
        if not control_unit.central.available:
            _LOGGER.warning(
                "CCU %s is not available, skipping backup",
                control_unit.central.name,
            )
            continue
        try:
            backup_data = await control_unit.central.create_backup_and_download()
            if backup_data is None:
                raise HomeAssistantError(f"Failed to create backup from CCU {control_unit.central.name}")
            backup_dir = Path(control_unit.backup_directory)
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / backup_data.filename
            await hass.async_add_executor_job(backup_path.write_bytes, backup_data.content)
            _LOGGER.info(
                "CCU backup saved to %s (%d bytes) before HA backup",
                backup_path,
                len(backup_data.content),
            )
        except BaseHomematicException as err:
            raise HomeAssistantError(f"Failed to create CCU backup for {control_unit.central.name}: {err}") from err


async def async_post_backup(hass: HomeAssistant) -> None:
    """Perform operations after a HA backup finishes."""
