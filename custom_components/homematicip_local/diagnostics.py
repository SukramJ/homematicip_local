"""Diagnostics support for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from dataclasses import asdict
import re
from typing import Any

from aiohomematic.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import HomematicConfigEntry
from .control_unit import ControlUnit

REDACT_CONFIG = {CONF_USERNAME, CONF_PASSWORD}

# Same shape the routing-key scoping in `__init__.py` recognises: ``CUX`` plus a
# two-digit device type plus a five-digit running number, so ``CUX2801001``.
# Matched against the device address here rather than a unique_id, so it is
# anchored and not surrounded by key separators.
_CUXD_ADDRESS = re.compile(r"^CUX\d{7}", re.IGNORECASE)


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: HomematicConfigEntry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    control_unit: ControlUnit = entry.runtime_data
    central = control_unit.central
    diag: dict[str, Any] = {"config": async_redact_data(entry.as_dict(), REDACT_CONFIG)}

    # The openccu-loom compat adapter exposes neither a device registry nor an
    # in-process metrics aggregator (metrics live in the daemon), so both are
    # optional here: models fall back to the device-derived set, metrics are
    # omitted.
    if (device_registry := getattr(central, "device_registry", None)) is not None:
        diag["models"] = device_registry.models
    else:
        diag["models"] = tuple(sorted({device.model for device in central.device_coordinator.devices}))
    diag["system_information"] = async_redact_data(asdict(central.system_information), "serial")
    diag["system_health"] = central.health.to_dict()
    if (metrics_aggregator := getattr(central, "metrics_aggregator", None)) is not None:
        diag["metrics"] = metrics_aggregator.snapshot().to_dict()
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

    # Two questions an architecture review could not answer from any repository:
    # does anyone run a daemon fronting several CCUs, and do CUxD devices occur
    # in production. Each decides whether a known divergence is a correctness
    # problem or a footnote, and neither is measurable without telemetry — which
    # this integration does not have and should not grow. A diagnostics dump
    # answers both without reporting anything: the numbers reach a maintainer
    # only when a user chooses to attach their own dump to a bug report.
    #
    # `daemon_central_count` exists on the openccu-loom adapter only, and only
    # from the release that publishes it, so it is read defensively and omitted
    # rather than guessed — the same treatment as `device_registry` above.
    deployment: dict[str, Any] = {
        "backend": control_unit.config.backend,
        "cuxd_devices": sum(1 for device in central.device_coordinator.devices if _CUXD_ADDRESS.match(device.address)),
    }
    if (central_count := getattr(central, "daemon_central_count", None)) is not None:
        deployment["daemon_centrals"] = central_count
    diag["deployment"] = deployment

    return diag
