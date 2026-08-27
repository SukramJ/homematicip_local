"""Tests for the device registry entries the integration creates."""

from __future__ import annotations

from typing import Any

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.homematicip_local.const import DOMAIN
from homeassistant.helpers import device_registry as dr, entity_registry as er

from tests import const
from tests.helper import Factory

# HmIP-BSL and HmIP-DRSI4 carry several multi-channel groups and therefore
# split into sub devices; the thermostat contributes a schedule sub device.
TEST_DEVICES: dict[str, str] = {
    "VCU6985973": "HmIP-BSL.json",
    "VCU7204276": "HmIP-DRSI4.json",
    "VCU3609622": "HmIP-eTRV-2.json",
    "VCU2128127": "HmIP-BSM.json",
    "VCU0000057": "HM-RCV-50.json",
}


@pytest.fixture
def entry_data_sub_devices(entry_data_v1: dict[str, Any]) -> dict[str, Any]:
    """Return config entry data with sub devices enabled."""
    return entry_data_v1 | {"advanced_config": {"sub_devices_enabled": True}}


@pytest.fixture
def mock_config_entry_sub_devices(entry_data_sub_devices: dict[str, Any]) -> MockConfigEntry:
    """Return a current-version config entry with sub devices enabled."""
    return MockConfigEntry(
        entry_id=const.CONFIG_ENTRY_ID,
        version=17,
        domain=DOMAIN,
        title=const.INSTANCE_NAME,
        data=entry_data_sub_devices,
        options={},
        source="user",
        unique_id=const.CONFIG_ENTRY_UNIQUE_ID,
    )


@pytest.fixture
async def factory_sub_devices(
    hass: Any,
    mock_config_entry_sub_devices: MockConfigEntry,
    session_player_from_full_session_homegear: Any,
) -> Factory:
    """Return a central factory whose config entry has sub devices enabled."""
    return Factory(
        hass=hass,
        mock_config_entry=mock_config_entry_sub_devices,
        player=session_player_from_full_session_homegear,
    )


@pytest.mark.asyncio
async def test_via_device_links_resolve_with_sub_devices(
    factory_sub_devices: Factory,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test that every device links to a registered via device and entities are added.

    A device info references its via device by registry id, and HA drops every
    entity of a device whose via device id is not a registered device. The
    sub-device split is the one path that anchors a device at another Homematic
    device instead of the central, so it is the path that has to hold.
    """
    hass, control = await factory_sub_devices.setup_environment(TEST_DEVICES)
    assert control.enable_sub_devices is True

    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    devices = dr.async_entries_for_config_entry(device_registry, factory_sub_devices.mock_config_entry.entry_id)
    devices_by_id = {device.id: device for device in devices}

    central_devices = [device for device in devices if (DOMAIN, control.central.name) in device.identifiers]
    assert len(central_devices) == 1
    central_device = central_devices[0]
    assert central_device.via_device_id is None

    # Every other device hangs off a device that is actually registered.
    for device in devices:
        if device.id == central_device.id:
            continue
        assert device.via_device_id in devices_by_id, f"unresolved via device for {sorted(device.identifiers)}"

    # The sub-device split anchors at a Homematic device, not at the central.
    sub_devices = [
        device for device in devices if device.via_device_id is not None and device.via_device_id != central_device.id
    ]
    assert sub_devices, "expected at least one sub device below a Homematic device"

    # No entity was dropped because of an invalid device info.
    assert entity_registry.entities
    assert not [record for record in caplog.records if "invalid device info" in record.getMessage()]


@pytest.mark.asyncio
async def test_schedule_sub_device_hangs_off_its_device(factory_sub_devices: Factory) -> None:
    """Test that a schedule sub device links to the device it belongs to."""
    hass, control = await factory_sub_devices.setup_environment(TEST_DEVICES)

    device_registry = dr.async_get(hass)
    entry_id = factory_sub_devices.mock_config_entry.entry_id
    hm_device = control.central.device_coordinator.get_device(address="VCU3609622")
    assert hm_device is not None

    main_device = device_registry.async_get_device_by_identifier((DOMAIN, hm_device.identifier), entry_id)
    schedule_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, f"{hm_device.identifier}-schedule"), entry_id
    )
    assert main_device is not None
    assert schedule_device is not None
    assert schedule_device.via_device_id == main_device.id


@pytest.mark.asyncio
async def test_virtual_remotes_link_to_the_central(factory_sub_devices: Factory) -> None:
    """Test that virtual remotes are anchored at the central."""
    hass, control = await factory_sub_devices.setup_environment(TEST_DEVICES)

    device_registry = dr.async_get(hass)
    entry_id = factory_sub_devices.mock_config_entry.entry_id
    control._async_add_virtual_remotes_to_device_registry()

    virtual_remotes = control.central.device_coordinator.get_virtual_remotes()
    assert virtual_remotes

    central_device = device_registry.async_get_device_by_identifier((DOMAIN, control.central.name), entry_id)
    assert central_device is not None
    for virtual_remote in virtual_remotes:
        device = device_registry.async_get_device_by_identifier((DOMAIN, virtual_remote.identifier), entry_id)
        assert device is not None
        assert device.via_device_id == central_device.id
