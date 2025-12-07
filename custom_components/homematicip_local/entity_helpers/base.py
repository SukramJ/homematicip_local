"""Base classes for Homematic(IP) Local entity descriptions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.button import ButtonEntityDescription
from homeassistant.components.number import NumberEntityDescription
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.helpers.entity import EntityDescription


class HmNameSource(StrEnum):
    """Enum to define the source of a translation."""

    DEVICE_CLASS = "device_class"
    ENTITY_NAME = "entity_name"
    PARAMETER = "parameter"


class HmEntityDescription(EntityDescription, frozen_or_thawed=True):
    """Base class describing Homematic(IP) Local entities."""

    name_source: HmNameSource = HmNameSource.PARAMETER


@dataclass(frozen=True, kw_only=True)
class HmNumberEntityDescription(HmEntityDescription, NumberEntityDescription):
    """Class describing Homematic(IP) Local number entities."""

    multiplier: float | None = None


@dataclass(frozen=True, kw_only=True)
class HmSelectEntityDescription(HmEntityDescription, SelectEntityDescription):
    """Class describing Homematic(IP) Local select entities."""


@dataclass(frozen=True, kw_only=True)
class HmSensorEntityDescription(HmEntityDescription, SensorEntityDescription):
    """Class describing Homematic(IP) Local sensor entities."""

    multiplier: float | None = None


@dataclass(frozen=True, kw_only=True)
class HmBinarySensorEntityDescription(HmEntityDescription, BinarySensorEntityDescription):
    """Class describing Homematic(IP) Local binary sensor entities."""


@dataclass(frozen=True, kw_only=True)
class HmButtonEntityDescription(HmEntityDescription, ButtonEntityDescription):
    """Class describing Homematic(IP) Local button entities."""
