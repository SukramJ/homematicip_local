"""Level sensor entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.base import HmSensorEntityDescription
from custom_components.homematicip_local.entity_helpers.factories import measurement_sensor, simple_sensor
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import PERCENTAGE

# Device groups for LEVEL parameter handling
_THERMOSTAT_DEVICES: tuple[str, ...] = (
    "HmIP-eTRV",
    "HmIP-HEATING",
    "HmIP-FALMOT-C12",
    "HmIPW-FALMOT-C12",
)

_COVER_DEVICES: tuple[str, ...] = (
    "HmIP-BROLL",
    "HmIP-FROLL",
    "HmIP-BBL",
    "HmIP-DRBLI4",
    "HmIPW-DRBL4",
    "HmIP-FBL",
)

_LIGHT_DEVICES: tuple[str, ...] = (
    "HmIP-BSL",
    "HmIP-BDT",
    "HmIP-DRDI3",
    "HmIP-FDT",
    "HmIPW-PDT",
    "HmIP-RGBW",
    "HmIP-SCTH230",
    "HmIPW-DRD3",
    "HmIPW-WRC6",
)

_BLIND_DEVICES: tuple[str, ...] = (
    "HmIP-BBL",
    "HmIP-DRBLI4",
    "HmIPW-DRBL4",
    "HmIP-FBL",
)


LEVEL_SENSOR_RULES: list[EntityDescriptionRule] = [
    # Thermostat valve level (pipe level)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("LEVEL",),
        devices=_THERMOSTAT_DEVICES,
        priority=10,
        description=HmSensorEntityDescription(
            key="LEVEL",
            entity_registry_enabled_default=False,
            multiplier=100,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="pipe_level",
        ),
    ),
    # Cover level
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("LEVEL",),
        devices=_COVER_DEVICES,
        priority=10,
        description=HmSensorEntityDescription(
            key="LEVEL",
            entity_registry_enabled_default=False,
            multiplier=100,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="cover_level",
        ),
    ),
    # Light level
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("LEVEL",),
        devices=_LIGHT_DEVICES,
        priority=10,
        description=HmSensorEntityDescription(
            key="LEVEL",
            entity_registry_enabled_default=False,
            multiplier=100,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="light_level",
        ),
    ),
    # Cover tilt (LEVEL_2 on blind devices)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("LEVEL_2",),
        devices=_BLIND_DEVICES,
        priority=10,
        description=HmSensorEntityDescription(
            key="LEVEL",
            entity_registry_enabled_default=False,
            multiplier=100,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="cover_tilt",
        ),
    ),
    # COLOR on specific devices (no state_class in original)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("COLOR",),
        devices=("HmIP-BSL", "HmIP-RGBW", "HmIPW-WRC6"),
        priority=10,
        description=simple_sensor(
            key="COLOR",
            enabled_default=False,
        ),
    ),
    # Generic level sensor (fallback)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("LEVEL", "LEVEL_2"),
        description=HmSensorEntityDescription(
            key="LEVEL",
            multiplier=100,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    # Filling level
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("FILLING_LEVEL",),
        description=measurement_sensor(
            key="FILLING_LEVEL",
            unit=PERCENTAGE,
        ),
    ),
    # Valve state (HM-CC-RT-DN, HM-CC-VD)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("VALVE_STATE",),
        devices=("HM-CC-RT-DN", "HM-CC-VD"),
        priority=10,
        description=measurement_sensor(
            key="VALVE_STATE",
            unit=PERCENTAGE,
            translation_key="pipe_level",
        ),
    ),
]
