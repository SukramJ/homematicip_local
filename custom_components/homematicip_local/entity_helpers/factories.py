"""Factory functions for creating entity descriptions."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, EntityCategory

from .base import (
    HmBinarySensorEntityDescription,
    HmButtonEntityDescription,
    HmNameSource,
    HmNumberEntityDescription,
    HmSensorEntityDescription,
)

# =============================================================================
# Sensor Factories
# =============================================================================


def measurement_sensor(
    key: str,
    *,
    device_class: SensorDeviceClass | None = None,
    unit: str | None = None,
    translation_key: str | None = None,
    suggested_display_precision: int | None = None,
    multiplier: float | None = None,
    icon: str | None = None,
    name_source: HmNameSource = HmNameSource.PARAMETER,
    **kwargs: Any,
) -> HmSensorEntityDescription:
    """
    Create a standard measurement sensor description.

    Automatically sets:
    - state_class = MEASUREMENT

    Example:
        measurement_sensor(
            "TEMPERATURE",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit=UnitOfTemperature.CELSIUS,
        )

    """
    return HmSensorEntityDescription(
        key=key,
        device_class=device_class,
        native_unit_of_measurement=unit,
        state_class=SensorStateClass.MEASUREMENT,
        translation_key=translation_key,
        suggested_display_precision=suggested_display_precision,
        multiplier=multiplier,
        icon=icon,
        name_source=name_source,
        **kwargs,
    )


def total_increasing_sensor(
    key: str,
    *,
    device_class: SensorDeviceClass | None = None,
    unit: str | None = None,
    translation_key: str | None = None,
    icon: str | None = None,
    **kwargs: Any,
) -> HmSensorEntityDescription:
    """
    Create a total increasing sensor description (e.g., energy counters).

    Automatically sets:
    - state_class = TOTAL_INCREASING

    Example:
        total_increasing_sensor(
            "ENERGY_COUNTER",
            device_class=SensorDeviceClass.ENERGY,
            unit=UnitOfEnergy.WATT_HOUR,
        )

    """
    return HmSensorEntityDescription(
        key=key,
        device_class=device_class,
        native_unit_of_measurement=unit,
        state_class=SensorStateClass.TOTAL_INCREASING,
        translation_key=translation_key,
        icon=icon,
        **kwargs,
    )


def total_sensor(
    key: str,
    *,
    device_class: SensorDeviceClass | None = None,
    unit: str | None = None,
    translation_key: str | None = None,
    **kwargs: Any,
) -> HmSensorEntityDescription:
    """
    Create a total sensor description.

    Automatically sets:
    - state_class = TOTAL

    Example:
        total_sensor(
            "WATER_VOLUME_SINCE_OPEN",
            device_class=SensorDeviceClass.WATER,
            unit=UnitOfVolume.LITERS,
        )

    """
    return HmSensorEntityDescription(
        key=key,
        device_class=device_class,
        native_unit_of_measurement=unit,
        state_class=SensorStateClass.TOTAL,
        translation_key=translation_key,
        **kwargs,
    )


def diagnostic_sensor(
    key: str,
    *,
    device_class: SensorDeviceClass | None = None,
    unit: str | None = None,
    translation_key: str | None = None,
    icon: str | None = None,
    enabled_default: bool = False,
    suggested_display_precision: int | None = None,
    **kwargs: Any,
) -> HmSensorEntityDescription:
    """
    Create a diagnostic sensor description.

    Automatically sets:
    - entity_category = DIAGNOSTIC
    - entity_registry_enabled_default = False (unless overridden)
    - state_class = MEASUREMENT

    Example:
        diagnostic_sensor(
            "RSSI",
            device_class=SensorDeviceClass.SIGNAL_STRENGTH,
            unit=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        )

    """
    return HmSensorEntityDescription(
        key=key,
        device_class=device_class,
        native_unit_of_measurement=unit,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=enabled_default,
        translation_key=translation_key,
        icon=icon,
        suggested_display_precision=suggested_display_precision,
        **kwargs,
    )


def enum_sensor(
    key: str,
    *,
    translation_key: str,
    enabled_default: bool = True,
    entity_category: EntityCategory | None = None,
    **kwargs: Any,
) -> HmSensorEntityDescription:
    """
    Create an enum sensor description.

    Automatically sets:
    - device_class = ENUM

    Example:
        enum_sensor("DOOR_STATE", translation_key="door_state")

    """
    return HmSensorEntityDescription(
        key=key,
        device_class=SensorDeviceClass.ENUM,
        translation_key=translation_key,
        entity_registry_enabled_default=enabled_default,
        entity_category=entity_category,
        **kwargs,
    )


def simple_sensor(
    key: str,
    *,
    translation_key: str | None = None,
    enabled_default: bool = True,
    **kwargs: Any,
) -> HmSensorEntityDescription:
    """
    Create a simple sensor description without state class.

    Use for sensors that don't fit measurement/total patterns.
    """
    return HmSensorEntityDescription(
        key=key,
        translation_key=translation_key,
        entity_registry_enabled_default=enabled_default,
        **kwargs,
    )


# =============================================================================
# Binary Sensor Factories
# =============================================================================


def binary_sensor(
    key: str,
    *,
    device_class: BinarySensorDeviceClass,
    enabled_default: bool = True,
    entity_category: EntityCategory | None = None,
    icon: str | None = None,
    **kwargs: Any,
) -> HmBinarySensorEntityDescription:
    """
    Create a binary sensor description.

    Example:
        binary_sensor("MOTION", device_class=BinarySensorDeviceClass.MOTION)

    """
    return HmBinarySensorEntityDescription(
        key=key,
        device_class=device_class,
        entity_registry_enabled_default=enabled_default,
        entity_category=entity_category,
        icon=icon,
        **kwargs,
    )


def diagnostic_binary_sensor(
    key: str,
    *,
    device_class: BinarySensorDeviceClass,
    enabled_default: bool = False,
    icon: str | None = None,
    **kwargs: Any,
) -> HmBinarySensorEntityDescription:
    """
    Create a diagnostic binary sensor description.

    Automatically sets:
    - entity_category = DIAGNOSTIC
    - entity_registry_enabled_default = False (unless overridden)

    Example:
        diagnostic_binary_sensor("LOW_BAT", device_class=BinarySensorDeviceClass.BATTERY)

    """
    return HmBinarySensorEntityDescription(
        key=key,
        device_class=device_class,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=enabled_default,
        icon=icon,
        **kwargs,
    )


# =============================================================================
# Button Factories
# =============================================================================


def button(
    key: str,
    *,
    translation_key: str | None = None,
    enabled_default: bool = False,
    entity_category: EntityCategory | None = None,
    **kwargs: Any,
) -> HmButtonEntityDescription:
    """
    Create a button description.

    Example:
        button("PRESS_SHORT")

    """
    return HmButtonEntityDescription(
        key=key,
        entity_registry_enabled_default=enabled_default,
        entity_category=entity_category,
        translation_key=translation_key,
        **kwargs,
    )


def config_button(
    key: str,
    *,
    translation_key: str | None = None,
    enabled_default: bool = False,
    **kwargs: Any,
) -> HmButtonEntityDescription:
    """
    Create a configuration button description.

    Automatically sets:
    - entity_category = CONFIG
    - entity_registry_enabled_default = False (unless overridden)

    Example:
        config_button("RESET_MOTION")

    """
    return HmButtonEntityDescription(
        key=key,
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=enabled_default,
        translation_key=translation_key,
        **kwargs,
    )


# =============================================================================
# Number Factories
# =============================================================================


def number(
    key: str,
    *,
    device_class: NumberDeviceClass | None = None,
    unit: str | None = None,
    translation_key: str | None = None,
    multiplier: float | None = None,
    enabled_default: bool = True,
    **kwargs: Any,
) -> HmNumberEntityDescription:
    """
    Create a number description.

    Example:
        number("FREQUENCY", device_class=NumberDeviceClass.FREQUENCY, unit="Hz")

    """
    return HmNumberEntityDescription(
        key=key,
        device_class=device_class,
        native_unit_of_measurement=unit,
        multiplier=multiplier,
        entity_registry_enabled_default=enabled_default,
        translation_key=translation_key,
        **kwargs,
    )


def percentage_number(
    key: str,
    *,
    translation_key: str | None = None,
    enabled_default: bool = True,
    **kwargs: Any,
) -> HmNumberEntityDescription:
    """
    Create a percentage number description with multiplier.

    Automatically sets:
    - multiplier = 100
    - native_unit_of_measurement = PERCENTAGE

    Example:
        percentage_number("LEVEL", translation_key="brightness_level")

    """
    return HmNumberEntityDescription(
        key=key,
        multiplier=100,
        native_unit_of_measurement=PERCENTAGE,
        entity_registry_enabled_default=enabled_default,
        translation_key=translation_key,
        **kwargs,
    )
