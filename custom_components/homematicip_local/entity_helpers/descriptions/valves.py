"""Valve entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.valve import ValveDeviceClass, ValveEntityDescription

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
