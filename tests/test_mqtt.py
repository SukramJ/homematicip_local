"""
Unit tests for custom_components.homematicip_local.mqtt.

Covers:
- Subscribe/unsubscribe logic depending on MQTT availability in hass.data.
- Message handlers for device and sysvar topics invoking central callbacks with parsed values.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from custom_components.homematicip_local.mqtt import MQTTConsumer


class _CentralStub:
    """Very small central stub exposing only methods used by MQTTConsumer."""

    def __init__(self) -> None:
        self._paths = [
            "devices/INTF/ADDR:1/VALUES/STATE",
            "devices/INTF/ADDR:2/VALUES/LEVEL",
        ]
        # Mock data point with event method and device.client.supports_rpc_callback = False
        self._mock_dp = MagicMock()
        self._mock_dp.event = MagicMock()
        self._mock_dp.device.client.supports_rpc_callback = False

        # Mock sysvar data point with event method
        self._mock_sv = MagicMock()
        self._mock_sv.event = MagicMock()

        # Mock hub_coordinator
        self.hub_coordinator = MagicMock()
        self.hub_coordinator.get_sysvar_data_point = MagicMock(return_value=self._mock_sv)

    def get_generic_data_point(self, state_path: str):  # noqa: ARG002
        return self._mock_dp

    def get_state_paths(self, rpc_callback_supported: bool = True) -> list[str]:  # noqa: ARG002
        return list(self._paths)


def _msg(topic: str, payload: str):
    # The handlers only access .topic and .payload; keep it simple
    return SimpleNamespace(topic=topic, payload=payload.encode())


class TestMQTTConsumer:
    """Tests for MQTTConsumer class."""

    def test_device_message_handler_calls_central(self, hass) -> None:
        """Device message handler should pass v field to central.data_point_path_event."""
        hass.data["mqtt"] = SimpleNamespace()
        central = _CentralStub()
        consumer = MQTTConsumer(hass=hass, central=central, mqtt_prefix="prefix")

        topic = "prefix/devices/INTF/ADDR:1/VALUES/STATE"
        consumer._on_device_mqtt_msg_receive(_msg(topic, payload='{"v": true}'))  # pylint: disable=protected-access

        # Verify that the data point's event method was called with correct arguments
        central._mock_dp.event.assert_called_once()
        call_kwargs = central._mock_dp.event.call_args.kwargs
        assert call_kwargs["value"] is True
        assert "received_at" in call_kwargs

    @pytest.mark.asyncio
    async def test_subscribe_and_unsubscribe_when_mqtt_available(self, hass, monkeypatch) -> None:
        """It should subscribe and then unsubscribe when MQTT is configured in hass.data."""
        # Provide dummy mqtt marker so _mqtt_is_configured returns True
        hass.data["mqtt"] = SimpleNamespace(client=object())

        central = _CentralStub()
        consumer = MQTTConsumer(hass=hass, central=central, mqtt_prefix="hm")

        # Patch MQTT subscribe/unsubscribe helpers to no-ops so we don't require a real client
        from custom_components.homematicip_local import mqtt as hm_mqtt

        def _noop(*args, **kwargs):
            return None

        async def _async_noop(*args, **kwargs):  # noqa: ANN001, ANN002
            return None

        # Patch the symbols used by our module (not the HA module) so calls no-op
        monkeypatch.setattr(hm_mqtt, "async_subscribe_topics", _async_noop)
        monkeypatch.setattr(hm_mqtt, "async_unsubscribe_topics", _noop)
        # Provide a minimal mqtt client marker with .connected used by HA utils when reached
        hass.data["mqtt"] = SimpleNamespace(client=SimpleNamespace(connected=True))

        # Call subscribe: this will build topics and call into MQTT helpers. We don't assert
        # the helper internals here, just ensure no exceptions and that a sub_state is created.
        await consumer.subscribe()
        assert consumer._sub_state is not None  # pylint: disable=protected-access

        # Unsubscribe should call into MQTT unsubscribe helper when sub_state exists.
        consumer.unsubscribe()

    @pytest.mark.asyncio
    async def test_subscribe_noop_when_mqtt_not_available(self, hass) -> None:
        """If MQTT not set in hass.data, subscribe/unsubscribe should no-op without error."""
        hass.data.pop("mqtt", None)
        central = _CentralStub()
        consumer = MQTTConsumer(hass=hass, central=central, mqtt_prefix="")

        await consumer.subscribe()  # no-op
        consumer.unsubscribe()  # no-op

    def test_sysvar_message_handler_calls_central(self, hass) -> None:
        """Sysvar message handler should pass v field to central.sysvar_data_point_path_event."""
        hass.data["mqtt"] = SimpleNamespace()
        central = _CentralStub()
        consumer = MQTTConsumer(hass=hass, central=central, mqtt_prefix="")

        topic = "sysvar/state/INTF/NAME"
        consumer._on_sysvar_mqtt_msg_receive(_msg(topic, payload='{"v": 42}'))  # pylint: disable=protected-access

        # Verify that the sysvar data point's event method was called with correct arguments
        central._mock_sv.event.assert_called_once()
        call_kwargs = central._mock_sv.event.call_args.kwargs
        assert call_kwargs["value"] == 42
        assert "received_at" in call_kwargs
