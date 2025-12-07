"""Number entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.factories import number, percentage_number
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.number import NumberDeviceClass
from homeassistant.const import UnitOfFrequency

# Devices where LEVEL should show pipe level translation
_THERMOSTAT_DEVICES: tuple[str, ...] = (
    "HmIP-eTRV",
    "HmIP-HEATING",
)


NUMBER_RULES: list[EntityDescriptionRule] = [
    # Frequency (generic)
    EntityDescriptionRule(
        category=DataPointCategory.NUMBER,
        parameters=("FREQUENCY",),
        description=number(
            key="FREQUENCY",
            device_class=NumberDeviceClass.FREQUENCY,
            unit=UnitOfFrequency.HERTZ,
        ),
    ),
    # Device-specific: HMW-IO-12-Sw14-DR uses mHz
    EntityDescriptionRule(
        category=DataPointCategory.NUMBER,
        parameters=("FREQUENCY",),
        devices=("HMW-IO-12-Sw14-DR",),
        priority=10,
        description=number(
            key="FREQUENCY",
            unit="mHz",
            translation_key="frequency",
        ),
    ),
    # Device-specific: Thermostat level (pipe level)
    EntityDescriptionRule(
        category=DataPointCategory.NUMBER,
        parameters=("LEVEL",),
        devices=_THERMOSTAT_DEVICES,
        priority=10,
        description=percentage_number(
            key="LEVEL",
            enabled_default=False,
            translation_key="pipe_level",
        ),
    ),
    # Generic level (percentage)
    EntityDescriptionRule(
        category=DataPointCategory.NUMBER,
        parameters=("LEVEL", "LEVEL_2"),
        description=percentage_number(
            key="LEVEL",
        ),
    ),
]
