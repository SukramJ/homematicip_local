"""
Tests for diagnostics module to achieve 100% coverage.

This suite validates:
- get_devices_per_type_stats returns a sorted tuple of unique models.
- get_data_points_by_platform_stats aggregates counts across data point sources and returns sorted mapping.
- async_get_config_entry_diagnostics composes the diagnostics payload and redacts sensitive config fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

import pytest

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.diagnostics import (
    async_get_config_entry_diagnostics,
    get_data_points_by_platform_stats,
    get_devices_per_type_stats,
)


class _CentralStub:
    """Very small central stub exposing only what the helpers need."""

    def __init__(self) -> None:
        self.devices: list[Any] = []
        self._data_points: list[Any] = []
        self.program_data_points: list[Any] = []
        self.sysvar_data_points: list[Any] = []

    def get_data_points(self, registered: bool | None = None) -> list[Any]:  # noqa: ARG002 - parity with real API
        return list(self._data_points)


@dataclass
class _SystemInformation:
    """Minimal dataclass mimicking the central system information object."""

    serial: str
    version: str


def _dp(category: DataPointCategory) -> Any:
    """Create a minimal data point-like object with a category attribute."""
    return SimpleNamespace(category=category)


class TestGetDevicesPerTypeStats:
    """Tests for get_devices_per_type_stats function."""

    def test_returns_sorted_unique_models(self) -> None:
        """It should return a sorted tuple of unique device models."""
        central = _CentralStub()
        central.devices = [
            SimpleNamespace(model="B-Model"),
            SimpleNamespace(model="A-Model"),
            SimpleNamespace(model="B-Model"),
        ]

        result = get_devices_per_type_stats(central=central)  # type: ignore[arg-type]

        assert result == ("A-Model", "B-Model")


class TestGetDataPointsByPlatformStats:
    """Tests for get_data_points_by_platform_stats function."""

    def test_aggregates_and_sorts(self) -> None:
        """It should count data points across all sources per category and return a sorted mapping."""
        central = _CentralStub()
        central._data_points = [_dp(DataPointCategory.BINARY_SENSOR), _dp(DataPointCategory.SENSOR)]
        central.program_data_points = [_dp(DataPointCategory.SWITCH)]
        central.sysvar_data_points = [_dp(DataPointCategory.SENSOR)]

        result = get_data_points_by_platform_stats(central=central)  # type: ignore[arg-type]

        # Expect counts per category and categories sorted by enum value (via dict(sorted(...)))
        assert result == {
            DataPointCategory.BINARY_SENSOR: 1,
            DataPointCategory.SENSOR: 2,
            DataPointCategory.SWITCH: 1,
        }


class TestAsyncGetConfigEntryDiagnostics:
    """Tests for async_get_config_entry_diagnostics function."""

    @pytest.mark.asyncio
    async def test_compiles_payload_and_redacts(self, hass, mock_loaded_config_entry) -> None:
        """It should build diagnostics payload and redact username/password from config."""
        entry = mock_loaded_config_entry
        control_unit = entry.runtime_data

        # Ensure central has required attributes used by diagnostics
        control_unit.central.devices = []
        control_unit.central.get_data_points.return_value = []
        control_unit.central.program_data_points = []
        control_unit.central.sysvar_data_points = []
        # Provide a minimal dataclass for system_information to satisfy asdict(...)
        control_unit.central.system_information = _SystemInformation(serial="ABC123", version="1.2.3")

        diag = await async_get_config_entry_diagnostics(hass, entry)

        # Config redaction: ensure sensitive fields are not equal to the original ones
        cfg = diag["config"]
        assert cfg["data"]["username"] != entry.data["username"]
        assert cfg["data"]["password"] != entry.data["password"]

        # Devices and platform stats are present
        assert diag["devices"] == ()
        assert diag["platform_stats"] == {}

        # System information present and shaped as a dict derived from dataclass
        assert isinstance(diag["system_information"], dict)
        assert diag["system_information"]["version"] == "1.2.3"
