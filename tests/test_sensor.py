"""Tests for switch entities of aiohomematic."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import PropertyMock, patch

import pytest

from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity
from custom_components.homematicip_local.sensor import AioHomematicSensor
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import STATE_UNKNOWN

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
