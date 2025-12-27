"""Diagnostics support for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict
from typing import Any

from aiohomematic.central import CentralUnit
from aiohomematic.central.metrics import MetricsSnapshot
from aiohomematic.const import CONF_PASSWORD, CONF_USERNAME, DataPointCategory
from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import HomematicConfigEntry
from .control_unit import ControlUnit

REDACT_CONFIG = {CONF_USERNAME, CONF_PASSWORD}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: HomematicConfigEntry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    control_unit: ControlUnit = entry.runtime_data
    diag: dict[str, Any] = {"config": async_redact_data(entry.as_dict(), REDACT_CONFIG)}

    diag["platform_stats"] = get_data_points_by_platform_stats(central=control_unit.central, registered=True)
    diag["devices"] = get_devices_per_type_stats(central=control_unit.central)
    diag["system_information"] = async_redact_data(asdict(control_unit.central.system_information), "serial")
    diag["system_health"] = get_system_health(central=control_unit.central)
    diag["metrics"] = get_metrics(central=control_unit.central)

    return diag


def get_devices_per_type_stats(*, central: CentralUnit) -> tuple[str, ...]:
    """Return the central statistics for devices by type."""
    return tuple(sorted({d.model for d in central.devices}))


def get_data_points_by_platform_stats(
    *, central: CentralUnit, registered: bool | None = None
) -> Mapping[DataPointCategory, int]:
    """Return the central statistics for data points by platform."""
    _data_points_by_platform: dict[DataPointCategory, int] = {}
    for dp in (
        central.get_data_points(registered=registered)
        + central.hub_coordinator.program_data_points
        + central.hub_coordinator.sysvar_data_points
    ):
        if (platform := dp.category) not in _data_points_by_platform:
            _data_points_by_platform[platform] = 0
        _data_points_by_platform[platform] += 1
    return dict(sorted(_data_points_by_platform.items()))


def get_system_health(*, central: CentralUnit) -> dict[str, Any]:
    """Return the system health information."""
    return {
        "overall": {
            "overall_score": central.health.overall_health_score,
            "all_healthy": central.health.all_clients_healthy,
            "failed_clients": central.health.failed_clients,
        },
        "clients": {
            health.interface_id: {
                "available": health.is_available,
                "health_score": health.health_score,
                "consecutive_failures": health.consecutive_failures,
                "last_event": health.last_event_received.isoformat() if health.last_event_received else None,
            }
            for health in central.health.client_health.values()
        },
    }


def get_metrics(*, central: CentralUnit) -> dict[str, Any]:
    """Return metrics snapshot as dictionary."""
    snapshot: MetricsSnapshot = central.metrics.snapshot()
    return _metrics_snapshot_to_dict(snapshot=snapshot)


def _metrics_snapshot_to_dict(*, snapshot: MetricsSnapshot) -> dict[str, Any]:
    """Convert MetricsSnapshot to a JSON-serializable dictionary."""
    return {
        "timestamp": snapshot.timestamp.isoformat(),
        "rpc": {
            "total_requests": snapshot.rpc.total_requests,
            "successful_requests": snapshot.rpc.successful_requests,
            "failed_requests": snapshot.rpc.failed_requests,
            "rejected_requests": snapshot.rpc.rejected_requests,
            "coalesced_requests": snapshot.rpc.coalesced_requests,
            "executed_requests": snapshot.rpc.executed_requests,
            "pending_requests": snapshot.rpc.pending_requests,
            "circuit_breakers_open": snapshot.rpc.circuit_breakers_open,
            "circuit_breakers_half_open": snapshot.rpc.circuit_breakers_half_open,
            "state_transitions": snapshot.rpc.state_transitions,
            "avg_latency_ms": round(snapshot.rpc.avg_latency_ms, 2),
            "max_latency_ms": round(snapshot.rpc.max_latency_ms, 2),
            "last_failure_time": (
                snapshot.rpc.last_failure_time.isoformat() if snapshot.rpc.last_failure_time else None
            ),
            "rates": {
                "success_rate": round(snapshot.rpc.success_rate, 2),
                "failure_rate": round(snapshot.rpc.failure_rate, 2),
                "rejection_rate": round(snapshot.rpc.rejection_rate, 2),
                "coalesce_rate": round(snapshot.rpc.coalesce_rate, 2),
            },
        },
        "events": {
            "total_published": snapshot.events.total_published,
            "total_subscriptions": snapshot.events.total_subscriptions,
            "handlers_executed": snapshot.events.handlers_executed,
            "handler_errors": snapshot.events.handler_errors,
            "avg_handler_duration_ms": round(snapshot.events.avg_handler_duration_ms, 2),
            "max_handler_duration_ms": round(snapshot.events.max_handler_duration_ms, 2),
            "events_by_type": dict(snapshot.events.events_by_type),
            "error_rate": round(snapshot.events.error_rate, 2),
        },
        "cache": {
            "data_cache": {
                "size": snapshot.cache.data_cache.size,
                "hits": snapshot.cache.data_cache.hits,
                "misses": snapshot.cache.data_cache.misses,
                "evictions": snapshot.cache.data_cache.evictions,
                "hit_rate": round(snapshot.cache.data_cache.hit_rate, 2),
            },
            "overall_hit_rate": round(snapshot.cache.overall_hit_rate, 2),
            "total_entries": snapshot.cache.total_entries,
        },
        "health": {
            "overall_score": round(snapshot.health.overall_score, 2),
            "clients_total": snapshot.health.clients_total,
            "clients_healthy": snapshot.health.clients_healthy,
            "clients_degraded": snapshot.health.clients_degraded,
            "clients_failed": snapshot.health.clients_failed,
            "reconnect_attempts": snapshot.health.reconnect_attempts,
            "last_event_time": snapshot.health.last_event_time.isoformat(),
            "availability_rate": round(snapshot.health.availability_rate, 2),
        },
        "recovery": {
            "attempts_total": snapshot.recovery.attempts_total,
            "successes": snapshot.recovery.successes,
            "failures": snapshot.recovery.failures,
            "max_retries_reached": snapshot.recovery.max_retries_reached,
            "in_progress": snapshot.recovery.in_progress,
            "last_recovery_time": (
                snapshot.recovery.last_recovery_time.isoformat() if snapshot.recovery.last_recovery_time else None
            ),
            "success_rate": round(snapshot.recovery.success_rate, 2),
        },
        "model": {
            "devices_total": snapshot.model.devices_total,
            "devices_available": snapshot.model.devices_available,
            "channels_total": snapshot.model.channels_total,
            "data_points_generic": snapshot.model.data_points_generic,
            "data_points_custom": snapshot.model.data_points_custom,
            "data_points_calculated": snapshot.model.data_points_calculated,
            "data_points_subscribed": snapshot.model.data_points_subscribed,
            "programs_total": snapshot.model.programs_total,
            "sysvars_total": snapshot.model.sysvars_total,
        },
        "services": {
            "total_calls": snapshot.services.total_calls,
            "total_errors": snapshot.services.total_errors,
            "avg_duration_ms": round(snapshot.services.avg_duration_ms, 2),
            "max_duration_ms": round(snapshot.services.max_duration_ms, 2),
            "error_rate": round(snapshot.services.error_rate, 2),
            "by_method": {
                method: {
                    "call_count": stats.call_count,
                    "error_count": stats.error_count,
                    "avg_duration_ms": round(stats.avg_duration_ms, 2),
                    "max_duration_ms": round(stats.max_duration_ms, 2),
                    "error_rate": round(stats.error_rate, 2),
                }
                for method, stats in snapshot.services.by_method.items()
            },
        },
    }
