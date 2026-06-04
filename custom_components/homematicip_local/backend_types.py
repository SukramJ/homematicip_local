"""Backend-agnostic ``isinstance`` tuples for data-point dispatch.

With the openccu-loom backend the data points handed to the platforms
are instances of openccu-loom-client's aiohomematic-*compatible*
classes, not of aiohomematic's own classes. aiohomematic's
Protocol-based metaclass blocks both subclassing (C-level slot-layout
conflict) and ``ABCMeta.register`` virtual subclassing, so platform
dispatch cannot rely on a shared class identity.

Instead, each dispatch checks ``isinstance`` against a tuple pairing the
aiohomematic class with its openccu-loom-client twin. This is purely
additive: a direct-CCU data point is never an instance of a loom class,
so the CCU code path is unchanged; a loom data point matches its twin.

If ``openccu-loom-client`` is not installed the tuples degrade to the
aiohomematic class alone, so a CCU-only install is unaffected.
"""

from __future__ import annotations

from typing import cast

from aiohomematic.model.custom import (
    CustomDpBlind,
    CustomDpCover,
    CustomDpGarage,
    CustomDpIpBlind,
    CustomDpIpFixedColorLight,
    CustomDpIpIrrigationValve,
    CustomDpIpThermostat,
    CustomDpSoundPlayer,
    CustomDpSoundPlayerLed,
    CustomDpSwitch,
)
from aiohomematic.model.generic import DpAction, DpButton, DpSwitch
from aiohomematic.model.hub import ProgramDpSwitch, SysvarDpSwitch

_g: object | None
_c: object | None
_h: object | None
try:
    from openccu_loom_client.compat.aiohomematic.model import (
        custom as _loom_custom,
        generic as _loom_generic,
        hub as _loom_hub,
    )
except ImportError:  # pragma: no cover - CCU-only install
    _g = _c = _h = None
else:
    _g = _loom_generic
    _c = _loom_custom
    _h = _loom_hub


def _pair[T](aio_cls: type[T], loom_attr: str, loom_module: object | None) -> tuple[type[T], ...]:
    """Return ``(aio_cls, loom_cls)`` if the loom twin exists, else ``(aio_cls,)``.

    The loom twin duck-types the aiohomematic class, so the tuple is typed
    homogeneously as ``tuple[type[aio_cls], ...]`` — an ``isinstance`` check
    against it narrows to the aiohomematic type, which is the documented
    contract for every platform dispatch.
    """
    if loom_module is not None:
        loom_cls = getattr(loom_module, loom_attr, None)
        if loom_cls is not None:
            return (aio_cls, cast("type[T]", loom_cls))
    return (aio_cls,)


# ---- generic ----
DP_SWITCH = _pair(DpSwitch, "DpSwitch", _g)
DP_ACTION = _pair(DpAction, "DpAction", _g)
DP_BUTTON = _pair(DpButton, "DpButton", _g)
DP_ACTION_OR_BUTTON: tuple[type[DpAction | DpButton], ...] = (*DP_ACTION, *DP_BUTTON)

# ---- hub ----
SYSVAR_DP_SWITCH = _pair(SysvarDpSwitch, "SysvarDpSwitch", _h)
PROGRAM_DP_SWITCH = _pair(ProgramDpSwitch, "ProgramDpSwitch", _h)

# ---- custom ----
CUSTOM_DP_SWITCH = _pair(CustomDpSwitch, "CustomDpSwitch", _c)
CUSTOM_DP_IP_THERMOSTAT = _pair(CustomDpIpThermostat, "CustomDpIpThermostat", _c)
CUSTOM_DP_COVER = _pair(CustomDpCover, "CustomDpCover", _c)
CUSTOM_DP_BLIND = _pair(CustomDpBlind, "CustomDpBlind", _c)
CUSTOM_DP_IP_BLIND = _pair(CustomDpIpBlind, "CustomDpIpBlind", _c)
CUSTOM_DP_GARAGE = _pair(CustomDpGarage, "CustomDpGarage", _c)
CUSTOM_DP_SOUND_PLAYER = _pair(CustomDpSoundPlayer, "CustomDpSoundPlayer", _c)
CUSTOM_DP_IP_IRRIGATION_VALVE = _pair(CustomDpIpIrrigationValve, "CustomDpIpIrrigationValve", _c)
CUSTOM_DP_IP_FIXED_COLOR_LIGHT = _pair(CustomDpIpFixedColorLight, "CustomDpIpFixedColorLight", _c)
CUSTOM_DP_SOUND_PLAYER_LED = _pair(CustomDpSoundPlayerLed, "CustomDpSoundPlayerLed", _c)
