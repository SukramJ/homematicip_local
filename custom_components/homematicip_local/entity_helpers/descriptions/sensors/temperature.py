"""Temperature sensor entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature

from ...factories import diagnostic_sensor, measurement_sensor
from ...registry import EntityDescriptionRule

# Devices where temperature is diagnostic info (switch devices with internal sensor)
_TEMPERATURE_DIAGNOSTIC_DEVICES: tuple[str, ...] = (
    "ELV-SH-BS",
    "HmIP-BB",
    "HmIP-BD",
    "HmIP-BR",
    "HmIP-BS",
    "HmIP-DR",
    "HmIP-FB",
    "HmIP-FD",
    "HmIP-FR",
    "HmIP-FS",
    "HmIP-MOD-OC8",
    "HmIP-PCB",
    "HmIP-PD",
    "HmIP-PS",
    "HmIP-USB",
    "HmIPW-DR",
    "HmIPW-FIO",
)


TEMPERATURE_SENSOR_RULES: list[EntityDescriptionRule] = [
    # Device-specific: Temperature as diagnostic on switch devices
    # Higher priority (10) to override the generic rule
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("ACTUAL_TEMPERATURE",),
        devices=_TEMPERATURE_DIAGNOSTIC_DEVICES,
        priority=10,
        description=diagnostic_sensor(
            key="ACTUAL_TEMPERATURE",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit=UnitOfTemperature.CELSIUS,
        ),
    ),
    # Generic temperature sensor
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("ACTUAL_TEMPERATURE", "TEMPERATURE"),
        description=measurement_sensor(
            key="TEMPERATURE",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit=UnitOfTemperature.CELSIUS,
        ),
    ),
    # Dew point
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("DEWPOINT", "DEW_POINT"),
        description=measurement_sensor(
            key="DEW_POINT",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit=UnitOfTemperature.CELSIUS,
            translation_key="dew_point",
            entity_registry_enabled_default=False,
        ),
    ),
    # Dew point spread (uses Kelvin)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("DEW_POINT_SPREAD",),
        description=measurement_sensor(
            key="DEW_POINT_SPREAD",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit=UnitOfTemperature.KELVIN,
            entity_registry_enabled_default=False,
        ),
    ),
    # Apparent temperature / Frost point (disabled by default)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("APPARENT_TEMPERATURE", "FROST_POINT"),
        description=measurement_sensor(
            key="APPARENT_TEMPERATURE",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit=UnitOfTemperature.CELSIUS,
            entity_registry_enabled_default=False,
        ),
    ),
]
