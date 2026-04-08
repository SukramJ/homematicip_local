"""Panel and Lovelace card registration for the Homematic frontend."""

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

# --- Panel (config UI) ---

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

# --- Lovelace cards ---

_CARD_FILES: Final[dict[str, str]] = {
    "climate-schedule-card": "homematicip-local-climate-schedule-card.js",
    "schedule-card": "homematicip-local-schedule-card.js",
    "status-card": "homematicip-local-status-card.js",
}

CARDS_REGISTERED_KEY: HassKey[bool] = HassKey("homematicip_local_cards_registered")
_CARDS_STATIC_REGISTERED_KEY: HassKey[bool] = HassKey("homematicip_local_cards_static_registered")


def _build_card_urls() -> dict[str, str]:
    """Build cache-busted URLs for card JS files."""
    urls: dict[str, str] = {}
    for card_name, filename in _CARD_FILES.items():
        file = _PANEL_DIR / filename
        if file.exists():
            file_hash = hashlib.md5(file.read_bytes()).hexdigest()[:8]  # noqa: S324
            urls[card_name] = f"/homematicip_local/{filename.removesuffix('.js')}-{file_hash}.js"
    return urls


_CARD_URLS: Final[dict[str, str]] = _build_card_urls()


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


# --- Lovelace card registration ---


async def _async_register_card_static_paths(hass: HomeAssistant) -> None:
    """Register static paths for Lovelace card JS files (once, permanently)."""
    if hass.data.get(_CARDS_STATIC_REGISTERED_KEY):
        return

    paths: list[StaticPathConfig] = []
    for card_name, url in _CARD_URLS.items():
        filename = _CARD_FILES[card_name]
        file = _PANEL_DIR / filename
        if file.exists():
            paths.append(StaticPathConfig(url, str(file), cache_headers=True))
        else:
            _LOGGER.warning(
                "Card frontend file not found at %s. Skipping %s registration",
                file,
                card_name,
            )

    if paths:
        await hass.http.async_register_static_paths(paths)
    hass.data[_CARDS_STATIC_REGISTERED_KEY] = True


async def async_register_cards(hass: HomeAssistant) -> None:
    """Register Lovelace card resources."""
    if hass.data.get(CARDS_REGISTERED_KEY):
        return

    await _async_register_card_static_paths(hass)

    if not hass.data.get(_CARDS_STATIC_REGISTERED_KEY):
        return

    if frontend.DATA_EXTRA_MODULE_URL not in hass.data:
        _LOGGER.warning("Frontend not yet initialized. Skipping card registration")
        return

    for card_name, url in _CARD_URLS.items():
        frontend.add_extra_js_url(hass, url)
        _LOGGER.debug("Registered Lovelace card %s at %s", card_name, url)

    hass.data[CARDS_REGISTERED_KEY] = True


def async_unregister_cards(hass: HomeAssistant) -> None:
    """Unregister Lovelace card resources."""
    if not hass.data.get(CARDS_REGISTERED_KEY):
        return

    if (url_manager := hass.data.get(frontend.DATA_EXTRA_MODULE_URL)) is not None:
        for url in _CARD_URLS.values():
            if url in url_manager.urls:
                frontend.remove_extra_js_url(hass, url)

    hass.data.pop(CARDS_REGISTERED_KEY, None)
    _LOGGER.debug("Unregistered Lovelace cards")
