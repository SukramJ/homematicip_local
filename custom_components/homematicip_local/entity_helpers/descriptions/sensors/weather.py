"""Weather sensor entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import DEGREE, LIGHT_LUX, UnitOfLength, UnitOfSpeed, UnitOfTime

from ...factories import measurement_sensor, total_increasing_sensor
from ...registry import EntityDescriptionRule

WEATHER_SENSOR_RULES: list[EntityDescriptionRule] = [
    # Brightness (no device class, custom translation)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("BRIGHTNESS",),
        description=measurement_sensor(
            key="BRIGHTNESS",
            translation_key="brightness",
        ),
    ),
    # Illumination (lux)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=(
            "ILLUMINATION",
            "AVERAGE_ILLUMINATION",
            "CURRENT_ILLUMINATION",
            "HIGHEST_ILLUMINATION",
            "LOWEST_ILLUMINATION",
            "LUX",
        ),
        description=measurement_sensor(
            key="ILLUMINATION",
            device_class=SensorDeviceClass.ILLUMINANCE,
            unit=LIGHT_LUX,
        ),
    ),
    # Wind direction
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=(
            "WIND_DIR",
            "WIND_DIR_RANGE",
            "WIND_DIRECTION",
            "WIND_DIRECTION_RANGE",
        ),
        description=measurement_sensor(
            key="WIND_DIR",
            unit=DEGREE,
            translation_key="wind_dir",
        ),
    ),
    # Wind speed
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("WIND_SPEED",),
        description=measurement_sensor(
            key="WIND_SPEED",
            device_class=SensorDeviceClass.WIND_SPEED,
            unit=UnitOfSpeed.KILOMETERS_PER_HOUR,
            translation_key="wind_speed",
        ),
    ),
    # Rain counter
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("RAIN_COUNTER",),
        description=total_increasing_sensor(
            key="RAIN_COUNTER",
            unit=UnitOfLength.MILLIMETERS,
            translation_key="rain_counter_total",
        ),
    ),
    # Sunshine duration
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("SUNSHINEDURATION",),
        description=total_increasing_sensor(
            key="SUNSHINEDURATION",
            unit=UnitOfTime.MINUTES,
            translation_key="sunshine_duration",
        ),
    ),
]
