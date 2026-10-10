"""Tests for switch entities of aiohomematic."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import PropertyMock, patch

import pytest

from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity
from custom_components.homematicip_local.sensor import AioHomematicSensor
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import STATE_UNKNOWN, UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests import const, helper
from tests.helper import Factory


def _make_sensor(*, unit: str | None, values: tuple[str, ...] | None) -> AioHomematicSensor:
    """Build an ``AioHomematicSensor`` exercising only its own ``__init__`` logic.

    The heavy base-entity initialisation is stubbed so the test focuses on the
    unit/enum decision in ``AioHomematicSensor.__init__``.
    """
    data_point = SimpleNamespace(multiplier=1, unit=unit, values=values)
    with (
        patch.object(AioHomematicGenericEntity, "__init__", return_value=None),
        patch.object(AioHomematicSensor, "device_class", new_callable=PropertyMock, return_value=None),
    ):
        return AioHomematicSensor(control_unit=None, data_point=data_point)  # type: ignore[arg-type]


TEST_DEVICES: dict[str, str] = {
    "VCU7837366": "HB-UNI-Sensor1.json",
}

ENERGY_DEVICES: dict[str, str] = {
    "VCU2128127": "HmIP-BSM.json",
}
ENERGY_COUNTER_ENTITY_ID = "sensor.hmip_bsm_vcu2128127_energy_counter"

# pylint: disable=protected-access


class TestSensor:
    """Tests for sensor entities."""

    @pytest.mark.asyncio
    async def test_sensor_to_trans(self, factory_homegear: Factory) -> None:
        """Test sensor without translation."""
        entity_id = "sensor.hb_uni_sensor1_vcu7837366_absolute_humidity"
        entity_name = "HB-UNI-Sensor1_VCU7837366 Absolute Humidity"

        hass, control = await factory_homegear.setup_environment(TEST_DEVICES)
        ha_state, data_point = helper.get_and_check_state(
            hass=hass, control=control, entity_id=entity_id, entity_name=entity_name
        )
        assert ha_state.state == STATE_UNKNOWN

        await control.central.event_coordinator.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU7837366:1", parameter="Abs_Luftfeuchte", value=1
        )
        await hass.async_block_till_done()
        await hass.async_block_till_done()
        assert hass.states.get(entity_id).state == "1.0"

        await control.central.event_coordinator.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU7837366:1", parameter="Abs_Luftfeuchte", value=0
        )
        await hass.async_block_till_done()
        await hass.async_block_till_done()
        assert hass.states.get(entity_id).state == "0.0"

    @pytest.mark.asyncio
    async def test_sensor_trans(self, factory_homegear: Factory) -> None:
        """Test sensor with translation."""
        entity_id = "sensor.hb_uni_sensor1_vcu7837366_dew_point"
        entity_name = "HB-UNI-Sensor1_VCU7837366 dew point"

        hass, control = await factory_homegear.setup_environment(TEST_DEVICES)
        ha_state, data_point = helper.get_and_check_state(
            hass=hass, control=control, entity_id=entity_id, entity_name=entity_name
        )
        assert ha_state.state == STATE_UNKNOWN

        await control.central.event_coordinator.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU7837366:1", parameter="Taupunkt", value=1
        )
        await hass.async_block_till_done()
        await hass.async_block_till_done()
        assert hass.states.get(entity_id).state == "1.0"

        await control.central.event_coordinator.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU7837366:1", parameter="Taupunkt", value=0
        )
        await hass.async_block_till_done()
        await hass.async_block_till_done()
        assert hass.states.get(entity_id).state == "0.0"


class TestSensorUnitAndEnum:
    """The unit/enum decision in ``AioHomematicSensor.__init__``."""

    def test_enum_data_point_with_unit_gets_no_unit(self) -> None:
        """An enum data point (values) must not carry a unit of measurement.

        Home Assistant rejects a unit on the non-numeric ``enum`` device class,
        so a data point reporting both ``unit`` and ``values`` (e.g. on the loom
        backend) must drop the unit and become an enum sensor.
        """
        sensor = _make_sensor(unit="V", values=("CLOSED", "OPEN", "TILTED"))
        assert getattr(sensor, "_attr_native_unit_of_measurement", None) is None
        assert sensor._attr_device_class == SensorDeviceClass.ENUM
        assert sensor._attr_options == ["closed", "open", "tilted"]

    def test_non_enum_data_point_keeps_unit(self) -> None:
        """A plain numeric data point still adopts its unit of measurement."""
        sensor = _make_sensor(unit="V", values=None)
        assert sensor._attr_native_unit_of_measurement == "V"


class TestEnergyCounterUnit:
    """ENERGY_COUNTER reports Wh and is suggested to Home Assistant in kWh."""

    @pytest.mark.asyncio
    async def test_new_energy_counter_is_shown_in_kwh(self, factory_homegear: Factory) -> None:
        """A newly registered energy counter shows kWh, converted from the device's Wh."""
        hass, control = await factory_homegear.setup_environment(ENERGY_DEVICES)

        entry = er.async_get(hass).async_get(ENERGY_COUNTER_ENTITY_ID)
        assert entry is not None
        assert entry.options["sensor.private"]["suggested_unit_of_measurement"] == UnitOfEnergy.KILO_WATT_HOUR

        await control.central.event_coordinator.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU2128127:7", parameter="ENERGY_COUNTER", value=1234.5
        )
        await hass.async_block_till_done()
        await hass.async_block_till_done()
        ha_state = hass.states.get(ENERGY_COUNTER_ENTITY_ID)
        assert ha_state.attributes["unit_of_measurement"] == UnitOfEnergy.KILO_WATT_HOUR
        assert float(ha_state.state) == pytest.approx(1.2345)

    @pytest.mark.asyncio
    async def test_registered_energy_counter_keeps_wh(self, hass: HomeAssistant, factory_homegear: Factory) -> None:
        """
        An energy counter already registered in Wh keeps Wh.

        Home Assistant stores the suggested unit only the first time it sees an
        entity, so an existing installation does not change its unit on update.
        """
        unique_id = "homematicip_local_vcu2128127_7_energy_counter"
        er.async_get(hass).async_get_or_create(
            "sensor",
            "homematicip_local",
            unique_id,
            suggested_object_id="hmip_bsm_vcu2128127_energy_counter",
            unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        )

        hass, control = await factory_homegear.setup_environment(ENERGY_DEVICES)

        entry = er.async_get(hass).async_get(ENERGY_COUNTER_ENTITY_ID)
        assert entry is not None
        assert entry.unique_id == unique_id
        assert "sensor.private" not in entry.options

        await control.central.event_coordinator.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU2128127:7", parameter="ENERGY_COUNTER", value=1234.5
        )
        await hass.async_block_till_done()
        await hass.async_block_till_done()
        ha_state = hass.states.get(ENERGY_COUNTER_ENTITY_ID)
        assert ha_state.attributes["unit_of_measurement"] == UnitOfEnergy.WATT_HOUR
        assert float(ha_state.state) == pytest.approx(1234.5)
