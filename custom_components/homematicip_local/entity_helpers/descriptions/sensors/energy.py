"""Energy and power sensor entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.factories import (
    measurement_sensor,
    simple_sensor,
    total_increasing_sensor,
    total_sensor,
)
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)

ENERGY_SENSOR_RULES: list[EntityDescriptionRule] = [
    # Power (Watt)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("POWER",),
        description=measurement_sensor(
            key="POWER",
            device_class=SensorDeviceClass.POWER,
            unit=UnitOfPower.WATT,
        ),
    ),
    # IEC Power (Watt)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("IEC_POWER",),
        description=measurement_sensor(
            key="IEC_POWER",
            device_class=SensorDeviceClass.POWER,
            unit=UnitOfPower.WATT,
        ),
    ),
    # Energy counter (Wh)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("ENERGY_COUNTER", "ENERGY_COUNTER_FEED_IN"),
        description=total_increasing_sensor(
            key="ENERGY_COUNTER",
            device_class=SensorDeviceClass.ENERGY,
            unit=UnitOfEnergy.WATT_HOUR,
        ),
    ),
    # IEC Energy counter (kWh)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("IEC_ENERGY_COUNTER",),
        description=total_increasing_sensor(
            key="IEC_ENERGY_COUNTER",
            device_class=SensorDeviceClass.ENERGY,
            unit=UnitOfEnergy.KILO_WATT_HOUR,
        ),
    ),
    # Voltage
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("VOLTAGE",),
        description=measurement_sensor(
            key="VOLTAGE",
            device_class=SensorDeviceClass.VOLTAGE,
            unit=UnitOfElectricPotential.VOLT,
        ),
    ),
    # Current
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("CURRENT",),
        description=measurement_sensor(
            key="CURRENT",
            device_class=SensorDeviceClass.CURRENT,
            unit=UnitOfElectricCurrent.MILLIAMPERE,
        ),
    ),
    # Frequency (generic)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("FREQUENCY",),
        description=measurement_sensor(
            key="FREQUENCY",
            device_class=SensorDeviceClass.FREQUENCY,
            unit=UnitOfFrequency.HERTZ,
        ),
    ),
    # Device-specific: HMW-IO-12-Sw14-DR uses mHz for frequency (no state_class)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("FREQUENCY",),
        devices=("HMW-IO-12-Sw14-DR",),
        priority=10,
        description=simple_sensor(
            key="FREQUENCY",
            native_unit_of_measurement="mHz",
            translation_key="frequency",
        ),
    ),
    # Gas sensors
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("GAS_ENERGY_COUNTER",),
        description=total_increasing_sensor(
            key="GAS_ENERGY_COUNTER",
            device_class=SensorDeviceClass.GAS,
            unit=UnitOfVolume.CUBIC_METERS,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("GAS_FLOW",),
        description=measurement_sensor(
            key="GAS_FLOW",
            device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
            unit=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("GAS_POWER",),
        description=simple_sensor(
            key="GAS_POWER",
            native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("GAS_VOLUME",),
        description=total_increasing_sensor(
            key="GAS_VOLUME",
            device_class=SensorDeviceClass.GAS,
            unit=UnitOfVolume.CUBIC_METERS,
        ),
    ),
    # Water sensors
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("WATER_FLOW",),
        description=measurement_sensor(
            key="WATER_FLOW",
            device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
            unit=UnitOfVolumeFlowRate.LITERS_PER_MINUTE,
            suggested_display_precision=1,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("WATER_VOLUME",),
        description=total_increasing_sensor(
            key="WATER_VOLUME",
            device_class=SensorDeviceClass.WATER,
            unit=UnitOfVolume.LITERS,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("WATER_VOLUME_SINCE_OPEN",),
        description=total_sensor(
            key="WATER_VOLUME_SINCE_OPEN",
            device_class=SensorDeviceClass.WATER,
            unit=UnitOfVolume.LITERS,
        ),
    ),
]
