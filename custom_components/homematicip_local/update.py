"""Switch platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Final

from aiohomematic.const import CCUType, DataPointCategory
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.model.hub.update import HmUpdate
from aiohomematic.model.update import DpUpdate
from aiohomematic.type_aliases import UnsubscribeCallback
from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import UndefinedType

from . import HomematicConfigEntry
from .const import DOMAIN
from .control_unit import ControlUnit, signal_new_data_point

_LOGGER = logging.getLogger(__name__)
ATTR_FIRMWARE_UPDATE_STATE: Final = "firmware_update_state"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU update platform."""
    control_unit: ControlUnit = entry.runtime_data

    @callback
    def async_add_update(data_points: tuple[DpUpdate, ...]) -> None:
        """Add update from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_UPDATE: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicUpdate(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    @callback
    def async_add_hub_update(data_points: tuple[HmUpdate, ...]) -> None:
        """Add hub update from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_UPDATE: Adding %i hub data points", len(data_points))

        if entities := [
            AioHomematicHubUpdate(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.UPDATE),
            target=async_add_update,
        )
    )

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.HUB_UPDATE),
            target=async_add_hub_update,
        )
    )

    async_add_update(data_points=control_unit.get_new_data_points(data_point_type=DpUpdate))


class AioHomematicUpdate(UpdateEntity):
    """Representation of the HomematicIP update entity."""

    _attr_supported_features = UpdateEntityFeature.PROGRESS | UpdateEntityFeature.INSTALL

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_entity_registry_enabled_default = True

    _unrecorded_attributes = frozenset({ATTR_FIRMWARE_UPDATE_STATE})

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: DpUpdate,
    ) -> None:
        """Initialize the generic entity."""
        self._cu: ControlUnit = control_unit
        self._data_point: DpUpdate = data_point
        self._attr_unique_id = f"{DOMAIN}_{data_point.unique_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, data_point.device.identifier)},
        )
        self._attr_extra_state_attributes = {ATTR_FIRMWARE_UPDATE_STATE: data_point.device.firmware_update_state}
        self._unsubscribe_callbacks: list[UnsubscribeCallback] = []
        _LOGGER.debug("init: Setting up %s", data_point.full_name)

    @property
    def available(self) -> bool:
        """Return if data point is available."""
        return self._data_point.available

    @property
    def in_progress(self) -> bool | None:
        """Update installation progress."""
        return self._data_point.in_progress

    @property
    def installed_version(self) -> str | None:
        """Version installed and in use."""
        return self._data_point.firmware

    @property
    def latest_version(self) -> str | None:
        """Latest version available for install."""
        return self._data_point.latest_firmware

    @property
    def name(self) -> str | UndefinedType | None:
        """Return the name of the entity."""
        return self._data_point.name

    async def async_added_to_hass(self) -> None:
        """Register callbacks and load initial data."""
        self._unsubscribe_callbacks.append(
            self._data_point.subscribe_to_data_point_updated(
                handler=self._async_entity_changed, custom_id=self.entity_id
            )
        )
        self._unsubscribe_callbacks.append(
            self._data_point.subscribe_to_device_removed(handler=self._async_device_removed)
        )

    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None:
        """Install an update."""
        await self._data_point.update_firmware(refresh_after_update_intervals=(10, 60))

    async def async_update(self) -> None:
        """Update entity."""
        await self._data_point.refresh_firmware_data()

    async def async_will_remove_from_hass(self) -> None:
        """Run when hmip device will be removed from hass."""
        # Remove callback from device.
        for unregister in self._unsubscribe_callbacks:
            if unregister is not None:
                unregister()

    @callback
    def _async_device_removed(self) -> None:
        """Handle hm device removal."""
        self.hass.async_create_task(self.async_remove(force_remove=True))

        if not self.registry_entry:
            return

        if device_id := self.registry_entry.device_id:
            # Remove from device registry.
            device_registry = dr.async_get(self.hass)
            if device_id in device_registry.devices:
                # This will also remove associated entities from entity registry.
                device_registry.async_remove_device(device_id)

    @callback
    def _async_entity_changed(self, *args: Any, **kwargs: Any) -> None:
        """Handle device state changes."""
        # Don't update disabled entities
        if self.enabled:
            _LOGGER.debug("Update state changed event emitted for %s", self.name)
            self.async_schedule_update_ha_state()
        else:
            _LOGGER.debug(
                "Update state changed event for %s not emitted. Entity is disabled",
                self.name,
            )


class AioHomematicHubUpdate(UpdateEntity):
    """Representation of the HomematicIP update entity."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_entity_registry_enabled_default = True

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: HmUpdate,
    ) -> None:
        """Initialize the hub entity."""
        self._cu: ControlUnit = control_unit
        self._data_point: HmUpdate = data_point
        self._attr_unique_id = f"{DOMAIN}_{data_point.unique_id}"
        self._attr_device_info = control_unit.device_info
        self._attr_supported_features = (
            UpdateEntityFeature.BACKUP | UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS
            if control_unit.central.system_information.ccu_type == CCUType.OPENCCU
            else UpdateEntityFeature.INSTALL
        )
        self._unsubscribe_callbacks: list[UnsubscribeCallback] = []
        _LOGGER.debug("init: Setting up %s", data_point.full_name)

    @property
    def available(self) -> bool:
        """Return if data point is available."""
        return self._data_point.available

    @property
    def in_progress(self) -> bool | None:
        """Update installation progress."""
        return self._data_point.in_progress

    @property
    def installed_version(self) -> str | None:
        """Version installed and in use."""
        return self._data_point.current_firmware

    @property
    def latest_version(self) -> str | None:
        """Latest version available for install."""
        return self._data_point.available_firmware or self._data_point.current_firmware

    @property
    def name(self) -> str | UndefinedType | None:
        """Return the name of the entity."""
        return self._data_point.name

    async def async_added_to_hass(self) -> None:
        """Register callbacks and load initial data."""
        self._unsubscribe_callbacks.append(
            self._data_point.subscribe_to_data_point_updated(
                handler=self._async_entity_changed, custom_id=self.entity_id
            )
        )
        self._unsubscribe_callbacks.append(
            self._data_point.subscribe_to_device_removed(handler=self._async_device_removed)
        )

    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None:
        """Install an update."""
        if backup:
            await self._async_create_backup()
        await self._data_point.install()

    async def async_update(self) -> None:
        """Update entity."""

    async def async_will_remove_from_hass(self) -> None:
        """Run when hmip device will be removed from hass."""
        # Remove callback from device.
        for unregister in self._unsubscribe_callbacks:
            if unregister is not None:
                unregister()

    async def _async_create_backup(self) -> None:
        """Create a backup before installing the update."""
        try:
            backup_data = await self._cu.central.create_backup_and_download()
            if backup_data is None:
                raise HomeAssistantError("Failed to create backup before update")

            # Save backup to file
            backup_dir = Path(self._cu.backup_directory)
            backup_dir.mkdir(parents=True, exist_ok=True)

            backup_path = backup_dir / backup_data.filename

            await self.hass.async_add_executor_job(backup_path.write_bytes, backup_data.content)

            _LOGGER.info(
                "CCU backup saved to %s (%d bytes) before firmware update", backup_path, len(backup_data.content)
            )
        except BaseHomematicException as err:
            raise HomeAssistantError(f"Failed to create backup before update: {err}") from err

    @callback
    def _async_device_removed(self) -> None:
        """Handle hm device removal."""
        self.hass.async_create_task(self.async_remove(force_remove=True))

        if not self.registry_entry:
            return

        if device_id := self.registry_entry.device_id:
            # Remove from device registry.
            device_registry = dr.async_get(self.hass)
            if device_id in device_registry.devices:
                # This will also remove associated entities from entity registry.
                device_registry.async_remove_device(device_id)

    @callback
    def _async_entity_changed(self, *args: Any, **kwargs: Any) -> None:
        """Handle device state changes."""
        # Don't update disabled entities
        if self.enabled:
            _LOGGER.debug("Update state changed event emitted for %s", self.name)
            self.async_schedule_update_ha_state()
        else:
            _LOGGER.debug(
                "Update state changed event for %s not emitted. Entity is disabled",
                self.name,
            )
