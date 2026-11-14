"""Tests for the generic entity base class."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.const import DOMAIN
from custom_components.homematicip_local.control_unit import ControlUnit
from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity, AioHomematicGenericHubEntity
from custom_components.homematicip_local.support import get_device_identifier

# pylint: disable=protected-access

_CENTRAL_NAME = "test_central"
_DEVICE_ADDRESS = "ABC1234567"
_DEVICE_INTERFACE = "HmIP-RF"
# What the integration composes itself — instance name plus interface type,
# never the backend's own identifier below.
_DEVICE_IDENTIFIER = f"{_DEVICE_ADDRESS}@{_CENTRAL_NAME}-{_DEVICE_INTERFACE}"
_BACKEND_IDENTIFIER = f"{_DEVICE_ADDRESS}@some-daemon-central-{_DEVICE_INTERFACE}"
_CENTRAL_DEVICE_ID = "central-device-registry-id"
_PARENT_DEVICE_ID = "parent-device-registry-id"


def _create_mock_data_point(
    *,
    category: DataPointCategory = DataPointCategory.SWITCH,
    device_name: str = "HmIP-PSM Test",
) -> MagicMock:
    """Create a mock data point for testing."""
    mock_dp = MagicMock()
    mock_dp.category = category
    mock_dp.unique_id = "test_unique_id"
    mock_dp.full_name = f"{device_name} Switch"
    mock_dp.available = True
    mock_dp.enabled_default = True
    mock_dp.is_valid = True
    mock_dp.additional_information = {}
    mock_dp.is_in_multiple_channels = False
    mock_dp.name_data = MagicMock()
    mock_dp.name_data.parameter_name = None

    # Device mock
    mock_device = MagicMock()
    mock_device.configure_mock(name=device_name)
    mock_device.identifier = _BACKEND_IDENTIFIER
    mock_device.manufacturer = "eQ-3"
    mock_device.model = "HmIP-PSM"
    mock_device.model_description = "Pluggable Switch and Meter"
    mock_device.address = _DEVICE_ADDRESS
    mock_device.interface = _DEVICE_INTERFACE
    mock_device.firmware = "1.0.0"
    mock_device.room = "Living Room"
    mock_device.interface_id = "test_interface"
    mock_device.has_sub_devices = False

    mock_central_info = MagicMock()
    mock_central_info.configure_mock(name=_CENTRAL_NAME)
    mock_device.central_info = mock_central_info

    mock_config = MagicMock()
    mock_config.locale = "de"
    mock_device.config_provider.config = mock_config

    mock_dp.device = mock_device

    mock_channel = MagicMock()
    mock_channel.address = "ABC1234567:1"
    mock_channel.is_in_multi_group = False
    mock_dp.channel = mock_channel

    return mock_dp


def _put_in_channel_group(mock_dp: MagicMock, *, group_no: int, group_name: str, room: str | None = None) -> None:
    """Place the data point's channel in a multi-channel group led by a master with the given name."""
    mock_dp.device.has_sub_devices = True
    mock_dp.channel.is_in_multi_group = True
    master = MagicMock()
    master.configure_mock(name=group_name)
    master.group_no = group_no
    master.room = room
    mock_dp.channel.group_master = master


def _create_mock_control_unit(*, enable_sub_devices: bool = False) -> MagicMock:
    """Create a mock control unit."""
    mock_cu = MagicMock(spec=ControlUnit)
    mock_cu.enable_sub_devices = enable_sub_devices
    mock_cu.disable_config_panel = True
    mock_cu.ensure_central_device_exists.return_value = _CENTRAL_DEVICE_ID
    mock_cu.ensure_parent_device_exists.return_value = _PARENT_DEVICE_ID
    # Mirror the real method rather than returning a fixed string, so these
    # tests keep exercising which identifier the entity asks for.
    mock_cu.device_identifier.side_effect = lambda *, device: (
        get_device_identifier(instance_name=_CENTRAL_NAME, address=device.address, interface=device.interface)
        or device.identifier
    )
    return mock_cu


def _create_entity(
    *,
    mock_dp: MagicMock,
    mock_cu: MagicMock,
) -> AioHomematicGenericEntity:
    """Create an AioHomematicGenericEntity with patched get_data_point."""
    with patch(
        "custom_components.homematicip_local.generic_entity.get_data_point",
        side_effect=lambda data_point: data_point,
    ):
        return AioHomematicGenericEntity(
            control_unit=mock_cu,
            data_point=mock_dp,
        )


class TestHaDeviceName:
    """Tests for _ha_device_name property."""

    def test_channel_group_name_is_plain_when_sub_devices_disabled(self) -> None:
        """Without sub devices every channel stays on the device, so the device name stands."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SWITCH, device_name="HmIP-BSL Test")
        _put_in_channel_group(mock_dp, group_no=2, group_name="Küche Licht")
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        assert entity._ha_device_name == "HmIP-BSL Test"

    def test_named_channel_group_uses_the_group_name(self) -> None:
        """A group whose master carries a user-given name is named after it, without the device prefix."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SWITCH, device_name="HmIP-BSL Test")
        _put_in_channel_group(mock_dp, group_no=2, group_name="Küche Licht")
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        assert entity._ha_device_name == "Küche Licht"

    def test_non_schedule_device_name(self) -> None:
        """Test that non-schedule device name is just the device name."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SWITCH,
            device_name="HmIP-PSM Test",
        )
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        assert entity._ha_device_name == "HmIP-PSM Test"

    def test_non_schedule_device_name_sub_devices_disabled(self) -> None:
        """Test that device name is plain when sub devices are disabled."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SCHEDULE_SWITCH,
            device_name="HmIP-PSM Test",
        )
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        # Without sub devices, schedule entities are on the main device
        assert entity._ha_device_name == "HmIP-PSM Test"

    def test_schedule_device_name_fallback_to_schedule(self) -> None:
        """Test that schedule device name falls back to 'Schedule' when no translation."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SCHEDULE_SWITCH,
            device_name="HmIP-PSM Test",
        )
        # Use a locale that has no translation
        mock_dp.device.config_provider.config.locale = "xx"
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        # A child device carries its own name only; HA prepends the parent's.
        assert entity._ha_device_name == "Schedule"

    def test_schedule_device_name_uses_translation(self) -> None:
        """Test that schedule device name uses CCU translation when available."""
        mock_dp = _create_mock_data_point(
            category=DataPointCategory.SCHEDULE_SWITCH,
            device_name="HmIP-PSM Test",
        )
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)

        with patch(
            "custom_components.homematicip_local.generic_entity.ccu_translations.get_parameter_translation",
            return_value="Zeitplan",
        ) as mock_translation:
            entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        mock_translation.assert_called_once_with(
            parameter="SCHEDULE_CHANNEL_SWITCH",
            locale="de",
        )
        assert entity._ha_device_name == "Zeitplan"

    @pytest.mark.parametrize(
        "category",
        [
            DataPointCategory.SCHEDULE_SWITCH,
            DataPointCategory.WEEK_PROFILE,
        ],
    )
    def test_schedule_device_name_with_sub_devices_enabled(
        self,
        category: DataPointCategory,
    ) -> None:
        """Test that schedule device name contains 'Schedule' when sub devices are enabled."""
        mock_dp = _create_mock_data_point(category=category, device_name="HmIP-PSM Test")
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        assert entity._ha_device_name in ("Schedule", "Zeitplan")
        assert "HmIP-PSM Test" not in entity._ha_device_name

    @pytest.mark.parametrize(
        ("locale", "group_name", "expected"),
        [
            ("de", "4", "Gruppe 4"),
            ("en", "4", "Group 4"),
            ("de-DE", "4", "Gruppe 4"),
            ("xx", "4", "Group 4"),
            # No name at all: the group number stands in.
            ("de", "", "Gruppe 2"),
        ],
    )
    def test_unnamed_channel_group_is_labelled_by_locale(self, locale: str, group_name: str, expected: str) -> None:
        """An unnamed group (CCU names it by its channel number) gets a localized label instead of the device prefix."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SWITCH, device_name="HmIP-BSL Test")
        mock_dp.device.config_provider.config.locale = locale
        _put_in_channel_group(mock_dp, group_no=2, group_name=group_name)
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        assert entity._ha_device_name == expected


class TestChildDeviceInfo:
    """Tests for the device info an entity lands on: the device itself or a child of it."""

    def test_channel_group_becomes_a_child_of_the_device(self) -> None:
        """A grouped channel lands on a child device: parent id, own name, the group's room, no hardware data."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SWITCH, device_name="HmIP-BSL Test")
        _put_in_channel_group(mock_dp, group_no=2, group_name="Küche Licht", room="Küche")
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        assert device_info["identifiers"] == {(DOMAIN, f"{_DEVICE_IDENTIFIER}-2")}
        assert device_info["parent_device_id"] == _PARENT_DEVICE_ID
        assert device_info["name"] == "Küche Licht"
        assert device_info["suggested_area"] == "Küche"
        assert "manufacturer" not in device_info
        assert "via_device_id" not in device_info
        # The parent is registered with the full device info of the device itself.
        parent_info = mock_cu.ensure_parent_device_exists.call_args.kwargs["device_info"]
        assert parent_info["identifiers"] == {(DOMAIN, _DEVICE_IDENTIFIER)}
        assert parent_info["name"] == "HmIP-BSL Test"
        assert parent_info["model"] == "HmIP-PSM"
        assert parent_info["suggested_area"] == "Living Room"
        assert parent_info["via_device_id"] == _CENTRAL_DEVICE_ID

    def test_channel_group_without_a_room_inherits_the_parent_area(self) -> None:
        """A group without its own room passes no area, so HA resolves the parent's."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SWITCH)
        _put_in_channel_group(mock_dp, group_no=2, group_name="Küche Licht", room=None)
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        assert device_info["suggested_area"] is None

    def test_multi_group_channel_without_group_master_stays_on_the_device(self) -> None:
        """Test that a group-master-less channel does not split off a child device."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SWITCH)
        mock_dp.device.has_sub_devices = True
        mock_dp.channel.is_in_multi_group = True
        mock_dp.channel.group_master = None
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        # Without a group master there is no child to split off, so the entity
        # stays on the device — which hangs off the central.
        assert device_info["identifiers"] == {(DOMAIN, _DEVICE_IDENTIFIER)}
        assert "parent_device_id" not in device_info
        assert device_info["via_device_id"] == _CENTRAL_DEVICE_ID
        mock_cu.ensure_parent_device_exists.assert_not_called()

    def test_non_schedule_no_subdevice(self) -> None:
        """Test that non-schedule entities land on the device, which hangs off the central."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SWITCH)
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        assert device_info["identifiers"] == {(DOMAIN, _DEVICE_IDENTIFIER)}
        assert device_info["name"] == "HmIP-PSM Test"
        assert device_info["manufacturer"] == "eQ-3"
        assert device_info["serial_number"] == _DEVICE_ADDRESS
        assert device_info["via_device_id"] == _CENTRAL_DEVICE_ID
        mock_cu.ensure_parent_device_exists.assert_not_called()

    @pytest.mark.parametrize(
        "category",
        [
            DataPointCategory.SCHEDULE_SWITCH,
            DataPointCategory.WEEK_PROFILE,
        ],
    )
    def test_schedule_creates_subdevice_when_sub_devices_enabled(
        self,
        category: DataPointCategory,
    ) -> None:
        """Test that a schedule child device is created below the device when sub devices are enabled."""
        mock_dp = _create_mock_data_point(category=category)
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        assert device_info["identifiers"] == {(DOMAIN, f"{_DEVICE_IDENTIFIER}-schedule")}
        assert device_info["parent_device_id"] == _PARENT_DEVICE_ID
        assert device_info["name"] == "Zeitplan"
        assert "via_device_id" not in device_info
        parent_info = mock_cu.ensure_parent_device_exists.call_args.kwargs["device_info"]
        assert parent_info["identifiers"] == {(DOMAIN, _DEVICE_IDENTIFIER)}

    @pytest.mark.parametrize(
        "category",
        [
            DataPointCategory.SCHEDULE_SWITCH,
            DataPointCategory.WEEK_PROFILE,
        ],
    )
    def test_schedule_no_subdevice_when_sub_devices_disabled(
        self,
        category: DataPointCategory,
    ) -> None:
        """Test that no separate schedule sub-device is created when sub devices are disabled."""
        mock_dp = _create_mock_data_point(category=category)
        mock_cu = _create_mock_control_unit(enable_sub_devices=False)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        # Entity stays on main device, not a separate schedule child device
        assert device_info["identifiers"] == {(DOMAIN, _DEVICE_IDENTIFIER)}
        assert device_info["via_device_id"] == _CENTRAL_DEVICE_ID
        mock_cu.ensure_parent_device_exists.assert_not_called()

    def test_schedule_wins_over_a_channel_group(self) -> None:
        """A schedule data point on a grouped channel lands on the schedule child, as before."""
        mock_dp = _create_mock_data_point(category=DataPointCategory.SCHEDULE_SWITCH)
        _put_in_channel_group(mock_dp, group_no=2, group_name="Küche Licht", room="Küche")
        mock_cu = _create_mock_control_unit(enable_sub_devices=True)
        entity = _create_entity(mock_dp=mock_dp, mock_cu=mock_cu)

        device_info = entity._attr_device_info
        assert device_info is not None
        assert device_info["identifiers"] == {(DOMAIN, f"{_DEVICE_IDENTIFIER}-schedule")}
        assert device_info["name"] == "Zeitplan"
        assert device_info["suggested_area"] is None


def _create_mock_hub_data_point(
    *,
    name: str = "alarm_messages",
    resolved_name: str | None = None,
) -> MagicMock:
    """Create a mock hub data point (no channel, no device-scoped naming)."""
    mock_dp = MagicMock()
    mock_dp.category = DataPointCategory.HUB_SENSOR
    mock_dp.unique_id = "loom_abc1234567_hub_alarm-messages"
    mock_dp.configure_mock(name=name)
    mock_dp.available = True
    mock_dp.enabled_default = True
    mock_dp.is_valid = True
    mock_dp.channel = None
    # A mock answers every attribute, so an unset resolved_name has to be
    # spelled out — otherwise the test cannot distinguish "the backend
    # resolved a name" from "the backend has no such attribute at all".
    mock_dp.resolved_name = resolved_name
    return mock_dp


def _create_hub_entity(*, mock_dp: MagicMock) -> AioHomematicGenericHubEntity:
    """Create a hub entity with patched get_data_point + entity-description lookup."""
    mock_cu = _create_mock_control_unit()
    mock_central = MagicMock()
    mock_central.event_bus.create_subscription_group.return_value = MagicMock()
    mock_cu.central = mock_central
    with (
        patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=lambda data_point: data_point,
        ),
        patch(
            "custom_components.homematicip_local.generic_entity.get_entity_description",
            return_value=None,
        ),
        patch.object(AioHomematicGenericHubEntity, "_get_device_info", return_value={}),
    ):
        return AioHomematicGenericHubEntity(control_unit=mock_cu, data_point=mock_dp)


class TestHubEntityNameFromBackend:
    """
    A backend that resolves its own entity names is rendered verbatim.

    openccu-loom is the naming authority for its own hub entities and
    hands the localized name over the wire. Rendering it here is what
    keeps the same words from living in this integration and in the
    daemon's catalogue at once, drifting apart on the first edit to
    either.
    """

    def test_an_empty_resolved_name_does_not_blank_the_entity(self) -> None:
        mock_dp = _create_mock_hub_data_point(name="alarm_messages", resolved_name="")
        entity = _create_hub_entity(mock_dp=mock_dp)

        assert entity.name == "alarm messages"

    def test_resolved_name_wins(self) -> None:
        mock_dp = _create_mock_hub_data_point(name="alarm_messages", resolved_name="Alarmmeldungen")
        entity = _create_hub_entity(mock_dp=mock_dp)

        assert entity.name == "Alarmmeldungen"

    def test_the_token_is_untouched_so_descriptions_still_match(self) -> None:
        """
        The data point keeps its English token in `name`.

        The entity-description lookup matches on it (`var_name_contains`),
        and a localized token there would cost the entity its icon, device
        class and category.
        """
        mock_dp = _create_mock_hub_data_point(name="alarm_messages", resolved_name="Alarmmeldungen")
        _create_hub_entity(mock_dp=mock_dp)

        assert mock_dp.name == "alarm_messages"

    def test_without_a_resolved_name_the_previous_behaviour_stands(self) -> None:
        """Aiohomematic data points carry no such attribute; nothing may change for them."""
        mock_dp = _create_mock_hub_data_point(name="alarm_messages", resolved_name=None)
        entity = _create_hub_entity(mock_dp=mock_dp)

        assert entity.name == "alarm messages"
