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

    # Command throttle statistics per interface
    diag["command_throttle"] = {
        client.interface_id: {
            "interval": client.command_throttle.interval,
            "is_enabled": client.command_throttle.is_enabled,
            "queue_size": client.command_throttle.queue_size,
            "throttled_count": client.command_throttle.throttled_count,
            "critical_count": client.command_throttle.critical_count,
            "burst_count": client.command_throttle.burst_count,
            "burst_threshold": client.command_throttle.burst_threshold,
            "burst_window": client.command_throttle.burst_window,
        }
        for client in central.client_coordinator.clients
    }

    return diag
