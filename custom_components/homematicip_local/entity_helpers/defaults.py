"""Default entity descriptions for Homematic(IP) Local."""

from __future__ import annotations

from typing import Final

from aiohomematic.const import DataPointCategory
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.helpers.entity import EntityDescription

from .base import HmButtonEntityDescription

# Default descriptions used when no specific rule matches
DEFAULT_DESCRIPTIONS: Final[dict[DataPointCategory, EntityDescription]] = {
    DataPointCategory.BUTTON: HmButtonEntityDescription(
        key="button_default",
        entity_registry_enabled_default=False,
        translation_key="button_press",
    ),
    DataPointCategory.SWITCH: SwitchEntityDescription(
        key="switch_default",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    DataPointCategory.SELECT: SelectEntityDescription(
        key="select_default",
        entity_category=EntityCategory.CONFIG,
    ),
    DataPointCategory.HUB_BUTTON: HmButtonEntityDescription(
        key="hub_button_default",
        translation_key="button_press",
    ),
    DataPointCategory.HUB_SWITCH: SwitchEntityDescription(
        key="hub_switch_default",
        device_class=SwitchDeviceClass.SWITCH,
    ),
}
