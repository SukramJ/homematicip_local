"""Tests for the openccu-loom box-ingress connection in ControlConfig.

A loom entry carrying an openccu-lite box account must hand that account to
openccu-loom-client's compat ``CentralConfig`` and ``check_config`` as their
``box_*`` keywords; a direct daemon entry must hand over none.
"""

from __future__ import annotations

import inspect
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.homematicip_local.const import (
    BACKEND_LOOM,
    CONF_BACKEND,
    CONF_INSTANCE_NAME,
    CONF_LOOM_BOX_PASSWORD,
    CONF_LOOM_BOX_USERNAME,
    CONF_LOOM_TOKEN,
    CONF_TLS,
)
from custom_components.homematicip_local.control_unit import ControlConfig, loom_box_kwargs
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

_CU = "custom_components.homematicip_local.control_unit"
_BOX_DATA = {CONF_LOOM_BOX_USERNAME: "boxadmin", CONF_LOOM_BOX_PASSWORD: "boxpw"}
_BOX_KWARGS = {"box_username": "boxadmin", "box_password": "boxpw"}


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

    def test_box_account_maps_to_box_kwargs(self) -> None:
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
