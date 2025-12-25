"""Air quality sensor entity description rules."""

from __future__ import annotations

from typing import Final

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.factories import measurement_sensor
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    CONCENTRATION_GRAMS_PER_CUBIC_METER,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
)

# Custom units
NUMBER_CONCENTRATION_CM3: Final = "1/cm\u00b3"  # HmIP-SFD
# Use greek small letter mu "\u03bc" instead of micro sign "\u00B5" for micro unit prefix
LENGTH_MICROMETER: Final = "\u03bcm"  # HmIP-SFD
KILOJOULS_PERKILOGRAM: Final = "kJ/kg"


AIR_QUALITY_SENSOR_RULES: list[EntityDescriptionRule] = [
    # CO2 concentration
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("CONCENTRATION",),
        description=measurement_sensor(
            key="CONCENTRATION",
            device_class=SensorDeviceClass.CO2,
            unit=CONCENTRATION_PARTS_PER_MILLION,
        ),
    ),
    # Humidity
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("HUMIDITY", "ACTUAL_HUMIDITY"),
        description=measurement_sensor(
            key="HUMIDITY",
            device_class=SensorDeviceClass.HUMIDITY,
            unit=PERCENTAGE,
        ),
    ),
    # Vapor concentration (absolute humidity)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("VAPOR_CONCENTRATION",),
        description=measurement_sensor(
            key="VAPOR_CONCENTRATION",
            device_class=SensorDeviceClass.ABSOLUTE_HUMIDITY,
            unit=CONCENTRATION_GRAMS_PER_CUBIC_METER,
            entity_registry_enabled_default=False,
        ),
    ),
    # Enthalpy
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("ENTHALPY",),
        description=measurement_sensor(
            key="ENTHALPY",
            unit=KILOJOULS_PERKILOGRAM,
            icon="mdi:fire",
            entity_registry_enabled_default=False,
        ),
    ),
    # PM1 mass concentration
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("MASS_CONCENTRATION_PM_1", "MASS_CONCENTRATION_PM_1_24H_AVERAGE"),
        description=measurement_sensor(
            key="MASS_CONCENTRATION_PM_1",
            device_class=SensorDeviceClass.PM1,
            unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
    ),
    # PM10 mass concentration
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("MASS_CONCENTRATION_PM_10", "MASS_CONCENTRATION_PM_10_24H_AVERAGE"),
        description=measurement_sensor(
            key="MASS_CONCENTRATION_PM_10",
            device_class=SensorDeviceClass.PM10,
            unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
    ),
    # PM2.5 mass concentration
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("MASS_CONCENTRATION_PM_2_5", "MASS_CONCENTRATION_PM_2_5_24H_AVERAGE"),
        description=measurement_sensor(
            key="MASS_CONCENTRATION_PM_2_5",
            device_class=SensorDeviceClass.PM25,
            unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ),
    ),
    # PM number concentrations
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("NUMBER_CONCENTRATION_PM_1",),
        description=measurement_sensor(
            key="NUMBER_CONCENTRATION_PM_1",
            unit=NUMBER_CONCENTRATION_CM3,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("NUMBER_CONCENTRATION_PM_10",),
        description=measurement_sensor(
            key="NUMBER_CONCENTRATION_PM_10",
            unit=NUMBER_CONCENTRATION_CM3,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("NUMBER_CONCENTRATION_PM_2_5",),
        description=measurement_sensor(
            key="NUMBER_CONCENTRATION_PM_2_5",
            unit=NUMBER_CONCENTRATION_CM3,
        ),
    ),
    # Typical particle size
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("TYPICAL_PARTICLE_SIZE",),
        description=measurement_sensor(
            key="TYPICAL_PARTICLE_SIZE",
            unit=LENGTH_MICROMETER,
        ),
    ),
    # Air pressure
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("AIR_PRESSURE",),
        description=measurement_sensor(
            key="AIR_PRESSURE",
            device_class=SensorDeviceClass.PRESSURE,
            unit="hPa",
        ),
    ),
    # Dirt level (e.g., vacuum cleaner sensors)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("DIRT_LEVEL",),
        description=measurement_sensor(
            key="DIRT_LEVEL",
            unit=PERCENTAGE,
        ),
    ),
    # Smoke level (e.g., smoke detector sensors)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("SMOKE_LEVEL",),
        description=measurement_sensor(
            key="SMOKE_LEVEL",
            unit=PERCENTAGE,
        ),
    ),
]
