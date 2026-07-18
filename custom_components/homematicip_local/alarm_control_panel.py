"""Alarm control panel platform for Homematic(IP) Local for OpenCCU.

This platform exists only on the openccu-loom backend: the daemon
(≥ 0.42.0) ships a native, local-first alarm engine and models each
alarm area (plus — with two or more areas — an aggregate master panel)
as a first-class panel entity. aiohomematic has no alarm engine, so
there is no aiohomematic class to pair with — dispatch runs on the
loom twin alone (``LOOM_DP_ALARM_CONTROL_PANEL`` degrades to the empty
tuple on a CCU-only install and the platform spawns nothing).

State tokens are daemon-computed (``alarmpanel.StateToken``) and match
Home Assistant's ``AlarmControlPanelState`` values 1:1; commands map
onto the daemon's protection modes exactly like its own MQTT command
plane (``ARM_HOME`` → ``perimeter``, ``ARM_AWAY`` → ``full``, …). The
master panel fans arm/disarm out to the real areas client-side,
mirroring the daemon's MQTT ``MasterArm`` semantics.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast, override

from aiohomematic.const import DataPointCategory, DataPointType
from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity
from homeassistant.components.alarm_control_panel.const import (
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
    CodeFormat,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HomematicConfigEntry
from .backend_types import LOOM_DP_ALARM_CONTROL_PANEL
from .control_unit import ControlUnit, signal_new_data_point
from .generic_entity import AioHomematicGenericHubEntity
from .support import handle_homematic_errors

if TYPE_CHECKING:
    # Typing-only: the platform never instantiates without the loom backend
    # (the dispatch tuple is empty on a CCU-only install), so the runtime
    # import stays optional in backend_types.
    from openccu_loom_client.compat.aiohomematic.model.alarm_panel import LoomDpAlarmControlPanel

    from aiohomematic.interfaces.model import GenericHubDataPointProtocol

_LOGGER = logging.getLogger(__name__)

# Daemon protection mode → HA arm feature. The vocabulary is wire-stable
# (docs/alarm-concept.md §13.3 in the openccu-loom repo).
_FEATURE_BY_MODE: dict[str, AlarmControlPanelEntityFeature] = {
    "perimeter": AlarmControlPanelEntityFeature.ARM_HOME,
    "full": AlarmControlPanelEntityFeature.ARM_AWAY,
    "night": AlarmControlPanelEntityFeature.ARM_NIGHT,
    "vacation": AlarmControlPanelEntityFeature.ARM_VACATION,
    "custom": AlarmControlPanelEntityFeature.ARM_CUSTOM_BYPASS,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU alarm control panel platform."""
    control_unit: ControlUnit = entry.runtime_data

    @callback
    def async_add_alarm_control_panel(data_points: tuple[Any, ...]) -> None:
        """Add alarm control panels from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_ALARM_CONTROL_PANEL: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicAlarmControlPanel(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
            # Loom-only surface: the tuple is empty on a CCU-only install,
            # so a stray announce can never spawn a panel there.
            if isinstance(data_point, LOOM_DP_ALARM_CONTROL_PANEL)
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.ALARM_CONTROL_PANEL),
            target=async_add_alarm_control_panel,
        )
    )

    async_add_alarm_control_panel(
        data_points=control_unit.get_new_data_points(data_point_type=DataPointType.ALARM_CONTROL_PANEL)
    )


class AioHomematicAlarmControlPanel(AioHomematicGenericHubEntity, AlarmControlPanelEntity):
    """Representation of the HomematicIP alarm control panel entity (openccu-loom)."""

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: LoomDpAlarmControlPanel,
    ) -> None:
        """Initialize the alarm control panel entity."""
        super().__init__(
            control_unit=control_unit,
            # The loom twin satisfies the hub protocol structurally (its
            # protocol tail is pinned client-side); only the enum homes
            # differ nominally, hence the cast.
            data_point=cast("GenericHubDataPointProtocol", data_point),
        )
        features = AlarmControlPanelEntityFeature(0)
        for mode in data_point.supported_modes:
            features |= _FEATURE_BY_MODE.get(mode, AlarmControlPanelEntityFeature(0))
        self._attr_supported_features = features

    @property
    def _panel(self) -> LoomDpAlarmControlPanel:
        """Return the data point as its concrete loom type."""
        return cast("LoomDpAlarmControlPanel", self._data_point)

    @property
    @override
    def alarm_state(self) -> AlarmControlPanelState | None:
        """Return the daemon-computed panel state (tokens match 1:1)."""
        try:
            return AlarmControlPanelState(self._panel.state)
        except ValueError:
            _LOGGER.debug("Unknown alarm panel state token: %s", self._panel.state)
            return None

    @property
    @override
    def code_arm_required(self) -> bool:
        """
        Return whether arming prompts for a code.

        Daemon-computed effective policy (openccu-loom-client ≥ 2026.7.13:
        area policy AND an applicable enabled PIN exists; the master panel
        aggregates any-area). Live policy edits ride ``alarm.panel_changed``,
        so this stays a property rather than a spawn-time ``_attr_``.
        """
        return self._panel.code_arm_required

    @property
    @override
    def code_format(self) -> CodeFormat | None:
        """
        Return the code-prompt format: numeric while any verb needs a code.

        Mirrors the daemon's own MQTT discovery (``code: REMOTE_CODE`` — a
        numeric code validated remotely). ``None`` hides the code field
        entirely; the daemon still enforces server-side either way (403 →
        error toast).
        """
        if self._panel.code_arm_required or self._panel.code_disarm_required:
            return CodeFormat.NUMBER
        return None

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the panel's live detail (mode, countdown, readiness, incident)."""
        return dict(self._panel.attributes)

    @handle_homematic_errors
    @override
    async def async_alarm_arm_away(self, code: str | None = None) -> None:
        """Arm in full mode (HA: away)."""
        await self._panel.arm(mode="full", code=code)

    @handle_homematic_errors
    @override
    async def async_alarm_arm_custom_bypass(self, code: str | None = None) -> None:
        """Arm in the user-defined custom mode."""
        await self._panel.arm(mode="custom", code=code)

    @handle_homematic_errors
    @override
    async def async_alarm_arm_home(self, code: str | None = None) -> None:
        """Arm in perimeter mode (HA: home)."""
        await self._panel.arm(mode="perimeter", code=code)

    @handle_homematic_errors
    @override
    async def async_alarm_arm_night(self, code: str | None = None) -> None:
        """Arm in night mode."""
        await self._panel.arm(mode="night", code=code)

    @handle_homematic_errors
    @override
    async def async_alarm_arm_vacation(self, code: str | None = None) -> None:
        """Arm in vacation mode."""
        await self._panel.arm(mode="vacation", code=code)

    @handle_homematic_errors
    @override
    async def async_alarm_disarm(self, code: str | None = None) -> None:
        """Disarm the panel's area (master: every area, best-effort)."""
        await self._panel.disarm(code=code)
