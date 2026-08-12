"""Tests for the openccu-loom alarm surfaces (device, reset button, counter)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.homematicip_local.button import AioHomematicAlarmMotionResetButton
from custom_components.homematicip_local.const import (
    ALARM_DEVICE_IDENTIFIER,
    ALARM_DEVICE_MANUFACTURER,
    ALARM_DEVICE_NAME,
    DOMAIN,
)
from custom_components.homematicip_local.sensor import AioHomematicAlarmTriggeredMotionSensor

# pylint: disable=protected-access

_PANEL_UNIQUE_ID = "openccu-loom_alarm_erdgeschoss"


def _create_mock_panel(*, zone_name: str = "Erdgeschoss", triggered_motion_count: int = 0) -> MagicMock:
    """Create a mock LoomDpAlarmControlPanel."""
    mock_dp = MagicMock()
    mock_dp.unique_id = _PANEL_UNIQUE_ID
    mock_dp.configure_mock(name=zone_name)
    mock_dp.available = True
    mock_dp.enabled_default = True
    mock_dp.channel = None
    # openccu-loom is the naming authority for the panel itself.
    mock_dp.resolved_name = zone_name
    mock_dp.triggered_motion_count = triggered_motion_count
    mock_dp.reset_motion = AsyncMock(return_value=MagicMock(reset=0, failed=0))
    return mock_dp


def _create_entity[EntityT](entity_class: type[EntityT], *, mock_dp: MagicMock) -> EntityT:
    """Build one alarm entity with the hub base's collaborators patched out."""
    mock_cu = MagicMock()
    mock_cu.central.event_bus.create_subscription_group.return_value = MagicMock()
    with (
        patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ),
        patch(
            "custom_components.homematicip_local.generic_entity.get_entity_description",
            return_value=None,
        ),
    ):
        return entity_class(control_unit=mock_cu, data_point=mock_dp)  # type: ignore[call-arg]


class TestAlarmDeviceInfo:
    """
    Every alarm surface lands on one device of its own, not on a CCU.

    Alarm zones are daemon-level and may hold sensors of several
    centrals, so attaching them to one central states a belonging that
    does not exist — and buries the panels among dozens of sysvars while
    it is at it.
    """

    @pytest.mark.parametrize(
        "entity_class",
        [AioHomematicAlarmMotionResetButton, AioHomematicAlarmTriggeredMotionSensor],
    )
    def test_alarm_entities_share_the_alarm_device(self, entity_class: type) -> None:
        entity = _create_entity(entity_class, mock_dp=_create_mock_panel())
        device_info = entity._attr_device_info
        assert device_info is not None
        assert device_info["identifiers"] == {(DOMAIN, ALARM_DEVICE_IDENTIFIER)}
        assert device_info["name"] == ALARM_DEVICE_NAME
        assert device_info["manufacturer"] == ALARM_DEVICE_MANUFACTURER

    def test_the_identifier_matches_the_daemons_mqtt_block(self) -> None:
        """
        Byte-identical to `alarm_discovery.go`'s `alarmDeviceBlock`.

        An installation running both bridges must see one alarm device,
        not two describing the same zones.
        """
        assert ALARM_DEVICE_IDENTIFIER == "openccu-loom_alarm"


class TestMotionResetButton:
    """The control that ends the wait for a detector's blocking time."""

    async def test_a_partial_result_warns_but_does_not_raise(self) -> None:
        """
        `failed > 0` means the verb ran and some detectors did not answer.

        Raising would tell the operator nothing happened, when in fact
        the rest of the zone was cleared.
        """
        panel = _create_mock_panel()
        panel.reset_motion = AsyncMock(return_value=MagicMock(reset=2, failed=1))
        button = _create_entity(AioHomematicAlarmMotionResetButton, mock_dp=panel)
        with patch("custom_components.homematicip_local.button._LOGGER") as mock_logger:
            await button.async_press()
        mock_logger.warning.assert_called_once()

    def test_it_is_not_a_config_entity(self) -> None:
        """
        openccu-loom shipped this as `config` first and nobody found it.

        Home Assistant files config entities into a collapsed section of
        the device page and keeps them out of dashboards; this is an
        operator control.
        """
        button = _create_entity(AioHomematicAlarmMotionResetButton, mock_dp=_create_mock_panel())
        assert button.entity_category is None

    async def test_press_resets_the_zone(self) -> None:
        panel = _create_mock_panel()
        button = _create_entity(AioHomematicAlarmMotionResetButton, mock_dp=panel)
        await button.async_press()
        panel.reset_motion.assert_awaited_once_with()

    def test_the_zone_reaches_the_entity_name(self) -> None:
        """One device holds every zone, so the name has to carry it."""
        button = _create_entity(
            AioHomematicAlarmMotionResetButton, mock_dp=_create_mock_panel(zone_name="Obergeschoss")
        )
        assert button._attr_translation_key == "alarm_reset_motion"
        assert button._attr_translation_placeholders == {"zone": "Obergeschoss"}

    def test_unique_id_does_not_collide_with_the_panel(self) -> None:
        """
        The button rides the panel's data point, so the base's id is taken.

        Without the suffix Home Assistant would drop whichever of the two
        entities registered second.
        """
        button = _create_entity(AioHomematicAlarmMotionResetButton, mock_dp=_create_mock_panel())
        assert button._attr_unique_id == f"{DOMAIN}_{_PANEL_UNIQUE_ID}_reset_motion"


class TestTriggeredMotionSensor:
    """The number beside the button — why a zone will not arm."""

    def test_it_is_diagnostic(self) -> None:
        """Unlike the button next to it, this reports rather than acts."""
        sensor = _create_entity(AioHomematicAlarmTriggeredMotionSensor, mock_dp=_create_mock_panel())
        assert sensor.entity_category is not None
        assert sensor.entity_category.value == "diagnostic"

    def test_it_reports_the_panel_count(self) -> None:
        sensor = _create_entity(
            AioHomematicAlarmTriggeredMotionSensor, mock_dp=_create_mock_panel(triggered_motion_count=3)
        )
        assert sensor.native_value == 3

    def test_unique_id_does_not_collide_with_the_panel(self) -> None:
        sensor = _create_entity(AioHomematicAlarmTriggeredMotionSensor, mock_dp=_create_mock_panel())
        assert sensor._attr_unique_id == f"{DOMAIN}_{_PANEL_UNIQUE_ID}_triggered_motion"
