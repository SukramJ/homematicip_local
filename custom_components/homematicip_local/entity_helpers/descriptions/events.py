"""Event entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.factories import event
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.event import EventDeviceClass

EVENT_RULES: list[EntityDescriptionRule] = [
    EntityDescriptionRule(
        category=DataPointCategory.EVENT_GROUP,
        devices=("HmIP-DBB",),
        description=event(
            key="event_doorbell",
            device_class=EventDeviceClass.DOORBELL,
        ),
    ),
]
