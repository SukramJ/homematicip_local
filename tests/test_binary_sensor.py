"""Tests for binary_sensor entities of aiohomematic."""

from __future__ import annotations

import pytest

from homeassistant.const import STATE_OFF, STATE_ON

from tests import const, helper
from tests.helper import Factory

TEST_DEVICES: dict[str, str] = {
    "VCU5864966": "HmIP-SWDO-I.json",
}

# pylint: disable=protected-access


class TestHmBinarySensor:
    """Tests for HmBinarySensor entity."""

    @pytest.mark.asyncio
    async def test_hmbinarysensor(
        self,
        factory_homegear: Factory,
    ) -> None:
        """Test HmBinarySensor."""

        entity_id = "binary_sensor.hmip_swdo_i_vcu5864966"
        entity_name = "HmIP-SWDO-I_VCU5864966"

        hass, control = await factory_homegear.setup_environment(TEST_DEVICES)
        ha_state, data_point = helper.get_and_check_state(
            hass=hass, control=control, entity_id=entity_id, entity_name=entity_name
        )

        assert ha_state.state == STATE_OFF

        await control.central.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU5864966:1", parameter="STATE", value=1
        )
        await hass.async_block_till_done()
        assert hass.states.get(entity_id).state == STATE_ON

        await control.central.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU5864966:1", parameter="STATE", value=0
        )
        await hass.async_block_till_done()
        assert hass.states.get(entity_id).state == STATE_OFF

        await control.central.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU5864966:1", parameter="STATE", value=None
        )
        await hass.async_block_till_done()
        assert hass.states.get(entity_id).state == STATE_OFF


class TestSysvarDpBinarySensor:
    """Tests for SysvarDpBinarySensor entity."""

    @pytest.mark.asyncio
    async def test_hmsysvarbinarysensor(
        self,
        factory_ccu: Factory,
    ) -> None:
        """Test SysvarDpBinarySensor."""
        entity_id = "binary_sensor.centraltest_sv_logic"
        entity_name = "CentralTest SV logic"

        hass, control = await factory_ccu.setup_environment({})
        ha_state, data_point = helper.get_and_check_state(
            hass=hass, control=control, entity_id=entity_id, entity_name=entity_name
        )

        assert ha_state.state == STATE_OFF
