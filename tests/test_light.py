"""Tests for light entities of homematicip_local."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from custom_components.homematicip_local.light import (
    ATTR_CHANNEL_BRIGHTNESS,
    ATTR_CHANNEL_COLOR,
    ATTR_COLOR,
    AioHomematicLight,
    async_setup_entry,
)
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_MODE,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    ATTR_TRANSITION,
)
from homeassistant.components.light.const import ColorMode, LightEntityFeature
from homeassistant.const import STATE_OFF, STATE_ON, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant


class MockRestoredState:
    """Mock restored state."""

    def __init__(self, state: str | None = STATE_ON, attributes: dict[str, Any] | None = None) -> None:
        """Initialize mock restored state."""
        self.state = state
        self.attributes = attributes or {}


def create_mock_light(
    *,
    is_valid: bool = True,
    brightness: int | None = 255,
    is_on: bool = True,
    color_temp_kelvin: int | None = 4000,
    hs_color: tuple[float, float] | None = (120.0, 50.0),
    effect: str | None = None,
    effects: set[str] | None = None,
    group_brightness: int | None = None,
    supports_hs_color: bool = False,
    supports_color_temperature: bool = False,
    supports_brightness: bool = True,
    supports_effects: bool = False,
    is_restored: bool = False,
    restored_state: MockRestoredState | None = None,
    is_fixed_color_light: bool = False,
    color_name: str | None = None,
    channel_color_name: str | None = None,
) -> AioHomematicLight:
    """Create a mock light entity with patched initialization."""
    # Create mock data point
    mock_data_point = MagicMock()
    mock_data_point.is_valid = is_valid
    mock_data_point.brightness = brightness
    mock_data_point.is_on = is_on
    mock_data_point.color_temp_kelvin = color_temp_kelvin
    mock_data_point.hs_color = hs_color
    mock_data_point.effect = effect
    mock_data_point.effects = effects
    mock_data_point.group_brightness = group_brightness
    mock_data_point.supports_hs_color = supports_hs_color
    mock_data_point.supports_color_temperature = supports_color_temperature
    mock_data_point.supports_brightness = supports_brightness
    mock_data_point.supports_effects = supports_effects
    mock_data_point.turn_on = AsyncMock()
    mock_data_point.turn_off = AsyncMock()
    mock_data_point.set_timer_on_time = Mock()

    # For CustomDpIpFixedColorLight support
    if is_fixed_color_light:
        mock_data_point.color_name = color_name
        mock_data_point.channel_color_name = channel_color_name

    # Create light instance bypassing __init__
    light = object.__new__(AioHomematicLight)
    light._data_point = mock_data_point
    light._cu = MagicMock()
    light._is_restored = is_restored
    light._restored_state = restored_state
    light._attr_unique_id = "test_unique_id"
    light._attr_device_info = {}
    light._static_state_attributes = {}
    light._unsubscribe_callbacks = []

    return light


class TestAioHomematicLightBrightness:
    """Tests for brightness property."""

    def test_brightness_invalid_no_restored_state(self) -> None:
        """Test brightness when data point is invalid and no restored state."""
        light = create_mock_light(is_valid=False, is_restored=False)
        assert light.brightness is None

    def test_brightness_invalid_with_restored_state(self) -> None:
        """Test brightness when data point is invalid but restored state exists."""
        restored = MockRestoredState(attributes={ATTR_BRIGHTNESS: 200})
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.brightness == 200

    def test_brightness_valid(self) -> None:
        """Test brightness when data point is valid."""
        light = create_mock_light(is_valid=True, brightness=128)
        assert light.brightness == 128


class TestAioHomematicLightColorMode:
    """Tests for color_mode property."""

    def test_color_mode_brightness(self) -> None:
        """Test color mode when only brightness is supported."""
        light = create_mock_light(
            is_valid=True, supports_hs_color=False, supports_color_temperature=False, supports_brightness=True
        )
        assert light.color_mode == ColorMode.BRIGHTNESS

    def test_color_mode_color_temp(self) -> None:
        """Test color mode when color temp is supported."""
        light = create_mock_light(is_valid=True, supports_hs_color=False, supports_color_temperature=True)
        assert light.color_mode == ColorMode.COLOR_TEMP

    def test_color_mode_hs(self) -> None:
        """Test color mode when HS color is supported."""
        light = create_mock_light(is_valid=True, supports_hs_color=True)
        assert light.color_mode == ColorMode.HS

    def test_color_mode_invalid_with_restored_state(self) -> None:
        """Test color mode when invalid but restored state exists."""
        restored = MockRestoredState(attributes={ATTR_COLOR_MODE: ColorMode.HS})
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.color_mode == ColorMode.HS

    def test_color_mode_onoff_fallback(self) -> None:
        """Test color mode fallback to ONOFF."""
        light = create_mock_light(
            is_valid=False,
            supports_hs_color=False,
            supports_color_temperature=False,
            supports_brightness=False,
            is_restored=False,
        )
        assert light.color_mode == ColorMode.ONOFF

    def test_color_mode_valid_no_features(self) -> None:
        """Test color mode with valid data point but no color features."""
        light = create_mock_light(
            is_valid=True,
            supports_hs_color=False,
            supports_color_temperature=False,
            supports_brightness=False,
        )
        # When valid but no features supported, it falls through to ONOFF
        assert light.color_mode == ColorMode.ONOFF


class TestAioHomematicLightColorTempKelvin:
    """Tests for color_temp_kelvin property."""

    def test_color_temp_kelvin_invalid_no_restored(self) -> None:
        """Test color temp when invalid and no restored state."""
        light = create_mock_light(is_valid=False, is_restored=False)
        assert light.color_temp_kelvin is None

    def test_color_temp_kelvin_invalid_with_restored(self) -> None:
        """Test color temp when invalid but restored state exists."""
        restored = MockRestoredState(attributes={ATTR_COLOR_TEMP_KELVIN: 6000})
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.color_temp_kelvin == 6000

    def test_color_temp_kelvin_valid(self) -> None:
        """Test color temp when data point is valid."""
        light = create_mock_light(is_valid=True, color_temp_kelvin=5000)
        assert light.color_temp_kelvin == 5000


class TestAioHomematicLightEffect:
    """Tests for effect property."""

    def test_effect(self) -> None:
        """Test effect property."""
        light = create_mock_light(effect="Rainbow")
        assert light.effect == "Rainbow"

    def test_effect_none(self) -> None:
        """Test effect property when no effect."""
        light = create_mock_light(effect=None)
        assert light.effect is None


class TestAioHomematicLightEffectList:
    """Tests for effect_list property."""

    def test_effect_list_empty_effects(self) -> None:
        """Test effect list when effects is empty set."""
        light = create_mock_light(effects=set())
        assert light.effect_list is None

    def test_effect_list_no_effects(self) -> None:
        """Test effect list when no effects."""
        light = create_mock_light(effects=None)
        assert light.effect_list is None

    def test_effect_list_with_effects(self) -> None:
        """Test effect list when effects exist."""
        light = create_mock_light(effects={"Rainbow", "Strobe", "Fade"})
        assert set(light.effect_list) == {"Rainbow", "Strobe", "Fade"}


class TestAioHomematicLightExtraStateAttributes:
    """Tests for extra_state_attributes property."""

    def test_extra_state_attributes_fixed_color_light(self) -> None:
        """Test extra state attributes for fixed color light."""
        # Need to mock isinstance check for CustomDpIpFixedColorLight
        light = create_mock_light(
            is_fixed_color_light=True,
            color_name="RED",
            channel_color_name="BLUE",
        )
        # Patch isinstance to return True for CustomDpIpFixedColorLight
        with patch(
            "custom_components.homematicip_local.light.isinstance",
            side_effect=lambda obj, cls: cls.__name__ == "CustomDpIpFixedColorLight",
        ):
            attrs = light.extra_state_attributes
            assert ATTR_COLOR in attrs
            assert attrs[ATTR_COLOR] == "RED"
            assert ATTR_CHANNEL_COLOR in attrs
            assert attrs[ATTR_CHANNEL_COLOR] == "BLUE"

    def test_extra_state_attributes_fixed_color_light_same_color(self) -> None:
        """Test extra state attributes for fixed color light when colors are same."""
        light = create_mock_light(
            is_fixed_color_light=True,
            color_name="RED",
            channel_color_name="RED",
        )
        with patch(
            "custom_components.homematicip_local.light.isinstance",
            side_effect=lambda obj, cls: cls.__name__ == "CustomDpIpFixedColorLight",
        ):
            attrs = light.extra_state_attributes
            assert ATTR_COLOR in attrs
            assert ATTR_CHANNEL_COLOR not in attrs

    def test_extra_state_attributes_no_group_brightness(self) -> None:
        """Test extra state attributes without group brightness."""
        light = create_mock_light(group_brightness=None)
        attrs = light.extra_state_attributes
        assert ATTR_CHANNEL_BRIGHTNESS not in attrs

    def test_extra_state_attributes_with_group_brightness(self) -> None:
        """Test extra state attributes with group brightness."""
        light = create_mock_light(group_brightness=150)
        attrs = light.extra_state_attributes
        assert ATTR_CHANNEL_BRIGHTNESS in attrs
        assert attrs[ATTR_CHANNEL_BRIGHTNESS] == 150


class TestAioHomematicLightHsColor:
    """Tests for hs_color property."""

    def test_hs_color_invalid_no_restored(self) -> None:
        """Test hs_color when invalid and no restored state."""
        light = create_mock_light(is_valid=False, is_restored=False)
        assert light.hs_color is None

    def test_hs_color_invalid_with_restored(self) -> None:
        """Test hs_color when invalid but restored state exists."""
        restored = MockRestoredState(attributes={ATTR_HS_COLOR: (90.0, 50.0)})
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.hs_color == (90.0, 50.0)

    def test_hs_color_valid(self) -> None:
        """Test hs_color when data point is valid."""
        light = create_mock_light(is_valid=True, hs_color=(180.0, 75.0))
        assert light.hs_color == (180.0, 75.0)


class TestAioHomematicLightIsOn:
    """Tests for is_on property."""

    def test_is_on_false(self) -> None:
        """Test is_on when light is off."""
        light = create_mock_light(is_valid=True, is_on=False)
        assert light.is_on is False

    def test_is_on_invalid_no_restored(self) -> None:
        """Test is_on when invalid and no restored state."""
        light = create_mock_light(is_valid=False, is_restored=False)
        assert light.is_on is None

    def test_is_on_invalid_restored_unavailable(self) -> None:
        """Test is_on when restored state is unavailable."""
        restored = MockRestoredState(state=STATE_UNAVAILABLE)
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.is_on is None

    def test_is_on_invalid_restored_unknown(self) -> None:
        """Test is_on when restored state is unknown."""
        restored = MockRestoredState(state=STATE_UNKNOWN)
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.is_on is None

    def test_is_on_invalid_with_restored_off(self) -> None:
        """Test is_on when invalid but restored state is off."""
        restored = MockRestoredState(state=STATE_OFF)
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.is_on is False

    def test_is_on_invalid_with_restored_on(self) -> None:
        """Test is_on when invalid but restored state is on."""
        restored = MockRestoredState(state=STATE_ON)
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.is_on is True

    def test_is_on_restored_no_state(self) -> None:
        """Test is_on when restored but no restored state object."""
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=None)
        assert light.is_on is None

    def test_is_on_true(self) -> None:
        """Test is_on when light is on."""
        light = create_mock_light(is_valid=True, is_on=True)
        assert light.is_on is True

    def test_is_on_valid_but_none(self) -> None:
        """Test is_on when valid but is_on is None."""
        light = create_mock_light(is_valid=True)
        light._data_point.is_on = None
        # is_on returns True only if is_on is True, not truthy
        assert light.is_on is False


class TestAioHomematicLightSupportedColorModes:
    """Tests for supported_color_modes property."""

    def test_supported_color_modes_both_hs_and_temp(self) -> None:
        """Test supported color modes with both HS and color temp."""
        light = create_mock_light(supports_hs_color=True, supports_color_temperature=True)
        assert ColorMode.HS in light.supported_color_modes
        assert ColorMode.COLOR_TEMP in light.supported_color_modes

    def test_supported_color_modes_brightness_only(self) -> None:
        """Test supported color modes with brightness only."""
        light = create_mock_light(supports_hs_color=False, supports_color_temperature=False, supports_brightness=True)
        assert ColorMode.BRIGHTNESS in light.supported_color_modes
        assert ColorMode.HS not in light.supported_color_modes
        assert ColorMode.COLOR_TEMP not in light.supported_color_modes

    def test_supported_color_modes_color_temp(self) -> None:
        """Test supported color modes with color temp."""
        light = create_mock_light(supports_color_temperature=True)
        assert ColorMode.COLOR_TEMP in light.supported_color_modes

    def test_supported_color_modes_hs(self) -> None:
        """Test supported color modes with HS."""
        light = create_mock_light(supports_hs_color=True)
        assert ColorMode.HS in light.supported_color_modes

    def test_supported_color_modes_onoff_only(self) -> None:
        """Test supported color modes with ONOFF only."""
        light = create_mock_light(supports_hs_color=False, supports_color_temperature=False, supports_brightness=False)
        assert ColorMode.ONOFF in light.supported_color_modes


class TestAioHomematicLightSupportedFeatures:
    """Tests for supported_features property."""

    def test_supported_features_transition(self) -> None:
        """Test supported features always includes transition."""
        light = create_mock_light(supports_effects=False)
        assert light.supported_features & LightEntityFeature.TRANSITION

    def test_supported_features_with_effects(self) -> None:
        """Test supported features with effects."""
        light = create_mock_light(supports_effects=True)
        assert light.supported_features & LightEntityFeature.EFFECT
        assert light.supported_features & LightEntityFeature.TRANSITION


class TestAioHomematicLightSetOnTime:
    """Tests for async_set_on_time method."""

    def test_set_on_time(self) -> None:
        """Test set_on_time method."""
        light = create_mock_light()
        light.async_set_on_time(on_time=60.0)
        light._data_point.set_timer_on_time.assert_called_once_with(on_time=60.0)

    def test_set_on_time_zero(self) -> None:
        """Test set_on_time with zero."""
        light = create_mock_light()
        light.async_set_on_time(on_time=0.0)
        light._data_point.set_timer_on_time.assert_called_once_with(on_time=0.0)


class TestAioHomematicLightTurnOff:
    """Tests for async_turn_off method."""

    @pytest.mark.asyncio
    async def test_turn_off_no_transition(self) -> None:
        """Test turn off without transition."""
        light = create_mock_light()
        await light.async_turn_off()
        light._data_point.turn_off.assert_called_once()
        call_kwargs = light._data_point.turn_off.call_args[1]
        # ramp_time should not be in kwargs when transition is 0
        assert "ramp_time" not in call_kwargs

    @pytest.mark.asyncio
    async def test_turn_off_with_transition(self) -> None:
        """Test turn off with transition."""
        light = create_mock_light()
        await light.async_turn_off(**{ATTR_TRANSITION: 5})
        light._data_point.turn_off.assert_called_once()
        call_kwargs = light._data_point.turn_off.call_args[1]
        assert "ramp_time" in call_kwargs
        assert call_kwargs["ramp_time"] == 5

    @pytest.mark.asyncio
    async def test_turn_off_with_zero_transition(self) -> None:
        """Test turn off with explicit zero transition."""
        light = create_mock_light()
        await light.async_turn_off(**{ATTR_TRANSITION: 0})
        light._data_point.turn_off.assert_called_once()
        call_kwargs = light._data_point.turn_off.call_args[1]
        # ramp_time should not be in kwargs when transition is 0
        assert "ramp_time" not in call_kwargs


class TestAioHomematicLightTurnOn:
    """Tests for async_turn_on method."""

    @pytest.mark.asyncio
    async def test_turn_on_all_kwargs(self) -> None:
        """Test turn on with all kwargs."""
        light = create_mock_light(color_temp_kelvin=None, hs_color=None, brightness=None)
        await light.async_turn_on(
            **{
                ATTR_BRIGHTNESS: 200,
                ATTR_COLOR_TEMP_KELVIN: 4500,
                ATTR_HS_COLOR: (240.0, 100.0),
                ATTR_TRANSITION: 2,
                ATTR_EFFECT: "Strobe",
            }
        )
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("brightness") == 200
        assert call_kwargs.get("color_temp_kelvin") == 4500
        assert call_kwargs.get("hs_color") == (240.0, 100.0)
        assert call_kwargs.get("ramp_time") == 2
        assert call_kwargs.get("effect") == "Strobe"

    @pytest.mark.asyncio
    async def test_turn_on_basic(self) -> None:
        """Test basic turn on."""
        light = create_mock_light()
        await light.async_turn_on()
        light._data_point.turn_on.assert_called_once()

    @pytest.mark.asyncio
    async def test_turn_on_defaults_brightness_to_255(self) -> None:
        """Test turn on defaults brightness to 255 when None."""
        light = create_mock_light(is_valid=True, brightness=None)
        # Need to also set up is_restored=False to ensure brightness returns None
        light._is_restored = False
        await light.async_turn_on()
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("brightness") == 255

    @pytest.mark.asyncio
    async def test_turn_on_uses_current_brightness(self) -> None:
        """Test turn on uses current brightness if not provided."""
        light = create_mock_light(is_valid=True, brightness=100)
        await light.async_turn_on()
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("brightness") == 100

    @pytest.mark.asyncio
    async def test_turn_on_uses_current_color_temp(self) -> None:
        """Test turn on uses current color temp if not provided."""
        light = create_mock_light(is_valid=True, color_temp_kelvin=3500)
        await light.async_turn_on()
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("color_temp_kelvin") == 3500

    @pytest.mark.asyncio
    async def test_turn_on_uses_current_hs_color(self) -> None:
        """Test turn on uses current hs_color if not provided."""
        light = create_mock_light(is_valid=True, hs_color=(240.0, 75.0))
        await light.async_turn_on()
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("hs_color") == (240.0, 75.0)

    @pytest.mark.asyncio
    async def test_turn_on_with_brightness(self) -> None:
        """Test turn on with brightness."""
        light = create_mock_light()
        await light.async_turn_on(**{ATTR_BRIGHTNESS: 128})
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("brightness") == 128

    @pytest.mark.asyncio
    async def test_turn_on_with_color_temp(self) -> None:
        """Test turn on with color temperature."""
        light = create_mock_light(color_temp_kelvin=None)
        await light.async_turn_on(**{ATTR_COLOR_TEMP_KELVIN: 5000})
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("color_temp_kelvin") == 5000

    @pytest.mark.asyncio
    async def test_turn_on_with_effect(self) -> None:
        """Test turn on with effect."""
        light = create_mock_light()
        await light.async_turn_on(**{ATTR_EFFECT: "Rainbow"})
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("effect") == "Rainbow"

    @pytest.mark.asyncio
    async def test_turn_on_with_hs_color(self) -> None:
        """Test turn on with HS color."""
        light = create_mock_light(hs_color=None)
        await light.async_turn_on(**{ATTR_HS_COLOR: (180.0, 50.0)})
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("hs_color") == (180.0, 50.0)

    @pytest.mark.asyncio
    async def test_turn_on_with_transition(self) -> None:
        """Test turn on with transition."""
        light = create_mock_light()
        await light.async_turn_on(**{ATTR_TRANSITION: 3})
        light._data_point.turn_on.assert_called_once()
        call_kwargs = light._data_point.turn_on.call_args[1]
        assert call_kwargs.get("ramp_time") == 3


class TestAsyncSetupEntry:
    """Tests for async_setup_entry function."""

    @pytest.mark.asyncio
    async def test_async_setup_entry(self, hass: HomeAssistant) -> None:
        """Test async_setup_entry sets up the platform."""
        mock_control_unit = MagicMock()
        mock_control_unit.get_new_data_points.return_value = ()

        mock_entry = MagicMock()
        mock_entry.runtime_data = mock_control_unit
        mock_entry.entry_id = "test_entry_id"
        mock_entry.async_on_unload = MagicMock()

        mock_async_add_entities = MagicMock()

        with patch("custom_components.homematicip_local.light.async_dispatcher_connect") as mock_dispatcher:
            await async_setup_entry(hass, mock_entry, mock_async_add_entities)

        mock_dispatcher.assert_called_once()
        mock_entry.async_on_unload.assert_called_once()
        mock_control_unit.get_new_data_points.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_setup_entry_with_data_points(self, hass: HomeAssistant) -> None:
        """Test async_setup_entry with existing data points."""
        mock_data_point = MagicMock()
        mock_data_point.category = "LIGHT"

        mock_control_unit = MagicMock()
        mock_control_unit.get_new_data_points.return_value = (mock_data_point,)

        mock_entry = MagicMock()
        mock_entry.runtime_data = mock_control_unit
        mock_entry.entry_id = "test_entry_id"
        mock_entry.async_on_unload = MagicMock()

        added_entities: list = []

        def capture_entities(entities: list) -> None:
            added_entities.extend(entities)

        mock_async_add_entities = MagicMock(side_effect=capture_entities)

        with (
            patch("custom_components.homematicip_local.light.async_dispatcher_connect"),
            patch("custom_components.homematicip_local.light.AioHomematicLight") as mock_light_class,
        ):
            mock_light_instance = MagicMock()
            mock_light_class.return_value = mock_light_instance

            await async_setup_entry(hass, mock_entry, mock_async_add_entities)

        mock_async_add_entities.assert_called_once()
        # Verify entities were passed
        call_args = mock_async_add_entities.call_args[0][0]
        assert len(call_args) == 1


class TestAioHomematicLightMinMaxColorTemp:
    """Tests for color temperature limits."""

    def test_max_color_temp_kelvin(self) -> None:
        """Test maximum color temperature attribute."""
        light = create_mock_light()
        assert light._attr_max_color_temp_kelvin == 6500

    def test_min_color_temp_kelvin(self) -> None:
        """Test minimum color temperature attribute."""
        light = create_mock_light()
        assert light._attr_min_color_temp_kelvin == 2000


class TestAioHomematicLightIsRestored:
    """Tests for is_restored property behavior."""

    def test_is_restored_false_no_restored_state(self) -> None:
        """Test is_restored returns False when no restored state."""
        light = create_mock_light(is_valid=False, is_restored=False, restored_state=None)
        assert light.is_restored is False

    def test_is_restored_false_state_is_none(self) -> None:
        """Test is_restored returns False when restored state.state is None."""
        restored = MockRestoredState(state=None)
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.is_restored is False

    def test_is_restored_false_when_valid(self) -> None:
        """Test is_restored returns False when data point is valid."""
        restored = MockRestoredState(state=STATE_ON)
        light = create_mock_light(is_valid=True, is_restored=True, restored_state=restored)
        assert light.is_restored is False

    def test_is_restored_true(self) -> None:
        """Test is_restored returns True when conditions are met."""
        # is_restored = not is_valid and restored_state is not None and restored_state.state is not None
        restored = MockRestoredState(state=STATE_ON)
        light = create_mock_light(is_valid=False, is_restored=True, restored_state=restored)
        assert light.is_restored is True
