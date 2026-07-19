"""Event entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from aiohomematic.device_semantics import DOORBELL_MODELS
from custom_components.homematicip_local.entity_helpers.factories import event
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.event import EventDeviceClass

EVENT_RULES: list[EntityDescriptionRule] = [
    EntityDescriptionRule(
        category=DataPointCategory.EVENT_GROUP,
        # Devices whose press/ring channel is a doorbell rather than a generic
        # button — sourced from openccu-data's curated device_semantics extract
        # (the same list openccu-loom's MQTT discovery embeds): HM-Sen-DB-PCB,
        # HmIP-DBB, HmIP-DSD-PCB.
        devices=tuple(sorted(DOORBELL_MODELS)),
        description=event(
            key="event_doorbell",
            device_class=EventDeviceClass.DOORBELL,
        ),
    ),
]
