"""Sensor entity description rules for Homematic(IP) Local."""

from __future__ import annotations

from ...registry import EntityDescriptionRule
from .air_quality import AIR_QUALITY_SENSOR_RULES
from .battery import BATTERY_SENSOR_RULES
from .energy import ENERGY_SENSOR_RULES
from .level import LEVEL_SENSOR_RULES
from .misc import MISC_SENSOR_RULES
from .temperature import TEMPERATURE_SENSOR_RULES
from .weather import WEATHER_SENSOR_RULES


def get_all_sensor_rules() -> list[EntityDescriptionRule]:
    """Get all sensor description rules."""
    return [
        *TEMPERATURE_SENSOR_RULES,
        *ENERGY_SENSOR_RULES,
        *AIR_QUALITY_SENSOR_RULES,
        *WEATHER_SENSOR_RULES,
        *BATTERY_SENSOR_RULES,
        *LEVEL_SENSOR_RULES,
        *MISC_SENSOR_RULES,
    ]
