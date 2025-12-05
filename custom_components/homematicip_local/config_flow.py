"""Config flow for Homematic(IP) Local for OpenCCU."""

from __future__ import annotations

import asyncio
import logging
from pprint import pformat
from typing import Any, Final, cast
from urllib.parse import urlparse

import voluptuous as vol
from voluptuous.schema_builder import UNDEFINED, Schema

from aiohomematic.backend_detection import BackendDetectionResult, DetectionConfig, detect_backend
from aiohomematic.const import (
    DEFAULT_ENABLE_PROGRAM_SCAN,
    DEFAULT_ENABLE_SYSVAR_SCAN,
    DEFAULT_JSON_RPC_PORT,
    DEFAULT_JSON_RPC_TLS_PORT,
    DEFAULT_OPTIONAL_SETTINGS,
    DEFAULT_PROGRAM_MARKERS,
    DEFAULT_SYS_SCAN_INTERVAL,
    DEFAULT_SYSVAR_MARKERS,
    DEFAULT_TLS,
    DEFAULT_UN_IGNORES,
    DEFAULT_USE_GROUP_CHANNEL_FOR_COVER_STATE,
    DescriptionMarker,
    Interface,
    OptionalSettings,
    SystemInformation,
    get_interface_default_port,
    get_json_rpc_default_port,
    is_interface_default_port,
)
from aiohomematic.exceptions import AuthFailure, BaseHomematicException, NoConnectionException, ValidationException
from homeassistant.config_entries import CONN_CLASS_LOCAL_PUSH, ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_PATH, CONF_PORT, CONF_USERNAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.selector import (
    BooleanSelector,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
from homeassistant.helpers.service_info import ssdp
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_ADVANCED_CONFIG,
    CONF_BACKUP_PATH,
    CONF_CALLBACK_HOST,
    CONF_CALLBACK_PORT_XML_RPC,
    CONF_CUSTOM_PORT_CONFIG,
    CONF_CUSTOM_PORTS,
    CONF_ENABLE_MQTT,
    CONF_ENABLE_PROGRAM_SCAN,
    CONF_ENABLE_SUB_DEVICES,
    CONF_ENABLE_SYSTEM_NOTIFICATIONS,
    CONF_ENABLE_SYSVAR_SCAN,
    CONF_INSTANCE_NAME,
    CONF_INTERFACE,
    CONF_JSON_PORT,
    CONF_LISTEN_ON_ALL_IP,
    CONF_MQTT_PREFIX,
    CONF_OPTIONAL_SETTINGS,
    CONF_PROGRAM_MARKERS,
    CONF_SYS_SCAN_INTERVAL,
    CONF_SYSVAR_MARKERS,
    CONF_TLS,
    CONF_UN_IGNORES,
    CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE,
    CONF_VERIFY_TLS,
    DEFAULT_BACKUP_PATH,
    DEFAULT_ENABLE_MQTT,
    DEFAULT_ENABLE_SUB_DEVICES,
    DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS,
    DEFAULT_LISTEN_ON_ALL_IP,
    DEFAULT_MQTT_PREFIX,
    DOMAIN,
)
from .control_unit import ControlConfig, ControlUnit, validate_config_and_get_system_information
from .support import InvalidConfig

# Step indicator constants for config flow
STEP_CENTRAL: Final = "1"
STEP_INTERFACE: Final = "2"
STEP_TLS_INTERFACES: Final = "2"
STEP_ADVANCED: Final = "3"
TOTAL_STEPS_BASIC: Final = "2"
TOTAL_STEPS_ADVANCED: Final = "3"

# Reconfigure flow steps
STEP_RECONFIGURE: Final = "1"
STEP_RECONFIGURE_TLS: Final = "2"
TOTAL_STEPS_RECONFIGURE: Final = "2"

_LOGGER = logging.getLogger(__name__)

# Interface enable/disable config keys
CONF_BIDCOS_RF_PORT: Final = "bidcos_rf_port"
CONF_BIDCOS_WIRED_PORT: Final = "bidcos_wired_port"
CONF_ENABLE_BIDCOS_RF: Final = "bidcos_rf_enabled"
CONF_ENABLE_BIDCOS_WIRED: Final = "bidcos_wired_enabled"
CONF_ENABLE_CCU_JACK: Final = "ccu_jack_enabled"
CONF_ENABLE_CUXD: Final = "cuxd_enabled"
CONF_ENABLE_HMIP_RF: Final = "hmip_rf_enabled"
CONF_ENABLE_VIRTUAL_DEVICES: Final = "virtual_devices_enabled"
CONF_HMIP_RF_PORT: Final = "hmip_rf_port"
CONF_VIRTUAL_DEVICES_PATH: Final = "virtual_devices_path"
CONF_VIRTUAL_DEVICES_PORT: Final = "virtual_devices_port"
CONF_RESET_PORT_DEFAULTS: Final = "reset_port_defaults"

# VirtualDevices path constant
IF_VIRTUAL_DEVICES_PATH: Final = "/groups"
TEXT_SELECTOR = TextSelector(TextSelectorConfig(type=TextSelectorType.TEXT))
PASSWORD_SELECTOR = TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD))
BOOLEAN_SELECTOR = BooleanSelector()
PORT_SELECTOR = vol.All(
    NumberSelector(NumberSelectorConfig(mode=NumberSelectorMode.BOX, min=1, max=65535)),
    vol.Coerce(int),
)
PORT_SELECTOR_OPTIONAL = vol.All(
    NumberSelector(NumberSelectorConfig(mode=NumberSelectorMode.BOX, min=0, max=65535)),
    vol.Coerce(int),
)
SCAN_INTERVAL_SELECTOR = vol.All(
    NumberSelector(NumberSelectorConfig(mode=NumberSelectorMode.BOX, min=5, step="any", unit_of_measurement="sec")),
    vol.Coerce(int),
)


def get_domain_schema(data: ConfigType) -> Schema:
    """Return the central/connection schema (callback settings are in advanced step)."""
    return vol.Schema(
        {
            vol.Required(CONF_INSTANCE_NAME, default=data.get(CONF_INSTANCE_NAME) or UNDEFINED): TEXT_SELECTOR,
            vol.Required(CONF_HOST, default=data.get(CONF_HOST)): TEXT_SELECTOR,
            vol.Required(CONF_USERNAME, default=data.get(CONF_USERNAME)): TEXT_SELECTOR,
            vol.Required(CONF_PASSWORD, default=data.get(CONF_PASSWORD)): PASSWORD_SELECTOR,
        }
    )


def get_options_schema(data: ConfigType) -> Schema:
    """Return the options schema (callback settings are in advanced_settings step)."""
    return vol.Schema(
        {
            vol.Required(CONF_HOST, default=data.get(CONF_HOST)): TEXT_SELECTOR,
            vol.Required(CONF_USERNAME, default=data.get(CONF_USERNAME)): TEXT_SELECTOR,
            vol.Required(CONF_PASSWORD, default=data.get(CONF_PASSWORD)): PASSWORD_SELECTOR,
        }
    )


def get_reconfigure_schema(data: ConfigType) -> Schema:
    """Return the reconfigure schema with only connection settings (TLS on next step)."""
    return vol.Schema(
        {
            vol.Required(CONF_HOST, default=data.get(CONF_HOST)): TEXT_SELECTOR,
            vol.Required(CONF_USERNAME, default=data.get(CONF_USERNAME)): TEXT_SELECTOR,
            vol.Required(CONF_PASSWORD, default=data.get(CONF_PASSWORD)): PASSWORD_SELECTOR,
        }
    )


def _get_step_placeholders(step: str, total: str) -> dict[str, str]:
    """Return description placeholders with step indicators."""
    return {
        "step_current": step,
        "step_total": total,
    }


def _get_retry_hint(error_type: str) -> str:
    """Return a retry hint based on the error type."""
    hints = {
        "invalid_auth": "verify_credentials",
        "cannot_connect": "check_network",
        "detection_failed": "check_ccu_settings",
        "invalid_config": "check_config_values",
    }
    return hints.get(error_type, "check_settings")


def _get_effective_port(interface: Interface, tls: bool, data: ConfigType) -> int:
    """Get the effective port for an interface - custom or TLS-based default."""
    custom_ports: dict[str, int] = data.get(CONF_CUSTOM_PORTS, {})
    interfaces: dict[Interface, dict[str, Any]] = data.get(CONF_INTERFACE, {})

    # Check for custom port in new format
    if interface.value in custom_ports:
        return int(custom_ports[interface.value])

    # Check for custom port in legacy interface format
    if interface in interfaces and CONF_PORT in interfaces[interface]:
        port: int = interfaces[interface][CONF_PORT]
        # Only return if it's a custom (non-default) port
        if not is_interface_default_port(interface, port):
            return port

    # Return TLS-based default
    return int(get_interface_default_port(interface, tls=tls) or 0)


def _get_effective_json_port(tls: bool, data: ConfigType) -> int:
    """Get the effective JSON-RPC port - custom or TLS-based default."""
    custom_port: int | None = data.get(CONF_JSON_PORT)
    if custom_port and custom_port not in (DEFAULT_JSON_RPC_PORT, DEFAULT_JSON_RPC_TLS_PORT):
        return int(custom_port)
    return int(get_json_rpc_default_port(tls=tls))


def get_tls_interfaces_schema(data: ConfigType, show_custom_ports_option: bool = True) -> Schema:
    """
    Return the TLS & interfaces schema (without ports - for simplified flow).

    Args:
        data: Configuration data
        show_custom_ports_option: Whether to show the custom port config checkbox

    """
    interfaces = data.get(CONF_INTERFACE, {})

    schema_dict: dict[Any, Any] = {
        # TLS settings
        vol.Required(CONF_TLS, default=data.get(CONF_TLS, False)): BOOLEAN_SELECTOR,
        vol.Required(CONF_VERIFY_TLS, default=data.get(CONF_VERIFY_TLS, False)): BOOLEAN_SELECTOR,
        # Interface checkboxes only (no ports)
        vol.Required(CONF_ENABLE_HMIP_RF, default=Interface.HMIP_RF in interfaces): BOOLEAN_SELECTOR,
        vol.Required(CONF_ENABLE_BIDCOS_RF, default=Interface.BIDCOS_RF in interfaces): BOOLEAN_SELECTOR,
        vol.Required(CONF_ENABLE_VIRTUAL_DEVICES, default=Interface.VIRTUAL_DEVICES in interfaces): BOOLEAN_SELECTOR,
        vol.Required(CONF_ENABLE_BIDCOS_WIRED, default=Interface.BIDCOS_WIRED in interfaces): BOOLEAN_SELECTOR,
        vol.Required(CONF_ENABLE_CCU_JACK, default=Interface.CCU_JACK in interfaces): BOOLEAN_SELECTOR,
        vol.Required(CONF_ENABLE_CUXD, default=Interface.CUXD in interfaces): BOOLEAN_SELECTOR,
    }

    # Add custom ports checkbox (for config flow, not for options flow which always shows ports)
    if show_custom_ports_option:
        schema_dict[vol.Optional(CONF_CUSTOM_PORT_CONFIG, default=False)] = BOOLEAN_SELECTOR

    return vol.Schema(schema_dict)


def get_port_config_schema(data: ConfigType) -> Schema:
    """
    Return the port configuration schema (for custom port configuration).

    Shows only JSON-RPC port and ports for enabled interfaces.
    Callback settings have been moved to advanced configuration.
    """
    tls = data.get(CONF_TLS, False)
    interfaces = data.get(CONF_INTERFACE, {})

    schema_dict: dict[Any, Any] = {
        # JSON-RPC port (always shown)
        vol.Optional(CONF_JSON_PORT, default=_get_effective_json_port(tls, data)): PORT_SELECTOR_OPTIONAL,
    }

    # Add port fields only for enabled interfaces
    if Interface.HMIP_RF in interfaces:
        schema_dict[vol.Required(CONF_HMIP_RF_PORT, default=_get_effective_port(Interface.HMIP_RF, tls, data))] = (
            PORT_SELECTOR
        )
    if Interface.BIDCOS_RF in interfaces:
        schema_dict[vol.Required(CONF_BIDCOS_RF_PORT, default=_get_effective_port(Interface.BIDCOS_RF, tls, data))] = (
            PORT_SELECTOR
        )
    if Interface.VIRTUAL_DEVICES in interfaces:
        schema_dict[
            vol.Required(CONF_VIRTUAL_DEVICES_PORT, default=_get_effective_port(Interface.VIRTUAL_DEVICES, tls, data))
        ] = PORT_SELECTOR
        schema_dict[
            vol.Required(
                CONF_VIRTUAL_DEVICES_PATH,
                default=interfaces.get(Interface.VIRTUAL_DEVICES, {}).get(CONF_PATH, IF_VIRTUAL_DEVICES_PATH),
            )
        ] = TEXT_SELECTOR
    if Interface.BIDCOS_WIRED in interfaces:
        schema_dict[
            vol.Required(CONF_BIDCOS_WIRED_PORT, default=_get_effective_port(Interface.BIDCOS_WIRED, tls, data))
        ] = PORT_SELECTOR

    return vol.Schema(schema_dict)


def get_interface_schema(use_tls: bool, data: ConfigType) -> Schema:
    """Return the full interface schema with TLS settings and interface ports (legacy/options flow)."""
    interfaces = data.get(CONF_INTERFACE, {})

    return vol.Schema(
        {
            # TLS settings at top
            vol.Required(CONF_TLS, default=use_tls): BOOLEAN_SELECTOR,
            vol.Required(CONF_VERIFY_TLS, default=data.get(CONF_VERIFY_TLS, False)): BOOLEAN_SELECTOR,
            # JSON-RPC port
            vol.Optional(CONF_JSON_PORT, default=data.get(CONF_JSON_PORT) or UNDEFINED): PORT_SELECTOR_OPTIONAL,
            # Interface settings with ports
            vol.Required(CONF_ENABLE_HMIP_RF, default=Interface.HMIP_RF in interfaces): BOOLEAN_SELECTOR,
            vol.Required(
                CONF_HMIP_RF_PORT, default=_get_effective_port(Interface.HMIP_RF, use_tls, data)
            ): PORT_SELECTOR,
            vol.Required(CONF_ENABLE_BIDCOS_RF, default=Interface.BIDCOS_RF in interfaces): BOOLEAN_SELECTOR,
            vol.Required(
                CONF_BIDCOS_RF_PORT, default=_get_effective_port(Interface.BIDCOS_RF, use_tls, data)
            ): PORT_SELECTOR,
            vol.Required(
                CONF_ENABLE_VIRTUAL_DEVICES, default=Interface.VIRTUAL_DEVICES in interfaces
            ): BOOLEAN_SELECTOR,
            vol.Required(
                CONF_VIRTUAL_DEVICES_PORT, default=_get_effective_port(Interface.VIRTUAL_DEVICES, use_tls, data)
            ): PORT_SELECTOR,
            vol.Required(CONF_VIRTUAL_DEVICES_PATH, default=IF_VIRTUAL_DEVICES_PATH): TEXT_SELECTOR,
            vol.Required(CONF_ENABLE_BIDCOS_WIRED, default=Interface.BIDCOS_WIRED in interfaces): BOOLEAN_SELECTOR,
            vol.Required(
                CONF_BIDCOS_WIRED_PORT, default=_get_effective_port(Interface.BIDCOS_WIRED, use_tls, data)
            ): PORT_SELECTOR,
            vol.Required(CONF_ENABLE_CCU_JACK, default=Interface.CCU_JACK in interfaces): BOOLEAN_SELECTOR,
            vol.Required(CONF_ENABLE_CUXD, default=Interface.CUXD in interfaces): BOOLEAN_SELECTOR,
        }
    )


def get_advanced_schema(data: ConfigType, all_un_ignore_parameters: list[str]) -> Schema:
    """Return the advanced schema with all fields including callback settings."""
    existing_parameters: list[str] = [
        p
        for p in data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_UN_IGNORES, DEFAULT_UN_IGNORES)
        if p in all_un_ignore_parameters
    ]

    advanced_schema = vol.Schema(
        {
            # Callback settings (moved here from port config)
            vol.Optional(CONF_CALLBACK_HOST, default=data.get(CONF_CALLBACK_HOST) or UNDEFINED): TEXT_SELECTOR,
            vol.Optional(
                CONF_CALLBACK_PORT_XML_RPC, default=data.get(CONF_CALLBACK_PORT_XML_RPC) or UNDEFINED
            ): PORT_SELECTOR_OPTIONAL,
            vol.Required(
                CONF_LISTEN_ON_ALL_IP,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_LISTEN_ON_ALL_IP, DEFAULT_LISTEN_ON_ALL_IP),
            ): BOOLEAN_SELECTOR,
            # Program/Sysvar scanning
            vol.Required(
                CONF_ENABLE_PROGRAM_SCAN,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_ENABLE_PROGRAM_SCAN, DEFAULT_ENABLE_PROGRAM_SCAN),
            ): BOOLEAN_SELECTOR,
            vol.Required(
                CONF_PROGRAM_MARKERS,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_PROGRAM_MARKERS, DEFAULT_PROGRAM_MARKERS),
            ): SelectSelector(
                config=SelectSelectorConfig(
                    mode=SelectSelectorMode.DROPDOWN,
                    multiple=True,
                    sort=True,
                    options=[str(v) for v in DescriptionMarker if v != DescriptionMarker.HAHM],
                )
            ),
            vol.Required(
                CONF_ENABLE_SYSVAR_SCAN,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_ENABLE_SYSVAR_SCAN, DEFAULT_ENABLE_SYSVAR_SCAN),
            ): BOOLEAN_SELECTOR,
            vol.Required(
                CONF_SYSVAR_MARKERS,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_SYSVAR_MARKERS, DEFAULT_SYSVAR_MARKERS),
            ): SelectSelector(
                config=SelectSelectorConfig(
                    mode=SelectSelectorMode.DROPDOWN,
                    multiple=True,
                    sort=True,
                    options=[str(v) for v in DescriptionMarker],
                )
            ),
            vol.Required(
                CONF_SYS_SCAN_INTERVAL,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_SYS_SCAN_INTERVAL, DEFAULT_SYS_SCAN_INTERVAL),
            ): SCAN_INTERVAL_SELECTOR,
            vol.Required(
                CONF_ENABLE_SYSTEM_NOTIFICATIONS,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(
                    CONF_ENABLE_SYSTEM_NOTIFICATIONS, DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS
                ),
            ): BOOLEAN_SELECTOR,
            # MQTT settings
            vol.Required(
                CONF_ENABLE_MQTT,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_ENABLE_MQTT, DEFAULT_ENABLE_MQTT),
            ): BOOLEAN_SELECTOR,
            vol.Optional(
                CONF_MQTT_PREFIX,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX),
            ): TEXT_SELECTOR,
            vol.Optional(
                CONF_UN_IGNORES,
                default=existing_parameters,
            ): SelectSelector(
                config=SelectSelectorConfig(
                    mode=SelectSelectorMode.DROPDOWN,
                    multiple=True,
                    sort=False,
                    options=all_un_ignore_parameters,
                )
            ),
            vol.Optional(
                CONF_ENABLE_SUB_DEVICES,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_ENABLE_SUB_DEVICES, DEFAULT_ENABLE_SUB_DEVICES),
            ): BOOLEAN_SELECTOR,
            vol.Optional(
                CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(
                    CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE, DEFAULT_USE_GROUP_CHANNEL_FOR_COVER_STATE
                ),
            ): BOOLEAN_SELECTOR,
            vol.Optional(
                CONF_OPTIONAL_SETTINGS,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_OPTIONAL_SETTINGS, DEFAULT_OPTIONAL_SETTINGS),
            ): SelectSelector(
                config=SelectSelectorConfig(
                    mode=SelectSelectorMode.DROPDOWN,
                    multiple=True,
                    sort=True,
                    options=[str(v) for v in OptionalSettings],
                )
            ),
        }
    )
    if not all_un_ignore_parameters:
        del advanced_schema.schema[CONF_UN_IGNORES]
    return advanced_schema


def get_advanced_settings_schema(data: ConfigType, all_un_ignore_parameters: list[str]) -> Schema:
    """Return the advanced settings schema without program/sysvar fields (for options flow menu)."""
    existing_parameters: list[str] = [
        p
        for p in data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_UN_IGNORES, DEFAULT_UN_IGNORES)
        if p in all_un_ignore_parameters
    ]

    advanced_settings_schema = vol.Schema(
        {
            # Callback settings (moved here from connection step)
            vol.Optional(CONF_CALLBACK_HOST, default=data.get(CONF_CALLBACK_HOST) or UNDEFINED): TEXT_SELECTOR,
            vol.Optional(
                CONF_CALLBACK_PORT_XML_RPC, default=data.get(CONF_CALLBACK_PORT_XML_RPC) or UNDEFINED
            ): PORT_SELECTOR_OPTIONAL,
            vol.Required(
                CONF_ENABLE_SYSTEM_NOTIFICATIONS,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(
                    CONF_ENABLE_SYSTEM_NOTIFICATIONS, DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS
                ),
            ): BOOLEAN_SELECTOR,
            vol.Required(
                CONF_LISTEN_ON_ALL_IP,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_LISTEN_ON_ALL_IP, DEFAULT_LISTEN_ON_ALL_IP),
            ): BOOLEAN_SELECTOR,
            vol.Required(
                CONF_ENABLE_MQTT,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_ENABLE_MQTT, DEFAULT_ENABLE_MQTT),
            ): BOOLEAN_SELECTOR,
            vol.Optional(
                CONF_MQTT_PREFIX,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX),
            ): TEXT_SELECTOR,
            vol.Optional(
                CONF_UN_IGNORES,
                default=existing_parameters,
            ): SelectSelector(
                config=SelectSelectorConfig(
                    mode=SelectSelectorMode.DROPDOWN,
                    multiple=True,
                    sort=False,
                    options=all_un_ignore_parameters,
                )
            ),
            vol.Optional(
                CONF_ENABLE_SUB_DEVICES,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_ENABLE_SUB_DEVICES, DEFAULT_ENABLE_SUB_DEVICES),
            ): BOOLEAN_SELECTOR,
            vol.Optional(
                CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(
                    CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE, DEFAULT_USE_GROUP_CHANNEL_FOR_COVER_STATE
                ),
            ): BOOLEAN_SELECTOR,
            vol.Optional(
                CONF_OPTIONAL_SETTINGS,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_OPTIONAL_SETTINGS, DEFAULT_OPTIONAL_SETTINGS),
            ): SelectSelector(
                config=SelectSelectorConfig(
                    mode=SelectSelectorMode.DROPDOWN,
                    multiple=True,
                    sort=True,
                    options=[str(v) for v in OptionalSettings],
                )
            ),
        }
    )
    if not all_un_ignore_parameters:
        del advanced_settings_schema.schema[CONF_UN_IGNORES]
    return advanced_settings_schema


async def _async_validate_config_and_get_system_information(
    hass: HomeAssistant, data: ConfigType, entry_id: str
) -> SystemInformation | None:
    """Validate the user input allows us to connect."""
    control_config = ControlConfig(hass=hass, entry_id=entry_id, data=data)
    control_config.check_config()
    return await validate_config_and_get_system_information(control_config=control_config)


async def _async_detect_backend(
    host: str,
    username: str,
    password: str,
) -> BackendDetectionResult | None:
    """Detect backend type and available interfaces."""
    config = DetectionConfig(
        host=host,
        username=username,
        password=password,
    )
    return await detect_backend(config=config)


class DomainConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the instance flow for Homematic(IP) Local for OpenCCU."""

    VERSION = 12
    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    def __init__(self) -> None:
        """Init the ConfigFlow."""
        self.data: ConfigType = {}
        self.serial: str | None = None
        self._detection_result: BackendDetectionResult | None = None
        self._detection_task: asyncio.Task[None] | None = None
        self._detection_error: str | None = None
        self._detection_error_detail: str | None = None
        self._validation_error: str | None = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return HomematicIPLocalOptionsFlowHandler(config_entry)

    async def async_step_advanced(
        self,
        advanced_input: ConfigType | None = None,
    ) -> ConfigFlowResult:
        """Handle the advanced step."""
        if advanced_input is None:
            _LOGGER.debug("ConfigFlow.step_advanced, no user input")
            return self.async_show_form(
                step_id="advanced",
                data_schema=get_advanced_schema(
                    data=self.data,
                    all_un_ignore_parameters=[],
                ),
                description_placeholders=_get_step_placeholders(STEP_ADVANCED, TOTAL_STEPS_ADVANCED),
            )
        _update_advanced_input(data=self.data, advanced_input=advanced_input)
        return await self._validate_and_finish_config_flow()

    async def async_step_central(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            self.data = _get_ccu_data(self.data, user_input=user_input)
            # Start detection task and show progress
            if not self._detection_task:
                self._detection_task = self.hass.async_create_task(
                    self._async_run_detection(), "homematicip_local_detect_backend"
                )
            return await self.async_step_detect()

        return self.async_show_form(
            step_id="central",
            data_schema=get_domain_schema(data=self.data),
            description_placeholders=_get_step_placeholders(STEP_CENTRAL, TOTAL_STEPS_BASIC),
        )

    async def async_step_central_error(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle return to central step with validation error."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = _get_step_placeholders(STEP_CENTRAL, TOTAL_STEPS_BASIC)

        if self._detection_error:
            errors["base"] = self._detection_error
            # Always set invalid_items placeholder to avoid showing literal [{invalid_items}] in message
            description_placeholders["invalid_items"] = self._detection_error_detail or self.data.get(CONF_HOST, "")
            # Add detailed error information
            description_placeholders["error_detail"] = self._detection_error_detail or ""
            description_placeholders["retry_hint"] = _get_retry_hint(self._detection_error)

        # Reset detection error state
        self._detection_error = None
        self._detection_error_detail = None

        return self.async_show_form(
            step_id="central",
            data_schema=get_domain_schema(data=self.data),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_configure_advanced(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Go to advanced configuration."""
        return await self.async_step_advanced()

    async def async_step_detect(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle the backend detection step."""
        if self._detection_task and not self._detection_task.done():
            return self.async_show_progress(
                step_id="detect",
                progress_action="detect_backend",
                progress_task=self._detection_task,
            )

        # Check for errors during detection - show them in central step
        if self._detection_error:
            self._detection_task = None
            return self.async_show_progress_done(next_step_id="central_error")

        # Detection complete (or was never started), proceed to interface step
        return self.async_show_progress_done(next_step_id="interface")

    async def async_step_finish_or_configure(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Show menu to choose between finishing setup or configuring advanced options."""
        return self.async_show_menu(
            step_id="finish_or_configure",
            menu_options=["finish_setup", "configure_advanced"],
        )

    async def async_step_finish_setup(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Finish the config flow without advanced settings."""
        return await self._validate_and_finish_config_flow()

    async def async_step_interface(
        self,
        interface_input: ConfigType | None = None,
    ) -> ConfigFlowResult:
        """Handle the interface step (TLS + interface checkboxes, optional custom ports)."""
        # Only process interface_input if it actually contains interface fields
        # (not if it's leftover user_input from previous steps)
        if interface_input is not None and CONF_ENABLE_HMIP_RF in interface_input:
            # Use simplified update function (automatic ports based on TLS)
            _update_tls_interfaces_input(data=self.data, interface_input=interface_input)

            # Check if user wants to configure custom ports
            if interface_input.get(CONF_CUSTOM_PORT_CONFIG, False):
                _LOGGER.debug("User requested custom port configuration")
                return await self.async_step_port_config()

            # User didn't request custom ports - validate with defaults
            try:
                await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id="validate"
                )
                # Validation successful - proceed to finish or advanced config
                return await self.async_step_finish_or_configure()
            except AuthFailure:
                # Auth errors should go back to central step - changing ports won't fix auth
                _LOGGER.debug("Authentication failed, returning to central step")
                self._detection_error = "invalid_auth"
                self._detection_error_detail = self.data.get(CONF_HOST, "")
                return await self.async_step_central_error()
            except (NoConnectionException, InvalidConfig, BaseHomematicException) as ex:
                # Connection/config errors - show port configuration to allow manual adjustment
                _LOGGER.debug("Validation failed with default ports, showing port config: %s", ex)
                self._validation_error = str(ex) if str(ex) else self.data.get(CONF_HOST, "")
                return await self.async_step_port_config()

        _LOGGER.debug("ConfigFlow.step_interface, no user input")
        placeholders = _get_step_placeholders(STEP_INTERFACE, TOTAL_STEPS_BASIC)
        # Add detection result info if available
        if self._detection_result:
            placeholders["detected_backend"] = self._detection_result.backend.value
            placeholders["detected_interfaces"] = ", ".join(
                i.value for i in self._detection_result.available_interfaces
            )
            placeholders["detected_tls"] = str(
                self._detection_result.tls or self._detection_result.https_redirect_enabled
            )
        return self.async_show_form(
            step_id="interface",
            data_schema=get_tls_interfaces_schema(data=self.data),
            description_placeholders=placeholders,
        )

    async def async_step_port_config(
        self,
        port_input: ConfigType | None = None,
    ) -> ConfigFlowResult:
        """Handle port configuration step (shown on validation error or advanced config)."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {
            "invalid_items": "",
            "error_detail": "",
            "retry_hint": "",
        }

        if port_input is not None:
            _update_port_config_input(data=self.data, port_input=port_input)

            # Validate configuration with updated ports
            try:
                await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id="validate"
                )
                # Validation successful - proceed to finish or advanced config
                return await self.async_step_finish_or_configure()
            except AuthFailure:
                errors["base"] = "invalid_auth"
                description_placeholders["invalid_items"] = self.data.get(CONF_HOST, "")
            except InvalidConfig as ic:
                errors["base"] = "invalid_config"
                description_placeholders["invalid_items"] = str(ic)
            except NoConnectionException as exc:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = str(exc) if str(exc) else self.data.get(CONF_HOST, "")
            except BaseHomematicException as bhe:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = bhe.args[0] if bhe.args else self.data.get(CONF_HOST, "")

        # Show validation error from interface step if present
        if not errors and hasattr(self, "_validation_error") and self._validation_error:
            errors["base"] = "cannot_connect"
            description_placeholders["invalid_items"] = self._validation_error
            description_placeholders["error_detail"] = (
                "Default ports did not work. Please adjust the port configuration below."
            )
            description_placeholders["retry_hint"] = (
                "Check if your CCU uses non-standard ports or if a firewall blocks the connection."
            )
            self._validation_error = None

        # Add TLS status info to placeholders
        tls_enabled = self.data.get(CONF_TLS, False)
        description_placeholders["tls_status"] = "enabled" if tls_enabled else "disabled"

        return self.async_show_form(
            step_id="port_config",
            data_schema=get_port_config_schema(data=self.data),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_reconfigure(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle reconfiguration of the integration - step 1: connection settings."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if entry is None:
            return self.async_abort(reason="reconfigure_failed")

        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = _get_step_placeholders(STEP_RECONFIGURE, TOTAL_STEPS_RECONFIGURE)

        # Check for errors from interface step (auth failure redirects here)
        if self._detection_error:
            errors["base"] = self._detection_error
            description_placeholders["invalid_items"] = self._detection_error_detail or self.data.get(CONF_HOST, "")
            description_placeholders["error_detail"] = self._detection_error_detail or ""
            description_placeholders["retry_hint"] = _get_retry_hint(self._detection_error)
            self._detection_error = None
            self._detection_error_detail = None

        if user_input is not None:
            # Store connection data and proceed to interface step
            self.data = dict(entry.data)
            self.data[CONF_HOST] = user_input[CONF_HOST]
            self.data[CONF_USERNAME] = user_input[CONF_USERNAME]
            self.data[CONF_PASSWORD] = user_input[CONF_PASSWORD]
            return await self.async_step_reconfigure_interface()

        # Use existing data if available (for returning with errors), otherwise entry data
        schema_data = self.data if self.data else dict(entry.data)

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=get_reconfigure_schema(schema_data),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_reconfigure_interface(self, interface_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle reconfiguration - step 2: TLS and interface settings (same semantics as config flow)."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if entry is None:
            return self.async_abort(reason="reconfigure_failed")

        if interface_input is not None and CONF_ENABLE_HMIP_RF in interface_input:
            # Use simplified update function (automatic ports based on TLS)
            _update_tls_interfaces_input(data=self.data, interface_input=interface_input)

            # Check if user wants to configure custom ports
            if interface_input.get(CONF_CUSTOM_PORT_CONFIG, False):
                _LOGGER.debug("Reconfigure: User requested custom port configuration")
                return await self.async_step_reconfigure_port_config()

            # User didn't request custom ports - validate with defaults
            try:
                await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id=entry.entry_id
                )
                # Validation successful - finish reconfiguration
                return self.async_update_reload_and_abort(
                    entry,
                    data=self.data,
                    reason="reconfigure_successful",
                )
            except AuthFailure:
                # Auth errors should go back to reconfigure step
                _LOGGER.debug("Reconfigure: Authentication failed, returning to reconfigure step")
                self._detection_error = "invalid_auth"
                self._detection_error_detail = self.data.get(CONF_HOST, "")
                return await self.async_step_reconfigure()
            except (NoConnectionException, InvalidConfig, BaseHomematicException) as ex:
                # Connection/config errors - show port configuration
                _LOGGER.debug("Reconfigure: Validation failed with default ports, showing port config: %s", ex)
                self._validation_error = str(ex) if str(ex) else self.data.get(CONF_HOST, "")
                return await self.async_step_reconfigure_port_config()

        return self.async_show_form(
            step_id="reconfigure_interface",
            data_schema=get_tls_interfaces_schema(data=self.data),
            description_placeholders=_get_step_placeholders(STEP_RECONFIGURE_TLS, TOTAL_STEPS_RECONFIGURE),
        )

    async def async_step_reconfigure_port_config(self, port_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle reconfiguration - port configuration (shown on request or validation error)."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if entry is None:
            return self.async_abort(reason="reconfigure_failed")

        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {
            "invalid_items": "",
            "error_detail": "",
            "retry_hint": "",
        }

        if port_input is not None:
            _update_port_config_input(data=self.data, port_input=port_input)

            # Validate configuration with updated ports
            try:
                await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id=entry.entry_id
                )
                # Validation successful - finish reconfiguration
                return self.async_update_reload_and_abort(
                    entry,
                    data=self.data,
                    reason="reconfigure_successful",
                )
            except AuthFailure:
                errors["base"] = "invalid_auth"
                description_placeholders["invalid_items"] = self.data.get(CONF_HOST, "")
            except InvalidConfig as ic:
                errors["base"] = "invalid_config"
                description_placeholders["invalid_items"] = str(ic)
            except NoConnectionException as exc:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = str(exc) if str(exc) else self.data.get(CONF_HOST, "")
            except BaseHomematicException as bhe:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = bhe.args[0] if bhe.args else self.data.get(CONF_HOST, "")

        # Show validation error from interface step if present
        if not errors and hasattr(self, "_validation_error") and self._validation_error:
            errors["base"] = "cannot_connect"
            description_placeholders["invalid_items"] = self._validation_error
            description_placeholders["error_detail"] = (
                "Default ports did not work. Please adjust the port configuration below."
            )
            description_placeholders["retry_hint"] = (
                "Check if your CCU uses non-standard ports or if a firewall blocks the connection."
            )
            self._validation_error = None

        # Add TLS status info to placeholders
        tls_enabled = self.data.get(CONF_TLS, False)
        description_placeholders["tls_status"] = "enabled" if tls_enabled else "disabled"

        return self.async_show_form(
            step_id="reconfigure_port_config",
            data_schema=get_port_config_schema(data=self.data),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_ssdp(self, discovery_info: ssdp.SsdpServiceInfo) -> ConfigFlowResult:
        """Handle a discovered Homematic CCU."""
        _LOGGER.debug("Homematic(IP) Local for OpenCCU SSDP discovery %s", pformat(discovery_info))
        instance_name = _get_instance_name(friendly_name=discovery_info.upnp.get("friendlyName")) or "OpenCCU"
        serial = _get_serial(model_description=discovery_info.upnp.get("modelDescription"))

        host = cast(str, urlparse(discovery_info.ssdp_location).hostname)
        await self.async_set_unique_id(serial)

        self._abort_if_unique_id_configured()

        self.data = {CONF_INSTANCE_NAME: instance_name, CONF_HOST: host}
        self.context["title_placeholders"] = {CONF_NAME: instance_name, CONF_HOST: host}
        return await self.async_step_user()

    async def async_step_user(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        return await self.async_step_central(user_input=user_input)

    def _apply_detected_interfaces(self) -> None:
        """Apply detected interfaces to config data."""
        if not self._detection_result:
            return

        # Use TLS setting from data (already computed from detection result)
        use_tls = self.data.get(CONF_TLS, False)
        interfaces: dict[Interface, dict[str, Any]] = {}

        for interface in self._detection_result.available_interfaces:
            if default_port := get_interface_default_port(interface, tls=use_tls):
                interface_config: dict[str, Any] = {CONF_PORT: default_port}
                # Add path for VirtualDevices
                if interface == Interface.VIRTUAL_DEVICES:
                    interface_config[CONF_PATH] = IF_VIRTUAL_DEVICES_PATH
                interfaces[interface] = interface_config

        self.data[CONF_INTERFACE] = interfaces

    async def _async_run_detection(self) -> None:
        """Run backend detection as background task."""
        try:
            self._detection_result = await _async_detect_backend(
                host=self.data[CONF_HOST],
                username=self.data[CONF_USERNAME],
                password=self.data[CONF_PASSWORD],
            )
        except AuthFailure:
            _LOGGER.warning("Backend detection failed: invalid authentication")
            self._detection_error = "invalid_auth"
            self._detection_error_detail = self.data[CONF_HOST]
            return
        except ValidationException as ve:
            _LOGGER.warning("Backend detection failed: invalid configuration - %s", ve)
            self._detection_error = "invalid_config"
            self._detection_error_detail = str(ve)
            return
        except NoConnectionException as ex:
            _LOGGER.warning("Backend detection failed: connection error - %s", ex)
            self._detection_error = "cannot_connect"
            self._detection_error_detail = str(ex) if str(ex) else self.data[CONF_HOST]
            return
        except BaseHomematicException as ex:
            _LOGGER.warning("Backend detection failed: %s - %s", type(ex).__name__, ex)
            self._detection_error = "cannot_connect"
            self._detection_error_detail = str(ex) if str(ex) else self.data[CONF_HOST]
            return

        if self._detection_result:
            # Enable TLS if detected via connection or if HTTPS redirect is enabled on CCU
            use_tls = self._detection_result.tls or self._detection_result.https_redirect_enabled is True
            _LOGGER.debug(
                "Backend detection successful: backend=%s, interfaces=%s, tls=%s, auth_enabled=%s, https_redirect=%s, use_tls=%s",
                self._detection_result.backend,
                self._detection_result.available_interfaces,
                self._detection_result.tls,
                self._detection_result.auth_enabled,
                self._detection_result.https_redirect_enabled,
                use_tls,
            )
            # Update TLS setting based on detection
            self.data[CONF_TLS] = use_tls
            # Pre-populate interfaces based on detection
            self._apply_detected_interfaces()
        else:
            # No backend found - could be connection, auth, or config issue
            _LOGGER.warning("Backend detection failed: no backend found at host %s", self.data[CONF_HOST])
            self._detection_error = "detection_failed"
            self._detection_error_detail = self.data[CONF_HOST]

    async def _validate_and_finish_config_flow(self) -> ConfigFlowResult:
        """Validate and finish the config flow."""

        errors = {}
        description_placeholders = {}

        try:
            system_information = await _async_validate_config_and_get_system_information(
                hass=self.hass, data=self.data, entry_id="validate"
            )
            if system_information is not None:
                await self.async_set_unique_id(system_information.serial)
            self._abort_if_unique_id_configured()
        except AuthFailure:
            errors["base"] = "invalid_auth"
            description_placeholders["invalid_items"] = self.data[CONF_HOST]
        except InvalidConfig as ic:
            errors["base"] = "invalid_config"
            description_placeholders["invalid_items"] = ic.args[0]
        except BaseHomematicException as bhe:
            errors["base"] = "cannot_connect"
            description_placeholders["invalid_items"] = bhe.args[0]
        else:
            return self.async_create_entry(title=self.data[CONF_INSTANCE_NAME], data=self.data)

        return self.async_show_form(
            step_id="central",
            data_schema=get_domain_schema(data=self.data),
            errors=errors,
            description_placeholders=description_placeholders,
        )


class HomematicIPLocalOptionsFlowHandler(OptionsFlow):
    """Handle Homematic(IP) Local for OpenCCU options."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize Homematic(IP) Local for OpenCCU options flow."""
        self.entry = entry
        self._control_unit: ControlUnit = entry.runtime_data
        self.data: ConfigType = dict(self.entry.data.items())
        self._validation_error: str | None = None

    async def async_step_advanced_settings(self, advanced_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle advanced settings (MQTT, device options, etc.)."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        if advanced_input is not None:
            _update_advanced_settings_input(data=self.data, advanced_input=advanced_input)
            try:
                system_information = await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id=self.entry.entry_id
                )
                if system_information is not None:
                    self.hass.config_entries.async_update_entry(
                        entry=self.entry,
                        unique_id=system_information.serial,
                        data=self.data,
                    )
                return self.async_create_entry(title="", data={})
            except AuthFailure:
                errors["base"] = "invalid_auth"
                description_placeholders["invalid_items"] = self.data[CONF_HOST]
            except InvalidConfig as ic:
                errors["base"] = "invalid_config"
                description_placeholders["invalid_items"] = ic.args[0]
            except BaseHomematicException as bhe:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = bhe.args[0]

        return self.async_show_form(
            step_id="advanced_settings",
            data_schema=get_advanced_settings_schema(
                data=self.data,
                all_un_ignore_parameters=self._control_unit.central.get_un_ignore_candidates(include_master=True),
            ),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_connection(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle connection settings (host, credentials)."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        if user_input is not None:
            self.data = _get_ccu_data(self.data, user_input=user_input)
            try:
                system_information = await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id=self.entry.entry_id
                )
                if system_information is not None:
                    self.hass.config_entries.async_update_entry(
                        entry=self.entry,
                        unique_id=system_information.serial,
                        data=self.data,
                    )
                return self.async_create_entry(title="", data={})
            except AuthFailure:
                errors["base"] = "invalid_auth"
                description_placeholders["invalid_items"] = self.data[CONF_HOST]
            except InvalidConfig as ic:
                errors["base"] = "invalid_config"
                description_placeholders["invalid_items"] = ic.args[0]
            except BaseHomematicException as bhe:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = bhe.args[0]

        return self.async_show_form(
            step_id="connection",
            data_schema=get_options_schema(data=self.data),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_init(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Show menu for options configuration."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["connection", "interfaces", "programs_sysvars", "advanced_settings"],
        )

    async def async_step_interfaces(self, interface_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle interface configuration (TLS + interface checkboxes, same as Config Flow)."""
        if interface_input is not None and CONF_ENABLE_HMIP_RF in interface_input:
            # Use simplified update function (automatic ports based on TLS)
            _update_tls_interfaces_input(data=self.data, interface_input=interface_input)

            # Check if user wants to configure custom ports
            if interface_input.get(CONF_CUSTOM_PORT_CONFIG, False):
                _LOGGER.debug("Options Flow: User requested custom port configuration")
                return await self.async_step_interfaces_port_config()

            # User didn't request custom ports - validate with defaults
            try:
                system_information = await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id=self.entry.entry_id
                )
                if system_information is not None:
                    self.hass.config_entries.async_update_entry(
                        entry=self.entry,
                        unique_id=system_information.serial,
                        data=self.data,
                    )
                return self.async_create_entry(title="", data={})
            except AuthFailure:
                # Auth errors should go back to connection step
                _LOGGER.debug("Options Flow: Authentication failed")
                return self.async_show_form(
                    step_id="interfaces",
                    data_schema=get_tls_interfaces_schema(data=self.data),
                    errors={"base": "invalid_auth"},
                    description_placeholders={"invalid_items": self.data[CONF_HOST]},
                )
            except (NoConnectionException, InvalidConfig, BaseHomematicException) as ex:
                # Connection/config errors - show port configuration
                _LOGGER.debug("Options Flow: Validation failed with default ports, showing port config: %s", ex)
                self._validation_error = str(ex) if str(ex) else self.data.get(CONF_HOST, "")
                return await self.async_step_interfaces_port_config()

        return self.async_show_form(
            step_id="interfaces",
            data_schema=get_tls_interfaces_schema(data=self.data),
        )

    async def async_step_interfaces_port_config(self, port_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle port configuration for Options Flow (shown on request or validation error)."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {
            "invalid_items": "",
            "error_detail": "",
            "retry_hint": "",
        }

        if port_input is not None:
            _update_port_config_input(data=self.data, port_input=port_input)

            # Validate configuration with updated ports
            try:
                system_information = await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id=self.entry.entry_id
                )
                if system_information is not None:
                    self.hass.config_entries.async_update_entry(
                        entry=self.entry,
                        unique_id=system_information.serial,
                        data=self.data,
                    )
                return self.async_create_entry(title="", data={})
            except AuthFailure:
                errors["base"] = "invalid_auth"
                description_placeholders["invalid_items"] = self.data[CONF_HOST]
            except InvalidConfig as ic:
                errors["base"] = "invalid_config"
                description_placeholders["invalid_items"] = str(ic)
            except NoConnectionException as exc:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = str(exc) if str(exc) else self.data.get(CONF_HOST, "")
            except BaseHomematicException as bhe:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = bhe.args[0] if bhe.args else self.data.get(CONF_HOST, "")

        # Show validation error from interfaces step if present
        if not errors and hasattr(self, "_validation_error") and self._validation_error:
            errors["base"] = "cannot_connect"
            description_placeholders["invalid_items"] = self._validation_error
            description_placeholders["error_detail"] = (
                "Default ports did not work. Please adjust the port configuration below."
            )
            description_placeholders["retry_hint"] = (
                "Check if your CCU uses non-standard ports or if a firewall blocks the connection."
            )
            self._validation_error = None

        # Add TLS status info to placeholders
        tls_enabled = self.data.get(CONF_TLS, False)
        description_placeholders["tls_status"] = "enabled" if tls_enabled else "disabled"

        return self.async_show_form(
            step_id="interfaces_port_config",
            data_schema=get_port_config_schema(data=self.data),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_programs_sysvars(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle programs and system variables configuration."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        if user_input is not None:
            # Update only program/sysvar related settings
            advanced_config = self.data.get(CONF_ADVANCED_CONFIG, {})
            advanced_config[CONF_ENABLE_PROGRAM_SCAN] = user_input.get(
                CONF_ENABLE_PROGRAM_SCAN, DEFAULT_ENABLE_PROGRAM_SCAN
            )
            advanced_config[CONF_PROGRAM_MARKERS] = user_input.get(CONF_PROGRAM_MARKERS, DEFAULT_PROGRAM_MARKERS)
            advanced_config[CONF_ENABLE_SYSVAR_SCAN] = user_input.get(
                CONF_ENABLE_SYSVAR_SCAN, DEFAULT_ENABLE_SYSVAR_SCAN
            )
            advanced_config[CONF_SYSVAR_MARKERS] = user_input.get(CONF_SYSVAR_MARKERS, DEFAULT_SYSVAR_MARKERS)
            advanced_config[CONF_SYS_SCAN_INTERVAL] = user_input.get(CONF_SYS_SCAN_INTERVAL, DEFAULT_SYS_SCAN_INTERVAL)
            self.data[CONF_ADVANCED_CONFIG] = advanced_config
            try:
                system_information = await _async_validate_config_and_get_system_information(
                    hass=self.hass, data=self.data, entry_id=self.entry.entry_id
                )
                if system_information is not None:
                    self.hass.config_entries.async_update_entry(
                        entry=self.entry,
                        unique_id=system_information.serial,
                        data=self.data,
                    )
                return self.async_create_entry(title="", data={})
            except AuthFailure:
                errors["base"] = "invalid_auth"
                description_placeholders["invalid_items"] = self.data[CONF_HOST]
            except InvalidConfig as ic:
                errors["base"] = "invalid_config"
                description_placeholders["invalid_items"] = ic.args[0]
            except BaseHomematicException as bhe:
                errors["base"] = "cannot_connect"
                description_placeholders["invalid_items"] = bhe.args[0]

        advanced_config = self.data.get(CONF_ADVANCED_CONFIG, {})
        return self.async_show_form(
            step_id="programs_sysvars",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ENABLE_PROGRAM_SCAN,
                        default=advanced_config.get(CONF_ENABLE_PROGRAM_SCAN, DEFAULT_ENABLE_PROGRAM_SCAN),
                    ): BOOLEAN_SELECTOR,
                    vol.Optional(
                        CONF_PROGRAM_MARKERS,
                        default=advanced_config.get(CONF_PROGRAM_MARKERS, DEFAULT_PROGRAM_MARKERS),
                    ): SelectSelector(
                        config=SelectSelectorConfig(
                            mode=SelectSelectorMode.DROPDOWN,
                            multiple=True,
                            sort=True,
                            options=[str(v) for v in DescriptionMarker if v != DescriptionMarker.HAHM],
                        )
                    ),
                    vol.Required(
                        CONF_ENABLE_SYSVAR_SCAN,
                        default=advanced_config.get(CONF_ENABLE_SYSVAR_SCAN, DEFAULT_ENABLE_SYSVAR_SCAN),
                    ): BOOLEAN_SELECTOR,
                    vol.Optional(
                        CONF_SYSVAR_MARKERS,
                        default=advanced_config.get(CONF_SYSVAR_MARKERS, DEFAULT_SYSVAR_MARKERS),
                    ): SelectSelector(
                        config=SelectSelectorConfig(
                            mode=SelectSelectorMode.DROPDOWN,
                            multiple=True,
                            sort=True,
                            options=[str(v) for v in DescriptionMarker],
                        )
                    ),
                    vol.Required(
                        CONF_SYS_SCAN_INTERVAL,
                        default=advanced_config.get(CONF_SYS_SCAN_INTERVAL, DEFAULT_SYS_SCAN_INTERVAL),
                    ): SCAN_INTERVAL_SELECTOR,
                }
            ),
            errors=errors,
            description_placeholders=description_placeholders,
        )


def _get_ccu_data(data: ConfigType, user_input: ConfigType) -> ConfigType:
    """Get CCU data from user input. TLS and ports are set from interface step or detection."""
    ccu_data = {
        CONF_INSTANCE_NAME: user_input.get(CONF_INSTANCE_NAME, data.get(CONF_INSTANCE_NAME)),
        CONF_HOST: user_input[CONF_HOST],
        CONF_USERNAME: user_input[CONF_USERNAME],
        CONF_PASSWORD: user_input[CONF_PASSWORD],
        # TLS and JSON port preserved from data (set by detection or interface step)
        CONF_TLS: data.get(CONF_TLS, DEFAULT_TLS),
        CONF_VERIFY_TLS: data.get(CONF_VERIFY_TLS, False),
        CONF_INTERFACE: data.get(CONF_INTERFACE, {}),
        CONF_ADVANCED_CONFIG: data.get(CONF_ADVANCED_CONFIG, {}),
    }
    # Callback settings: prefer user_input (Options Flow), fall back to data (Config Flow Advanced step)
    if (
        (callback_host := user_input.get(CONF_CALLBACK_HOST))
        and callback_host.strip() != ""
        or (callback_host := data.get(CONF_CALLBACK_HOST))
        and callback_host.strip() != ""
    ):
        ccu_data[CONF_CALLBACK_HOST] = callback_host
    if (callback_port_xml_rpc := user_input.get(CONF_CALLBACK_PORT_XML_RPC)) is not None or (
        callback_port_xml_rpc := data.get(CONF_CALLBACK_PORT_XML_RPC)
    ) is not None:
        ccu_data[CONF_CALLBACK_PORT_XML_RPC] = callback_port_xml_rpc
    # JSON port is preserved from data (set by interface step)
    if (json_port := data.get(CONF_JSON_PORT)) is not None:
        ccu_data[CONF_JSON_PORT] = json_port

    return ccu_data


def _update_interface_input(data: ConfigType, interface_input: ConfigType) -> None:
    """Update data with interface input including TLS settings and JSON port."""
    if not interface_input:
        return

    # Update TLS settings from interface input
    data[CONF_TLS] = interface_input[CONF_TLS]
    data[CONF_VERIFY_TLS] = interface_input[CONF_VERIFY_TLS]

    # Update JSON port from interface input
    if (json_port := interface_input.get(CONF_JSON_PORT)) is not None:
        data[CONF_JSON_PORT] = json_port
    elif CONF_JSON_PORT in data:
        del data[CONF_JSON_PORT]

    # Update interface configuration
    data[CONF_INTERFACE] = {}
    if interface_input[CONF_ENABLE_HMIP_RF] is True:
        data[CONF_INTERFACE][Interface.HMIP_RF] = {
            CONF_PORT: interface_input[CONF_HMIP_RF_PORT],
        }
    if interface_input[CONF_ENABLE_BIDCOS_RF] is True:
        data[CONF_INTERFACE][Interface.BIDCOS_RF] = {
            CONF_PORT: interface_input[CONF_BIDCOS_RF_PORT],
        }
    if interface_input[CONF_ENABLE_VIRTUAL_DEVICES] is True:
        data[CONF_INTERFACE][Interface.VIRTUAL_DEVICES] = {
            CONF_PORT: interface_input[CONF_VIRTUAL_DEVICES_PORT],
            CONF_PATH: interface_input.get(CONF_VIRTUAL_DEVICES_PATH),
        }
    if interface_input[CONF_ENABLE_BIDCOS_WIRED] is True:
        data[CONF_INTERFACE][Interface.BIDCOS_WIRED] = {
            CONF_PORT: interface_input[CONF_BIDCOS_WIRED_PORT],
        }
    if interface_input[CONF_ENABLE_CCU_JACK] is True:
        data[CONF_INTERFACE][Interface.CCU_JACK] = {}
    if interface_input[CONF_ENABLE_CUXD] is True:
        data[CONF_INTERFACE][Interface.CUXD] = {}


def _update_tls_interfaces_input(data: ConfigType, interface_input: ConfigType) -> None:
    """Update data with TLS + interface selection using default ports (for simplified flow)."""
    if not interface_input:
        return

    # Update TLS settings from interface input
    tls = interface_input[CONF_TLS]
    data[CONF_TLS] = tls
    data[CONF_VERIFY_TLS] = interface_input[CONF_VERIFY_TLS]

    # Get custom ports (if any)
    custom_ports: dict[str, int] = data.get(CONF_CUSTOM_PORTS, {})

    # Update interface configuration with default ports (or custom if set)
    data[CONF_INTERFACE] = {}

    def _get_port(interface: Interface) -> int:
        """Get custom port if available, otherwise TLS-based default."""
        if interface.value in custom_ports:
            return int(custom_ports[interface.value])
        return int(get_interface_default_port(interface, tls=tls) or 0)

    if interface_input[CONF_ENABLE_HMIP_RF] is True:
        data[CONF_INTERFACE][Interface.HMIP_RF] = {CONF_PORT: _get_port(Interface.HMIP_RF)}
    if interface_input[CONF_ENABLE_BIDCOS_RF] is True:
        data[CONF_INTERFACE][Interface.BIDCOS_RF] = {CONF_PORT: _get_port(Interface.BIDCOS_RF)}
    if interface_input[CONF_ENABLE_VIRTUAL_DEVICES] is True:
        data[CONF_INTERFACE][Interface.VIRTUAL_DEVICES] = {
            CONF_PORT: _get_port(Interface.VIRTUAL_DEVICES),
            CONF_PATH: IF_VIRTUAL_DEVICES_PATH,
        }
    if interface_input[CONF_ENABLE_BIDCOS_WIRED] is True:
        data[CONF_INTERFACE][Interface.BIDCOS_WIRED] = {CONF_PORT: _get_port(Interface.BIDCOS_WIRED)}
    if interface_input[CONF_ENABLE_CCU_JACK] is True:
        data[CONF_INTERFACE][Interface.CCU_JACK] = {}
    if interface_input[CONF_ENABLE_CUXD] is True:
        data[CONF_INTERFACE][Interface.CUXD] = {}


def _update_port_config_input(data: ConfigType, port_input: ConfigType) -> None:
    """
    Update data with port configuration input (for custom port configuration).

    Note: Callback settings have been moved to advanced configuration.
    """
    if not port_input:
        return

    tls = data.get(CONF_TLS, False)
    interfaces = data.get(CONF_INTERFACE, {})

    # Track custom ports (non-default)
    custom_ports: dict[str, int] = data.get(CONF_CUSTOM_PORTS, {})

    # Update JSON port
    if (json_port := port_input.get(CONF_JSON_PORT)) and json_port != get_json_rpc_default_port(tls=tls):
        data[CONF_JSON_PORT] = json_port
    elif CONF_JSON_PORT in data:
        del data[CONF_JSON_PORT]

    # Update interface ports
    for interface in (Interface.HMIP_RF, Interface.BIDCOS_RF, Interface.VIRTUAL_DEVICES, Interface.BIDCOS_WIRED):
        if interface not in interfaces:
            continue

        port_key = {
            Interface.HMIP_RF: CONF_HMIP_RF_PORT,
            Interface.BIDCOS_RF: CONF_BIDCOS_RF_PORT,
            Interface.VIRTUAL_DEVICES: CONF_VIRTUAL_DEVICES_PORT,
            Interface.BIDCOS_WIRED: CONF_BIDCOS_WIRED_PORT,
        }[interface]

        if port_key in port_input:
            port = port_input[port_key]
            interfaces[interface][CONF_PORT] = port
            # Track if it's a custom (non-default) port
            if not is_interface_default_port(interface, port):
                custom_ports[interface.value] = port
            elif interface.value in custom_ports:
                del custom_ports[interface.value]

    # Update VirtualDevices path if present
    if Interface.VIRTUAL_DEVICES in interfaces and CONF_VIRTUAL_DEVICES_PATH in port_input:
        interfaces[Interface.VIRTUAL_DEVICES][CONF_PATH] = port_input[CONF_VIRTUAL_DEVICES_PATH]

    # Store custom ports only if non-empty
    if custom_ports:
        data[CONF_CUSTOM_PORTS] = custom_ports
    elif CONF_CUSTOM_PORTS in data:
        del data[CONF_CUSTOM_PORTS]


def _update_advanced_input(data: ConfigType, advanced_input: ConfigType) -> None:
    """Update data with advanced input (for advanced step with all fields including callbacks)."""
    if not advanced_input:
        return

    # Update callback settings (moved here from port config)
    if callback_host := advanced_input.get(CONF_CALLBACK_HOST):
        data[CONF_CALLBACK_HOST] = callback_host
    elif CONF_CALLBACK_HOST in data:
        del data[CONF_CALLBACK_HOST]

    if callback_port := advanced_input.get(CONF_CALLBACK_PORT_XML_RPC):
        data[CONF_CALLBACK_PORT_XML_RPC] = callback_port
    elif CONF_CALLBACK_PORT_XML_RPC in data:
        del data[CONF_CALLBACK_PORT_XML_RPC]

    # Update advanced config settings
    data[CONF_ADVANCED_CONFIG] = {}
    data[CONF_ADVANCED_CONFIG][CONF_LISTEN_ON_ALL_IP] = advanced_input[CONF_LISTEN_ON_ALL_IP]
    data[CONF_ADVANCED_CONFIG][CONF_PROGRAM_MARKERS] = advanced_input[CONF_PROGRAM_MARKERS]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_PROGRAM_SCAN] = advanced_input[CONF_ENABLE_PROGRAM_SCAN]
    data[CONF_ADVANCED_CONFIG][CONF_SYSVAR_MARKERS] = advanced_input[CONF_SYSVAR_MARKERS]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SYSVAR_SCAN] = advanced_input[CONF_ENABLE_SYSVAR_SCAN]
    data[CONF_ADVANCED_CONFIG][CONF_SYS_SCAN_INTERVAL] = advanced_input[CONF_SYS_SCAN_INTERVAL]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SYSTEM_NOTIFICATIONS] = advanced_input[CONF_ENABLE_SYSTEM_NOTIFICATIONS]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_MQTT] = advanced_input[CONF_ENABLE_MQTT]
    data[CONF_ADVANCED_CONFIG][CONF_MQTT_PREFIX] = advanced_input[CONF_MQTT_PREFIX]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SUB_DEVICES] = advanced_input[CONF_ENABLE_SUB_DEVICES]
    data[CONF_ADVANCED_CONFIG][CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE] = advanced_input[
        CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE
    ]
    data[CONF_ADVANCED_CONFIG][CONF_OPTIONAL_SETTINGS] = advanced_input[CONF_OPTIONAL_SETTINGS]

    if advanced_input.get(CONF_UN_IGNORES):
        data[CONF_ADVANCED_CONFIG][CONF_UN_IGNORES] = advanced_input[CONF_UN_IGNORES]


def _update_advanced_settings_input(data: ConfigType, advanced_input: ConfigType) -> None:
    """Update data with advanced settings input (preserves program/sysvar settings)."""
    if not advanced_input:
        return

    # Update callback settings (moved here from connection step)
    if callback_host := advanced_input.get(CONF_CALLBACK_HOST):
        data[CONF_CALLBACK_HOST] = callback_host
    elif CONF_CALLBACK_HOST in data:
        del data[CONF_CALLBACK_HOST]

    if callback_port := advanced_input.get(CONF_CALLBACK_PORT_XML_RPC):
        data[CONF_CALLBACK_PORT_XML_RPC] = callback_port
    elif CONF_CALLBACK_PORT_XML_RPC in data:
        del data[CONF_CALLBACK_PORT_XML_RPC]

    # Preserve existing program/sysvar settings (configured separately in programs_sysvars step)
    existing_config = data.get(CONF_ADVANCED_CONFIG, {})
    data[CONF_ADVANCED_CONFIG] = {
        CONF_PROGRAM_MARKERS: existing_config.get(CONF_PROGRAM_MARKERS, DEFAULT_PROGRAM_MARKERS),
        CONF_ENABLE_PROGRAM_SCAN: existing_config.get(CONF_ENABLE_PROGRAM_SCAN, DEFAULT_ENABLE_PROGRAM_SCAN),
        CONF_SYSVAR_MARKERS: existing_config.get(CONF_SYSVAR_MARKERS, DEFAULT_SYSVAR_MARKERS),
        CONF_ENABLE_SYSVAR_SCAN: existing_config.get(CONF_ENABLE_SYSVAR_SCAN, DEFAULT_ENABLE_SYSVAR_SCAN),
        CONF_SYS_SCAN_INTERVAL: existing_config.get(CONF_SYS_SCAN_INTERVAL, DEFAULT_SYS_SCAN_INTERVAL),
    }
    # Update with new advanced settings input
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SYSTEM_NOTIFICATIONS] = advanced_input[CONF_ENABLE_SYSTEM_NOTIFICATIONS]
    data[CONF_ADVANCED_CONFIG][CONF_LISTEN_ON_ALL_IP] = advanced_input[CONF_LISTEN_ON_ALL_IP]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_MQTT] = advanced_input[CONF_ENABLE_MQTT]
    data[CONF_ADVANCED_CONFIG][CONF_MQTT_PREFIX] = advanced_input[CONF_MQTT_PREFIX]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SUB_DEVICES] = advanced_input[CONF_ENABLE_SUB_DEVICES]
    data[CONF_ADVANCED_CONFIG][CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE] = advanced_input[
        CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE
    ]
    data[CONF_ADVANCED_CONFIG][CONF_OPTIONAL_SETTINGS] = advanced_input[CONF_OPTIONAL_SETTINGS]
    data[CONF_ADVANCED_CONFIG][CONF_BACKUP_PATH] = advanced_input.get(CONF_BACKUP_PATH, DEFAULT_BACKUP_PATH)

    if advanced_input.get(CONF_UN_IGNORES):
        data[CONF_ADVANCED_CONFIG][CONF_UN_IGNORES] = advanced_input[CONF_UN_IGNORES]


def _get_instance_name(friendly_name: Any | None) -> str | None:
    """Return the instance name from the friendly_name."""
    if not friendly_name:
        return None
    name = str(friendly_name)
    if name.startswith("OpenCCU - "):
        return name.replace("OpenCCU - ", "")
    if name.startswith("OpenCCU "):
        return name.replace("OpenCCU ", "")
    return name


def _get_serial(model_description: Any | None) -> str | None:
    """Return the serial from the model_description."""
    if not model_description:
        return None
    model_desc = str(model_description)
    if len(model_desc) > 10:
        return model_desc[-10:]
    return None
