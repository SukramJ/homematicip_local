"""Select entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.base import HmSelectEntityDescription
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.const import EntityCategory

SELECT_RULES: list[EntityDescriptionRule] = [
    # Heating/Cooling mode
    EntityDescriptionRule(
        category=DataPointCategory.SELECT,
        parameters=("HEATING_COOLING",),
        description=HmSelectEntityDescription(
            key="HEATING_COOLING",
            entity_category=EntityCategory.CONFIG,
            entity_registry_enabled_default=False,
            translation_key="heating_cooling",
        ),
    ),
]
