"""
Tests for diagnostics module to achieve 100% coverage.

This suite validates:
- async_get_config_entry_diagnostics composes the diagnostics payload and redacts sensitive config fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.homematicip_local.diagnostics import async_get_config_entry_diagnostics


@dataclass
class _SystemInformation:
    """Minimal dataclass mimicking the central system information object."""

    serial: str
    version: str


class TestAsyncGetConfigEntryDiagnostics:
    """Tests for async_get_config_entry_diagnostics function."""

    @pytest.mark.asyncio
    async def test_compiles_payload_and_redacts(self, hass, mock_loaded_config_entry) -> None:
        """It should build diagnostics payload and redact username/password from config."""
        entry = mock_loaded_config_entry
        control_unit = entry.runtime_data

        # Mock device_registry.models
        mock_device_registry = MagicMock()
        mock_device_registry.models = ("HmIP-SMI", "HmIP-SWDO")
        control_unit.central.device_registry = mock_device_registry

        # Provide a minimal dataclass for system_information to satisfy asdict(...)
        control_unit.central.system_information = _SystemInformation(serial="ABC123", version="1.2.3")

        # Mock health.to_dict()
        mock_health = MagicMock()
        mock_health.to_dict.return_value = {
            "overall_score": 100,
            "clients_total": 1,
            "clients_healthy": 1,
        }
        control_unit.central.health = mock_health

        # Mock metrics_aggregator.snapshot().to_dict()
        mock_metrics_snapshot = MagicMock()
        mock_metrics_snapshot.to_dict.return_value = {
            "timestamp": "2025-01-01T00:00:00",
            "rpc": {"total_requests": 100},
            "events": {"total_published": 50},
            "cache": {"overall_hit_rate": 0.95},
            "health": {"overall_score": 100},
            "recovery": {"attempts_total": 0},
            "model": {"devices_total": 10},
            "services": {"total_calls": 25},
        }
        mock_metrics_aggregator = MagicMock()
        mock_metrics_aggregator.snapshot.return_value = mock_metrics_snapshot
        control_unit.central.metrics_aggregator = mock_metrics_aggregator

        # Mock cache_coordinator.incident_store.get_diagnostics() (async method)
        mock_incident_store = MagicMock()
        mock_incident_store.get_diagnostics = AsyncMock(return_value={"incidents": []})
        mock_cache_coordinator = MagicMock()
        mock_cache_coordinator.incident_store = mock_incident_store
        control_unit.central.cache_coordinator = mock_cache_coordinator

        # Mock client_coordinator.clients with command_throttle properties
        mock_throttle = MagicMock()
        mock_throttle.interval = 0.5
        mock_throttle.is_enabled = True
        mock_throttle.queue_size = 0
        mock_throttle.throttled_count = 10
        mock_throttle.critical_count = 2
        mock_throttle.burst_count = 1
        mock_throttle.burst_threshold = 5
        mock_throttle.burst_window = 0.5

        mock_client = MagicMock()
        mock_client.interface_id = "HmIP-RF"
        mock_client.command_throttle = mock_throttle

        mock_client_coordinator = MagicMock()
        mock_client_coordinator.clients = (mock_client,)
        control_unit.central.client_coordinator = mock_client_coordinator

        diag = await async_get_config_entry_diagnostics(hass, entry)

        # Config redaction: ensure sensitive fields are not equal to the original ones
        cfg = diag["config"]
        assert cfg["data"]["username"] != entry.data["username"]
        assert cfg["data"]["password"] != entry.data["password"]

        # Models are present
        assert diag["models"] == ("HmIP-SMI", "HmIP-SWDO")

        # System information present and shaped as a dict derived from dataclass
        assert isinstance(diag["system_information"], dict)
        assert diag["system_information"]["version"] == "1.2.3"
        # Serial should be redacted
        assert diag["system_information"]["serial"] != "ABC123"

        # System health present (from to_dict())
        assert "system_health" in diag
        assert diag["system_health"]["overall_score"] == 100

        # Metrics present with expected structure (from to_dict())
        assert "metrics" in diag
        assert "timestamp" in diag["metrics"]
        assert "rpc" in diag["metrics"]
        assert "events" in diag["metrics"]
        assert "cache" in diag["metrics"]
        assert "health" in diag["metrics"]
        assert "recovery" in diag["metrics"]
        assert "model" in diag["metrics"]
        assert "services" in diag["metrics"]

        # Command throttle statistics present
        assert "command_throttle" in diag
        assert "HmIP-RF" in diag["command_throttle"]
        throttle_data = diag["command_throttle"]["HmIP-RF"]
        assert throttle_data["interval"] == 0.5
        assert throttle_data["is_enabled"] is True
        assert throttle_data["queue_size"] == 0
        assert throttle_data["throttled_count"] == 10
        assert throttle_data["critical_count"] == 2
        assert throttle_data["burst_count"] == 1
        assert throttle_data["burst_threshold"] == 5
        assert throttle_data["burst_window"] == 0.5
