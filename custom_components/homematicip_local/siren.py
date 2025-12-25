"""Siren platform for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

import logging
from typing import Any

from aiohomematic.const import DataPointCategory
from aiohomematic.model.custom import BaseCustomDpSiren, CustomDpSoundPlayer, PlaySoundArgs, SirenOnArgs
from homeassistant.components.siren import SirenEntity
from homeassistant.components.siren.const import ATTR_DURATION, ATTR_TONE, SirenEntityFeature
from homeassistant.const import STATE_ON, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HomematicConfigEntry
from .control_unit import ControlUnit, signal_new_data_point
from .generic_entity import AioHomematicGenericRestoreEntity
from .services import ATTR_AVAILABLE_SOUNDFILES, ATTR_CURRENT_SOUNDFILE, ATTR_LIGHT, ATTR_SUPPORTS_SOUNDFILES
from .support import handle_homematic_errors

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomematicConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local for OpenCCU siren platform."""
    control_unit: ControlUnit = entry.runtime_data

    @callback
    def async_add_siren(data_points: tuple[BaseCustomDpSiren, ...]) -> None:
        """Add siren from Homematic(IP) Local for OpenCCU."""
        _LOGGER.debug("ASYNC_ADD_SIREN: Adding %i data points", len(data_points))

        if entities := [
            AioHomematicSiren(
                control_unit=control_unit,
                data_point=data_point,
            )
            for data_point in data_points
        ]:
            async_add_entities(entities)

    entry.async_on_unload(
        func=async_dispatcher_connect(
            hass=hass,
            signal=signal_new_data_point(entry_id=entry.entry_id, platform=DataPointCategory.SIREN),
            target=async_add_siren,
        )
    )

    async_add_siren(data_points=control_unit.get_new_data_points(data_point_type=BaseCustomDpSiren))


class AioHomematicSiren(AioHomematicGenericRestoreEntity[BaseCustomDpSiren], SirenEntity):
    """Representation of the HomematicIP siren entity."""

    _attr_supported_features = SirenEntityFeature.TURN_OFF | SirenEntityFeature.TURN_ON

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: BaseCustomDpSiren,
    ) -> None:
        """Initialize the siren entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        if data_point.supports_tones:
            self._attr_supported_features |= SirenEntityFeature.TONES
        if data_point.supports_duration:
            self._attr_supported_features |= SirenEntityFeature.DURATION

    @property
    def available_lights(self) -> list[int | str] | dict[int, str] | None:
        """Return a list of available lights."""
        return self._data_point.available_lights  # type: ignore[return-value]

    @property
    def available_tones(self) -> list[int | str] | dict[int, str] | None:
        """Return a list of available tones."""
        return self._data_point.available_tones  # type: ignore[return-value]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes for sound player entities."""
        if not isinstance(self._data_point, CustomDpSoundPlayer):
            return {}
        return {
            ATTR_AVAILABLE_SOUNDFILES: self._data_point.available_soundfiles,
            ATTR_CURRENT_SOUNDFILE: self._data_point.current_soundfile,
            ATTR_SUPPORTS_SOUNDFILES: self._data_point.supports_soundfiles,
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if siren is on."""
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

    @handle_homematic_errors
    async def async_play_sound(
        self,
        *,
        soundfile: str | int | None = None,
        volume: float | None = None,
        on_time: float | None = None,
        ramp_time: float | None = None,
        repetitions: int | None = None,
    ) -> None:
        """Play a sound on HmIP-MP3P devices."""
        if not isinstance(self._data_point, CustomDpSoundPlayer):
            _LOGGER.warning(
                "play_sound is only supported for HmIP-MP3P sound player entities, not %s",
                type(self._data_point).__name__,
            )
            return

        kwargs: PlaySoundArgs = {}
        if soundfile is not None:
            kwargs["soundfile"] = soundfile
        if volume is not None:
            kwargs["volume"] = volume
        if on_time is not None:
            kwargs["on_time"] = on_time
        if ramp_time is not None:
            kwargs["ramp_time"] = ramp_time
        if repetitions is not None:
            kwargs["repetitions"] = repetitions

        await self._data_point.play_sound(**kwargs)

    @handle_homematic_errors
    async def async_stop_sound(self) -> None:
        """Stop sound playback on HmIP-MP3P devices."""
        if not isinstance(self._data_point, CustomDpSoundPlayer):
            _LOGGER.warning(
                "stop_sound is only supported for HmIP-MP3P sound player entities, not %s",
                type(self._data_point).__name__,
            )
            return

        await self._data_point.stop_sound()

    @handle_homematic_errors
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the device off."""
        await self._data_point.turn_off()

    @handle_homematic_errors
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the device on."""
        hm_kwargs = SirenOnArgs()
        if tone := kwargs.get(ATTR_TONE):
            hm_kwargs["acoustic_alarm"] = tone
        if light := kwargs.get(ATTR_LIGHT):
            hm_kwargs["optical_alarm"] = light
        if duration := kwargs.get(ATTR_DURATION):
            hm_kwargs["duration"] = duration
        await self._data_point.turn_on(**hm_kwargs)
