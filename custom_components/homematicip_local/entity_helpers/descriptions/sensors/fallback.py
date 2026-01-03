"""
Fallback sensor entity description rules based on unit.

These rules have very low priority and only match when no other rule matches.
They provide basic state_class and device_class for sensors based on their unit.
"""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.factories import measurement_sensor
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import CONCENTRATION_GRAMS_PER_CUBIC_METER, PERCENTAGE, UnitOfPressure, UnitOfTemperature

# Priority for fallback rules (very low, so they only match when nothing else does)
_FALLBACK_PRIORITY = -100


FALLBACK_SENSOR_RULES: list[EntityDescriptionRule] = [
    # Percentage fallback
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        unit=PERCENTAGE,
        priority=_FALLBACK_PRIORITY,
        description=measurement_sensor(
            key="PERCENTAGE_FALLBACK",
            unit=PERCENTAGE,
        ),
    ),
    # Pressure (bar) fallback
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        unit=UnitOfPressure.BAR,
        priority=_FALLBACK_PRIORITY,
        description=measurement_sensor(
            key="PRESSURE_BAR_FALLBACK",
            device_class=SensorDeviceClass.PRESSURE,
            unit=UnitOfPressure.BAR,
        ),
    ),
    # Temperature (Celsius) fallback
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        unit=UnitOfTemperature.CELSIUS,
        priority=_FALLBACK_PRIORITY,
        description=measurement_sensor(
            key="TEMPERATURE_CELSIUS_FALLBACK",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit=UnitOfTemperature.CELSIUS,
        ),
    ),
    # Absolute humidity (g/m³) fallback
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        unit=CONCENTRATION_GRAMS_PER_CUBIC_METER,
        priority=_FALLBACK_PRIORITY,
        description=measurement_sensor(
            key="CONCENTRATION_FALLBACK",
            unit=CONCENTRATION_GRAMS_PER_CUBIC_METER,
        ),
    ),
]
