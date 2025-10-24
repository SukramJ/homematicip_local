"""
Unit tests for custom_components.homematicip_local.device_action.

These tests aim to reach 100% coverage for device_action.py by exercising:
- ACTION_SCHEMA validation
- async_get_actions across all branches
- async_call_action_from_config across all branches

All tests avoid modifying production code and rely on simple fakes/mocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry, mock_device_registry

from custom_components.homematicip_local import DOMAIN as HMIP_DOMAIN
from custom_components.homematicip_local.device_action import ACTION_SCHEMA
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
import homeassistant.helpers.config_validation as cv

from tests.const import INTERFACE_ID


@pytest.fixture
def device_reg(hass: HomeAssistant) -> dr.DeviceRegistry:
    """Return an empty, loaded device registry."""
    return mock_device_registry(hass)


def _add_device_with_identifiers(
    hass: HomeAssistant, device_reg: dr.DeviceRegistry, entry: MockConfigEntry, *, address: str, interface_id: str
) -> dr.DeviceEntry:
    """Create a device entry with the required Homematic identifier format."""
    entry.add_to_hass(hass)
    from aiohomematic.const import IDENTIFIER_SEPARATOR  # import inside to match runtime

    identifier_value = f"{address}{IDENTIFIER_SEPARATOR}{interface_id}"
    return device_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(HMIP_DOMAIN, identifier_value)},
    )


@dataclass
class _FakeChannel:
    no: int


class _FakeActionDp:
    """Simple fake matching the interface of a DpAction/DpButton used by the module."""

    def __init__(self, parameter: str, channel_no: int) -> None:
        self.parameter = parameter  # e.g. "PRESS_SHORT" or "PRESS_LONG"
        self.channel = _FakeChannel(channel_no)
        # send_value is awaited in the code when used for matching action
        self.send_value = AsyncMock()


def _make_runtime_data(has_client: bool, *, hm_device: Any | None) -> Any:
    """Create a ControlUnit-like object with a .central supporting has_client/get_device."""
    central = Mock()
    central.has_client.return_value = has_client
    central.get_device.return_value = hm_device

    runtime_data = Mock()
    runtime_data.central = central
    return runtime_data


def test_action_schema_validation() -> None:
    """ACTION_SCHEMA should accept valid config and reject invalid types."""
    # valid
    cfg = {CONF_DOMAIN: HMIP_DOMAIN, CONF_DEVICE_ID: "dev123", CONF_TYPE: "press_short", "subtype": 1}
    validated = ACTION_SCHEMA(cfg)
    assert validated[CONF_TYPE] == "press_short"

    # invalid type -> raises vol.Invalid via cv.Invalid
    with pytest.raises(cv.vol.Invalid):
        ACTION_SCHEMA({CONF_DEVICE_ID: "dev123", CONF_TYPE: "unknown", "subtype": 1})


@pytest.mark.asyncio
async def test_async_get_actions_all_paths(
    hass: HomeAssistant, device_reg: dr.DeviceRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Cover all branches in async_get_actions."""
    from custom_components.homematicip_local import device_action as da

    # 1) No device in registry -> []
    actions = await da.async_get_actions(hass, device_id="missing")
    assert actions == []

    # Prepare entry and device with identifiers
    entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
    device_entry = _add_device_with_identifiers(hass, device_reg, entry, address="ABC0001", interface_id=INTERFACE_ID)

    # 2) No runtime_data with proper client (has_client False) -> []
    entry.runtime_data = _make_runtime_data(has_client=False, hm_device=None)
    actions = await da.async_get_actions(hass, device_id=device_entry.id)
    assert actions == []

    # 3) has client but central returns no device -> []
    entry.runtime_data = _make_runtime_data(has_client=True, hm_device=None)
    actions = await da.async_get_actions(hass, device_id=device_entry.id)
    assert actions == []

    # 4) hm_device with non-action data points only -> filtered to []
    non_action_dp = object()  # won't match isinstance checks after patching below

    # Patch DpAction/DpButton in module to our fake so isinstance works with fake objects
    class MyDpAction(_FakeActionDp):
        pass

    class MyDpButton(_FakeActionDp):
        pass

    monkeypatch.setattr(da, "DpAction", MyDpAction)
    monkeypatch.setattr(da, "DpButton", MyDpButton)

    hm_device = Mock()
    hm_device.generic_data_points = [non_action_dp]
    entry.runtime_data = _make_runtime_data(has_client=True, hm_device=hm_device)
    actions = await da.async_get_actions(hass, device_id=device_entry.id)
    assert actions == []

    # 5) hm_device with action DPs where one has unsupported parameter -> filtered
    dp_other = MyDpAction(parameter="FOO", channel_no=2)
    hm_device.generic_data_points = [dp_other]
    actions = await da.async_get_actions(hass, device_id=device_entry.id)
    assert actions == []

    # 6) hm_device with valid action DPs -> action dicts created
    dp_short = MyDpAction(parameter="PRESS_SHORT", channel_no=1)
    dp_long = MyDpButton(parameter="PRESS_LONG", channel_no=3)
    hm_device.generic_data_points = [dp_short, dp_long]
    actions = await da.async_get_actions(hass, device_id=device_entry.id)
    assert {
        CONF_DOMAIN: HMIP_DOMAIN,
        CONF_DEVICE_ID: device_entry.id,
        CONF_TYPE: "press_short",
        "subtype": 1,
    } in actions
    assert {
        CONF_DOMAIN: HMIP_DOMAIN,
        CONF_DEVICE_ID: device_entry.id,
        CONF_TYPE: "press_long",
        "subtype": 3,
    } in actions


@pytest.mark.asyncio
async def test_async_call_action_from_config_all_paths(
    hass: HomeAssistant, device_reg: dr.DeviceRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Cover early returns and positive path for async_call_action_from_config."""
    from custom_components.homematicip_local import device_action as da

    # 1) No device -> return silently
    await da.async_call_action_from_config(
        hass, {CONF_DEVICE_ID: "missing", CONF_TYPE: "press_short", "subtype": 1}, {}, None
    )

    # Prepare entry/device
    entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
    device_entry = _add_device_with_identifiers(hass, device_reg, entry, address="ABC0002", interface_id=INTERFACE_ID)

    # 2) has_client False -> no call
    entry.runtime_data = _make_runtime_data(has_client=False, hm_device=None)
    await da.async_call_action_from_config(
        hass,
        {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1},
        {},
        None,
    )

    # Patch DpAction/DpButton to our fakes
    class MyDpAction(_FakeActionDp):
        pass

    class MyDpButton(_FakeActionDp):
        pass

    monkeypatch.setattr(da, "DpAction", MyDpAction)
    monkeypatch.setattr(da, "DpButton", MyDpButton)

    # 3) has_client True but no device -> early return
    entry.runtime_data = _make_runtime_data(has_client=True, hm_device=None)
    await da.async_call_action_from_config(
        hass,
        {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1},
        {},
        None,
    )

    # 4) device present but no matching DP -> no send_value
    hm_device = Mock()
    hm_device.generic_data_points = [MyDpAction("PRESS_LONG", 4)]
    entry.runtime_data = _make_runtime_data(has_client=True, hm_device=hm_device)
    await da.async_call_action_from_config(
        hass,
        {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1},
        {},
        None,
    )
    # ensure it didn't call
    hm_device.generic_data_points[0].send_value.assert_not_called()

    # 5) matching DP -> send_value(True) awaited
    dp = MyDpButton("PRESS_SHORT", 1)
    hm_device.generic_data_points = [dp]
    await da.async_call_action_from_config(
        hass,
        {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1},
        {},
        None,
    )
    dp.send_value.assert_awaited_once_with(value=True)
