"""Cover entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.cover import CoverDeviceClass, CoverEntityDescription

COVER_RULES: list[EntityDescriptionRule] = [
    # Blinds (with tilt)
    EntityDescriptionRule(
        category=DataPointCategory.COVER,
        devices=("HmIP-BBL", "HmIP-FBL", "HmIP-DRBLI4", "HmIPW-DRBL4"),
        description=CoverEntityDescription(
            key="BLIND",
            device_class=CoverDeviceClass.BLIND,
        ),
    ),
    # Shutters (no tilt)
    EntityDescriptionRule(
        category=DataPointCategory.COVER,
        devices=("HmIP-BROLL", "HmIP-FROLL", "HM-LC-Bl1PBU-FM"),
        description=CoverEntityDescription(
            key="SHUTTER",
            device_class=CoverDeviceClass.SHUTTER,
        ),
    ),
    # Shade (HmIP-HDM1)
    EntityDescriptionRule(
        category=DataPointCategory.COVER,
        devices=("HmIP-HDM1",),
        description=CoverEntityDescription(
            key="HmIP-HDM1",
            device_class=CoverDeviceClass.SHADE,
        ),
    ),
    # Garage door
    EntityDescriptionRule(
        category=DataPointCategory.COVER,
        devices=("HmIP-MOD-HO", "HmIP-MOD-TM"),
        description=CoverEntityDescription(
            key="GARAGE-HO",
            device_class=CoverDeviceClass.GARAGE,
        ),
    ),
    # Window actuator
    EntityDescriptionRule(
        category=DataPointCategory.COVER,
        devices=("HM-Sec-Win",),
        description=CoverEntityDescription(
            key="HM-Sec-Win",
            device_class=CoverDeviceClass.WINDOW,
        ),
    ),
]
