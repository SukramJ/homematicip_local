"""Tests for the Homematic configuration panel registration."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.homematicip_local import _any_entry_has_panel_enabled
from custom_components.homematicip_local.const import (
    BACKEND_CCU,
    BACKEND_LOOM,
    CONF_ADVANCED_CONFIG,
    CONF_BACKEND,
    CONF_DISABLE_CONFIG_PANEL,
)
from custom_components.homematicip_local.control_unit import ControlUnit
from custom_components.homematicip_local.panel import (
    _STATIC_PATH_REGISTERED_KEY,
    PANEL_REGISTERED_KEY,
    async_register_panel,
    async_unregister_panel,
)
from homeassistant.core import HomeAssistant


@pytest.fixture
def mock_hass_http(hass: HomeAssistant) -> HomeAssistant:
    """Provide hass with a mocked http attribute."""
    hass.http = MagicMock()
    hass.http.async_register_static_paths = AsyncMock()
    return hass


class TestAsyncRegisterPanel:
    """Tests for async_register_panel."""

    @pytest.mark.asyncio
    async def test_register_panel_after_reload(self, mock_hass_http: HomeAssistant) -> None:
        """Test that re-registering panel after unload does not re-register static path."""
        hass = mock_hass_http
        with (
            patch(
                "custom_components.homematicip_local.panel.Path.exists",
                return_value=True,
            ),
            patch(
                "custom_components.homematicip_local.panel.panel_custom.async_register_panel",
                new_callable=AsyncMock,
            ),
        ):
            # Initial registration
            await async_register_panel(hass)

        assert hass.data.get(PANEL_REGISTERED_KEY) is True
        assert hass.data.get(_STATIC_PATH_REGISTERED_KEY) is True
        hass.http.async_register_static_paths.assert_called_once()

        # Simulate unload (clears panel key but NOT static path key)
        with patch("custom_components.homematicip_local.panel.frontend.async_remove_panel"):
            async_unregister_panel(hass)

        assert hass.data.get(PANEL_REGISTERED_KEY) is None
        assert hass.data.get(_STATIC_PATH_REGISTERED_KEY) is True

        # Re-register after reload - static path must NOT be registered again
        hass.http.async_register_static_paths.reset_mock()
        with (
            patch(
                "custom_components.homematicip_local.panel.panel_custom.async_register_panel",
                new_callable=AsyncMock,
            ) as mock_panel,
        ):
            await async_register_panel(hass)

        assert hass.data.get(PANEL_REGISTERED_KEY) is True
        hass.http.async_register_static_paths.assert_not_called()
        mock_panel.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_panel_idempotent(self, mock_hass_http: HomeAssistant) -> None:
        """Test that registering twice does not call register again."""
        hass = mock_hass_http
        hass.data[PANEL_REGISTERED_KEY] = True

        await async_register_panel(hass)

        hass.http.async_register_static_paths.assert_not_called()

    @pytest.mark.asyncio
    async def test_register_panel_missing_file(self, mock_hass_http: HomeAssistant) -> None:
        """Test that missing frontend file skips registration."""
        hass = mock_hass_http
        with patch(
            "custom_components.homematicip_local.panel.Path.exists",
            return_value=False,
        ):
            await async_register_panel(hass)

        assert hass.data.get(PANEL_REGISTERED_KEY) is None
        assert hass.data.get(_STATIC_PATH_REGISTERED_KEY) is None
        hass.http.async_register_static_paths.assert_not_called()

    @pytest.mark.asyncio
    async def test_register_panel_success(self, mock_hass_http: HomeAssistant) -> None:
        """Test successful panel registration."""
        hass = mock_hass_http
        with (
            patch(
                "custom_components.homematicip_local.panel.Path.exists",
                return_value=True,
            ),
            patch(
                "custom_components.homematicip_local.panel.panel_custom.async_register_panel",
                new_callable=AsyncMock,
            ) as mock_panel,
        ):
            await async_register_panel(hass)

        assert hass.data.get(PANEL_REGISTERED_KEY) is True
        assert hass.data.get(_STATIC_PATH_REGISTERED_KEY) is True
        hass.http.async_register_static_paths.assert_called_once()
        mock_panel.assert_called_once()


class TestAsyncUnregisterPanel:
    """Tests for async_unregister_panel."""

    @pytest.mark.asyncio
    async def test_unregister_panel_not_registered(self, hass: HomeAssistant) -> None:
        """Test that unregistering when not registered is a no-op."""
        with patch("custom_components.homematicip_local.panel.frontend.async_remove_panel") as mock_remove:
            async_unregister_panel(hass)

        mock_remove.assert_not_called()

    @pytest.mark.asyncio
    async def test_unregister_panel_success(self, hass: HomeAssistant) -> None:
        """Test successful panel unregistration."""
        hass.data[PANEL_REGISTERED_KEY] = True

        with patch("custom_components.homematicip_local.panel.frontend.async_remove_panel") as mock_remove:
            async_unregister_panel(hass)

        mock_remove.assert_called_once_with(hass, "homematic-config")
        assert hass.data.get(PANEL_REGISTERED_KEY) is None


class TestAnyEntryHasPanelEnabled:
    """
    Which config entries make the panel worth registering.

    The panel is registered once for the whole domain, so this predicate
    decides for the installation, not for one entry.
    """

    @staticmethod
    def _entry(*, backend: str | None = None, disable_panel: bool = False, loaded: bool = True) -> MagicMock:
        entry = MagicMock()
        data: dict[str, object] = {CONF_ADVANCED_CONFIG: {CONF_DISABLE_CONFIG_PANEL: disable_panel}}
        if backend is not None:
            data[CONF_BACKEND] = backend
        entry.data = data
        entry.runtime_data = object() if loaded else None
        return entry

    @staticmethod
    def _hass_with(*entries: MagicMock) -> MagicMock:
        hass = MagicMock()
        hass.config_entries.async_entries.return_value = list(entries)
        return hass

    def test_a_ccu_entry_alongside_a_loom_entry_still_enables_it(self) -> None:
        # The CCU entry genuinely needs the panel, and registration is
        # domain-wide. The panel's own entry picker drops the loom one.
        hass = self._hass_with(self._entry(backend=BACKEND_LOOM), self._entry(backend=BACKEND_CCU))
        assert _any_entry_has_panel_enabled(hass=hass) is True

    def test_an_unloaded_entry_does_not(self) -> None:
        hass = self._hass_with(self._entry(backend=BACKEND_CCU, loaded=False))
        assert _any_entry_has_panel_enabled(hass=hass) is False

    def test_ccu_entry_enables_the_panel(self) -> None:
        hass = self._hass_with(self._entry(backend=BACKEND_CCU))
        assert _any_entry_has_panel_enabled(hass=hass) is True

    def test_explicitly_disabled_ccu_entry_does_not(self) -> None:
        hass = self._hass_with(self._entry(backend=BACKEND_CCU, disable_panel=True))
        assert _any_entry_has_panel_enabled(hass=hass) is False

    def test_loom_entry_alone_does_not(self) -> None:
        # The daemon ships its own Config UI covering the same ground for
        # every CCU it serves; a second, narrower one is worse than none.
        hass = self._hass_with(self._entry(backend=BACKEND_LOOM))
        assert _any_entry_has_panel_enabled(hass=hass) is False


class TestDeviceConfigurationUrl:
    """Where a device page sends someone who clicks "Configure".

    The two backends answer differently because they own different
    editors, and on loom the answer has to be an address a *browser* can
    follow — not the one this integration connects on.
    """

    @staticmethod
    def _unit(*, backend: str, config_ui_url: str = "", url: str = "", disable_panel: bool = False) -> SimpleNamespace:
        return SimpleNamespace(
            _config=SimpleNamespace(backend=backend),
            _entry_id="entry-1",
            _disable_config_panel=disable_panel,
            _central=SimpleNamespace(config_ui_url=config_ui_url, url=url),
        )

    def test_ccu_backend_links_at_the_config_panel(self) -> None:
        url = self._call(self._unit(backend=BACKEND_CCU))
        assert url is not None
        assert url.startswith("homeassistant://homematic-config#view=device-detail")
        assert "device=0001D3C99C1234" in url

    def test_ccu_backend_offers_nothing_when_the_panel_is_off(self) -> None:
        assert self._call(self._unit(backend=BACKEND_CCU, disable_panel=True)) is None

    def test_loom_falls_back_to_the_connection_address(self) -> None:
        unit = self._unit(backend=BACKEND_LOOM, url="http://loom.lan:8080/api/v1")
        assert self._call(unit) == "http://loom.lan:8080/app/#/devices/0001D3C99C1234"

    def test_loom_offers_nothing_when_no_address_is_known(self) -> None:
        # Better than a link into nothing.
        assert self._call(self._unit(backend=BACKEND_LOOM)) is None

    def test_loom_prefers_the_operator_declared_public_url(self) -> None:
        # The daemon's own answer wins over anything derived here: behind a
        # reverse proxy the connection address is not browser-reachable.
        unit = self._unit(
            backend=BACKEND_LOOM,
            config_ui_url="https://loom.example.de/app/",
            url="http://172.30.33.4:8080/api/v1",
        )
        assert self._call(unit) == "https://loom.example.de/app/#/devices/0001D3C99C1234"

    def _call(self, unit: SimpleNamespace) -> str | None:
        return ControlUnit.device_configuration_url(unit, address="0001D3C99C1234", interface_id="home:HmIP-RF")
