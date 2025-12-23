"""Helper."""

from __future__ import annotations

from collections.abc import Callable, Coroutine, Mapping
from copy import deepcopy
from functools import wraps
import logging
import re
from typing import Any, TypeAlias, TypeVar, cast

import voluptuous as vol

from aiohomematic import validator as val
from aiohomematic.const import IDENTIFIER_SEPARATOR
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.interfaces.model import (
    CalculatedDataPointProtocol,
    CustomDataPointProtocol,
    GenericDataPointProtocolAny,
    GenericProgramDataPointProtocol,
    GenericSysvarDataPointProtocol,
)
from homeassistant.const import CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.loader import async_get_integration

from .const import (
    CONF_SUBTYPE,
    EVENT_ADDRESS,
    EVENT_CHANNEL_NO,
    EVENT_DEVICE_ID,
    EVENT_ERROR,
    EVENT_ERROR_VALUE,
    EVENT_IDENTIFIER,
    EVENT_INTERFACE_ID,
    EVENT_MESSAGE,
    EVENT_MODEL,
    EVENT_NAME,
    EVENT_PARAMETER,
    EVENT_TITLE,
    EVENT_UNAVAILABLE,
    EVENT_VALUE,
)

# Union for entity types used as base class for data points
HmBaseDataPointProtocol: TypeAlias = CalculatedDataPointProtocol | CustomDataPointProtocol | GenericDataPointProtocolAny
# Generic base type used for data points in Homematic(IP) Local for OpenCCU
HmGenericDataPointProtocol = TypeVar("HmGenericDataPointProtocol", bound=HmBaseDataPointProtocol)
# Generic base type used for sysvar data points in Homematic(IP) Local for OpenCCU
HmGenericProgramDataPointProtocol = TypeVar("HmGenericProgramDataPointProtocol", bound=GenericProgramDataPointProtocol)
# Generic base type used for sysvar data points in Homematic(IP) Local for OpenCCU
HmGenericSysvarDataPointProtocol = TypeVar("HmGenericSysvarDataPointProtocol", bound=GenericSysvarDataPointProtocol)

BASE_EVENT_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(EVENT_DEVICE_ID): str,
        vol.Required(EVENT_NAME): str,
        vol.Required(EVENT_ADDRESS): val.device_address,
        vol.Required(EVENT_CHANNEL_NO): val.channel_no,
        vol.Required(EVENT_MODEL): str,
        vol.Required(EVENT_INTERFACE_ID): str,
        vol.Required(EVENT_PARAMETER): str,
        vol.Optional(EVENT_VALUE): vol.Any(bool, int),
    }
)
CLICK_EVENT_SCHEMA = BASE_EVENT_DATA_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): str,
        vol.Required(CONF_SUBTYPE): int,
        vol.Remove(EVENT_CHANNEL_NO): int,
        vol.Remove(EVENT_PARAMETER): str,
        vol.Remove(EVENT_VALUE): vol.Any(bool, int),
    },
    extra=vol.ALLOW_EXTRA,
)
DEVICE_AVAILABILITY_EVENT_SCHEMA = BASE_EVENT_DATA_SCHEMA.extend(
    {
        vol.Required(EVENT_IDENTIFIER): str,
        vol.Required(EVENT_TITLE): str,
        vol.Required(EVENT_MESSAGE): str,
        vol.Required(EVENT_UNAVAILABLE): bool,
    },
    extra=vol.ALLOW_EXTRA,
)
DEVICE_ERROR_EVENT_SCHEMA = BASE_EVENT_DATA_SCHEMA.extend(
    {
        vol.Required(EVENT_IDENTIFIER): str,
        vol.Required(EVENT_TITLE): str,
        vol.Required(EVENT_MESSAGE): str,
        vol.Required(EVENT_ERROR_VALUE): vol.Any(bool, int),
        vol.Required(EVENT_ERROR): bool,
    },
    extra=vol.ALLOW_EXTRA,
)

_LOGGER = logging.getLogger(__name__)


def handle_homematic_errors[**P, R](
    func: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]:
    """
    Handle aiohomematic exceptions and convert to HomeAssistantError.

    This decorator prevents log flooding by converting backend exceptions
    to HomeAssistantError, which Home Assistant displays as a toast notification
    instead of logging repeatedly.
    """

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await func(*args, **kwargs)
        except BaseHomematicException as exc:
            raise HomeAssistantError(str(exc)) from exc

    return wrapper


def cleanup_click_event_data(event_data: dict[str, Any]) -> dict[str, Any]:
    """Cleanup the click_event."""
    cleand_event_data = deepcopy(event_data)
    cleand_event_data.update(
        {
            CONF_TYPE: cleand_event_data[EVENT_PARAMETER].lower(),
            CONF_SUBTYPE: cleand_event_data[EVENT_CHANNEL_NO],
        }
    )
    del cleand_event_data[EVENT_PARAMETER]
    del cleand_event_data[EVENT_CHANNEL_NO]
    return cleand_event_data


def is_valid_event(event_data: Mapping[str, Any], schema: vol.Schema) -> bool:
    """Validate event_data against a given schema."""
    try:
        schema(event_data)
    except vol.Invalid as err:
        _LOGGER.debug("The EVENT could not be validated. %s, %s", err.path, err.msg)
        return False
    return True


def get_device_address_at_interface_from_identifiers(
    identifiers: set[tuple[str, str]],
) -> tuple[str, str] | None:
    """Get the device_address from device_info.identifiers."""
    for identifier in identifiers:
        if IDENTIFIER_SEPARATOR in identifier[1]:
            return cast(tuple[str, str], identifier[1].split(IDENTIFIER_SEPARATOR))
    return None


def get_data_point[DP](data_point: DP) -> DP:
    """Return the Homematic data point. Makes it mockable."""
    return data_point


class InvalidConfig(HomeAssistantError):
    """Error to indicate there is invalid config."""


async def get_aiohomematic_version(hass: HomeAssistant, domain: str, package_name: str) -> str | None:
    """Return the version of a package from manifest.json."""
    integration = await async_get_integration(hass, domain)
    requirements = integration.manifest.get("requirements", [])

    for req in requirements:
        match = re.match(r"^([a-zA-Z0-9_.\-]+)\s*[<>=!~]*\s*([0-9a-zA-Z_.\-]+)?$", req)
        if match:
            name, version = match.groups()
            if name.lower() == package_name.lower():
                return version or "0.0.0"

    return None
