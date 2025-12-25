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
    # Acoustic notification selection (e.g., HmIP-WRCD)
    EntityDescriptionRule(
        category=DataPointCategory.SELECT,
        parameters=("ACOUSTIC_NOTIFICATION_SELECTION",),
        description=HmSelectEntityDescription(
            key="ACOUSTIC_NOTIFICATION_SELECTION",
            translation_key="acoustic_notification_selection",
        ),
    ),
    # Display data icon (e.g., HmIP-WRCD)
    EntityDescriptionRule(
        category=DataPointCategory.SELECT,
        parameters=("DISPLAY_DATA_ICON",),
        description=HmSelectEntityDescription(
            key="DISPLAY_DATA_ICON",
            translation_key="display_data_icon",
        ),
    ),
    # Display data background color (e.g., HmIP-WRCD)
    EntityDescriptionRule(
        category=DataPointCategory.SELECT,
        parameters=("DISPLAY_DATA_BACKGROUND_COLOR",),
        description=HmSelectEntityDescription(
            key="DISPLAY_DATA_BACKGROUND_COLOR",
            translation_key="display_data_background_color",
        ),
    ),
    # Display data alignment (e.g., HmIP-WRCD)
    EntityDescriptionRule(
        category=DataPointCategory.SELECT,
        parameters=("DISPLAY_DATA_ALIGNMENT",),
        description=HmSelectEntityDescription(
            key="DISPLAY_DATA_ALIGNMENT",
            translation_key="display_data_alignment",
        ),
    ),
    # Display data text color (e.g., HmIP-WRCD)
    EntityDescriptionRule(
        category=DataPointCategory.SELECT,
        parameters=("DISPLAY_DATA_TEXT_COLOR",),
        description=HmSelectEntityDescription(
            key="DISPLAY_DATA_TEXT_COLOR",
            translation_key="display_data_text_color",
        ),
    ),
]
