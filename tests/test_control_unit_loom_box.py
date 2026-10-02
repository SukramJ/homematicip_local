"""Tests for the openccu-loom box-ingress connection in ControlConfig.

A loom entry carrying an openccu-lite box token must hand that token to
openccu-loom-client's compat ``CentralConfig`` and ``check_config`` as their
``box_*`` keyword; a direct daemon entry must hand over none, and so must an
entry still holding a box web account from an earlier release (it is sent
through reauthentication instead).
"""

from __future__ import annotations

import inspect
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiohomematic.exceptions import AuthFailure
from custom_components.homematicip_local.const import (
    BACKEND_LOOM,
    CONF_BACKEND,
    CONF_INSTANCE_NAME,
    CONF_LOOM_BOX_PASSWORD,
    CONF_LOOM_BOX_TOKEN,
    CONF_LOOM_BOX_USERNAME,
    CONF_LOOM_TOKEN,
    CONF_TLS,
)
from custom_components.homematicip_local.control_unit import (
    BaseControlUnit,
    ControlConfig,
    is_loom_box_gate_error,
    loom_box_kwargs,
)
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

_CU = "custom_components.homematicip_local.control_unit"
_BOX_TOKEN = "olt_0123456789abcdef0123456789abcdef"
_BOX_DATA = {CONF_LOOM_BOX_TOKEN: _BOX_TOKEN}
_BOX_KWARGS = {"box_token": _BOX_TOKEN}


def _loom_data(**extra: Any) -> dict[str, Any]:
    return {
        CONF_BACKEND: BACKEND_LOOM,
        CONF_INSTANCE_NAME: "box-loom",
        CONF_HOST: "box.local",
        CONF_TLS: True,
        **extra,
    }


class TestLoomBoxKwargs:
    """The entry-data → client-keyword projection."""

    def test_box_token_maps_to_box_kwargs(self) -> None:
        assert loom_box_kwargs(data=_loom_data(**_BOX_DATA)) == _BOX_KWARGS

    def test_client_accepts_every_emitted_keyword(self) -> None:
        """Every keyword the integration emits is a declared parameter of the client's compat API.

        The client raises ``TypeError`` for an unknown ``box_*`` keyword, so a
        misspelt name here would fail every box-mode setup at runtime.
        """
        from openccu_loom_client.compat.aiohomematic.central import CentralConfig, check_config, list_ccus

        emitted = set(loom_box_kwargs(data=_loom_data(**_BOX_DATA)))
        for target in (CentralConfig.__init__, check_config, list_ccus):
            assert emitted <= set(inspect.signature(target).parameters), target

    def test_direct_entry_maps_to_nothing(self) -> None:
        assert loom_box_kwargs(data=_loom_data(**{CONF_LOOM_TOKEN: "tok"})) == {}

    def test_legacy_box_account_maps_to_nothing(self) -> None:
        legacy = {CONF_LOOM_BOX_USERNAME: "boxadmin", CONF_LOOM_BOX_PASSWORD: "boxpw"}
        assert loom_box_kwargs(data=_loom_data(**legacy)) == {}


class TestControlConfigLoomBox:
    """ControlConfig threads the box account into the client."""

    @pytest.mark.parametrize(
        ("extra", "expected"),
        [
            (_BOX_DATA, _BOX_KWARGS),
            ({CONF_LOOM_TOKEN: "tok"}, {}),
        ],
    )
    async def test_check_config_passes_box_kwargs(
        self, hass: HomeAssistant, extra: dict[str, str], expected: dict[str, str]
    ) -> None:
        loom_check_config = AsyncMock(return_value=[])
        with patch(f"{_CU}._import_loom_check_config", return_value=loom_check_config):
            await ControlConfig(hass=hass, entry_id="validate", data=_loom_data(**extra)).check_config()
        kwargs = loom_check_config.await_args.kwargs
        assert {k: v for k, v in kwargs.items() if k.startswith("box_")} == expected

    @pytest.mark.parametrize(
        ("extra", "expected"),
        [
            (_BOX_DATA, _BOX_KWARGS),
            ({CONF_LOOM_TOKEN: "tok"}, {}),
        ],
    )
    async def test_create_central_passes_box_kwargs(
        self, hass: HomeAssistant, extra: dict[str, str], expected: dict[str, str]
    ) -> None:
        loom_central_config = MagicMock()
        loom_central_config.return_value.create_central = AsyncMock(return_value=MagicMock())
        with (
            patch(f"{_CU}._import_loom_central_config", return_value=loom_central_config),
            patch(f"{_CU}.aiohttp_client.async_get_clientsession", return_value=MagicMock()),
        ):
            await ControlConfig(hass=hass, entry_id="entry", data=_loom_data(**extra)).create_central()
        kwargs = loom_central_config.call_args.kwargs
        assert {k: v for k, v in kwargs.items() if k.startswith("box_")} == expected
        assert kwargs["host"] == "box.local"


class TestBoxGateError:
    """Which loom-client errors send the entry through reauthentication."""

    def test_box_gate_refusals_are_gate_errors(self) -> None:
        from openccu_loom_client import LoomBoxGateError, LoomBoxTokenError

        assert is_loom_box_gate_error(LoomBoxTokenError("revoked"))
        assert is_loom_box_gate_error(LoomBoxGateError("no scope"))

    def test_other_loom_errors_are_not(self) -> None:
        from openccu_loom_client import LoomAuthError, LoomTransportError

        assert not is_loom_box_gate_error(LoomTransportError("unreachable"))
        assert not is_loom_box_gate_error(LoomAuthError(status=401, method="GET", url="x"))

    async def test_start_central_turns_a_gate_refusal_into_auth_failure(self) -> None:
        """The caller, not only the helper: a refused box token must reach setup as AuthFailure."""
        from openccu_loom_client import LoomBoxTokenError, LoomTransportError

        unit = SimpleNamespace(
            _instance_name="box-loom", _central=SimpleNamespace(start=AsyncMock(side_effect=LoomBoxTokenError("401")))
        )
        with pytest.raises(AuthFailure):
            await BaseControlUnit.start_central(unit)  # type: ignore[arg-type]
        # Any other start failure keeps its old treatment: logged, not raised.
        unit._central.start = AsyncMock(side_effect=LoomTransportError("unreachable"))
        await BaseControlUnit.start_central(unit)  # type: ignore[arg-type]
