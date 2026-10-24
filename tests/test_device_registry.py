"""Tests for the device registry entries the integration creates."""

from __future__ import annotations

from typing import Any

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.homematicip_local.const import DOMAIN
from custom_components.homematicip_local.support import get_device_identifier
from homeassistant.helpers import device_registry as dr, entity_registry as er

from tests import const
from tests.helper import Factory

# HmIP-BSL and HmIP-DRSI4 carry several multi-channel groups and therefore
# split into child devices; the thermostat contributes a schedule child.
TEST_DEVICES: dict[str, str] = {
    "VCU6985973": "HmIP-BSL.json",
    "VCU7204276": "HmIP-DRSI4.json",
    "VCU3609622": "HmIP-eTRV-2.json",
    "VCU2128127": "HmIP-BSM.json",
    "VCU0000057": "HM-RCV-50.json",
}
_THERMOSTAT = "VCU3609622"
_SWITCH_ACTUATOR = "VCU7204276"


def _entry_data(entry_data_v1: dict[str, Any], *, sub_devices_enabled: bool) -> dict[str, Any]:
    return entry_data_v1 | {"advanced_config": {"sub_devices_enabled": sub_devices_enabled}}


def _config_entry(data: dict[str, Any]) -> MockConfigEntry:
    return MockConfigEntry(
        entry_id=const.CONFIG_ENTRY_ID,
        version=17,
        domain=DOMAIN,
        title=const.INSTANCE_NAME,
        data=data,
        options={},
        source="user",
        unique_id=const.CONFIG_ENTRY_UNIQUE_ID,
    )


@pytest.fixture
def mock_config_entry_sub_devices(entry_data_v1: dict[str, Any]) -> MockConfigEntry:
    """Return a current-version config entry with sub devices enabled."""
    return _config_entry(_entry_data(entry_data_v1, sub_devices_enabled=True))


@pytest.fixture
def mock_config_entry_no_sub_devices(entry_data_v1: dict[str, Any]) -> MockConfigEntry:
    """Return a current-version config entry with sub devices disabled."""
    return _config_entry(_entry_data(entry_data_v1, sub_devices_enabled=False))


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


@pytest.fixture
async def factory_no_sub_devices(
    hass: Any,
    mock_config_entry_no_sub_devices: MockConfigEntry,
    session_player_from_full_session_homegear: Any,
) -> Factory:
    """Return a central factory whose config entry has sub devices disabled."""
    return Factory(
        hass=hass,
        mock_config_entry=mock_config_entry_no_sub_devices,
        player=session_player_from_full_session_homegear,
    )


@pytest.mark.asyncio
async def test_devices_hang_off_the_central_and_split_into_children(
    factory_sub_devices: Factory,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test that every main device links to the central and the split-off parts are child devices.

    A device info references its via device and a child device info its parent
    by registry id, and HA drops every entity whose device info points at an
    unregistered id. The sub-device split is the one path that anchors a device
    at another Homematic device instead of the central, so it is the path that
    has to hold.
    """
    hass, control = await factory_sub_devices.setup_environment(TEST_DEVICES)
    assert control.enable_sub_devices is True

    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    entry_id = factory_sub_devices.mock_config_entry.entry_id
    devices = dr.async_entries_for_config_entry(device_registry, entry_id)
    devices_by_id = {device.id: device for device in devices}

    central_devices = [device for device in devices if (DOMAIN, control.central.name) in device.identifiers]
    assert len(central_devices) == 1
    central_device = central_devices[0]
    assert central_device.via_device_id is None

    # Every main device hangs off the central; the via link is for hub relations only.
    for device in devices:
        if device.id == central_device.id:
            continue
        assert device.via_device_id == central_device.id, f"unexpected via device for {sorted(device.identifiers)}"

    # The split-off parts of a device are its children, and every parent is registered.
    children = dr.async_child_entries_for_config_entry(device_registry, entry_id)
    assert children, "expected at least one child device below a Homematic device"
    for child in children:
        assert child.parent_device_id in devices_by_id, f"unresolved parent for {sorted(child.identifiers)}"
        assert child.parent_device_id != central_device.id
        # A child carries entities of its own.
        assert er.async_entries_for_device(entity_registry, child.id, include_disabled_entities=True)

    # No entity was dropped because of an invalid device info.
    assert entity_registry.entities
    assert not [
        record
        for record in caplog.records
        if "invalid device info" in record.getMessage() or "error adding device" in record.getMessage()
    ]


@pytest.mark.asyncio
async def test_schedule_child_hangs_off_its_device(factory_sub_devices: Factory) -> None:
    """Test that a schedule child device links to the device it belongs to and carries its own name only."""
    hass, control = await factory_sub_devices.setup_environment(TEST_DEVICES)

    device_registry = dr.async_get(hass)
    entry_id = factory_sub_devices.mock_config_entry.entry_id
    hm_device = control.central.device_coordinator.get_device(address=_THERMOSTAT)
    assert hm_device is not None

    main_device = device_registry.async_get_device_by_identifier((DOMAIN, hm_device.identifier), entry_id)
    schedule_device = device_registry.async_get_child_device_by_identifier(
        (DOMAIN, f"{hm_device.identifier}-schedule"), entry_id
    )
    assert main_device is not None
    assert main_device.name == hm_device.name
    assert schedule_device is not None
    assert schedule_device.parent_device_id == main_device.id
    # HA composes "<parent> <child>" itself, so the child does not repeat the parent.
    assert schedule_device.name in ("Schedule", "Zeitplan")
    # The old sub device is not around as a main device any more.
    assert (
        device_registry.async_get_device_by_identifier((DOMAIN, f"{hm_device.identifier}-schedule"), entry_id) is None
    )


@pytest.mark.asyncio
async def test_channel_group_child_carries_the_group_room(factory_sub_devices: Factory) -> None:
    """Test that a channel group child is keyed by its group number and named without the device prefix."""
    hass, control = await factory_sub_devices.setup_environment(TEST_DEVICES)

    device_registry = dr.async_get(hass)
    entry_id = factory_sub_devices.mock_config_entry.entry_id
    hm_device = control.central.device_coordinator.get_device(address=_SWITCH_ACTUATOR)
    assert hm_device is not None
    assert hm_device.has_sub_devices

    main_device = device_registry.async_get_device_by_identifier((DOMAIN, hm_device.identifier), entry_id)
    assert main_device is not None
    group_children = dr.async_entries_for_parent_device(device_registry, main_device.id)
    assert group_children
    for child in group_children:
        assert child.name
        assert not child.name.startswith(hm_device.name)


@pytest.mark.asyncio
async def test_legacy_sub_devices_are_converted_in_place(
    hass: Any,
    mock_config_entry_sub_devices: MockConfigEntry,
    session_player_from_full_session_homegear: Any,
) -> None:
    """
    Test that a sub device registered as a main device by an earlier release becomes a child, keeping its device_id.

    Earlier releases split a device with via_device links. HA converts such an
    entry when a child device info with the same identifiers arrives — but only
    if the integration did not register it as a main device in this session, so
    the parent-creation path must leave the child to the entity platform.
    """
    entry = mock_config_entry_sub_devices
    entry.add_to_hass(hass)
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    # Seed the registry the way a pre-child-device release left it. The
    # identifier is composed the way the integration composes it; the test
    # checks below that the running control unit agrees.
    device_identifier = get_device_identifier(
        instance_name=const.INSTANCE_NAME, address=_THERMOSTAT, interface="BidCos-RF"
    )
    assert device_identifier is not None
    central = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id, identifiers={(DOMAIN, const.INSTANCE_NAME)}, name=const.INSTANCE_NAME
    )
    legacy_main = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, device_identifier)},
        name="Thermostat",
        via_device_id=central.id,
    )
    legacy_sub = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, f"{device_identifier}-schedule")},
        name="Thermostat Zeitplan",
        manufacturer="eQ-3",
        via_device_id=legacy_main.id,
    )
    device_registry.async_update_device(legacy_sub.id, name_by_user="Mein Zeitplan")
    legacy_sub_id = legacy_sub.id
    # HA refuses to convert a device the same config entry registered as a main
    # device in this session. In production the legacy entries come from
    # storage; here the unload hook draws that session boundary.
    device_registry.async_config_entry_unloaded(entry.entry_id)

    factory = Factory(hass=hass, mock_config_entry=entry, player=session_player_from_full_session_homegear)
    _, control = await factory.setup_environment(TEST_DEVICES)
    hm_device = control.central.device_coordinator.get_device(address=_THERMOSTAT)
    assert hm_device is not None
    assert control.device_identifier(device=hm_device) == device_identifier

    converted = device_registry.async_get(legacy_sub_id)
    assert isinstance(converted, dr.ChildDeviceEntry), "the legacy sub device was not converted in place"
    assert converted.parent_device_id == legacy_main.id
    assert converted.identifiers == {(DOMAIN, f"{device_identifier}-schedule")}
    # The user's own name survives, the integration's name loses the device prefix.
    assert converted.name_by_user == "Mein Zeitplan"
    assert converted.name in ("Schedule", "Zeitplan")
    assert er.async_entries_for_device(entity_registry, legacy_sub_id, include_disabled_entities=True)
    # The parent kept its id and got its device data from the entities landing on it.
    parent = device_registry.async_get(legacy_main.id)
    assert isinstance(parent, dr.DeviceEntry)
    assert parent.name == hm_device.name
    assert parent.manufacturer


@pytest.mark.asyncio
async def test_disabling_sub_devices_moves_entities_onto_the_device(
    hass: Any,
    entry_data_v1: dict[str, Any],
    session_player_from_full_session_homegear: Any,
) -> None:
    """
    Test that switching sub devices off lands the entities on the device while the child entries stay.

    HA cannot turn a child back into a main device, and the device identifiers
    do not overlap with those of the children, so the entities move over and
    the children are left behind without entities, as orphaned sub devices were.
    """
    entry = _config_entry(_entry_data(entry_data_v1, sub_devices_enabled=True))
    factory = Factory(hass=hass, mock_config_entry=entry, player=session_player_from_full_session_homegear)
    _, control = await factory.setup_environment(TEST_DEVICES)
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    hm_device = control.central.device_coordinator.get_device(address=_THERMOSTAT)
    assert hm_device is not None
    schedule_child = device_registry.async_get_child_device_by_identifier(
        (DOMAIN, f"{hm_device.identifier}-schedule"), entry.entry_id
    )
    assert schedule_child is not None
    schedule_entities = er.async_entries_for_device(entity_registry, schedule_child.id, include_disabled_entities=True)
    assert schedule_entities

    await hass.config_entries.async_unload(entry.entry_id)
    hass.config_entries.async_update_entry(entry, data=_entry_data(entry_data_v1, sub_devices_enabled=False))
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    main_device = device_registry.async_get_device_by_identifier((DOMAIN, hm_device.identifier), entry.entry_id)
    assert main_device is not None
    for entity_entry in schedule_entities:
        assert entity_registry.async_get(entity_entry.entity_id).device_id == main_device.id
    # The child entry is still there, without entities, as HA cannot convert it back.
    assert isinstance(device_registry.async_get(schedule_child.id), dr.ChildDeviceEntry)
    assert not er.async_entries_for_device(entity_registry, schedule_child.id, include_disabled_entities=True)


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
