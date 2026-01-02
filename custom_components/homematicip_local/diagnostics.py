"""Diagnostics support for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from aiohomematic.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import HomematicConfigEntry
from .control_unit import ControlUnit

REDACT_CONFIG = {CONF_USERNAME, CONF_PASSWORD}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: HomematicConfigEntry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    control_unit: ControlUnit = entry.runtime_data
    central = control_unit.central
    metrics = central.metrics_aggregator.snapshot()
    diag: dict[str, Any] = {"config": async_redact_data(entry.as_dict(), REDACT_CONFIG)}

    diag["models"] = central.device_registry.models
    diag["system_information"] = async_redact_data(asdict(central.system_information), "serial")
    diag["system_health"] = central.health.to_dict()
    diag["metrics"] = metrics.to_dict()
    diag["incident_store"] = await central.cache_coordinator.incident_store.get_diagnostics()

    return diag
