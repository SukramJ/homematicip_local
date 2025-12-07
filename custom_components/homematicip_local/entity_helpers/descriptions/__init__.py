"""Entity description rules for Homematic(IP) Local."""

from __future__ import annotations

from ..registry import EntityDescriptionRule
from .binary_sensors import BINARY_SENSOR_RULES
from .buttons import BUTTON_RULES
from .covers import COVER_RULES
from .hub import HUB_RULES
from .locks import LOCK_RULES
from .numbers import NUMBER_RULES
from .selects import SELECT_RULES
from .sensors import get_all_sensor_rules
from .sirens import SIREN_RULES
from .switches import SWITCH_RULES
from .valves import VALVE_RULES


def get_all_rules() -> list[EntityDescriptionRule]:
    """
    Get all entity description rules.

    Returns a flat list of all rules from all modules.
    Rules are returned in module order; the registry handles
    sorting by priority.
    """
    return [
        # Sensors (grouped by domain)
        *get_all_sensor_rules(),
        # Other platforms
        *BINARY_SENSOR_RULES,
        *BUTTON_RULES,
        *COVER_RULES,
        *SWITCH_RULES,
        *NUMBER_RULES,
        *SELECT_RULES,
        *LOCK_RULES,
        *VALVE_RULES,
        *SIREN_RULES,
        # Hub-specific
        *HUB_RULES,
    ]
