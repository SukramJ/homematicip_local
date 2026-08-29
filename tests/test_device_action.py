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

from aiohomematic.const import IDENTIFIER_SEPARATOR
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


def _make_runtime_data(*, hm_device: Any | None) -> Any:
    """Create a ControlUnit-like object whose central resolves a device by address."""
    device_coordinator = Mock()
    device_coordinator.get_device.return_value = hm_device

    central = Mock()
    central.device_coordinator = device_coordinator

    runtime_data = Mock()
    runtime_data.central = central
    return runtime_data


class TestActionSchema:
    """Tests for ACTION_SCHEMA validation."""

    def test_action_schema_validation(self) -> None:
        """ACTION_SCHEMA should accept valid config and reject invalid types."""
        # valid
        cfg = {CONF_DOMAIN: HMIP_DOMAIN, CONF_DEVICE_ID: "dev123", CONF_TYPE: "press_short", "subtype": 1}
        validated = ACTION_SCHEMA(cfg)
        assert validated[CONF_TYPE] == "press_short"

        # invalid type -> raises vol.Invalid via cv.Invalid
        with pytest.raises(cv.vol.Invalid):
            ACTION_SCHEMA({CONF_DEVICE_ID: "dev123", CONF_TYPE: "unknown", "subtype": 1})


class TestAsyncGetActions:
    """Tests for async_get_actions function."""

    @pytest.mark.asyncio
    async def test_async_get_actions_all_paths(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Cover all branches in async_get_actions."""
        from custom_components.homematicip_local import device_action as da

        # 1) No device in registry -> []
        actions = await da.async_get_actions(hass, device_id="missing")
        assert actions == []

        # Prepare entry and device with identifiers
        entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
        device_entry = _add_device_with_identifiers(
            hass, device_reg, entry, address="ABC0001", interface_id=INTERFACE_ID
        )

        # 2) The central knows no device at that address -> []
        entry.runtime_data = _make_runtime_data(hm_device=None)
        actions = await da.async_get_actions(hass, device_id=device_entry.id)
        assert actions == []

        # Patch the action/button dispatch tuple to our fakes so isinstance works with fake objects
        class MyDpAction(_FakeActionDp):
            pass

        class MyDpButton(_FakeActionDp):
            pass

        monkeypatch.setattr(da, "DP_ACTION_OR_BUTTON", (MyDpAction, MyDpButton))

        # 4) hm_device with non-action data points only -> filtered to []
        non_action_dp = object()  # won't match isinstance checks after patching below

        hm_device = Mock()
        hm_device.generic_data_points = [non_action_dp]  # List of data points
        entry.runtime_data = _make_runtime_data(hm_device=hm_device)
        actions = await da.async_get_actions(hass, device_id=device_entry.id)
        assert actions == []

        # 5) hm_device with action DPs where one has unsupported parameter -> filtered
        dp_other = MyDpAction(parameter="FOO", channel_no=2)
        hm_device.generic_data_points = [dp_other]  # List with unsupported parameter
        entry.runtime_data = _make_runtime_data(hm_device=hm_device)
        actions = await da.async_get_actions(hass, device_id=device_entry.id)
        assert actions == []

        # 6) hm_device with valid action DPs -> action dicts created
        dp_short = MyDpAction(parameter="PRESS_SHORT", channel_no=1)
        dp_long = MyDpButton(parameter="PRESS_LONG", channel_no=3)
        hm_device.generic_data_points = [dp_short, dp_long]  # List with valid DPs
        entry.runtime_data = _make_runtime_data(hm_device=hm_device)
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


class TestAsyncCallActionFromConfig:
    """Tests for async_call_action_from_config function."""

    @pytest.mark.asyncio
    async def test_async_call_action_from_config_all_paths(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Cover early returns and positive path for async_call_action_from_config."""
        from custom_components.homematicip_local import device_action as da

        # 1) No device -> return silently
        await da.async_call_action_from_config(
            hass, {CONF_DEVICE_ID: "missing", CONF_TYPE: "press_short", "subtype": 1}, {}, None
        )

        # Prepare entry/device
        entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
        device_entry = _add_device_with_identifiers(
            hass, device_reg, entry, address="ABC0002", interface_id=INTERFACE_ID
        )

        # Patch the action/button dispatch tuple to our fakes
        class MyDpAction(_FakeActionDp):
            pass

        class MyDpButton(_FakeActionDp):
            pass

        monkeypatch.setattr(da, "DP_ACTION_OR_BUTTON", (MyDpAction, MyDpButton))

        # 2) The central knows no device at that address -> early return
        entry.runtime_data = _make_runtime_data(hm_device=None)
        await da.async_call_action_from_config(
            hass,
            {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1},
            {},
            None,
        )

        # 4) device present but no matching DP -> no send_value
        hm_device = Mock()
        dp_no_match = MyDpAction("PRESS_LONG", 4)
        hm_device.generic_data_points = [dp_no_match]  # List with non-matching DP
        entry.runtime_data = _make_runtime_data(hm_device=hm_device)
        await da.async_call_action_from_config(
            hass,
            {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1},
            {},
            None,
        )
        # ensure it didn't call
        dp_no_match.send_value.assert_not_called()

        # 5) matching DP -> send_value(True) awaited
        dp = MyDpButton("PRESS_SHORT", 1)
        hm_device.generic_data_points = [dp]  # List with matching DP
        await da.async_call_action_from_config(
            hass,
            {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1},
            {},
            None,
        )
        dp.send_value.assert_awaited_once_with(value=True)


class TestAsyncGetActionsRejectedDevices:
    """The two ways a device entry yields no actions before any backend is asked."""

    @pytest.mark.asyncio
    async def test_config_entry_of_another_domain_is_skipped(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry
    ) -> None:
        """A device can belong to several config entries; only ours is asked.

        Without the domain guard the loop would read ``runtime_data`` of a
        foreign integration, where it is whatever that integration put there.
        """
        from custom_components.homematicip_local import device_action as da

        foreign = MockConfigEntry(domain="other_domain", data={})
        foreign.add_to_hass(hass)
        foreign.runtime_data = "not a control unit"
        device_entry = device_reg.async_get_or_create(
            config_entry_id=foreign.entry_id,
            identifiers={(HMIP_DOMAIN, f"ABC0003{IDENTIFIER_SEPARATOR}{INTERFACE_ID}")},
        )

        assert await da.async_get_actions(hass, device_id=device_entry.id) == []
        await da.async_call_action_from_config(
            hass, {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1}, {}, None
        )

    @pytest.mark.asyncio
    async def test_device_without_an_address_identifier(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry
    ) -> None:
        """The central's own entry carries a bare name, no ``address@…``.

        It is a device of this integration like any other, so it reaches both
        entry points, and neither may treat the name as an address.
        """
        from custom_components.homematicip_local import device_action as da

        entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
        entry.add_to_hass(hass)
        central_entry = device_reg.async_get_or_create(
            config_entry_id=entry.entry_id, identifiers={(HMIP_DOMAIN, "CentralName")}
        )
        entry.runtime_data = _make_runtime_data(hm_device=Mock())

        assert await da.async_get_actions(hass, device_id=central_entry.id) == []
        await da.async_call_action_from_config(
            hass, {CONF_DEVICE_ID: central_entry.id, CONF_TYPE: "press_short", "subtype": 1}, {}, None
        )
        entry.runtime_data.central.device_coordinator.get_device.assert_not_called()


class TestAsyncCallActionSkipsForeignDataPoints:
    """The action loop walks every generic data point of the device."""

    @pytest.mark.asyncio
    async def test_non_action_data_point_is_skipped(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A device mixes action data points with sensors; only the former may be sent to."""
        from custom_components.homematicip_local import device_action as da

        class MyDpAction(_FakeActionDp):
            pass

        monkeypatch.setattr(da, "DP_ACTION_OR_BUTTON", (MyDpAction,))

        entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
        device_entry = _add_device_with_identifiers(
            hass, device_reg, entry, address="ABC0004", interface_id=INTERFACE_ID
        )
        matching = MyDpAction(parameter="PRESS_SHORT", channel_no=1)
        hm_device = Mock()
        # The sensor comes first, so the loop has to skip it to reach the button.
        hm_device.generic_data_points = [object(), matching]
        entry.runtime_data = _make_runtime_data(hm_device=hm_device)

        await da.async_call_action_from_config(
            hass, {CONF_DEVICE_ID: device_entry.id, CONF_TYPE: "press_short", "subtype": 1}, {}, None
        )

        matching.send_value.assert_awaited_once_with(value=True)
