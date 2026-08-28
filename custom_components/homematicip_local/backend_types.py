"""Backend-agnostic ``isinstance`` tuples for data-point dispatch.

With the openccu-loom backend the data points handed to the platforms
are instances of openccu-loom-client's aiohomematic-*compatible*
classes, not of aiohomematic's own classes, and there is no way to make
one class identity cover both.

Not for the reason this docstring used to give. Subclassing an
aiohomematic model class works — measured twice, 15 of 15 dispatch
classes — so the "C-level slot-layout conflict" claim was wrong. Two
other things are true and are what actually rule the alternatives out:

* ``ABCMeta.register`` fails *silently*. ``CustomDpCover.register(cls)``
  returns without error and ``isinstance`` stays ``False``, so a virtual
  registration would read as working and dispatch nothing.
* Inheriting is worse than useless. On a subclass that skips
  ``__init__`` — which a daemon-mediated twin must, since aiohomematic's
  constructors want a live ``CentralUnit`` — 93 of 153 members raise on
  access, 42 of them public, including the ones the platforms read:
  ``current_position``, ``is_closed``, ``unique_id``, ``name``,
  ``available``, ``usage``.

Instead, each dispatch checks ``isinstance`` against a tuple pairing the
aiohomematic class with its openccu-loom-client twin. This is purely
additive: a direct-CCU data point is never an instance of a loom class,
so the CCU code path is unchanged; a loom data point matches its twin.

If ``openccu-loom-client`` is not installed the tuples degrade to the
aiohomematic class alone, so a CCU-only install is unaffected.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

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

if TYPE_CHECKING:
    from openccu_loom_client.compat.aiohomematic.model.alarm_panel import LoomDpAlarmControlPanel

_g: object | None
_c: object | None
_h: object | None
_a: object | None
try:
    from openccu_loom_client.compat.aiohomematic.model import (
        alarm_panel as _loom_alarm_panel,
        custom as _loom_custom,
        generic as _loom_generic,
        hub as _loom_hub,
    )
except ImportError:  # pragma: no cover - CCU-only install
    _g = _c = _h = _a = None
else:
    _g = _loom_generic
    _c = _loom_custom
    _h = _loom_hub
    _a = _loom_alarm_panel


_LOGGER = logging.getLogger(__name__)


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
        # The module imported, so openccu-loom-client is installed and this
        # twin is expected — it has been renamed or removed. Degrading to the
        # aiohomematic class alone would silently drop every loom entity of
        # this type out of its platform: a blind loses tilt, a garage loses
        # its class, a sound player loses its soundfiles, and nothing says so.
        _LOGGER.warning(
            "openccu-loom-client is installed but exposes no %s; entities of this type will not be "
            "dispatched on the openccu-loom backend. This is a version mismatch between the "
            "integration and openccu-loom-client",
            loom_attr,
        )
    return (aio_cls,)


def _loom_only(loom_attr: str, loom_module: object | None) -> tuple[type[Any], ...]:
    """Return ``(loom_cls,)`` for a loom-native surface with no aiohomematic class.

    Used for surfaces that exist only on the openccu-loom backend (the alarm
    control panel: the CCU has no alarm engine, so aiohomematic ships no class
    to pair with). Degrades to the *empty* tuple on a CCU-only install —
    ``isinstance(x, ())`` is always ``False``, so the platform simply spawns
    nothing. Callers annotate the constant with the concrete loom type so
    ``isinstance`` narrows.
    """
    if loom_module is not None:
        loom_cls = getattr(loom_module, loom_attr, None)
        if loom_cls is not None:
            return (cast("type[Any]", loom_cls),)
    return ()


# ---- generic ----
DP_SWITCH = _pair(DpSwitch, "DpSwitch", _g)
DP_ACTION = _pair(DpAction, "DpAction", _g)
DP_BUTTON = _pair(DpButton, "DpButton", _g)
DP_ACTION_OR_BUTTON: tuple[type[DpAction | DpButton], ...] = (*DP_ACTION, *DP_BUTTON)

# ---- hub ----
SYSVAR_DP_SWITCH = _pair(SysvarDpSwitch, "SysvarDpSwitch", _h)
PROGRAM_DP_SWITCH = _pair(ProgramDpSwitch, "ProgramDpSwitch", _h)

# ---- loom-only (no aiohomematic class) ----
LOOM_DP_ALARM_CONTROL_PANEL: tuple[type[LoomDpAlarmControlPanel], ...] = _loom_only("LoomDpAlarmControlPanel", _a)

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
