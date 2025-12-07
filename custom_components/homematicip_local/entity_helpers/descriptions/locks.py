"""Lock entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from homeassistant.components.lock import LockEntityDescription
from homeassistant.const import EntityCategory

from ..registry import EntityDescriptionRule

LOCK_RULES: list[EntityDescriptionRule] = [
    # Button lock
    EntityDescriptionRule(
        category=DataPointCategory.LOCK,
        postfix="BUTTON_LOCK",
        description=LockEntityDescription(
            key="BUTTON_LOCK",
            entity_category=EntityCategory.CONFIG,
            entity_registry_enabled_default=False,
            translation_key="button_lock",
        ),
    ),
]
