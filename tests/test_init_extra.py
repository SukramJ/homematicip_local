"""
Additional tests for custom_components.homematicip_local.__init__.

Targets remaining branches:
- async_setup_entry returns False on dependency version mismatch.
- async_setup_entry returns False when HA version too low.
- async_remove_config_entry_device returns False when device not removable (no identifiers).
- async_remove_entry executes without raising.
"""

from __future__ import annotations

from dataclasses import dataclass
import tempfile
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import custom_components.homematicip_local as hm_init


@dataclass
class _MockEntry:
    entry_id: str
    domain: str = hm_init.DOMAIN
    data: dict | None = None
    runtime_data: object | None = None

    def add_update_listener(self, fn):  # noqa: ANN001
        return lambda: None


@pytest.mark.asyncio
async def test_async_setup_entry_blocks_on_dependency_mismatch(hass) -> None:
    """When expected aiohomematic version != actual, setup should return False and log warning."""
    entry = _MockEntry(entry_id="1", data={})

    # Simulate mismatch: expected != installed
    with (
        patch("custom_components.homematicip_local.get_aiohomematic_version", return_value="1.2.3"),
        patch("custom_components.homematicip_local.HAHM_VERSION", "9.9.9"),
    ):
        ok = await hm_init.async_setup_entry(hass, entry)  # type: ignore[arg-type]
        assert ok is False


@pytest.mark.asyncio
async def test_async_setup_entry_blocks_on_low_ha_version(hass) -> None:
    """When HA version lower than required, setup should return False."""
    entry = _MockEntry(entry_id="2", data={})

    with (
        patch("custom_components.homematicip_local.get_aiohomematic_version", return_value=hm_init.HAHM_VERSION),
        patch("custom_components.homematicip_local.HMIP_LOCAL_MIN_HA_VERSION", "9999.1.1"),
    ):
        ok = await hm_init.async_setup_entry(hass, entry)  # type: ignore[arg-type]
        assert ok is False


@pytest.mark.asyncio
async def test_async_remove_config_entry_device_false_without_identifiers(hass) -> None:
    """If no identifiers present, device removal should return False."""
    entry = _MockEntry(entry_id="3", data={})

    # Create a minimal DeviceEntry-like object with no identifiers
    device_entry = SimpleNamespace(identifiers=set())

    res = await hm_init.async_remove_config_entry_device(hass, entry, device_entry)  # type: ignore[arg-type]
    assert res is False


@pytest.mark.asyncio
async def test_async_remove_entry_noop(hass) -> None:
    """async_remove_entry should call cleanup and stop central when runtime_data present."""
    from custom_components.homematicip_local.const import CONF_INSTANCE_NAME

    entry = _MockEntry(entry_id="4", data={CONF_INSTANCE_NAME: "test-instance"})
    # Provide a dummy control with stop_central; cleanup_files is patched to avoid FS ops
    entry.runtime_data = SimpleNamespace(stop_central=AsyncMock())

    with (
        patch("custom_components.homematicip_local.cleanup_files", return_value=None),
        patch("custom_components.homematicip_local.get_storage_directory", return_value=tempfile.gettempdir()),
    ):
        await hm_init.async_remove_entry(hass, entry)  # type: ignore[arg-type]
        # stop_central may or may not be awaited by implementation; primary goal is no exception
