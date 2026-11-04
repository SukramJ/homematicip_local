"""Tests for climate entities of Homematic(IP) Local."""

from __future__ import annotations

import inspect

import pytest

from custom_components.homematicip_local.climate import AioHomematicClimate
from homeassistant.components.climate import ATTR_CURRENT_TEMPERATURE
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant

from tests import const, helper
from tests.helper import Factory

TEST_DEVICES: dict[str, str] = {
    "VCU3609622": "HmIP-eTRV-2.json",
}

_ENTITY_ID = "climate.hmip_etrv_2_vcu3609622"
_ENTITY_NAME = "HmIP-eTRV-2_VCU3609622"
_CHANNEL_ADDRESS = "VCU3609622:1"


async def _send(*, hass: HomeAssistant, control: object, parameter: str, value: float) -> None:
    """Send a channel 1 event and wait until HA has processed it."""
    await control.central.event_coordinator.data_point_event(  # type: ignore[attr-defined]
        interface_id=const.INTERFACE_ID, channel_address=_CHANNEL_ADDRESS, parameter=parameter, value=value
    )
    await hass.async_block_till_done()
    await hass.async_block_till_done()


class TestIpThermostat:
    """Tests for the HmIP-eTRV-2 climate entity."""

    def test_entity_provides_native_temperatures(self) -> None:
        """The entity implements HA's native_ temperature API, not the deprecated names.

        Home Assistant 2026.11 serves a subclass that still provides ``current_temperature``
        or ``target_temperature`` through a fallback and logs a deprecation; from 2027.11 on
        such an entity reports no temperatures at all. Read off the class, so the fallback
        HA installs for a deprecated override is not mistaken for the real property.
        """
        for name in ("native_current_temperature", "native_target_temperature"):
            assert isinstance(inspect.getattr_static(AioHomematicClimate, name), property), name
        for name in ("current_temperature", "target_temperature", "_attr_temperature_unit"):
            assert name not in vars(AioHomematicClimate), name

    @pytest.mark.asyncio
    async def test_temperatures_reach_the_state(self, factory_homegear: Factory) -> None:
        """Measured and target temperature from the device show up as HA state attributes."""
        hass, control = await factory_homegear.setup_environment(TEST_DEVICES)
        helper.get_and_check_state(hass=hass, control=control, entity_id=_ENTITY_ID, entity_name=_ENTITY_NAME)

        await _send(hass=hass, control=control, parameter="ACTUAL_TEMPERATURE", value=21.5)
        await _send(hass=hass, control=control, parameter="SET_POINT_TEMPERATURE", value=23.0)

        attributes = hass.states.get(_ENTITY_ID).attributes
        assert attributes[ATTR_CURRENT_TEMPERATURE] == 21.5
        assert attributes[ATTR_TEMPERATURE] == 23.0
        assert attributes["temperature_unit"] == UnitOfTemperature.CELSIUS
