"""Tests for reloading a loom entry when its central's system information changes.

The integration reads ``system_information`` once, when it creates its
entities. The loom backend publishes ``SystemInformationChangedEvent`` when a
re-read differs; the control unit reloads its entry when the type or a
capability moved, and only then.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from openccu_loom_client.compat.aiohomematic.central.events import SystemInformationChangedEvent
from openccu_loom_client.compat.aiohomematic.const import LoomSystemInformation

from aiohomematic.central.events import EventBus
from aiohomematic.const import CCUType
from custom_components.homematicip_local.const import BACKEND_CCU, BACKEND_LOOM
from custom_components.homematicip_local.control_unit import BaseControlUnit, ControlUnit

_CU = "custom_components.homematicip_local.control_unit"
_ENTRY_ID = "loom-entry"
_CENTRAL_NAME = "box-central"
_BEFORE = LoomSystemInformation(
    ccu_type=CCUType.OPENCCU_LITE,
    backup_available=False,
    system_update_available=False,
    version="1.0.0",
    hostname="box",
)


def _make_control_unit(*, backend: str) -> tuple[ControlUnit, EventBus, MagicMock]:
    """Return a control unit on a real aiohomematic event bus, its bus, and its hass mock."""
    bus = EventBus(task_scheduler=MagicMock())
    central = MagicMock()
    central.name = _CENTRAL_NAME
    central.event_bus = bus
    hass = MagicMock()
    control_unit = object.__new__(ControlUnit)
    control_unit._config = SimpleNamespace(backend=backend)
    control_unit._hass = hass
    control_unit._entry_id = _ENTRY_ID
    control_unit._central = central
    control_unit._enable_mqtt = False
    control_unit._mqtt_consumer = None
    control_unit._orphan_cleanup_unsub = None
    control_unit._subscription_group = bus.create_subscription_group(name="homematicip_local")
    return control_unit, bus, hass


async def _start(control_unit: ControlUnit) -> None:
    """Run the production start_central with its unrelated collaborators stubbed."""
    with (
        patch.object(BaseControlUnit, "start_central", AsyncMock()),
        patch.object(ControlUnit, "_async_add_central_to_device_registry"),
        patch.object(ControlUnit, "_async_signal_central_state_changed"),
        patch(f"{_CU}.async_call_later"),
    ):
        await control_unit.start_central()


async def _stop(control_unit: ControlUnit) -> None:
    """Run the production stop_central with the base teardown stubbed."""
    with patch.object(BaseControlUnit, "stop_central", AsyncMock()):
        await control_unit.stop_central()


def _event(*, current: LoomSystemInformation, central_name: str = _CENTRAL_NAME) -> SystemInformationChangedEvent:
    return SystemInformationChangedEvent(
        timestamp=datetime.now(tz=UTC),
        central_name=central_name,
        previous=_BEFORE,
        current=current,
    )


class TestReloadOnSystemInformationChange:
    """A loom entry reloads when ccu_type, has_backup or has_system_update moved."""

    async def test_backup_change_reloads_once(self) -> None:
        control_unit, bus, hass = _make_control_unit(backend=BACKEND_LOOM)
        await _start(control_unit)

        await bus.publish(event=_event(current=replace(_BEFORE, backup_available=True)))

        hass.config_entries.async_schedule_reload.assert_called_once_with(_ENTRY_ID)

    async def test_ccu_backend_does_not_subscribe(self) -> None:
        control_unit, bus, hass = _make_control_unit(backend=BACKEND_CCU)
        await _start(control_unit)

        assert bus.get_subscription_count(event_type=SystemInformationChangedEvent) == 0
        await bus.publish(event=_event(current=replace(_BEFORE, backup_available=True)))

        hass.config_entries.async_schedule_reload.assert_not_called()

    async def test_ccu_type_change_reloads(self) -> None:
        control_unit, bus, hass = _make_control_unit(backend=BACKEND_LOOM)
        await _start(control_unit)

        await bus.publish(event=_event(current=replace(_BEFORE, ccu_type=CCUType.UNKNOWN)))

        hass.config_entries.async_schedule_reload.assert_called_once_with(_ENTRY_ID)

    async def test_event_for_other_central_does_not_reload(self) -> None:
        control_unit, bus, hass = _make_control_unit(backend=BACKEND_LOOM)
        await _start(control_unit)

        await bus.publish(event=_event(current=replace(_BEFORE, backup_available=True), central_name="other"))

        hass.config_entries.async_schedule_reload.assert_not_called()

    async def test_no_reload_after_unload(self) -> None:
        control_unit, bus, hass = _make_control_unit(backend=BACKEND_LOOM)
        await _start(control_unit)
        await _stop(control_unit)

        await bus.publish(event=_event(current=replace(_BEFORE, backup_available=True)))

        hass.config_entries.async_schedule_reload.assert_not_called()

    async def test_system_update_change_reloads(self) -> None:
        control_unit, bus, hass = _make_control_unit(backend=BACKEND_LOOM)
        await _start(control_unit)

        await bus.publish(event=_event(current=replace(_BEFORE, system_update_available=True)))

        hass.config_entries.async_schedule_reload.assert_called_once_with(_ENTRY_ID)

    async def test_version_or_hostname_change_does_not_reload(self) -> None:
        control_unit, bus, hass = _make_control_unit(backend=BACKEND_LOOM)
        await _start(control_unit)

        await bus.publish(event=_event(current=replace(_BEFORE, version="1.0.1")))
        await bus.publish(event=_event(current=replace(_BEFORE, hostname="box-renamed")))

        hass.config_entries.async_schedule_reload.assert_not_called()
