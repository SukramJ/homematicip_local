"""Valve entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from homeassistant.components.valve import ValveDeviceClass, ValveEntityDescription

from ..registry import EntityDescriptionRule

VALVE_RULES: list[EntityDescriptionRule] = [
    # Water valve (irrigation)
    EntityDescriptionRule(
        category=DataPointCategory.VALVE,
        devices=("ELV-SH-WSM ", "HmIP-WSM"),
        description=ValveEntityDescription(
            key="WSM",
            device_class=ValveDeviceClass.WATER,
            translation_key="irrigation_valve",
        ),
    ),
]
