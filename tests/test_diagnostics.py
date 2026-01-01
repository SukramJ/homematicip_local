"""
Tests for diagnostics module to achieve 100% coverage.

This suite validates:
- async_get_config_entry_diagnostics composes the diagnostics payload and redacts sensitive config fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import MagicMock

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
