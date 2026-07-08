"""Event entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.factories import event
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.event import EventDeviceClass

EVENT_RULES: list[EntityDescriptionRule] = [
    EntityDescriptionRule(
        category=DataPointCategory.EVENT_GROUP,
        # HmIP-DBB: wireless doorbell button. HmIP-DSD-PCB: doorbell sensor PCB whose
        # input channel signals a ring — both are doorbells, not generic buttons.
        devices=("HmIP-DBB", "HmIP-DSD-PCB"),
        description=event(
            key="event_doorbell",
            device_class=EventDeviceClass.DOORBELL,
        ),
    ),
]
