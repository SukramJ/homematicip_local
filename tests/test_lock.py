"""Tests for lock entities of Homematic(IP) Local."""

from __future__ import annotations

import asyncio

import pytest

from homeassistant.components.lock import LockState
from homeassistant.core import HomeAssistant

from tests import const, helper
from tests.helper import Factory

TEST_DEVICES: dict[str, str] = {
    "VCU9724704": "HmIP-DLD.json",
}

_ENTITY_ID = "lock.hmip_dld_vcu9724704"
_ENTITY_NAME = "HmIP-DLD_VCU9724704"

# HmIP-DLD channel 1 event sequences recorded in homematicip_local#1343.
# Each step is (LOCK_STATE, ACTIVITY_STATE, expected HA state).
# LOCK_STATE: 1=LOCKED, 2=UNLOCKED. ACTIVITY_STATE: 1=UP, 2=DOWN, 3=STABLE.
_OPEN_FROM_UNLOCKED: tuple[tuple[int, int, LockState], ...] = (
    (2, 1, LockState.OPENING),
    (2, 1, LockState.OPENING),
    (2, 2, LockState.OPENING),
    (2, 3, LockState.UNLOCKED),
)
_OPEN_FROM_LOCKED: tuple[tuple[int, int, LockState], ...] = (
    (2, 1, LockState.OPENING),
    (2, 2, LockState.OPENING),
    (2, 3, LockState.UNLOCKED),
)
_LOCK: tuple[tuple[int, int, LockState], ...] = (
    (2, 2, LockState.LOCKING),
    (1, 3, LockState.LOCKED),
)
_UNLOCK: tuple[tuple[int, int, LockState], ...] = (
    (1, 1, LockState.UNLOCKING),
    (2, 3, LockState.UNLOCKED),
)


async def _send(*, hass: HomeAssistant, control: object, parameter: str, value: int) -> None:
    """Send a channel 1 event and wait until HA has processed it."""
    await control.central.event_coordinator.data_point_event(  # type: ignore[attr-defined]
        interface_id=const.INTERFACE_ID, channel_address="VCU9724704:1", parameter=parameter, value=value
    )
    await hass.async_block_till_done()
    await asyncio.sleep(0.1)
    await hass.async_block_till_done()


class TestIpLock:
    """Tests for the HmIP-DLD lock entity."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("initial_lock_state", "sequence"),
        [
            (2, _OPEN_FROM_UNLOCKED),
            (1, _OPEN_FROM_LOCKED),
            (2, _LOCK),
            (1, _UNLOCK),
        ],
        ids=["open_from_unlocked", "open_from_locked", "lock", "unlock"],
    )
    async def test_lock_movement_state(
        self,
        factory_homegear: Factory,
        initial_lock_state: int,
        sequence: tuple[tuple[int, int, LockState], ...],
    ) -> None:
        """Replay recorded DLD sequences; opening the latch must never show as locking."""
        hass, control = await factory_homegear.setup_environment(TEST_DEVICES)
        helper.get_and_check_state(hass=hass, control=control, entity_id=_ENTITY_ID, entity_name=_ENTITY_NAME)

        await _send(hass=hass, control=control, parameter="LOCK_STATE", value=initial_lock_state)
        await _send(hass=hass, control=control, parameter="ACTIVITY_STATE", value=3)

        for lock_state, activity_state, expected in sequence:
            # The backend sends LOCK_STATE before ACTIVITY_STATE within one multicall.
            await _send(hass=hass, control=control, parameter="LOCK_STATE", value=lock_state)
            await _send(hass=hass, control=control, parameter="ACTIVITY_STATE", value=activity_state)
            assert hass.states.get(_ENTITY_ID).state == expected
