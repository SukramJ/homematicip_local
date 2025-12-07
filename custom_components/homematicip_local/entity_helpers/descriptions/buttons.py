"""Button entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory

from ..factories import button, config_button
from ..registry import EntityDescriptionRule

BUTTON_RULES: list[EntityDescriptionRule] = [
    # Reset motion
    EntityDescriptionRule(
        category=DataPointCategory.BUTTON,
        parameters=("RESET_MOTION",),
        description=config_button(
            key="RESET_MOTION",
        ),
    ),
    # Reset presence
    EntityDescriptionRule(
        category=DataPointCategory.BUTTON,
        parameters=("RESET_PRESENCE",),
        description=config_button(
            key="RESET_PRESENCE",
        ),
    ),
    # Press long
    EntityDescriptionRule(
        category=DataPointCategory.BUTTON,
        parameters=("PRESS_LONG",),
        description=button(
            key="PRESS_LONG",
        ),
    ),
    # Press short
    EntityDescriptionRule(
        category=DataPointCategory.BUTTON,
        parameters=("PRESS_SHORT",),
        description=button(
            key="PRESS_SHORT",
        ),
    ),
]
