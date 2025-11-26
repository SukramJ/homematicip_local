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
    DEFAULT_DELAY_NEW_DEVICE_CREATION,
    DEFAULT_ENABLE_PROGRAM_SCAN,
    DEFAULT_ENABLE_SYSVAR_SCAN,
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
    CONF_CALLBACK_HOST,
    CONF_CALLBACK_PORT_XML_RPC,
    CONF_DELAY_NEW_DEVICE_CREATION,
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
    DEFAULT_ENABLE_MQTT,
    DEFAULT_ENABLE_SUB_DEVICES,
    DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS,
    DEFAULT_LISTEN_ON_ALL_IP,
    DEFAULT_MQTT_PREFIX,
    DOMAIN,
)
from .control_unit import ControlConfig, ControlUnit, validate_config_and_get_system_information
from .support import InvalidConfig

_LOGGER = logging.getLogger(__name__)

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

IF_BIDCOS_RF_PORT: Final = 2001
IF_BIDCOS_RF_TLS_PORT: Final = 42001
IF_BIDCOS_WIRED_PORT: Final = 2000
IF_BIDCOS_WIRED_TLS_PORT: Final = 42000
IF_HMIP_RF_PORT: Final = 2010
IF_HMIP_RF_TLS_PORT: Final = 42010
IF_VIRTUAL_DEVICES_PORT: Final = 9292
IF_VIRTUAL_DEVICES_TLS_PORT: Final = 49292
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
    """Return the interface schema with or without tls ports."""
    return vol.Schema(
        {
            vol.Required(CONF_INSTANCE_NAME, default=data.get(CONF_INSTANCE_NAME) or UNDEFINED): TEXT_SELECTOR,
            vol.Required(CONF_HOST, default=data.get(CONF_HOST)): TEXT_SELECTOR,
            vol.Required(CONF_USERNAME, default=data.get(CONF_USERNAME)): TEXT_SELECTOR,
            vol.Required(CONF_PASSWORD, default=data.get(CONF_PASSWORD)): PASSWORD_SELECTOR,
            vol.Required(CONF_TLS, default=data.get(CONF_TLS, DEFAULT_TLS)): BOOLEAN_SELECTOR,
            vol.Required(CONF_VERIFY_TLS, default=data.get(CONF_VERIFY_TLS, False)): BOOLEAN_SELECTOR,
            vol.Optional(CONF_CALLBACK_HOST, default=data.get(CONF_CALLBACK_HOST) or UNDEFINED): TEXT_SELECTOR,
            vol.Optional(
                CONF_CALLBACK_PORT_XML_RPC, default=data.get(CONF_CALLBACK_PORT_XML_RPC) or UNDEFINED
            ): PORT_SELECTOR_OPTIONAL,
            vol.Optional(CONF_JSON_PORT, default=data.get(CONF_JSON_PORT) or UNDEFINED): PORT_SELECTOR_OPTIONAL,
        }
    )


def get_options_schema(data: ConfigType) -> Schema:
    """Return the options schema."""
    options_schema = get_domain_schema(data=data)
    del options_schema.schema[CONF_INSTANCE_NAME]
    return options_schema


def get_interface_schema(use_tls: bool, data: ConfigType, from_config_flow: bool) -> Schema:
    """Return the interface schema with or without tls ports."""
    interfaces = data.get(CONF_INTERFACE, {})
    # HmIP-RF
    enable_hmip_rf = Interface.HMIP_RF in interfaces
    hmip_port = (
        custom_port
        if (
            enable_hmip_rf
            and (custom_port := interfaces[Interface.HMIP_RF][CONF_PORT]) not in (IF_HMIP_RF_TLS_PORT, IF_HMIP_RF_PORT)
        )
        else (IF_HMIP_RF_TLS_PORT if use_tls else IF_HMIP_RF_PORT)
    )

    # BidCos-RF
    enable_bidcos_rf = Interface.BIDCOS_RF in interfaces
    bidcos_rf_port = (
        custom_port
        if (
            enable_bidcos_rf
            and (custom_port := interfaces[Interface.BIDCOS_RF][CONF_PORT])
            not in (IF_BIDCOS_RF_TLS_PORT, IF_BIDCOS_RF_PORT)
        )
        else (IF_BIDCOS_RF_TLS_PORT if use_tls else IF_BIDCOS_RF_PORT)
    )

    # Virtual devices
    enable_virtual_devices = Interface.VIRTUAL_DEVICES in interfaces
    virtual_devices_port = (
        custom_port
        if (
            enable_virtual_devices
            and (custom_port := interfaces[Interface.VIRTUAL_DEVICES][CONF_PORT])
            not in (IF_VIRTUAL_DEVICES_TLS_PORT, IF_VIRTUAL_DEVICES_PORT)
        )
        else (IF_VIRTUAL_DEVICES_TLS_PORT if use_tls else IF_VIRTUAL_DEVICES_PORT)
    )

    # BidCos-Wired
    enable_bidcos_wired = Interface.BIDCOS_WIRED in interfaces
    bidcos_wired_port = (
        custom_port
        if (
            enable_bidcos_wired
            and (custom_port := interfaces[Interface.BIDCOS_WIRED][CONF_PORT])
            not in (IF_BIDCOS_WIRED_TLS_PORT, IF_BIDCOS_WIRED_PORT)
        )
        else (IF_BIDCOS_WIRED_TLS_PORT if use_tls else IF_BIDCOS_WIRED_PORT)
    )

    # CCU-Jack
    enable_ccu_jack = Interface.CCU_JACK in interfaces
    # CUxD
    enable_cuxd = Interface.CUXD in interfaces

    advanced_config = bool(data.get(CONF_ADVANCED_CONFIG))
    interface_schema = vol.Schema(
        {
            vol.Required(CONF_ENABLE_HMIP_RF, default=enable_hmip_rf): BOOLEAN_SELECTOR,
            vol.Required(CONF_HMIP_RF_PORT, default=hmip_port): PORT_SELECTOR,
            vol.Required(CONF_ENABLE_BIDCOS_RF, default=enable_bidcos_rf): BOOLEAN_SELECTOR,
            vol.Required(CONF_BIDCOS_RF_PORT, default=bidcos_rf_port): PORT_SELECTOR,
            vol.Required(CONF_ENABLE_VIRTUAL_DEVICES, default=enable_virtual_devices): BOOLEAN_SELECTOR,
            vol.Required(CONF_VIRTUAL_DEVICES_PORT, default=virtual_devices_port): PORT_SELECTOR,
            vol.Required(CONF_VIRTUAL_DEVICES_PATH, default=IF_VIRTUAL_DEVICES_PATH): TEXT_SELECTOR,
            vol.Required(CONF_ENABLE_BIDCOS_WIRED, default=enable_bidcos_wired): BOOLEAN_SELECTOR,
            vol.Required(CONF_BIDCOS_WIRED_PORT, default=bidcos_wired_port): PORT_SELECTOR,
            vol.Required(CONF_ENABLE_CCU_JACK, default=enable_ccu_jack): BOOLEAN_SELECTOR,
            vol.Required(CONF_ENABLE_CUXD, default=enable_cuxd): BOOLEAN_SELECTOR,
            vol.Required(CONF_ADVANCED_CONFIG, default=advanced_config): BOOLEAN_SELECTOR,
        }
    )
    if from_config_flow:
        del interface_schema.schema[CONF_ADVANCED_CONFIG]
    return interface_schema


def get_advanced_schema(data: ConfigType, all_un_ignore_parameters: list[str]) -> Schema:
    """Return the advanced schema."""
    existing_parameters: list[str] = [
        p
        for p in data.get(CONF_ADVANCED_CONFIG, {}).get(CONF_UN_IGNORES, DEFAULT_UN_IGNORES)
        if p in all_un_ignore_parameters
    ]

    advanced_schema = vol.Schema(
        {
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
                CONF_DELAY_NEW_DEVICE_CREATION,
                default=data.get(CONF_ADVANCED_CONFIG, {}).get(
                    CONF_DELAY_NEW_DEVICE_CREATION, DEFAULT_DELAY_NEW_DEVICE_CREATION
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

    VERSION = 10
    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    def __init__(self) -> None:
        """Init the ConfigFlow."""
        self.data: ConfigType = {}
        self.serial: str | None = None
        self._detection_result: BackendDetectionResult | None = None
        self._detection_task: asyncio.Task[None] | None = None
        self._detection_error: str | None = None
        self._detection_error_detail: str | None = None

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

        return self.async_show_form(step_id="central", data_schema=get_domain_schema(data=self.data))

    async def async_step_central_error(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Handle return to central step with validation error."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        if self._detection_error:
            errors["base"] = self._detection_error
            # Always set invalid_items placeholder to avoid showing literal [{invalid_items}] in message
            description_placeholders["invalid_items"] = self._detection_error_detail or self.data.get(CONF_HOST, "")

        # Reset detection error state
        self._detection_error = None
        self._detection_error_detail = None

        return self.async_show_form(
            step_id="central",
            data_schema=get_domain_schema(data=self.data),
            errors=errors,
            description_placeholders=description_placeholders,
        )

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

    async def async_step_interface(
        self,
        interface_input: ConfigType | None = None,
    ) -> ConfigFlowResult:
        """Handle the interface step."""
        # Only process interface_input if it actually contains interface fields
        # (not if it's leftover user_input from previous steps)
        if interface_input is not None and CONF_ENABLE_HMIP_RF in interface_input:
            _update_interface_input(data=self.data, interface_input=interface_input)
            if interface_input.get(CONF_ADVANCED_CONFIG):
                return await self.async_step_advanced()
            return await self._validate_and_finish_config_flow()

        _LOGGER.debug("ConfigFlow.step_interface, no user input")
        return self.async_show_form(
            step_id="interface",
            data_schema=get_interface_schema(
                use_tls=self.data[CONF_TLS],
                data=self.data,
                from_config_flow=False,
            ),
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
            if interface == Interface.HMIP_RF:
                interfaces[Interface.HMIP_RF] = {
                    CONF_PORT: IF_HMIP_RF_TLS_PORT if use_tls else IF_HMIP_RF_PORT,
                }
            elif interface == Interface.BIDCOS_RF:
                interfaces[Interface.BIDCOS_RF] = {
                    CONF_PORT: IF_BIDCOS_RF_TLS_PORT if use_tls else IF_BIDCOS_RF_PORT,
                }
            elif interface == Interface.BIDCOS_WIRED:
                interfaces[Interface.BIDCOS_WIRED] = {
                    CONF_PORT: IF_BIDCOS_WIRED_TLS_PORT if use_tls else IF_BIDCOS_WIRED_PORT,
                }
            elif interface == Interface.VIRTUAL_DEVICES:
                interfaces[Interface.VIRTUAL_DEVICES] = {
                    CONF_PORT: IF_VIRTUAL_DEVICES_TLS_PORT if use_tls else IF_VIRTUAL_DEVICES_PORT,
                }

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
                    all_un_ignore_parameters=self._control_unit.central.get_un_ignore_candidates(include_master=True),
                ),
            )
        _update_advanced_input(data=self.data, advanced_input=advanced_input)
        return await self._validate_and_finish_options_flow()

    async def async_step_central(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Manage the Homematic(IP) Local for OpenCCU devices options."""
        if user_input is not None:
            self.data = _get_ccu_data(self.data, user_input=user_input)
            return await self.async_step_interface()

        return self.async_show_form(
            step_id="central",
            data_schema=get_options_schema(data=self.data),
        )

    async def async_step_init(self, user_input: ConfigType | None = None) -> ConfigFlowResult:
        """Manage the Homematic(IP) Local for OpenCCU options."""
        return await self.async_step_central(user_input=user_input)

    async def async_step_interface(
        self,
        interface_input: ConfigType | None = None,
    ) -> ConfigFlowResult:
        """Handle the interface step."""
        if interface_input is not None:
            _update_interface_input(data=self.data, interface_input=interface_input)
            if interface_input.get(CONF_ADVANCED_CONFIG):
                return await self.async_step_advanced()
            return await self._validate_and_finish_options_flow()

        _LOGGER.debug("ConfigFlow.step_interface, no user input")
        return self.async_show_form(
            step_id="interface",
            data_schema=get_interface_schema(
                use_tls=self.data[CONF_TLS],
                data=self.data,
                from_config_flow=False,
            ),
        )

    async def _validate_and_finish_options_flow(self) -> ConfigFlowResult:
        """Validate and finish the options flow."""

        errors = {}
        description_placeholders = {}

        try:
            system_information = await _async_validate_config_and_get_system_information(
                hass=self.hass, data=self.data, entry_id=self.entry.entry_id
            )
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
            if system_information is not None:
                self.hass.config_entries.async_update_entry(
                    entry=self.entry,
                    unique_id=system_information.serial,
                    data=self.data,
                )
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="central",
            data_schema=get_options_schema(data=self.data),
            errors=errors,
            description_placeholders=description_placeholders,
        )


def _get_ccu_data(data: ConfigType, user_input: ConfigType) -> ConfigType:
    ccu_data = {
        CONF_INSTANCE_NAME: user_input.get(CONF_INSTANCE_NAME, data.get(CONF_INSTANCE_NAME)),
        CONF_HOST: user_input[CONF_HOST],
        CONF_USERNAME: user_input[CONF_USERNAME],
        CONF_PASSWORD: user_input[CONF_PASSWORD],
        CONF_TLS: user_input[CONF_TLS],
        CONF_VERIFY_TLS: user_input[CONF_VERIFY_TLS],
        CONF_INTERFACE: data.get(CONF_INTERFACE, {}),
        CONF_ADVANCED_CONFIG: data.get(CONF_ADVANCED_CONFIG, {}),
    }
    if (callback_host := user_input.get(CONF_CALLBACK_HOST)) and callback_host.strip() != "":
        ccu_data[CONF_CALLBACK_HOST] = callback_host
    if (callback_port_xml_rpc := user_input.get(CONF_CALLBACK_PORT_XML_RPC)) is not None:
        ccu_data[CONF_CALLBACK_PORT_XML_RPC] = callback_port_xml_rpc
    if (json_port := user_input.get(CONF_JSON_PORT)) is not None:
        ccu_data[CONF_JSON_PORT] = json_port

    return ccu_data


def _update_interface_input(data: ConfigType, interface_input: ConfigType) -> None:
    if not interface_input:
        return

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
    if interface_input[CONF_ADVANCED_CONFIG] is False:
        data[CONF_ADVANCED_CONFIG] = {}


def _update_advanced_input(data: ConfigType, advanced_input: ConfigType) -> None:
    if not advanced_input:
        return

    data[CONF_ADVANCED_CONFIG] = {}
    data[CONF_ADVANCED_CONFIG][CONF_PROGRAM_MARKERS] = advanced_input[CONF_PROGRAM_MARKERS]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_PROGRAM_SCAN] = advanced_input[CONF_ENABLE_PROGRAM_SCAN]
    data[CONF_ADVANCED_CONFIG][CONF_SYSVAR_MARKERS] = advanced_input[CONF_SYSVAR_MARKERS]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SYSVAR_SCAN] = advanced_input[CONF_ENABLE_SYSVAR_SCAN]
    data[CONF_ADVANCED_CONFIG][CONF_SYS_SCAN_INTERVAL] = advanced_input[CONF_SYS_SCAN_INTERVAL]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SYSTEM_NOTIFICATIONS] = advanced_input[CONF_ENABLE_SYSTEM_NOTIFICATIONS]
    data[CONF_ADVANCED_CONFIG][CONF_LISTEN_ON_ALL_IP] = advanced_input[CONF_LISTEN_ON_ALL_IP]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_MQTT] = advanced_input[CONF_ENABLE_MQTT]
    data[CONF_ADVANCED_CONFIG][CONF_MQTT_PREFIX] = advanced_input[CONF_MQTT_PREFIX]
    data[CONF_ADVANCED_CONFIG][CONF_ENABLE_SUB_DEVICES] = advanced_input[CONF_ENABLE_SUB_DEVICES]
    data[CONF_ADVANCED_CONFIG][CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE] = advanced_input[
        CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE
    ]
    data[CONF_ADVANCED_CONFIG][CONF_DELAY_NEW_DEVICE_CREATION] = advanced_input[CONF_DELAY_NEW_DEVICE_CREATION]
    data[CONF_ADVANCED_CONFIG][CONF_OPTIONAL_SETTINGS] = advanced_input[CONF_OPTIONAL_SETTINGS]

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
