"""Panel registration for the Homematic device configuration UI."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Final

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant
from homeassistant.util.hass_dict import HassKey

_LOGGER: Final = logging.getLogger(__name__)

_PANEL_DIR: Final = Path(__file__).parent / "frontend"
_PANEL_FILE: Final = _PANEL_DIR / "homematic-config.js"
_PANEL_HASH: Final = hashlib.md5(_PANEL_FILE.read_bytes()).hexdigest()[:8]  # noqa: S324
_PANEL_URL: Final = f"/homematicip_local/homematic-config-{_PANEL_HASH}.js"

PANEL_ICON: Final = "mdi:wrench-cog"
PANEL_NAME: Final = "homematic-config"
_PANEL_TITLES: Final[dict[str, str]] = {
    "de": "HM Gerätekonfiguration",
    "en": "HM Device Configuration",
}
_DEFAULT_PANEL_TITLE: Final = "HM Device Configuration"

PANEL_REGISTERED_KEY: HassKey[bool] = HassKey(f"{PANEL_NAME}_registered")
_STATIC_PATH_REGISTERED_KEY: HassKey[bool] = HassKey(f"{PANEL_NAME}_static_path_registered")


async def _async_register_static_path(hass: HomeAssistant) -> None:
    """
    Register the static path for the panel frontend file (once, permanently).

    aiohttp does not support removing routes, so the static path must only
    be registered once per HA process lifetime.
    """
    if hass.data.get(_STATIC_PATH_REGISTERED_KEY):
        return

    if not _PANEL_FILE.exists():
        _LOGGER.warning(
            "Panel frontend file not found at %s. Skipping panel registration",
            _PANEL_FILE,
        )
        return

    await hass.http.async_register_static_paths([StaticPathConfig(_PANEL_URL, str(_PANEL_FILE), cache_headers=True)])
    hass.data[_STATIC_PATH_REGISTERED_KEY] = True


async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the Homematic configuration panel."""
    if hass.data.get(PANEL_REGISTERED_KEY):
        return

    await _async_register_static_path(hass)

    if not hass.data.get(_STATIC_PATH_REGISTERED_KEY):
        return

    hass.data[PANEL_REGISTERED_KEY] = True
    await panel_custom.async_register_panel(
        hass,
        webcomponent_name=PANEL_NAME,
        frontend_url_path="homematic-config",
        sidebar_title=_PANEL_TITLES.get(hass.config.language, _DEFAULT_PANEL_TITLE),
        sidebar_icon=PANEL_ICON,
        module_url=_PANEL_URL,
        require_admin=True,
        config={"_panel_custom": {"name": PANEL_NAME, "module_url": _PANEL_URL}},
    )
    _LOGGER.debug("Registered Homematic configuration panel at %s", _PANEL_URL)


def async_unregister_panel(hass: HomeAssistant) -> None:
    """Unregister the Homematic configuration panel."""
    if not hass.data.get(PANEL_REGISTERED_KEY):
        return
    hass.data.pop(PANEL_REGISTERED_KEY, None)
    frontend.async_remove_panel(hass, "homematic-config")
    _LOGGER.debug("Unregistered Homematic configuration panel")
