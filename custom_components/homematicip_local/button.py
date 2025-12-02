"""button for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from datetime import datetime
import logging
from pathlib import Path

from aiohomematic.const import DataPointCategory
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.model.generic import DpButton
from aiohomematic.model.hub import ProgramDpButton
from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HomematicConfigEntry
from .const import DOMAIN
from .control_unit import ControlUnit, signal_new_data_point
from .generic_entity import ATTR_DESCRIPTION, ATTR_NAME, AioHomematicGenericEntity, AioHomematicGenericHubEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU binary_sensor platform."""
    control_unit: ControlUnit = entry.runtime_data

    @callback
    def async_add_button(data_points: tuple[DpButton, ...]) -> None:
        """Add button from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_BUTTON: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicButton(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    @callback
    def async_add_program_button(data_points: tuple[ProgramDpButton, ...]) -> None:
        """Add program button from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_PROGRAM_BUTTON: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicProgramButton(control_unit=control_unit, data_point=data_point) for data_point in data_points
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.BUTTON),
            target=async_add_button,
        )
    )

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.HUB_BUTTON),
            target=async_add_program_button,
        )
    )

    async_add_button(data_points=control_unit.get_new_data_points(data_point_type=DpButton))

    async_add_program_button(data_points=control_unit.get_new_hub_data_points(data_point_type=ProgramDpButton))

    # Add hub-level backup button
    async_add_entities([HmipLocalCreateBackupButton(control_unit=control_unit)])


class AioHomematicButton(AioHomematicGenericEntity[DpButton], ButtonEntity):
    """Representation of the Homematic(IP) Local for OpenCCU button."""

    async def async_press(self) -> None:
        """Execute a button press."""
        await self._data_point.press()


class AioHomematicProgramButton(AioHomematicGenericHubEntity, ButtonEntity):
    """Representation of the Homematic(IP) Local for OpenCCU button."""

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: ProgramDpButton,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        self._data_point: ProgramDpButton = data_point
        self._attr_extra_state_attributes = {
            ATTR_NAME: self._data_point.name,
            ATTR_DESCRIPTION: self._data_point.description,
        }

    async def async_press(self) -> None:
        """Execute a button press."""
        await self._data_point.press()


class HmipLocalCreateBackupButton(ButtonEntity):
    """Representation of the Homematic(IP) Local backup button entity."""

    _attr_has_entity_name = True
    _attr_entity_registry_enabled_default = True
    _attr_translation_key = "create_backup"

    def __init__(self, control_unit: ControlUnit) -> None:
        """Initialize the button entity."""
        self._cu: ControlUnit = control_unit
        self._attr_unique_id = f"{DOMAIN}_{control_unit.central.name}_create_backup"
        self._attr_device_info = control_unit.device_info
        _LOGGER.debug("init: Setting up create backup button for %s", control_unit.central.name)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._cu.central.available

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            backup_bytes = await self._cu.central.create_backup_and_download()
            if backup_bytes is None:
                raise HomeAssistantError("Failed to create and download CCU backup")

            # Save backup to file
            backup_dir = Path(self._cu.backup_directory)
            backup_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ccu_backup_{self._cu.central.name}_{timestamp}.sbk"
            backup_path = backup_dir / filename

            await self.hass.async_add_executor_job(backup_path.write_bytes, backup_bytes)

            _LOGGER.info("CCU backup saved to %s (%d bytes)", backup_path, len(backup_bytes))
        except BaseHomematicException as err:
            raise HomeAssistantError(f"Failed to create CCU backup: {err}") from err
