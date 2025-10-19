"""Module with aiohomematic services."""

from __future__ import annotations

from datetime import datetime
import logging
from typing import TYPE_CHECKING, Final, cast

from aiohomematic.const import ForcedDeviceAvailability, ParamsetKey
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.model.device import Device
from aiohomematic.support import get_device_address, to_bool
import aiohomematic.validator as haval
import voluptuous as vol

from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN
from homeassistant.components.cover import ATTR_POSITION, ATTR_TILT_POSITION, DOMAIN as COVER_DOMAIN
from homeassistant.components.light import DOMAIN as LIGHT_DOMAIN
from homeassistant.components.siren import ATTR_DURATION, ATTR_TONE, DOMAIN as SIREN_DOMAIN
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.components.valve import DOMAIN as VALVE_DOMAIN
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_DEVICE_ID
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.service import (
    async_register_admin_service,
    async_register_platform_entity_service,
    verify_domain_control,
)

from .const import DOMAIN, HmipLocalServices
from .control_unit import ControlUnit
from .support import get_device_address_at_interface_from_identifiers

if TYPE_CHECKING:
    from . import HomematicConfigEntry

_LOGGER = logging.getLogger(__name__)

ATTR_AWAY_END: Final = "end"
ATTR_AWAY_HOURS: Final = "hours"
ATTR_AWAY_START: Final = "start"
ATTR_AWAY_TEMPERATURE: Final = "away_temperature"
ATTR_BASE_TEMPERATURE: Final = "base_temperature"
ATTR_LIGHT: Final = "light"
ATTR_ON_TIME: Final = "on_time"
ATTR_PROFILE: Final = "profile"
ATTR_PROFILE_DATA: Final = "profile_data"
ATTR_SIMPLE_PROFILE_DATA: Final = "simple_profile_data"
ATTR_SIMPLE_WEEKDAY_LIST: Final = "simple_weekday_list"
ATTR_SOURCE_ENTITY_ID: Final = "source_entity_id"
ATTR_SOURCE_PROFILE: Final = "source_profile"
ATTR_TARGET_PROFILE: Final = "target_profile"
ATTR_WEEKDAY: Final = "weekday"
ATTR_WEEKDAY_DATA: Final = "weekday_data"

CONF_ADDRESS: Final = "address"
CONF_CHANNEL: Final = "channel"
CONF_CHANNEL_ADDRESS: Final = "channel_address"
CONF_DEVICE_ADDRESS: Final = "device_address"
CONF_DESCRIPTION: Final = "description"
CONF_ENTRY_ID: Final = "entry_id"
CONF_INTERFACE_ID: Final = "interface_id"
CONF_NAME: Final = "name"
CONF_ON_TIME: Final = "on_time"
CONF_PARAMETER: Final = "parameter"
CONF_PARAMSET: Final = "paramset"
CONF_PARAMSET_KEY: Final = "paramset_key"
CONF_RANDOMIZE_OUTPUT: Final = "randomize_output"
CONF_RECEIVER_CHANNEL_ADDRESS: Final = "receiver_channel_address"
CONF_RX_MODE: Final = "rx_mode"
CONF_SENDER_CHANNEL_ADDRESS: Final = "sender_channel_address"
CONF_TIME: Final = "time"
CONF_VALUE: Final = "value"
CONF_VALUE_TYPE: Final = "value_type"
CONF_WAIT_FOR_CALLBACK: Final = "wait_for_callback"

DEFAULT_CHANNEL: Final = 1

BASE_SCHEMA_DEVICE = vol.Schema(
    {
        vol.Optional(CONF_DEVICE_ID): cv.string,
        vol.Optional(CONF_DEVICE_ADDRESS): haval.device_address,
    }
)

SCHEMA_ADD_LINK = vol.All(
    {
        vol.Required(CONF_RECEIVER_CHANNEL_ADDRESS): haval.channel_address,
        vol.Required(CONF_SENDER_CHANNEL_ADDRESS): haval.channel_address,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_DESCRIPTION): cv.string,
    }
)

SCHEMA_CREATE_CENTRAL_LINKS = vol.All(
    cv.has_at_least_one_key(CONF_DEVICE_ID, CONF_ENTRY_ID),
    cv.has_at_most_one_key(CONF_DEVICE_ID, CONF_ENTRY_ID),
    vol.Schema(
        {
            vol.Optional(CONF_ENTRY_ID): cv.string,
            vol.Optional(CONF_DEVICE_ID): cv.string,
        }
    ),
)

SCHEMA_CLEAR_CACHE = vol.Schema(
    {
        vol.Required(CONF_ENTRY_ID): cv.string,
    }
)

SCHEMA_EXPORT_DEVICE_DEFINITION = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.string,
    }
)

SCHEMA_FETCH_SYSTEM_VARIABLES = vol.Schema(
    {
        vol.Required(CONF_ENTRY_ID): cv.string,
    }
)

SCHEMA_FORCE_DEVICE_AVAILABILITY = vol.All(
    cv.has_at_least_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    cv.has_at_most_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    BASE_SCHEMA_DEVICE,
)

SCHEMA_GET_DEVICE_VALUE = vol.All(
    cv.has_at_least_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    cv.has_at_most_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    BASE_SCHEMA_DEVICE.extend(
        {
            vol.Required(CONF_CHANNEL, default=DEFAULT_CHANNEL): haval.channel_no,
            vol.Required(CONF_PARAMETER): vol.All(cv.string, vol.Upper),
        }
    ),
)

SCHEMA_GET_LINK_PEERS = vol.All(
    cv.has_at_least_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    cv.has_at_most_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    BASE_SCHEMA_DEVICE.extend(
        {
            vol.Optional(CONF_CHANNEL): haval.channel_no,
        }
    ),
)

SCHEMA_GET_LINK_PARAMSET = vol.All(
    {
        vol.Optional(CONF_RECEIVER_CHANNEL_ADDRESS): haval.channel_address,
        vol.Optional(CONF_SENDER_CHANNEL_ADDRESS): haval.channel_address,
    }
)

SCHEMA_GET_PARAMSET = vol.All(
    cv.has_at_least_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    cv.has_at_most_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    BASE_SCHEMA_DEVICE.extend(
        {
            vol.Optional(CONF_CHANNEL): haval.channel_no,
            vol.Required(CONF_PARAMSET_KEY): vol.All(haval.paramset_key, vol.In(["MASTER", "VALUES"])),
        }
    ),
)

SCHEMA_GET_VARIABLE_VALUE = vol.Schema(
    {
        vol.Required(CONF_ENTRY_ID): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)

SCHEMA_RECORD_SESSION = vol.Schema(
    {
        vol.Required(CONF_ENTRY_ID): cv.string,
        vol.Required(CONF_ON_TIME): cv.positive_int,
        vol.Required(CONF_RANDOMIZE_OUTPUT): cv.boolean,
    }
)

SCHEMA_REMOVE_CENTRAL_LINKS = vol.All(
    cv.has_at_least_one_key(CONF_DEVICE_ID, CONF_ENTRY_ID),
    cv.has_at_most_one_key(CONF_DEVICE_ID, CONF_ENTRY_ID),
    vol.Schema(
        {
            vol.Optional(CONF_ENTRY_ID): cv.string,
            vol.Optional(CONF_DEVICE_ID): cv.string,
        }
    ),
)

SCHEMA_REMOVE_LINK = vol.All(
    {
        vol.Required(CONF_RECEIVER_CHANNEL_ADDRESS): haval.channel_address,
        vol.Required(CONF_SENDER_CHANNEL_ADDRESS): haval.channel_address,
    }
)

SCHEMA_SET_VARIABLE_VALUE = vol.Schema(
    {
        vol.Required(CONF_ENTRY_ID): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_VALUE): cv.match_all,
    }
)

SCHEMA_SET_DEVICE_VALUE = vol.All(
    cv.has_at_least_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    cv.has_at_most_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    BASE_SCHEMA_DEVICE.extend(
        {
            vol.Required(CONF_CHANNEL, default=DEFAULT_CHANNEL): haval.channel_no,
            vol.Required(CONF_PARAMETER): vol.All(cv.string, vol.Upper),
            vol.Required(CONF_VALUE): cv.match_all,
            vol.Optional(CONF_WAIT_FOR_CALLBACK): haval.wait_for,
            vol.Optional(CONF_VALUE_TYPE): vol.In(["boolean", "dateTime.iso8601", "double", "int", "string"]),
            vol.Optional(CONF_RX_MODE): vol.All(cv.string, vol.Upper),
        }
    ),
)

SCHEMA_PUT_LINK_PARAMSET = vol.All(
    {
        vol.Optional(CONF_RECEIVER_CHANNEL_ADDRESS): haval.channel_address,
        vol.Optional(CONF_SENDER_CHANNEL_ADDRESS): haval.channel_address,
        vol.Required(CONF_PARAMSET): dict,
        vol.Optional(CONF_RX_MODE): vol.All(cv.string, vol.Upper),
    }
)

SCHEMA_PUT_PARAMSET = vol.All(
    cv.has_at_least_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    cv.has_at_most_one_key(CONF_DEVICE_ID, CONF_DEVICE_ADDRESS),
    BASE_SCHEMA_DEVICE.extend(
        {
            vol.Optional(CONF_CHANNEL): haval.channel_no,
            vol.Required(CONF_PARAMSET_KEY): vol.All(haval.paramset_key, vol.In(["MASTER", "VALUES"])),
            vol.Required(CONF_PARAMSET): dict,
            vol.Optional(CONF_WAIT_FOR_CALLBACK): haval.wait_for,
            vol.Optional(CONF_RX_MODE): vol.All(cv.string, vol.Upper),
        }
    ),
)

SCHEMA_UPDATE_DEVICE_FIRMWARE_DATA = vol.Schema(
    {
        vol.Required(CONF_ENTRY_ID): cv.string,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Create the aiohomematic services."""

    @verify_domain_control(DOMAIN)
    async def async_call_hmip_local_service(service: ServiceCall) -> ServiceResponse:
        """Call correct Homematic(IP) Local for OpenCCU service."""
        service_name = service.service

        if service_name == HmipLocalServices.CREATE_CENTRAL_LINKS:
            await _async_service_create_central_link(hass=hass, service=service)
        elif service_name == HmipLocalServices.ADD_LINK:
            await _async_service_add_link(hass=hass, service=service)
        elif service_name == HmipLocalServices.CLEAR_CACHE:
            await _async_service_clear_cache(hass=hass, service=service)
        elif service_name == HmipLocalServices.EXPORT_DEVICE_DEFINITION:
            await _async_service_export_device_definition(hass=hass, service=service)
        elif service_name == HmipLocalServices.FETCH_SYSTEM_VARIABLES:
            await _async_service_fetch_system_variables(hass=hass, service=service)
        elif service_name == HmipLocalServices.FORCE_DEVICE_AVAILABILITY:
            await _async_service_force_device_availability(hass=hass, service=service)
        elif service_name == HmipLocalServices.GET_DEVICE_VALUE:
            return await _async_service_get_device_value(hass=hass, service=service)
        elif service_name == HmipLocalServices.GET_LINK_PEERS:
            return await _async_service_get_link_peers(hass=hass, service=service)
        elif service_name == HmipLocalServices.GET_LINK_PARAMSET:
            return await _async_service_get_link_paramset(hass=hass, service=service)
        elif service_name == HmipLocalServices.GET_PARAMSET:
            return await _async_service_get_paramset(hass=hass, service=service)
        elif service_name == HmipLocalServices.GET_VARIABLE_VALUE:
            return await _async_service_get_variable_value(hass=hass, service=service)
        elif service_name == HmipLocalServices.PUT_LINK_PARAMSET:
            await _async_service_put_link_paramset(hass=hass, service=service)
        elif service_name == HmipLocalServices.PUT_PARAMSET:
            await _async_service_put_paramset(hass=hass, service=service)
        elif service_name == HmipLocalServices.RECORD_SESSION:
            await _async_service_record_session(hass=hass, service=service)
        elif service_name == HmipLocalServices.REMOVE_CENTRAL_LINKS:
            await _async_service_remove_central_link(hass=hass, service=service)
        elif service_name == HmipLocalServices.REMOVE_LINK:
            await _async_service_remove_link(hass=hass, service=service)
        elif service_name == HmipLocalServices.SET_DEVICE_VALUE:
            await _async_service_set_device_value(hass=hass, service=service)
        elif service_name == HmipLocalServices.SET_VARIABLE_VALUE:
            await _async_service_set_variable_value(hass=hass, service=service)
        elif service_name == HmipLocalServices.UPDATE_DEVICE_FIRMWARE_DATA:
            await _async_service_update_device_firmware_data(hass=hass, service=service)
        return None

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.ADD_LINK,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_ADD_LINK,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.CREATE_CENTRAL_LINKS,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_CREATE_CENTRAL_LINKS,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.CLEAR_CACHE,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_CLEAR_CACHE,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.EXPORT_DEVICE_DEFINITION,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_EXPORT_DEVICE_DEFINITION,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.FETCH_SYSTEM_VARIABLES,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_FETCH_SYSTEM_VARIABLES,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.FORCE_DEVICE_AVAILABILITY,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_FORCE_DEVICE_AVAILABILITY,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.GET_DEVICE_VALUE,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_GET_DEVICE_VALUE,
        supports_response=SupportsResponse.OPTIONAL,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.GET_LINK_PEERS,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_GET_LINK_PEERS,
        supports_response=SupportsResponse.OPTIONAL,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.GET_LINK_PARAMSET,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_GET_LINK_PARAMSET,
        supports_response=SupportsResponse.OPTIONAL,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.GET_PARAMSET,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_GET_PARAMSET,
        supports_response=SupportsResponse.OPTIONAL,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.GET_VARIABLE_VALUE,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_GET_VARIABLE_VALUE,
        supports_response=SupportsResponse.OPTIONAL,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.RECORD_SESSION,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_RECORD_SESSION,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.REMOVE_CENTRAL_LINKS,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_REMOVE_CENTRAL_LINKS,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.REMOVE_LINK,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_REMOVE_LINK,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.SET_VARIABLE_VALUE,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_SET_VARIABLE_VALUE,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.SET_DEVICE_VALUE,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_SET_DEVICE_VALUE,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.PUT_LINK_PARAMSET,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_PUT_LINK_PARAMSET,
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=HmipLocalServices.PUT_PARAMSET,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_PUT_PARAMSET,
    )

    async_register_admin_service(
        hass=hass,
        domain=DOMAIN,
        service=HmipLocalServices.UPDATE_DEVICE_FIRMWARE_DATA,
        service_func=async_call_hmip_local_service,
        schema=SCHEMA_UPDATE_DEVICE_FIRMWARE_DATA,
    )

    ############################## Platform specific registrations ##############################

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.ENABLE_AWAY_MODE_BY_CALENDAR,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Optional(ATTR_AWAY_START): cv.datetime,
            vol.Required(ATTR_AWAY_END): cv.datetime,
            vol.Required(ATTR_AWAY_TEMPERATURE, default=18.0): vol.All(vol.Coerce(float), vol.Range(min=5.0, max=30.5)),
        },
        func="async_enable_away_mode_by_calendar",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.ENABLE_AWAY_MODE_BY_DURATION,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Required(ATTR_AWAY_HOURS): cv.positive_int,
            vol.Required(ATTR_AWAY_TEMPERATURE, default=18.0): vol.All(vol.Coerce(float), vol.Range(min=5.0, max=30.5)),
        },
        func="async_enable_away_mode_by_duration",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.DISABLE_AWAY_MODE,
        entity_domain=CLIMATE_DOMAIN,
        schema={},
        func="async_disable_away_mode",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.COPY_SCHEDULE,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Required(ATTR_SOURCE_ENTITY_ID): cv.string,
        },
        func="async_copy_schedule",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.COPY_SCHEDULE_PROFILE,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Optional(ATTR_SOURCE_ENTITY_ID): cv.string,
            vol.Required(ATTR_SOURCE_PROFILE): cv.string,
            vol.Required(ATTR_TARGET_PROFILE): cv.string,
        },
        func="async_copy_schedule_profile",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.GET_SCHEDULE_PROFILE,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Required(ATTR_PROFILE): cv.string,
        },
        func="async_get_schedule_profile",
        supports_response=SupportsResponse.OPTIONAL,
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.GET_SCHEDULE_PROFILE_WEEKDAY,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Required(ATTR_PROFILE): cv.string,
            vol.Required(ATTR_WEEKDAY): cv.string,
        },
        func="async_get_schedule_profile_weekday",
        supports_response=SupportsResponse.OPTIONAL,
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.SET_SCHEDULE_PROFILE,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Required(ATTR_PROFILE): cv.string,
            vol.Required(ATTR_PROFILE_DATA): dict,
        },
        func="async_set_schedule_profile",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.SET_SCHEDULE_PROFILE_WEEKDAY,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Required(ATTR_PROFILE): cv.string,
            vol.Required(ATTR_WEEKDAY): cv.string,
            vol.Required(ATTR_WEEKDAY_DATA): dict,
        },
        func="async_set_schedule_profile_weekday",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.SET_SCHEDULE_SIMPLE_PROFILE,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Required(ATTR_PROFILE): cv.string,
            vol.Required(ATTR_BASE_TEMPERATURE): cv.positive_float,
            vol.Required(ATTR_SIMPLE_PROFILE_DATA): dict,
        },
        func="async_set_schedule_simple_profile",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.SET_SCHEDULE_SIMPLE_PROFILE_WEEKDAY,
        entity_domain=CLIMATE_DOMAIN,
        schema={
            vol.Required(ATTR_PROFILE): cv.string,
            vol.Required(ATTR_WEEKDAY): cv.string,
            vol.Required(ATTR_BASE_TEMPERATURE): cv.positive_float,
            vol.Required(ATTR_SIMPLE_WEEKDAY_LIST): list,
        },
        func="async_set_schedule_simple_profile_weekday",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.SET_COVER_COMBINED_POSITION,
        entity_domain=COVER_DOMAIN,
        schema={
            vol.Required(ATTR_POSITION): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Optional(ATTR_TILT_POSITION): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Optional(CONF_WAIT_FOR_CALLBACK): cv.positive_int,
        },
        func="async_set_cover_combined_position",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.LIGHT_SET_ON_TIME,
        entity_domain=LIGHT_DOMAIN,
        schema={vol.Required(ATTR_ON_TIME): vol.All(vol.Coerce(int), vol.Range(min=-1, max=8580000))},
        func="async_set_on_time",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.TURN_ON_SIREN,
        entity_domain=SIREN_DOMAIN,
        schema={
            vol.Optional(ATTR_TONE): cv.string,
            vol.Optional(ATTR_LIGHT): cv.string,
            vol.Optional(ATTR_DURATION): cv.positive_int,
        },
        func="async_turn_on",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.SWITCH_SET_ON_TIME,
        entity_domain=SWITCH_DOMAIN,
        schema={vol.Required(ATTR_ON_TIME): vol.All(vol.Coerce(int), vol.Range(min=-1, max=8580000))},
        func="async_set_on_time",
    )

    async_register_platform_entity_service(
        hass=hass,
        service_domain=DOMAIN,
        service_name=HmipLocalServices.VALVE_SET_ON_TIME,
        entity_domain=VALVE_DOMAIN,
        schema={vol.Required(ATTR_ON_TIME): vol.All(vol.Coerce(int), vol.Range(min=-1, max=8580000))},
        func="async_set_on_time",
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Homematic(IP) Local for OpenCCU services."""
    if len(async_get_loaded_config_entries(hass=hass)) > 0:
        return

    for hmip_local_service in HmipLocalServices:
        hass.services.async_remove(domain=DOMAIN, service=hmip_local_service)


async def _async_service_add_link(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to call the addLink method for link creation on a Homematic(IP) Local for OpenCCU connection."""
    sender_channel_address = service.data[CONF_SENDER_CHANNEL_ADDRESS]
    receiver_channel_address = service.data[CONF_RECEIVER_CHANNEL_ADDRESS]
    name = service.data.get(CONF_NAME, f"{sender_channel_address} -> {receiver_channel_address}")
    description = service.data.get(CONF_DESCRIPTION, "created by HA")

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        try:
            await hm_device.client.add_link(
                sender_address=sender_channel_address,
                receiver_address=receiver_channel_address,
                name=name,
                description=description,
            )
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc
        _LOGGER.debug("Called add_link")


async def _async_service_create_central_link(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to create central links for Homematic(IP) Local for OpenCCU devices."""
    try:
        if (entry_id := service.data.get(CONF_ENTRY_ID)) is not None and (
            control := _async_get_control_unit(hass=hass, entry_id=entry_id)
        ) is not None:
            await control.central.create_central_links()
        elif hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
            await hm_device.create_central_links()
    except BaseHomematicException as bhexc:
        raise HomeAssistantError(bhexc) from bhexc
    _LOGGER.debug("Called create_central_links")


async def _async_service_remove_central_link(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to remove central links for Homematic(IP) Local for OpenCCU devices."""
    try:
        if (entry_id := service.data.get(CONF_ENTRY_ID)) is not None and (
            control := _async_get_control_unit(hass=hass, entry_id=entry_id)
        ) is not None:
            await control.central.remove_central_links()
        elif hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
            await hm_device.remove_central_links()
    except BaseHomematicException as bhexc:
        raise HomeAssistantError(bhexc) from bhexc
    _LOGGER.debug("Called remove_central_links")


async def _async_service_remove_link(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to call the removeLink method for link removal on a Homematic(IP) Local for OpenCCU connection."""
    sender_channel_address = service.data[CONF_SENDER_CHANNEL_ADDRESS]
    receiver_channel_address = service.data[CONF_RECEIVER_CHANNEL_ADDRESS]

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        try:
            await hm_device.client.remove_link(
                sender_address=sender_channel_address,
                receiver_address=receiver_channel_address,
            )
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc
        _LOGGER.debug("Called remove_link")


async def _async_service_export_device_definition(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to call setValue method for Homematic(IP) Local for OpenCCU devices."""
    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        try:
            await hm_device.export_device_definition()
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc

        _LOGGER.debug(
            "Called export_device_definition: %s, %s",
            hm_device.name,
            hm_device.address,
        )


async def _async_service_force_device_availability(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to force device availability on a Homematic(IP) Local for OpenCCU devices."""
    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        hm_device.set_forced_availability(forced_availability=ForcedDeviceAvailability.FORCE_TRUE)
        _LOGGER.debug(
            "Called force_device_availability: %s, %s",
            hm_device.name,
            hm_device.address,
        )


async def _async_service_get_device_value(hass: HomeAssistant, service: ServiceCall) -> ServiceResponse:
    """Service to call getValue method for Homematic(IP) Local for OpenCCU devices."""
    channel_no = service.data[CONF_CHANNEL]
    parameter = service.data[CONF_PARAMETER]

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        try:
            if (
                value := await hm_device.client.get_value(
                    channel_address=f"{hm_device.address}:{channel_no}",
                    paramset_key=ParamsetKey.VALUES,
                    parameter=parameter,
                )
            ) is not None:
                return {"result": value}
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc
    return None


async def _async_service_get_link_peers(hass: HomeAssistant, service: ServiceCall) -> ServiceResponse:
    """Service to call the getLinkPeers method on a Homematic(IP) Local for OpenCCU connection."""
    channel_no = service.data.get(CONF_CHANNEL)

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        address = f"{hm_device.address}:{channel_no}" if channel_no is not None else hm_device.address
        try:
            return cast(ServiceResponse, {address: await hm_device.client.get_link_peers(address=address)})
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc
    return None


async def _async_service_get_link_paramset(hass: HomeAssistant, service: ServiceCall) -> ServiceResponse:
    """Service to call the getParamset method for links on a Homematic(IP) Local for OpenCCU connection."""
    sender_channel_address = service.data[CONF_SENDER_CHANNEL_ADDRESS]
    receiver_channel_address = service.data[CONF_RECEIVER_CHANNEL_ADDRESS]

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        try:
            return dict(
                await hm_device.client.get_paramset(
                    address=receiver_channel_address,
                    paramset_key=sender_channel_address,
                )
            )
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc
    return None


async def _async_service_get_paramset(hass: HomeAssistant, service: ServiceCall) -> ServiceResponse:
    """Service to call the getParamset method on a Homematic(IP) Local for OpenCCU connection."""
    channel_no = service.data.get(CONF_CHANNEL)
    paramset_key = ParamsetKey(service.data[CONF_PARAMSET_KEY])

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        address = f"{hm_device.address}:{channel_no}" if channel_no is not None else hm_device.address
        try:
            return dict(
                await hm_device.client.get_paramset(
                    address=address,
                    paramset_key=paramset_key,
                )
            )
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc
    return None


async def _async_service_get_variable_value(hass: HomeAssistant, service: ServiceCall) -> ServiceResponse:
    """Service to call read value from Homematic(IP) Local for OpenCCU system variable."""
    entry_id = service.data[CONF_ENTRY_ID]
    name = service.data[CONF_NAME]

    if control := _async_get_control_unit(hass=hass, entry_id=entry_id):
        try:
            if (value := await control.central.get_system_variable(legacy_name=name)) is not None:
                return {"result": value}
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc
    return None


async def _async_service_set_device_value(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to call setValue method for Homematic(IP) Local for OpenCCU devices."""
    channel_no = service.data[CONF_CHANNEL]
    parameter = service.data[CONF_PARAMETER]
    value = service.data[CONF_VALUE]
    value_type = service.data.get(CONF_VALUE_TYPE)
    wait_for_callback = service.data.get(CONF_WAIT_FOR_CALLBACK)
    rx_mode = service.data.get(CONF_RX_MODE)
    if value_type:
        # Convert value into correct XML-RPC Type.
        # https://docs.python.org/3/library/xmlrpc.client.html#xmlrpc.client.ServerProxy
        if value_type == "int":
            value = int(value)
        elif value_type == "double":
            value = float(value)
        elif value_type == "boolean":
            value = to_bool(value=value)
        elif value_type == "dateTime.iso8601":
            value = datetime.strptime(value, "%Y%m%dT%H:%M:%S")
        else:
            # Default is 'string'
            value = str(value)

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        try:
            await hm_device.client.set_value(
                channel_address=f"{hm_device.address}:{channel_no}",
                paramset_key=ParamsetKey.VALUES,
                parameter=parameter,
                value=value,
                wait_for_callback=wait_for_callback,
                rx_mode=rx_mode,
                check_against_pd=True,
            )
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc


async def _async_service_set_variable_value(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to call setValue method for Homematic(IP) Local for OpenCCU system variable."""
    entry_id = service.data[CONF_ENTRY_ID]
    name = service.data[CONF_NAME]
    value = service.data[CONF_VALUE]

    if control := _async_get_control_unit(hass=hass, entry_id=entry_id):
        await control.central.set_system_variable(legacy_name=name, value=value)


async def _async_service_clear_cache(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to clear the cache."""
    entry_id = service.data[CONF_ENTRY_ID]
    if control := _async_get_control_unit(hass=hass, entry_id=entry_id):
        await control.central.clear_files()


async def _async_service_fetch_system_variables(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to fetch system variables from backend."""
    entry_id = service.data[CONF_ENTRY_ID]
    if control := _async_get_control_unit(hass=hass, entry_id=entry_id):
        await control.central.fetch_program_data(scheduled=False)
        await control.central.fetch_sysvar_data(scheduled=False)


async def _async_service_put_link_paramset(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to call the putParamset method for link manipulation on a Homematic(IP) Local for OpenCCU connection."""
    sender_channel_address = service.data[CONF_SENDER_CHANNEL_ADDRESS]
    receiver_channel_address = service.data[CONF_RECEIVER_CHANNEL_ADDRESS]
    # When passing in the paramset from a YAML file we get an OrderedDict
    # here instead of a dict, so add this explicit cast.
    # The service schema makes sure that this cast works.
    values = dict(service.data[CONF_PARAMSET])
    rx_mode = service.data.get(CONF_RX_MODE)

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        try:
            await hm_device.client.put_paramset(
                channel_address=receiver_channel_address,
                paramset_key_or_link_address=sender_channel_address,
                values=values,
                rx_mode=rx_mode,
                check_against_pd=True,
            )
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc


async def _async_service_put_paramset(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to call the putParamset method on a Homematic(IP) Local for OpenCCU connection."""
    channel_no = service.data.get(CONF_CHANNEL)
    paramset_key = ParamsetKey(service.data[CONF_PARAMSET_KEY])
    # When passing in the paramset from a YAML file we get an OrderedDict
    # here instead of a dict, so add this explicit cast.
    # The service schema makes sure that this cast works.
    values = dict(service.data[CONF_PARAMSET])
    wait_for_callback = service.data.get(CONF_WAIT_FOR_CALLBACK)
    rx_mode = service.data.get(CONF_RX_MODE)

    if hm_device := _async_get_hm_device_by_service_data(hass=hass, service=service):
        channel_address = f"{hm_device.address}:{channel_no}" if channel_no is not None else hm_device.address
        try:
            await hm_device.client.put_paramset(
                channel_address=channel_address,
                paramset_key_or_link_address=paramset_key,
                values=values,
                wait_for_callback=wait_for_callback,
                rx_mode=rx_mode,
                check_against_pd=True,
            )
        except BaseHomematicException as bhexc:
            raise HomeAssistantError(bhexc) from bhexc


async def _async_service_record_session(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to clear the cache."""
    entry_id = service.data[CONF_ENTRY_ID]
    on_time = service.data[CONF_ON_TIME]
    randomize_output = service.data[CONF_RANDOMIZE_OUTPUT]

    if control := _async_get_control_unit(hass=hass, entry_id=entry_id):
        await control.central.recorder.activate(
            on_time=on_time, auto_save=True, randomize_output=randomize_output, use_ts_in_file_name=True
        )


async def _async_service_update_device_firmware_data(hass: HomeAssistant, service: ServiceCall) -> None:
    """Service to clear the cache."""
    entry_id = service.data[CONF_ENTRY_ID]
    if control := _async_get_control_unit(hass=hass, entry_id=entry_id):
        await control.central.refresh_firmware_data()


@callback
def _async_get_control_unit(hass: HomeAssistant, entry_id: str) -> ControlUnit | None:
    """Get ControlUnit by entry_id."""
    entry: HomematicConfigEntry | None = hass.config_entries.async_get_entry(entry_id=entry_id)
    if entry and (control_unit := entry.runtime_data):
        return control_unit

    _LOGGER.warning("Config entry %s is deactivated or not available", entry_id)
    return None


@callback
def _async_get_hm_device_by_service_data(hass: HomeAssistant, service: ServiceCall) -> Device | None:
    """Service to force device availability on a Homematic(IP) Local for OpenCCU devices."""
    hm_device: Device | None = None
    message = "No device found"

    if device_id := service.data.get(CONF_DEVICE_ID):
        hm_device = _asnyc_get_hm_device_by_id(hass=hass, device_id=device_id)
        if not hm_device:
            message = f"No device found by device_id {device_id} for service {service.domain}.{service.service}"
    elif device_address := service.data.get(CONF_DEVICE_ADDRESS):
        hm_device = _async_get_hm_device_by_address(hass=hass, device_address=device_address)
        if not hm_device:
            message = (
                f"No device found by device_address {device_address} for service {service.domain}.{service.service}"
            )
    elif channel_address := service.data.get(CONF_CHANNEL_ADDRESS):
        hm_device = _async_get_hm_device_by_address(
            hass=hass, device_address=get_device_address(address=channel_address)
        )
        if not hm_device:
            message = (
                f"No device found by channel_address {channel_address} for service {service.domain}.{service.service}"
            )
    elif receiver_channel_address := service.data.get(CONF_RECEIVER_CHANNEL_ADDRESS):
        hm_device = _async_get_hm_device_by_address(
            hass=hass, device_address=get_device_address(address=receiver_channel_address)
        )
        if not hm_device:
            message = f"No device found by receiver_channel_address {receiver_channel_address} for service {service.domain}.{service.service}"
    if not hm_device:
        _LOGGER.warning(message)
        raise HomeAssistantError(message)
    return hm_device


@callback
def async_get_config_entries(hass: HomeAssistant) -> list[HomematicConfigEntry]:
    """Get config entries for HomematicIP local."""
    return hass.config_entries.async_entries(domain=DOMAIN, include_ignore=False, include_disabled=False)


@callback
def async_get_loaded_config_entries(hass: HomeAssistant) -> list[HomematicConfigEntry]:
    """Get config entries for HomematicIP local."""
    return [
        entry
        for entry in hass.config_entries.async_entries(domain=DOMAIN, include_ignore=False, include_disabled=False)
        if entry.state == ConfigEntryState.LOADED
    ]


@callback
def _async_get_control_units(hass: HomeAssistant) -> list[ControlUnit]:
    """Get control units for HomematicIP local."""
    return [entry.runtime_data for entry in async_get_config_entries(hass=hass)]


@callback
def _async_get_hm_device_by_address(hass: HomeAssistant, device_address: str) -> Device | None:
    """Return the Homematic device."""
    for control_unit in _async_get_control_units(hass=hass):
        if hm_device := control_unit.central.get_device(address=device_address):
            return hm_device
    return None


@callback
def _async_get_cu_by_interface_id(hass: HomeAssistant, interface_id: str) -> ControlUnit | None:
    """Get ControlUnit by interface_id."""
    for control_unit in _async_get_control_units(hass=hass):
        if control_unit.central.has_client(interface_id=interface_id):
            return control_unit
    return None


@callback
def _asnyc_get_hm_device_by_id(hass: HomeAssistant, device_id: str) -> Device | None:
    """Return the Homematic device."""
    device_entry: DeviceEntry | None = dr.async_get(hass).async_get(device_id)
    if not device_entry:
        return None
    if (data := get_device_address_at_interface_from_identifiers(identifiers=device_entry.identifiers)) is None:
        return None
    device_address, interface_id = data
    for control_unit in _async_get_control_units(hass=hass):
        if control_unit.central.has_client(interface_id=interface_id) and (
            hm_device := control_unit.central.get_device(address=device_address)
        ):
            return hm_device
    return None
