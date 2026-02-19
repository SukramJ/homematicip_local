"""Light platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

import logging
from typing import Any, Final, override

from aiohomematic.const import DataPointCategory
from aiohomematic.model.custom import (
    FIXED_COLOR_TO_HS_CONVERTER,
    CustomDpDimmer,
    CustomDpIpFixedColorLight,
    CustomDpSoundPlayerLed,
    LightOffArgs,
    LightOnArgs,
    SoundPlayerLedOnArgs,
)
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_MODE,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    ATTR_TRANSITION,
    LightEntity,
)
from homeassistant.components.light.const import ColorMode, LightEntityFeature
from homeassistant.const import STATE_ON, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HomematicConfigEntry
from .control_unit import ControlUnit, signal_new_data_point
from .generic_entity import AioHomematicGenericEntity, AioHomematicGenericRestoreEntity
from .services import ATTR_AVAILABLE_COLORS
from .support import handle_homematic_errors

ATTR_COLOR: Final = "color"
ATTR_CHANNEL_COLOR: Final = "channel_color"
ATTR_CHANNEL_BRIGHTNESS: Final = "channel_brightness"
ATTR_LAST_BRIGHTNESS: Final = "last_brightness"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU light platform."""
    control_unit: ControlUnit = entry.runtime_data

    @callback
    def async_add_light(data_points: tuple[CustomDpDimmer, ...]) -> None:
        """Add light from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_LIGHT: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicLight(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.LIGHT),
            target=async_add_light,
        )
    )

    async_add_light(data_points=control_unit.get_new_data_points(data_point_type=CustomDpDimmer))


class AioHomematicLight(AioHomematicGenericRestoreEntity[CustomDpDimmer], LightEntity):
    """Representation of the HomematicIP light entity."""

    _attr_min_color_temp_kelvin = 2000  # 500 Mireds
    _attr_max_color_temp_kelvin = 6500  # 153 Mireds

    __no_recored_attributes = AioHomematicGenericEntity.NO_RECORDED_ATTRIBUTES
    __no_recored_attributes.update(
        {ATTR_AVAILABLE_COLORS, ATTR_CHANNEL_BRIGHTNESS, ATTR_CHANNEL_COLOR, ATTR_COLOR, ATTR_LAST_BRIGHTNESS}
    )
    _unrecorded_attributes = frozenset(__no_recored_attributes)

    @property
    @override
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        if self._data_point.is_valid:
            return self._data_point.brightness
        if self.is_restored and self._restored_state:
            return self._restored_state.attributes.get(ATTR_BRIGHTNESS)
        return None

    @property
    @override
    def color_mode(self) -> ColorMode | None:
        """Return the color mode of the light."""
        if self._data_point.is_valid:
            if self._data_point.has_hs_color:
                return ColorMode.HS
            if self._data_point.has_color_temperature:
                return ColorMode.COLOR_TEMP
            if self._data_point.capabilities.brightness:
                return ColorMode.BRIGHTNESS
        if self.is_restored and self._restored_state:
            return self._restored_state.attributes.get(ATTR_COLOR_MODE)

        return ColorMode.ONOFF

    @property
    @override
    def color_temp_kelvin(self) -> int | None:
        """Return the color temperature in kelvin."""
        if self._data_point.is_valid:
            return self._data_point.color_temp_kelvin
        if self.is_restored and self._restored_state:
            return self._restored_state.attributes.get(ATTR_COLOR_TEMP_KELVIN)
        return None

    @property
    @override
    def effect(self) -> str | None:
        """Return the current effect."""
        return self._data_point.effect

    @property
    @override
    def effect_list(self) -> list[str] | None:
        """Return the list of supported effects."""
        return list(self._data_point.effects) if self._data_point.effects else None

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the generic entity."""
        attributes = super().extra_state_attributes
        if self._data_point.group_brightness is not None:
            attributes[ATTR_CHANNEL_BRIGHTNESS] = self._data_point.group_brightness

        if isinstance(self._data_point, CustomDpIpFixedColorLight):
            attributes[ATTR_COLOR] = self._data_point.color_name
            if (
                self._data_point.channel_color_name
                and self._data_point.color_name != self._data_point.channel_color_name
            ):
                attributes[ATTR_CHANNEL_COLOR] = self._data_point.channel_color_name

        if isinstance(self._data_point, CustomDpSoundPlayerLed):
            attributes[ATTR_AVAILABLE_COLORS] = self._data_point.available_colors
            attributes[ATTR_COLOR] = self._data_point.color_name

        if (last_brightness := self.last_brightness) is not None:
            attributes[ATTR_LAST_BRIGHTNESS] = last_brightness

        return attributes

    @property
    @override
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hue and saturation color value [float, float]."""
        if self._data_point.is_valid:
            return self._data_point.hs_color
        if self.is_restored and self._restored_state:
            return self._restored_state.attributes.get(ATTR_HS_COLOR)
        return None

    @property
    @override
    def is_on(self) -> bool | None:
        """Return true if dimmer is on."""
        if self._data_point.is_valid:
            return self._data_point.is_on is True
        if (
            self.is_restored
            and self._restored_state
            and (restored_state := self._restored_state.state)
            not in (
                STATE_UNKNOWN,
                STATE_UNAVAILABLE,
            )
        ):
            return restored_state == STATE_ON
        return None

    @property
    def last_brightness(self) -> int | None:
        """Return the last non-off brightness value (0-255)."""
        if (last_level := self._data_point.last_level) is not None and last_level > 0:
            return self._data_point.level_to_brightness(last_level)
        return None

    @property
    @override
    def supported_color_modes(self) -> set[ColorMode] | None:
        """Flag supported color modes."""
        supported_color_modes: set[ColorMode] = set()
        if self._data_point.has_hs_color:
            supported_color_modes.add(ColorMode.HS)
        if self._data_point.has_color_temperature:
            supported_color_modes.add(ColorMode.COLOR_TEMP)

        if len(supported_color_modes) == 0 and self._data_point.capabilities.brightness:
            supported_color_modes.add(ColorMode.BRIGHTNESS)
        if len(supported_color_modes) == 0:
            supported_color_modes.add(ColorMode.ONOFF)

        return supported_color_modes

    @property
    @override
    def supported_features(self) -> LightEntityFeature:
        """Return the list of supported features."""
        supported_features = LightEntityFeature.TRANSITION
        if self._data_point.has_effects:
            supported_features |= LightEntityFeature.EFFECT
        return supported_features

    @override
    async def async_added_to_hass(self) -> None:
        """Restore last_brightness from previous state."""
        await super().async_added_to_hass()

        # Restore last_non_default_value from HA state for persistence across restarts
        if (
            self._restored_state is not None
            and (stored := self._restored_state.attributes.get(ATTR_LAST_BRIGHTNESS)) is not None
            and self._data_point.last_level is None
        ):
            stored_level = self._data_point.brightness_to_level(int(stored))
            self._data_point.set_last_level(value=stored_level)

    @handle_homematic_errors
    async def async_set_led(
        self,
        *,
        color: str | None = None,
        brightness: int | None = None,
        on_time: float | None = None,
        ramp_time: float | None = None,
        repetitions: int | None = None,
        flash_time: int | None = None,
    ) -> None:
        """Set LED on HmIP-MP3P devices."""
        if not isinstance(self._data_point, CustomDpSoundPlayerLed):
            _LOGGER.warning(
                "set_led is only supported for HmIP-MP3P LED entities, not %s",
                type(self._data_point).__name__,
            )
            return

        kwargs: SoundPlayerLedOnArgs = {}
        if color is not None:
            # Convert fixed color name to hs_color tuple for aiohomematic
            hs_color = FIXED_COLOR_TO_HS_CONVERTER.get(color.upper())
            if hs_color is not None:
                kwargs["hs_color"] = hs_color
            else:
                _LOGGER.warning(
                    "Invalid color '%s'. Must be one of: %s",
                    color,
                    ", ".join(FIXED_COLOR_TO_HS_CONVERTER.keys()),
                )
        if brightness is not None:
            kwargs["brightness"] = brightness
        if on_time is not None:
            kwargs["on_time"] = on_time
        if ramp_time is not None:
            kwargs["ramp_time"] = ramp_time
        if repetitions is not None:
            kwargs["repetitions"] = repetitions
        if flash_time is not None:
            kwargs["flash_time"] = flash_time

        await self._data_point.turn_on(**kwargs)

    @callback
    def async_set_on_time(self, on_time: float) -> None:
        """Set the on time of the light."""
        self._data_point.set_timer_on_time(on_time=on_time)

    @override
    @handle_homematic_errors
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        hm_kwargs = LightOffArgs()
        # Use transition from kwargs, if not applicable use 0.
        if ramp_time := kwargs.get(ATTR_TRANSITION, 0):
            hm_kwargs["ramp_time"] = ramp_time
        await self._data_point.turn_off(**hm_kwargs)

    @override
    @handle_homematic_errors
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        hm_kwargs = LightOnArgs()
        # Use color_temp_kelvin from kwargs, if not applicable use current color_temp_kelvin.
        if color_temp_kelvin := kwargs.get(ATTR_COLOR_TEMP_KELVIN, self.color_temp_kelvin):
            hm_kwargs["color_temp_kelvin"] = color_temp_kelvin
        # Use hs_color from kwargs, if not applicable use current hs_color.
        if hs_color := kwargs.get(ATTR_HS_COLOR, self.hs_color):
            hm_kwargs["hs_color"] = hs_color
        # Use brightness from kwargs, with optional last_brightness fallback when light is off.
        brightness: int | None = kwargs.get(ATTR_BRIGHTNESS)
        if brightness is None:
            if self._data_point.is_on:
                brightness = self.brightness or 255
            elif self._cu.enable_light_last_brightness:
                brightness = self.last_brightness or self.brightness or 255
            else:
                brightness = self.brightness or 255
        hm_kwargs["brightness"] = brightness
        # Use transition from kwargs, if not applicable use 0.
        if ramp_time := kwargs.get(ATTR_TRANSITION, 0):
            hm_kwargs["ramp_time"] = ramp_time
        # Use effect from kwargs
        if effect := kwargs.get(ATTR_EFFECT):
            hm_kwargs["effect"] = effect

        await self._data_point.turn_on(**hm_kwargs)
