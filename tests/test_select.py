"""Tests for select entities of homematicip_local."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from custom_components.homematicip_local.const import DOMAIN
from custom_components.homematicip_local.select import (
    GARAGE_DOOR_MODE_CLOSED,
    GARAGE_DOOR_MODE_OPEN,
    GARAGE_DOOR_MODE_VENTILATION,
    AioHomematicGarageDoorModeSelect,
)


def _make_garage_door_mode_select(*, current_position: int | None) -> AioHomematicGarageDoorModeSelect:
    """Create a garage door mode select, bypassing __init__ side effects."""
    select = object.__new__(AioHomematicGarageDoorModeSelect)
    data_point = MagicMock()
    data_point.current_position = current_position
    data_point.close = AsyncMock()
    data_point.vent = AsyncMock()
    data_point.open = AsyncMock()
    select._data_point = data_point
    select._attr_unique_id = f"{DOMAIN}_garage_test_door_mode"
    return select


class TestGarageDoorModeSelectCurrentOption:
    """current_option reflects the garage door's physical position."""

    def test_closed_position_maps_to_closed(self) -> None:
        """A fully closed door reports the closed mode."""
        select = _make_garage_door_mode_select(current_position=0)
        assert select.current_option == GARAGE_DOOR_MODE_CLOSED

    def test_ventilation_position_maps_to_ventilation(self) -> None:
        """A door in the ventilation position reports the ventilation mode."""
        select = _make_garage_door_mode_select(current_position=10)
        assert select.current_option == GARAGE_DOOR_MODE_VENTILATION

    def test_open_position_maps_to_open(self) -> None:
        """A fully open door reports the open mode."""
        select = _make_garage_door_mode_select(current_position=100)
        assert select.current_option == GARAGE_DOOR_MODE_OPEN

    def test_unknown_position_maps_to_none(self) -> None:
        """An unresolvable position (e.g. during travel) reports no mode."""
        select = _make_garage_door_mode_select(current_position=None)
        assert select.current_option is None


class TestGarageDoorModeSelectOptions:
    """options always exposes exactly the three physical door modes."""

    def test_options_are_closed_ventilation_open(self) -> None:
        """The three physical states are exposed, in a stable order."""
        select = _make_garage_door_mode_select(current_position=0)
        assert select.options == [GARAGE_DOOR_MODE_CLOSED, GARAGE_DOOR_MODE_VENTILATION, GARAGE_DOOR_MODE_OPEN]


class TestGarageDoorModeSelectSelectOption:
    """async_select_option dispatches to the matching CustomDpGarage command."""

    async def test_select_closed_calls_close(self) -> None:
        """Selecting 'closed' issues the close command."""
        select = _make_garage_door_mode_select(current_position=100)
        await select.async_select_option(GARAGE_DOOR_MODE_CLOSED)
        select._data_point.close.assert_awaited_once()
        select._data_point.vent.assert_not_awaited()
        select._data_point.open.assert_not_awaited()

    async def test_select_ventilation_calls_vent(self) -> None:
        """Selecting 'ventilation' issues the vent (PARTIAL_OPEN) command."""
        select = _make_garage_door_mode_select(current_position=0)
        await select.async_select_option(GARAGE_DOOR_MODE_VENTILATION)
        select._data_point.vent.assert_awaited_once()
        select._data_point.close.assert_not_awaited()
        select._data_point.open.assert_not_awaited()

    async def test_select_open_calls_open(self) -> None:
        """Selecting 'open' issues the open command."""
        select = _make_garage_door_mode_select(current_position=0)
        await select.async_select_option(GARAGE_DOOR_MODE_OPEN)
        select._data_point.open.assert_awaited_once()
        select._data_point.close.assert_not_awaited()
        select._data_point.vent.assert_not_awaited()
