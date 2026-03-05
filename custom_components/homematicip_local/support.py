"""Helper."""

from __future__ import annotations

from collections.abc import Callable, Coroutine, Mapping
from copy import deepcopy
from functools import wraps
import logging
import re
from typing import Any, Final, TypeAlias, TypeVar

from pydantic import ValidationError
import voluptuous as vol

from aiohomematic.const import CHANNEL_ADDRESS_PATTERN, DEVICE_ADDRESS_PATTERN, IDENTIFIER_SEPARATOR, ParamsetKey
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.interfaces import (
    CalculatedDataPointProtocol,
    CombinedDataPointProtocol,
    CustomDataPointProtocol,
    GenericDataPointProtocolAny,
    GenericProgramDataPointProtocol,
    GenericSysvarDataPointProtocol,
)
from aiohomematic.model.week_profile_data_point import WeekProfileDataPoint
from aiohomematic.support.address import get_device_address
from homeassistant.const import CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.loader import async_get_integration

from .const import (
    CONF_SUBTYPE,
    EVENT_ADDRESS,
    EVENT_CHANNEL_NO,
    EVENT_DEVICE_ADDRESS,
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

_LOGGER = logging.getLogger(__name__)

# Validator constants
_CHANNEL_NO_MIN: Final = 0
_CHANNEL_NO_MAX: Final = 255
_WAIT_FOR_MIN: Final = 0
_WAIT_FOR_MAX: Final = 120


def validate_channel_no(value: Any) -> int:
    """Validate and return channel number."""
    try:
        channel = int(value)
    except (ValueError, TypeError) as err:
        raise vol.Invalid(f"Channel number must be an integer, got {type(value).__name__}") from err

    if not _CHANNEL_NO_MIN <= channel <= _CHANNEL_NO_MAX:
        raise vol.Invalid(f"Channel number must be between {_CHANNEL_NO_MIN} and {_CHANNEL_NO_MAX}")

    return channel


def validate_wait_for(value: Any) -> int:
    """Validate and return wait time in seconds."""
    try:
        wait_time = int(value)
    except (ValueError, TypeError) as err:
        raise vol.Invalid(f"Wait time must be a number, got {type(value).__name__}") from err

    if not _WAIT_FOR_MIN <= wait_time <= _WAIT_FOR_MAX:
        raise vol.Invalid(f"Wait time must be between {_WAIT_FOR_MIN} and {_WAIT_FOR_MAX} seconds")

    return wait_time


def validate_device_address(value: Any) -> str:
    """Validate and return device address. Accept channel addresses and extract the device part."""
    if not isinstance(value, str):
        raise vol.Invalid(f"Device address must be a string, got {type(value).__name__}")

    if DEVICE_ADDRESS_PATTERN.match(value) is not None:
        return value

    if CHANNEL_ADDRESS_PATTERN.match(value) is not None:
        return get_device_address(address=value)

    raise vol.Invalid(f"Invalid device address format: {value}")


def validate_channel_address(value: Any) -> str:
    """Validate and return channel address."""
    if not isinstance(value, str):
        raise vol.Invalid(f"Channel address must be a string, got {type(value).__name__}")

    if CHANNEL_ADDRESS_PATTERN.match(value) is None:
        raise vol.Invalid(f"Invalid channel address format: {value}")

    return value


def validate_paramset_key(value: Any) -> str:
    """Validate and return paramset key."""
    if isinstance(value, ParamsetKey):
        return value.value

    if not isinstance(value, str):
        raise vol.Invalid(f"Paramset key must be a string, got {type(value).__name__}")

    if value not in [pk.value for pk in ParamsetKey]:
        raise vol.Invalid(f"Invalid paramset key: {value}. Must be one of: {[pk.value for pk in ParamsetKey]}")

    return value


# Union for entity types used as base class for data points
HmBaseDataPointProtocol: TypeAlias = (
    CalculatedDataPointProtocol
    | CombinedDataPointProtocol
    | CustomDataPointProtocol
    | GenericDataPointProtocolAny
    | WeekProfileDataPoint
)
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
        vol.Required(EVENT_ADDRESS): validate_device_address,
        vol.Required(EVENT_CHANNEL_NO): validate_channel_no,
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
        except ValidationError as exc:
            # Pydantic validation errors - format user-friendly message
            errors = "; ".join(e["msg"] for e in exc.errors())
            raise HomeAssistantError(f"Invalid schedule data: {errors}") from exc
        except ValueError as exc:
            # Domain-specific validation errors from aiohomematic
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
    # Rename device_address to address (required by TRIGGER_SCHEMA)
    if EVENT_DEVICE_ADDRESS in cleand_event_data:
        cleand_event_data[EVENT_ADDRESS] = cleand_event_data.pop(EVENT_DEVICE_ADDRESS)
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
    """
    Get the device_address and interface_id from device_info.identifiers.

    Handles both regular devices (address@interface_id) and sub-devices
    (address@interface_id-group_no) by stripping the group suffix.
    """
    for identifier in identifiers:
        if IDENTIFIER_SEPARATOR in identifier[1]:
            parts = identifier[1].split(IDENTIFIER_SEPARATOR, 1)
            if len(parts) == 2:
                dev_address = parts[0]
                # Strip any sub-device group suffix (e.g., "-1") from interface_id
                interface_id = re.sub(r"-\d+$", "", parts[1])
                return dev_address, interface_id
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
