"""Battery and voltage sensor entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.factories import diagnostic_sensor
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import PERCENTAGE, UnitOfElectricPotential

BATTERY_SENSOR_RULES: list[EntityDescriptionRule] = [
    # Operating voltage (battery state)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("BATTERY_STATE", "OPERATING_VOLTAGE"),
        description=diagnostic_sensor(
            key="OPERATING_VOLTAGE",
            device_class=SensorDeviceClass.VOLTAGE,
            unit=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
        ),
    ),
    # Operating voltage level (percentage)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("OPERATING_VOLTAGE_LEVEL",),
        description=diagnostic_sensor(
            key="OPERATING_VOLTAGE_LEVEL",
            device_class=SensorDeviceClass.BATTERY,
            unit=PERCENTAGE,
        ),
    ),
]
