"""Tests for button entities of homematicip_local."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from openccu_loom_client.compat.aiohomematic.const import LoomSystemInformation
import pytest

from aiohomematic.const import CCUType, CentralState, SystemInformation
from custom_components.homematicip_local.button import HmipLocalCreateBackupButton, async_setup_entry
from custom_components.homematicip_local.const import BACKEND_CCU, BACKEND_LOOM, DOMAIN
from custom_components.homematicip_local.control_unit import BaseControlUnit, ControlUnit, signal_central_state_changed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send


def _make_backup_button(control_unit: object, *, entry_id: str = "test-entry") -> HmipLocalCreateBackupButton:
    """Create a backup button, bypassing __init__ side effects."""
    button = object.__new__(HmipLocalCreateBackupButton)
    button._cu = control_unit
    button._attr_unique_id = f"{DOMAIN}_CCU_create_backup"
    button._attr_device_info = {"identifiers": {(DOMAIN, "CCU")}}
    return button


def _make_control_unit(
    hass: HomeAssistant, *, entry_id: str = "test-entry", available: bool = False, name: str = "CCU"
) -> ControlUnit:
    """Create a minimal ControlUnit bound to a real hass, bypassing __init__."""
    control_unit = object.__new__(ControlUnit)
    control_unit._hass = hass
    control_unit._entry_id = entry_id
    central = MagicMock()
    central.available = available
    central.name = name
    control_unit._central = central
    return control_unit


class TestBackupButtonAvailability:
    """The backup button's availability tracks the central."""

    def test_available_mirrors_central_available(self) -> None:
        """Available is True once the central is available."""
        button = _make_backup_button(MagicMock(central=MagicMock(available=True)))
        assert button.available is True

    def test_available_mirrors_central_unavailable(self) -> None:
        """Available is False while the central is not available."""
        button = _make_backup_button(MagicMock(central=MagicMock(available=False)))
        assert button.available is False

    async def test_becomes_available_after_central_state_signal(self, hass: HomeAssistant) -> None:
        """
        The button flips from unavailable to available on the central-state signal.

        This is the reported bug: the button is added before the central is
        started (so it reads unavailable at add time) and has no data point or
        poll to refresh on. It must re-render when the control unit announces the
        central started. The whole path is exercised here — the production notify
        method fans out over the real dispatcher into the button's real
        subscription.
        """
        control_unit = _make_control_unit(hass, entry_id="e1", available=False)
        button = _make_backup_button(control_unit, entry_id="e1")
        button.hass = hass
        button.async_write_ha_state = Mock()
        button.async_on_remove = Mock()

        await button.async_added_to_hass()

        # Added while the central is still stopped.
        assert button.available is False

        # The central reaches its running state and the control unit announces it.
        control_unit._central.available = True
        control_unit._async_signal_central_state_changed()
        await hass.async_block_till_done()

        button.async_write_ha_state.assert_called()
        assert button.available is True

    async def test_unsubscribes_on_remove(self, hass: HomeAssistant) -> None:
        """The dispatcher subscription is torn down when the entity is removed."""
        control_unit = _make_control_unit(hass, entry_id="e1", available=False)
        button = _make_backup_button(control_unit, entry_id="e1")
        button.hass = hass
        button.async_write_ha_state = Mock()

        unsubscribes: list = []
        button.async_on_remove = unsubscribes.append

        await button.async_added_to_hass()
        assert unsubscribes, "async_added_to_hass must register an unsubscribe"

        # Simulate HA removing the entity.
        for unsubscribe in unsubscribes:
            unsubscribe()

        button.async_write_ha_state.reset_mock()
        async_dispatcher_send(hass, signal_central_state_changed(entry_id="e1"))
        await hass.async_block_till_done()

        button.async_write_ha_state.assert_not_called()


class TestCentralStateSignalWiring:
    """The control unit is the production caller of the central-state signal."""

    def test_notify_dispatches_on_the_signal(self, hass: HomeAssistant) -> None:
        """_async_signal_central_state_changed sends the entry-scoped signal."""
        control_unit = _make_control_unit(hass, entry_id="e1")
        with patch("custom_components.homematicip_local.control_unit.async_dispatcher_send") as send:
            control_unit._async_signal_central_state_changed()
        send.assert_called_once_with(hass, signal_central_state_changed(entry_id="e1"))

    async def test_runtime_state_transition_signals(self, hass: HomeAssistant) -> None:
        """Every central-state transition re-announces the change."""
        control_unit = _make_control_unit(hass, entry_id="e1")
        control_unit._instance_name = "X"
        control_unit._async_signal_central_state_changed = Mock()
        event = SimpleNamespace(new_state=CentralState.RUNNING)

        with patch.object(ControlUnit, "_on_central_running", new=AsyncMock()):
            await control_unit._on_central_state_changed(event=event)

        control_unit._async_signal_central_state_changed.assert_called_once()

    def test_signal_is_entry_scoped(self) -> None:
        """The signal name is scoped to the config entry, so entries don't cross-talk."""
        assert signal_central_state_changed(entry_id="a") != signal_central_state_changed(entry_id="b")

    async def test_start_central_signals_after_start(self, hass: HomeAssistant) -> None:
        """
        start_central announces the central-state change once the central is up.

        Without this the loom backend — which reaches its running state without
        emitting a state event — would never notify the backup button, leaving it
        unavailable forever.
        """
        control_unit = _make_control_unit(hass, entry_id="e1")
        control_unit._instance_name = "X"
        control_unit._config = SimpleNamespace(backend=BACKEND_CCU)
        control_unit._subscription_group = MagicMock()
        control_unit._enable_mqtt = False
        control_unit._orphan_cleanup_unsub = None
        control_unit._async_signal_central_state_changed = Mock()

        with (
            patch.object(ControlUnit, "_async_add_central_to_device_registry"),
            patch.object(BaseControlUnit, "start_central", new=AsyncMock()),
            patch("custom_components.homematicip_local.control_unit.async_call_later"),
        ):
            await control_unit.start_central()

        control_unit._async_signal_central_state_changed.assert_called_once()


async def _added_backup_buttons(
    hass: HomeAssistant, *, backend: str, system_information: SystemInformation
) -> list[HmipLocalCreateBackupButton]:
    """Run the button platform setup and return the backup buttons it added."""
    control_unit = MagicMock()
    control_unit.config.backend = backend
    control_unit.central.system_information = system_information
    control_unit.central.name = "CCU"
    control_unit.get_new_data_points = MagicMock(return_value=())
    control_unit.get_new_hub_data_points = MagicMock(return_value=())
    entry = MagicMock()
    entry.entry_id = "test-entry"
    entry.runtime_data = control_unit
    async_add_entities = Mock()

    await async_setup_entry(hass, entry, async_add_entities)

    return [
        entity
        for call in async_add_entities.call_args_list
        for entity in call.args[0]
        if isinstance(entity, HmipLocalCreateBackupButton)
    ]


class TestBackupButtonOffered:
    """The backup button is offered exactly when the central can create a backup, on both backends."""

    @pytest.mark.parametrize(
        ("backend", "system_information", "offered"),
        [
            (BACKEND_LOOM, LoomSystemInformation(ccu_type=CCUType.OPENCCU_LITE, backup_available=True), True),
            (BACKEND_LOOM, LoomSystemInformation(ccu_type=CCUType.OPENCCU_LITE, backup_available=False), False),
            (BACKEND_LOOM, LoomSystemInformation(ccu_type=CCUType.OPENCCU, backup_available=False), False),
            (BACKEND_LOOM, LoomSystemInformation(ccu_type=CCUType.UNKNOWN), False),
            (BACKEND_CCU, SystemInformation(ccu_type=CCUType.OPENCCU), True),
            (BACKEND_CCU, SystemInformation(ccu_type=CCUType.CCU), False),
            (BACKEND_CCU, SystemInformation(ccu_type=CCUType.UNKNOWN), False),
        ],
        ids=[
            "loom-lite-backup",
            "loom-lite-no-backup",
            "loom-openccu-no-backup",
            "loom-unknown",
            "ccu-openccu",
            "ccu-original-ccu",
            "ccu-unknown",
        ],
    )
    async def test_button_follows_has_backup(
        self, hass: HomeAssistant, backend: str, system_information: SystemInformation, offered: bool
    ) -> None:
        """The button is added if and only if system_information.has_backup holds."""
        buttons = await _added_backup_buttons(hass, backend=backend, system_information=system_information)
        assert len(buttons) == (1 if offered else 0)
