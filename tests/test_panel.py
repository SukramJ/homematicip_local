"""Tests for the Homematic configuration panel registration."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

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
