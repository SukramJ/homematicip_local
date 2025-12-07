"""Entity helpers for Homematic(IP) Local."""

from __future__ import annotations

import dataclasses
import logging
from typing import TYPE_CHECKING

from aiohomematic.interfaces.model import (
    CalculatedDataPointProtocol,
    CustomDataPointProtocol,
    GenericDataPointProtocol,
    GenericHubDataPointProtocol,
)
from homeassistant.helpers.typing import UNDEFINED, UndefinedType

from .base import (
    HmBinarySensorEntityDescription,
    HmButtonEntityDescription,
    HmEntityDescription,
    HmNameSource,
    HmNumberEntityDescription,
    HmSelectEntityDescription,
    HmSensorEntityDescription,
)
from .defaults import DEFAULT_DESCRIPTIONS
from .descriptions import get_all_rules
from .descriptions.sensors.air_quality import KILOJOULS_PERKILOGRAM, LENGTH_MICROMETER, NUMBER_CONCENTRATION_CM3
from .registry import REGISTRY, EntityDescriptionRule

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription

    from ..support import HmGenericDataPointProtocol

_LOGGER = logging.getLogger(__name__)

# Re-export for backwards compatibility
__all__ = [
    # Public API
    "get_entity_description",
    # Registry
    "EntityDescriptionRule",
    "REGISTRY",
    # Base classes
    "HmEntityDescription",
    "HmNameSource",
    "HmBinarySensorEntityDescription",
    "HmButtonEntityDescription",
    "HmNumberEntityDescription",
    "HmSelectEntityDescription",
    "HmSensorEntityDescription",
    # Constants (for backwards compatibility)
    "NUMBER_CONCENTRATION_CM3",
    "LENGTH_MICROMETER",
    "KILOJOULS_PERKILOGRAM",
]

# Mutable container to track initialization state (avoids global statement)
_init_state: dict[str, bool] = {"initialized": False}


def _initialize_registry() -> None:
    """Initialize the registry with all rules and defaults."""
    if _init_state["initialized"]:
        return

    # Register all rules
    REGISTRY.register_all(get_all_rules())

    # Set defaults
    for category, description in DEFAULT_DESCRIPTIONS.items():
        REGISTRY.set_default(category, description)

    # Validate in debug mode
    if _LOGGER.isEnabledFor(logging.DEBUG):
        warnings = REGISTRY.validate()
        for warning in warnings:
            _LOGGER.warning("Entity description validation: %s", warning)

    _init_state["initialized"] = True


# Initialize on module load
_initialize_registry()


def get_entity_description(
    *,
    data_point: HmGenericDataPointProtocol | CustomDataPointProtocol | GenericHubDataPointProtocol,
) -> EntityDescription | None:
    """
    Get the entity description for a data point.

    This is the main public API for entity description lookup.

    Args:
        data_point: The data point to get a description for

    Returns:
        An EntityDescription configured for the data point, or None

    """
    # Extract lookup parameters from data point
    category = data_point.category

    # Build lookup kwargs based on data point type
    parameter: str | None = None
    device_model: str | None = None
    unit: str | None = None
    postfix: str | None = None
    var_name: str | None = None

    if isinstance(data_point, (CalculatedDataPointProtocol, GenericDataPointProtocol)):
        parameter = data_point.parameter
        device_model = data_point.device.model
        if hasattr(data_point, "unit") and data_point.unit:
            unit = data_point.unit

    if isinstance(data_point, CustomDataPointProtocol):
        device_model = data_point.device.model
        postfix = data_point.data_point_name_postfix

    if isinstance(data_point, GenericHubDataPointProtocol):
        var_name = data_point.name

    # Find matching description
    entity_desc = REGISTRY.find(
        category=category,
        parameter=parameter,
        device_model=device_model,
        unit=unit,
        postfix=postfix,
        var_name=var_name,
    )

    if entity_desc is None:
        return None

    # Apply data point-specific modifications
    name, translation_key = _get_name_and_translation_key(
        data_point=data_point,
        entity_desc=entity_desc,
    )

    enabled_default = entity_desc.entity_registry_enabled_default if data_point.enabled_default else False

    return dataclasses.replace(
        entity_desc,
        name=name,
        translation_key=translation_key,
        has_entity_name=True,
        entity_registry_enabled_default=enabled_default,
    )


def _get_name_and_translation_key(
    *,
    data_point: HmGenericDataPointProtocol | CustomDataPointProtocol | GenericHubDataPointProtocol,
    entity_desc: EntityDescription,
) -> tuple[str | UndefinedType | None, str | None]:
    """Get the name and translation_key for an entity."""
    name = data_point.name

    if entity_desc.translation_key:
        return name, entity_desc.translation_key

    if isinstance(data_point, (CalculatedDataPointProtocol, GenericDataPointProtocol)):
        if isinstance(entity_desc, HmEntityDescription):
            if entity_desc.name_source == HmNameSource.ENTITY_NAME:
                return name, name.lower()
            if entity_desc.name_source == HmNameSource.DEVICE_CLASS:
                return UNDEFINED, None

        return name, data_point.parameter.lower()

    return name, name.lower()
