"""Siren entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.siren import SirenEntityDescription

SIREN_RULES: list[EntityDescriptionRule] = [
    # Smoke detector siren (SWSD)
    EntityDescriptionRule(
        category=DataPointCategory.SIREN,
        devices=("HmIP-SWSD",),
        description=SirenEntityDescription(
            key="SWSD",
            entity_registry_enabled_default=False,
        ),
    ),
]
