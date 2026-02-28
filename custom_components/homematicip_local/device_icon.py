"""Device icon proxy for the Homematic configuration panel."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

from aiohttp import ClientError, web

from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.http import HomeAssistantView
from homeassistant.util.hass_dict import HassKey

if TYPE_CHECKING:
    from .control_unit import ControlUnit

_CCU_IMAGE_PATH: Final = "/config/img/devices/250"

# Only allow safe filenames: word chars, hyphens, dots — no path traversal
_SAFE_FILENAME_RE: Final = re.compile(r"^[\w\-.]+\.png$")

ICON_VIEW_REGISTERED_KEY: HassKey[bool] = HassKey("homematicip_local_icon_view_registered")


class DeviceIconView(HomeAssistantView):
    """Proxy device icon images from the CCU."""

    url = "/api/homematicip_local/{entry_id}/device_icon/{filename}"
    name = "api:homematicip_local:device_icon"
    requires_auth = False

    async def get(
        self,
        request: web.Request,
        entry_id: str,
        filename: str,
    ) -> web.Response:
        """Proxy a device icon image from the CCU."""
        if not _SAFE_FILENAME_RE.match(filename):
            raise web.HTTPNotFound

        hass: HomeAssistant = request.app["hass"]

        if (entry := hass.config_entries.async_get_entry(entry_id)) is None:
            raise web.HTTPNotFound

        if not hasattr(entry, "runtime_data"):
            raise web.HTTPNotFound

        control: ControlUnit = entry.runtime_data
        base_url = control.central.config.create_central_url()
        ccu_url = f"{base_url}{_CCU_IMAGE_PATH}/{filename}"

        # Reuse the same client session that was passed to aiohomematic
        session = aiohttp_client.async_get_clientsession(hass)

        try:
            async with session.get(ccu_url, ssl=control.central.config.verify_tls) as resp:
                if resp.status != 200:
                    raise web.HTTPNotFound
                data = await resp.read()
                return web.Response(
                    body=data,
                    content_type=resp.content_type or "image/png",
                    headers={"Cache-Control": "public, max-age=86400"},
                )
        except ClientError as err:
            raise web.HTTPNotFound from err
