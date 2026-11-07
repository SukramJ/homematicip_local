"""
Unit tests for custom_components.homematicip_local.device_trigger.

These tests target 100% coverage for device_trigger.py and cover:
- TRIGGER_SCHEMA validation
- async_get_triggers across all branches
- async_attach_trigger integration with HA event trigger
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from pytest_homeassistant.common import MockConfigEntry, mock_device_registry

from aiohomematic.const import IDENTIFIER_SEPARATOR
from custom_components.homematicip_local import DOMAIN as HMIP_DOMAIN
from custom_components.homematicip_local.device_trigger import TRIGGER_SCHEMA
from homeassistant.const import CONF_ADDRESS, CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

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
    from aiohomematic.const import IDENTIFIER_SEPARATOR

    identifier_value = f"{address}{IDENTIFIER_SEPARATOR}{interface_id}"
    return device_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(HMIP_DOMAIN, identifier_value)},
    )


@dataclass
class _FakeEventType:
    value: str


class _FakeClickEvent:
    """Simple fake of ClickEvent for tests."""

    def __init__(self, *, usage: Any, event_type: str, event_data: dict[str, Any]) -> None:
        self.usage = usage
        self.event_type = _FakeEventType(event_type)
        self._event_data = event_data

    def get_event_data(self) -> dict[str, Any]:
        return self._event_data


def _deprecation_reports(caplog: pytest.LogCaptureFixture) -> list[str]:
    """Return the deprecation notices Home Assistant logged for this integration."""
    return [record.getMessage() for record in caplog.records if "deprecated" in record.getMessage()]


def _make_runtime_data(*, hm_device: Any | None) -> Any:
    """Create a ControlUnit-like object whose central resolves a device by address."""
    device_coordinator = Mock()
    device_coordinator.get_device.return_value = hm_device

    central = Mock()
    central.device_coordinator = device_coordinator

    runtime_data = Mock()
    runtime_data.central = central
    return runtime_data


class TestTriggerSchema:
    """Tests for TRIGGER_SCHEMA validation."""

    def test_trigger_schema_validation(self) -> None:
        """TRIGGER_SCHEMA should accept a minimal valid config and coerce types."""
        cfg = {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: HMIP_DOMAIN,
            CONF_DEVICE_ID: "dev123",
            "interface_id": INTERFACE_ID,
            CONF_ADDRESS: "ABC0001",
            CONF_TYPE: "press_short",
            "subtype": 1,
            "event_type": "homematicip_local.click",
        }
        validated = TRIGGER_SCHEMA(cfg)
        assert validated[CONF_TYPE] == "press_short"
        assert validated[CONF_PLATFORM] == "device"


class TestAsyncGetTriggers:
    """Tests for async_get_triggers function."""

    @pytest.mark.asyncio
    async def test_async_get_triggers_all_paths(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Cover all branches in async_get_triggers."""
        from custom_components.homematicip_local import device_trigger as dt

        # 1) No device -> []
        triggers = await dt.async_get_triggers(hass, device_id="missing")
        assert triggers == []

        # 2) Device with identifiers missing the separator -> []
        entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
        entry.add_to_hass(hass)
        dev = device_reg.async_get_or_create(config_entry_id=entry.entry_id, identifiers={(HMIP_DOMAIN, "foo")})
        triggers = await dt.async_get_triggers(hass, device_id=dev.id)
        assert triggers == []

        device_entry = _add_device_with_identifiers(
            hass, device_reg, entry, address="ABC0002", interface_id=INTERFACE_ID
        )

        # Prepare fake DataPointUsage and ClickEvent used in module
        class MyDataPointUsage:
            NO_CREATE = object()

        monkeypatch.setattr(dt, "DataPointUsage", MyDataPointUsage)

        # 3) The central knows no device at that address -> []
        entry.runtime_data = _make_runtime_data(hm_device=None)
        triggers = await dt.async_get_triggers(hass, device_id=device_entry.id)
        assert triggers == []

        # Patch the ClickEvent dispatch pair in module so isinstance checks work
        class MyClickEvent(_FakeClickEvent):
            pass

        monkeypatch.setattr(dt, "CLICK_EVENT", (MyClickEvent,))

        # 5) device present but event not ClickEvent -> filtered
        hm_device = Mock()
        hm_device.generic_events = [object()]  # List with non-ClickEvent object

        entry.runtime_data = _make_runtime_data(hm_device=hm_device)
        triggers = await dt.async_get_triggers(hass, device_id=device_entry.id)
        assert triggers == []

        # 6) ClickEvent with usage NO_CREATE -> skipped
        from custom_components.homematicip_local.const import EVENT_CHANNEL_NO, EVENT_PARAMETER, EVENT_VALUE

        ev_data = {
            EVENT_PARAMETER: "PRESS_SHORT",
            EVENT_CHANNEL_NO: 1,
            EVENT_VALUE: True,
        }
        hm_device.generic_events = [  # List with NO_CREATE ClickEvent
            MyClickEvent(usage=MyDataPointUsage.NO_CREATE, event_type="evt", event_data=ev_data)
        ]
        triggers = await dt.async_get_triggers(hass, device_id=device_entry.id)
        assert triggers == []

        # 7) Valid ClickEvent -> trigger dict created (uses cleanup_click_event_data)
        hm_device.generic_events = [  # List with valid ClickEvent
            MyClickEvent(usage=object(), event_type="evt_type", event_data=ev_data)
        ]
        triggers = await dt.async_get_triggers(hass, device_id=device_entry.id)
        assert len(triggers) == 1
        trig = triggers[0]
        assert trig[CONF_PLATFORM] == "device"
        assert trig[CONF_DOMAIN] == HMIP_DOMAIN
        assert trig[CONF_DEVICE_ID] == device_entry.id
        assert trig["event_type"] == "evt_type"
        # From cleanup_click_event_data
        assert trig[CONF_TYPE] == "press_short"
        assert trig["subtype"] == 1

    @pytest.mark.asyncio
    async def test_async_get_triggers_lists_loom_click_events(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry
    ) -> None:
        """
        A loom device lists its keys as triggers.

        On the openccu-loom backend `generic_events` holds openccu-loom-client's
        twins, never aiohomematic instances. Dispatching on aiohomematic's
        ClickEvent alone dropped every one of them, so a loom device had no
        triggers. The trigger carries what the keypress bus event carries
        (control_unit.py `_on_device_trigger`), so an automation built on it fires.
        """
        from types import SimpleNamespace

        from openccu_loom_client.compat.aiohomematic.model.event import ClickEvent as LoomClickEvent, ImpulseEvent

        from custom_components.homematicip_local import device_trigger as dt

        entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
        entry.add_to_hass(hass)
        device_entry = _add_device_with_identifiers(
            hass, device_reg, entry, address="VCU0000001", interface_id=INTERFACE_ID
        )
        loom_device = SimpleNamespace(interface_id=INTERFACE_ID, model="HmIP-RC8")

        def _source(*, channel: int, parameter: str, usage: str) -> SimpleNamespace:
            return SimpleNamespace(
                device=loom_device,
                device_address="VCU0000001",
                channel_number=channel,
                parameter=parameter,
                summary=SimpleNamespace(usage=usage),
            )

        hm_device = Mock()
        hm_device.generic_events = [
            LoomClickEvent(data_point=_source(channel=1, parameter="PRESS_SHORT", usage="event")),
            LoomClickEvent(data_point=_source(channel=1, parameter="PRESS_LONG", usage="event")),
            # The channel operation mode excludes this key: no trigger, as in the reference.
            LoomClickEvent(data_point=_source(channel=2, parameter="PRESS_SHORT", usage="no_create")),
            # Not a keypress: device triggers list click events only.
            ImpulseEvent(data_point=_source(channel=0, parameter="SEQUENCE_OK", usage="event")),
        ]
        entry.runtime_data = _make_runtime_data(hm_device=hm_device)

        triggers = await dt.async_get_triggers(hass, device_id=device_entry.id)

        assert sorted((t[CONF_TYPE], t["subtype"]) for t in triggers) == [("press_long", 1), ("press_short", 1)]
        for trigger in triggers:
            assert trigger[CONF_PLATFORM] == "device"
            assert trigger[CONF_DEVICE_ID] == device_entry.id
            assert trigger["event_type"] == "homematic.keypress"
            assert trigger[CONF_ADDRESS] == "VCU0000001"
            assert trigger["interface_id"] == INTERFACE_ID
            TRIGGER_SCHEMA(trigger)  # what HA validates before attaching


class TestAsyncAttachTrigger:
    """Tests for async_attach_trigger function."""

    @pytest.mark.asyncio
    async def test_async_attach_trigger(self, hass: HomeAssistant, monkeypatch: pytest.MonkeyPatch) -> None:
        """Ensure async_attach_trigger forwards to event trigger with expected config."""
        from custom_components.homematicip_local import device_trigger as dt

        remove_cb = Mock()
        async_attach = AsyncMock(return_value=remove_cb)
        monkeypatch.setattr(dt.event_trigger, "async_attach_trigger", async_attach)

        config = {
            "interface_id": INTERFACE_ID,
            CONF_ADDRESS: "ABC0003",
            CONF_TYPE: "press_short",
            "subtype": 1,
            "event_type": "evt_type",
        }
        action = AsyncMock()
        trigger_info = Mock()

        cb = await dt.async_attach_trigger(hass, config, action, trigger_info)
        assert cb is remove_cb

        # Validate that event trigger was called with the expected event data and platform_type="device"
        assert async_attach.await_count == 1
        called_kwargs = async_attach.await_args.kwargs
        assert called_kwargs["platform_type"] == "device"
        ev_cfg = called_kwargs["config"]
        # event_type may be wrapped in a Jinja2 Template or list thereof by the trigger schema
        et_val = ev_cfg[dt.event_trigger.CONF_EVENT_TYPE]
        if isinstance(et_val, list):
            et_val = et_val[0]
        if hasattr(et_val, "template"):
            assert et_val.template == "evt_type"
        else:
            assert et_val == "evt_type"

        assert ev_cfg[dt.event_trigger.CONF_EVENT_DATA] == {
            "interface_id": INTERFACE_ID,
            CONF_ADDRESS: "ABC0003",
            CONF_TYPE: "press_short",
            "subtype": 1,
        }


class TestAsyncGetTriggersForeignConfigEntry:
    """A device can belong to several config entries; only ours is asked."""

    @pytest.mark.asyncio
    async def test_config_entry_of_another_domain_is_skipped(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry
    ) -> None:
        """Without the domain guard the loop would read a foreign integration's runtime_data."""
        from custom_components.homematicip_local import device_trigger as dt

        foreign = MockConfigEntry(domain="other_domain", data={})
        foreign.add_to_hass(hass)
        foreign.runtime_data = "not a control unit"
        device_entry = device_reg.async_get_or_create(
            config_entry_id=foreign.entry_id,
            identifiers={(HMIP_DOMAIN, f"ABC0009{IDENTIFIER_SEPARATOR}{INTERFACE_ID}")},
        )

        assert await dt.async_get_triggers(hass, device_id=device_entry.id) == []

    @pytest.mark.asyncio
    async def test_entry_lookup_reads_config_entry_id(
        self, hass: HomeAssistant, device_reg: dr.DeviceRegistry, caplog: pytest.LogCaptureFixture
    ) -> None:
        """The device's entry is resolved without a deprecation notice.

        HA 2026.11 reports ``DeviceEntry.config_entries`` as deprecated on every read
        (a device belongs to one entry, ``config_entry_id``) and drops it in 2027.10.
        """
        from custom_components.homematicip_local import device_trigger as dt

        entry = MockConfigEntry(domain=HMIP_DOMAIN, data={})
        device_entry = _add_device_with_identifiers(
            hass, device_reg, entry, address="ABC0004", interface_id=INTERFACE_ID
        )
        entry.runtime_data = _make_runtime_data(hm_device=None)

        assert await dt.async_get_triggers(hass, device_id=device_entry.id) == []
        assert _deprecation_reports(caplog) == []
