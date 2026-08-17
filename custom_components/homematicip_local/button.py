"""button for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast, override

from aiohomematic.const import DataPointCategory, DataPointType
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.model.generic import DpButton
from aiohomematic.model.hub import ProgramDpButton
from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import UndefinedType

from . import HomematicConfigEntry
from .backend_types import LOOM_DP_ALARM_CONTROL_PANEL
from .const import DOMAIN
from .control_unit import ControlUnit, signal_central_state_changed, signal_new_data_point
from .generic_entity import (
    ATTR_DESCRIPTION,
    ATTR_NAME,
    AioHomematicAlarmEntity,
    AioHomematicGenericEntity,
    AioHomematicGenericHubEntity,
)
from .support import handle_homematic_errors

if TYPE_CHECKING:
    # Typing-only: the loom twin is absent on a CCU-only install, where the
    # dispatch tuple is empty and this entity is never constructed.
    from openccu_loom_client.compat.aiohomematic.model.alarm_panel import LoomDpAlarmControlPanel

    from aiohomematic.interfaces.model import GenericHubDataPointProtocol

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

    @callback
    def async_add_alarm_motion_reset_button(data_points: tuple[Any, ...]) -> None:
        """Add a motion-reset button per alarm panel (openccu-loom only)."""
        _LOGGER.debug("ASYNC_ADD_ALARM_MOTION_RESET_BUTTON: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicAlarmMotionResetButton(control_unit=control_unit, data_point=data_point)
            for data_point in data_points
            # Loom-only surface: the tuple is empty on a CCU-only install.
            if isinstance(data_point, LOOM_DP_ALARM_CONTROL_PANEL)
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.BUTTON),
            target=async_add_button,
        )
    )

    # The reset button rides the alarm panel data point, so it spawns off the
    # same announce a panel does — including a zone created at runtime.
    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.ALARM_CONTROL_PANEL),
            target=async_add_alarm_motion_reset_button,
        )
    )

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.HUB_BUTTON),
            target=async_add_program_button,
        )
    )

    async_add_button(
        data_points=control_unit.get_new_data_points(
            data_point_type=DataPointType.BUTTON, category=DataPointCategory.BUTTON
        )
    )

    async_add_program_button(data_points=control_unit.get_new_hub_data_points(data_point_type=ProgramDpButton))

    async_add_alarm_motion_reset_button(
        data_points=control_unit.get_new_data_points(data_point_type=DataPointType.ALARM_CONTROL_PANEL)
    )

    # Add hub-level backup button
    async_add_entities([HmipLocalCreateBackupButton(control_unit=control_unit)])


class AioHomematicButton(AioHomematicGenericEntity[DpButton], ButtonEntity):
    """Representation of the Homematic(IP) Local for OpenCCU button."""

    @override
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

    @override
    async def async_press(self) -> None:
        """Execute a button press."""
        await self._data_point.press()


class AioHomematicAlarmMotionResetButton(AioHomematicAlarmEntity, ButtonEntity):
    """
    Clears a zone's latched motion/presence detectors (openccu-loom).

    A detector holds its ``MOTION`` flag until the device's own blocking
    time expires, and reads as open until then — which blocks an arm or
    forces an auto-bypass with nothing to do but wait. This is the
    control that ends the wait; the daemon offers the same one in its own
    UI and over MQTT.

    Deliberately **not** ``EntityCategory.CONFIG``. openccu-loom shipped
    it that way first and nobody found it: Home Assistant files config
    entities into a collapsed section of the device page and keeps them
    out of dashboards. This is an operator control, so it stays a plain
    one; only the counter beside it is diagnostic.

    Rides the panel data point, so it inherits the panel's availability,
    its refresh subscription and its removal when a zone disappears.
    """

    _attr_translation_key = "alarm_reset_motion"

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: LoomDpAlarmControlPanel,
    ) -> None:
        """Initialize the motion-reset button."""
        super().__init__(
            control_unit=control_unit,
            # Same structural-satisfaction cast the panel platform makes:
            # only the enum homes differ nominally.
            data_point=cast("GenericHubDataPointProtocol", data_point),
        )
        # The base keys the unique id on the data point alone, which the
        # panel entity already claims — this rides the same data point.
        self._attr_unique_id = f"{DOMAIN}_{data_point.unique_id}_reset_motion"
        # One device holds every zone, so the zone has to be in the entity
        # name or the buttons are indistinguishable. Only used when the
        # daemon's own name is unavailable — see `name`.
        self._attr_translation_placeholders = {"zone": data_point.name}

    @property
    def _panel(self) -> LoomDpAlarmControlPanel:
        """Return the data point as its concrete loom type."""
        return cast("LoomDpAlarmControlPanel", self._data_point)

    @property
    @override
    def name(self) -> str | UndefinedType | None:
        """
        Return the daemon's name for this button, else compose one here.

        openccu-loom is the naming authority for its own entities and has
        named this button in its i18n catalogue all along — the words
        just never left the MQTT discovery plane, so this integration
        wrote them a second time. Rendering the daemon's copy is what
        keeps a zone reading the same whether Home Assistant learned it
        through this backend or through the daemon's MQTT bridge.

        The fallback below is the local translation, which a daemon
        without the catalogue route leaves in charge. Note what is *not*
        used: the hub base prefers the data point's own resolved name,
        and that name belongs to the *panel* this entity rides — taking
        it would leave the button and the panel sharing one name.

        The isinstance check is not belt-and-braces: `getattr` on a mock
        answers with a truthy mock, and a bare truthiness test would make
        every mocked panel in a test suite take this branch.
        """
        if isinstance(daemon_name := self._panel.reset_motion_name, str) and daemon_name:
            return daemon_name
        return super(AioHomematicGenericHubEntity, self).name

    @handle_homematic_errors
    @override
    async def async_press(self) -> None:
        """Clear this zone's latched detectors (master: every zone)."""
        result = await self._panel.reset_motion()
        if result.failed:
            # Not an error: the verb ran and the daemon reports the partial
            # outcome in the body. Raising would claim nothing happened.
            _LOGGER.warning(
                "Motion reset for %s: %i detector(s) cleared, %i did not answer",
                self._panel.name,
                result.reset,
                result.failed,
            )
        else:
            _LOGGER.debug("Motion reset for %s: %i detector(s) cleared", self._panel.name, result.reset)


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
    @override
    def available(self) -> bool:
        """Return if entity is available."""
        return self._cu.central.available

    @override
    async def async_added_to_hass(self) -> None:
        """Re-evaluate availability whenever the central's state changes.

        Home Assistant sets this platform up before the central is started, so
        at add time the central is still stopped and ``available`` reads False.
        This entity rides no data point and does not poll, so without a
        subscription it would keep that first reading forever — across restarts
        and reloads. The control unit fans a signal out once the central has
        started and on every later state transition; re-render on each.
        """
        await super().async_added_to_hass()
        self.async_on_remove(
            async_dispatcher_connect(
                hass=self.hass,
                signal=signal_central_state_changed(entry_id=self._cu.entry_id),
                target=self._async_central_state_changed,
            )
        )

    @override
    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            backup_data = await self._cu.central.create_backup_and_download()
            if backup_data is None:
                raise HomeAssistantError("Failed to create and download CCU backup")

            # Save backup to file
            backup_dir = Path(self._cu.backup_directory)
            backup_path = backup_dir / backup_data.filename

            def _write_backup() -> None:
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_path.write_bytes(backup_data.content)

            await self.hass.async_add_executor_job(_write_backup)

            _LOGGER.info("CCU backup saved to %s (%d bytes)", backup_path, len(backup_data.content))
        except BaseHomematicException as err:
            raise HomeAssistantError(f"Failed to create CCU backup: {err}") from err

    @callback
    def _async_central_state_changed(self) -> None:
        """Write the entity state after the central's availability may have changed."""
        self.async_write_ha_state()
