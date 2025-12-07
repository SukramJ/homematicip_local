"""Switch entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntityDescription
from homeassistant.const import EntityCategory

from ..registry import EntityDescriptionRule

SWITCH_RULES: list[EntityDescriptionRule] = [
    # Outlet (HmIP-PS)
    EntityDescriptionRule(
        category=DataPointCategory.SWITCH,
        devices=("HmIP-PS",),
        description=SwitchEntityDescription(
            key="OUTLET",
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
    # Inhibit
    EntityDescriptionRule(
        category=DataPointCategory.SWITCH,
        parameters=("INHIBIT",),
        description=SwitchEntityDescription(
            key="INHIBIT",
            device_class=SwitchDeviceClass.SWITCH,
            entity_registry_enabled_default=False,
        ),
    ),
    # Motion/Presence detection active
    EntityDescriptionRule(
        category=DataPointCategory.SWITCH,
        parameters=("MOTION_DETECTION_ACTIVE", "PRESENCE_DETECTION_ACTIVE"),
        description=SwitchEntityDescription(
            key="MOTION_DETECTION_ACTIVE",
            device_class=SwitchDeviceClass.SWITCH,
            entity_category=EntityCategory.CONFIG,
            entity_registry_enabled_default=False,
        ),
    ),
]
