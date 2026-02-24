"""Homematic(IP) Local for OpenCCU is a Python 3 module for Home Assistant and Homematic(IP) devices."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from functools import partial
import logging
import time
from types import UnionType
from typing import Any, Final, Self, TypeVar, cast

from aiohomematic import __version__ as AIOHM_VERSION
from aiohomematic.central import CentralConfig, CentralUnit, check_config
from aiohomematic.central.events import (
    DataPointsCreatedEvent,
    DeviceLifecycleEvent,
    DeviceLifecycleEventType,
    DeviceTriggerEvent,
    OptimisticRollbackEvent,
    SystemStatusChangedEvent,
)
from aiohomematic.client import InterfaceConfig
from aiohomematic.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    DEFAULT_ENABLE_PROGRAM_SCAN,
    DEFAULT_ENABLE_SYSVAR_SCAN,
    DEFAULT_INTERFACES_REQUIRING_PERIODIC_REFRESH,
    DEFAULT_OPTIONAL_SETTINGS,
    DEFAULT_PROGRAM_MARKERS,
    DEFAULT_SYSVAR_MARKERS,
    DEFAULT_UN_IGNORES,
    DEFAULT_USE_GROUP_CHANNEL_FOR_COVER_STATE,
    IP_ANY_V4,
    PORT_ANY,
    CentralState,
    ClientState,
    DataPointCategory,
    DescriptionMarker,
    DeviceTriggerEventType,
    FailureReason,
    IntegrationIssueSeverity,
    IntegrationIssueType,
    Interface,
    Manufacturer,
    OptionalSettings,
    ScheduleTimerConfig,
    SystemInformation,
    TimeoutConfig,
    get_interface_default_port,
)
from aiohomematic.exceptions import AuthFailure, BaseHomematicException
from aiohomematic.model.data_point import CallbackDataPoint
from aiohomematic.support.address import get_device_address
from aiohomematic.type_aliases import UnsubscribeCallback
from homeassistant.const import CONF_HOST, CONF_PATH, CONF_PORT
from homeassistant.core import HomeAssistant, callback

# --- Repairs/fix flow support ---
from homeassistant.helpers import aiohttp_client, device_registry as dr, issue_registry as ir
from homeassistant.helpers.device_registry import DeviceEntry, DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.issue_registry import async_delete_issue

from .const import (
    CONF_ADVANCED_CONFIG,
    CONF_BACKUP_PATH,
    CONF_CALLBACK_HOST,
    CONF_CALLBACK_PORT_XML_RPC,
    CONF_COMMAND_THROTTLE_INTERVAL,
    CONF_ENABLE_CONFIG_PANEL,
    CONF_ENABLE_LIGHT_LAST_BRIGHTNESS,
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
    DEFAULT_COMMAND_THROTTLE_INTERVAL,
    DEFAULT_ENABLE_CONFIG_PANEL,
    DEFAULT_ENABLE_DEVICE_FIRMWARE_CHECK,
    DEFAULT_ENABLE_LIGHT_LAST_BRIGHTNESS,
    DEFAULT_ENABLE_MQTT,
    DEFAULT_ENABLE_SUB_DEVICES,
    DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS,
    DEFAULT_LISTEN_ON_ALL_IP,
    DEFAULT_MQTT_PREFIX,
    DEFAULT_SYS_SCAN_INTERVAL,
    DOMAIN,
    EVENT_ADDRESS,
    EVENT_AGE_SECONDS,
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
    EVENT_REASON,
    EVENT_RESTORED_VALUE,
    EVENT_ROLLED_BACK_VALUE,
    EVENT_TITLE,
    EVENT_UNAVAILABLE,
    EVENT_VALUE,
    FILTER_ERROR_EVENT_PARAMETERS,
)
from .mqtt import MQTTConsumer
from .repairs import REPAIR_CALLBACKS
from .support import (
    CLICK_EVENT_SCHEMA,
    DEVICE_AVAILABILITY_EVENT_SCHEMA,
    DEVICE_ERROR_EVENT_SCHEMA,
    InvalidConfig,
    cleanup_click_event_data,
    is_valid_event,
)

_LOGGER = logging.getLogger(__name__)

# Event type for device availability (not in DeviceTriggerEventType as it comes from DeviceLifecycleEvent)
EVENT_TYPE_DEVICE_AVAILABILITY: Final = "homematic.device_availability"
# Event type for optimistic rollback (from OptimisticRollbackEvent)
EVENT_TYPE_OPTIMISTIC_ROLLBACK: Final = f"{DOMAIN}.optimistic_rollback"

_DATA_POINT_T = TypeVar("_DATA_POINT_T", bound=CallbackDataPoint)


class BaseControlUnit:
    """Base central point to control a central unit."""

    def __init__(self, *, control_config: ControlConfig, central: CentralUnit) -> None:
        """Init the control unit."""
        self._config: Final = control_config
        self._hass: Final = control_config.hass
        self._entry_id: Final = control_config.entry_id
        self._instance_name: Final = control_config.instance_name
        self._backup_directory: Final = control_config.backup_directory
        self._enable_config_panel: Final = control_config.enable_config_panel
        self._enable_light_last_brightness: Final = control_config.enable_light_last_brightness
        self._enable_mqtt: Final = control_config.enable_mqtt
        self._enable_sub_devices: Final = control_config.enable_sub_devices
        self._mqtt_prefix: Final = control_config.mqtt_prefix
        self._enable_system_notifications: Final = control_config.enable_system_notifications
        self._central: Final = central
        self._attr_device_info: Final = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self._central.name,
                )
            },
            manufacturer=Manufacturer.EQ3,
            model=self._central.model,
            name=self._central.name,
            serial_number=self._central.system_information.serial,
            sw_version=self._central.version,
        )
        self._unsubscribe_callbacks: Final[list[UnsubscribeCallback]] = []

    @classmethod
    async def async_create(cls, *, control_config: ControlConfig) -> Self:
        """Create a new control unit instance asynchronously."""
        central = await control_config.create_central()
        return cls(control_config=control_config, central=central)

    @property
    def backup_directory(self) -> str:
        """Return the backup directory path."""
        return self._backup_directory

    @property
    def central(self) -> CentralUnit:
        """Return the Homematic(IP) Local for OpenCCU central unit instance."""
        return self._central

    @property
    def config(self) -> ControlConfig:
        """Return the control unit configuration."""
        return self._config

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device specific attributes."""
        return self._attr_device_info

    @property
    def enable_config_panel(self) -> bool:
        """Return if the configuration panel is enabled."""
        return self._enable_config_panel

    @property
    def enable_light_last_brightness(self) -> bool:
        """Return if last brightness for lights is enabled."""
        return self._enable_light_last_brightness

    @property
    def enable_sub_devices(self) -> bool:
        """Return if sub devices are enabled."""
        return self._enable_sub_devices

    @property
    def entry_id(self) -> str:
        """Return the Homematic(IP) Local config entry id."""
        return self._entry_id

    async def start_central(self) -> None:
        """Start the central unit."""
        _LOGGER.debug(
            "Starting central unit %s",
            self._instance_name,
        )
        try:
            await self._central.start()
            _LOGGER.info("Started central unit for %s (%s)", self._instance_name, AIOHM_VERSION)
        except AuthFailure:
            # Don't catch - let it propagate to trigger reauth
            raise
        except BaseHomematicException as ex:
            _LOGGER.warning(
                "START_CENTRAL: Failed to start central unit for %s: %s",
                self._instance_name,
                ex,
                exc_info=True,
            )

    async def stop_central(self, *args: Any) -> None:
        """Stop the control unit."""
        _LOGGER.debug(
            "Stopping central unit %s",
            self._instance_name,
        )
        if self._central.state != CentralState.STOPPED:
            await self._central.stop()
            _LOGGER.info("Stopped central unit for %s", self._instance_name)


class ControlUnit(BaseControlUnit):
    """Unit to control a central unit."""

    def __init__(self, *, control_config: ControlConfig, central: CentralUnit) -> None:
        """Init the control unit."""
        super().__init__(control_config=control_config, central=central)
        self._mqtt_consumer: MQTTConsumer | None = None
        self._auto_confirm_until: Final = control_config.auto_confirm_until

    def ensure_via_device_exists(self, identifier: str, suggested_area: str | None, via_device: str) -> None:
        """Create a via device for a device."""
        device_registry = dr.async_get(self._hass)

        if device_registry.async_get_device(identifiers={(DOMAIN, via_device)}) is not None:
            return

        if via_device != self.central.name:
            device_registry.async_get_or_create(
                config_entry_id=self._entry_id,
                identifiers={
                    (
                        DOMAIN,
                        via_device,
                    )
                },
                suggested_area=suggested_area,
                via_device=(DOMAIN, self.central.name),
            )

        device_registry.async_get_or_create(
            config_entry_id=self._entry_id,
            identifiers={
                (
                    DOMAIN,
                    identifier,
                )
            },
            suggested_area=suggested_area,
            via_device=(DOMAIN, via_device),
        )

    def get_new_data_points(
        self,
        *,
        data_point_type: type[_DATA_POINT_T] | UnionType,
    ) -> tuple[_DATA_POINT_T, ...]:
        """Return all data points by type."""
        category = (
            data_point_type.__args__[0].default_category()
            if isinstance(data_point_type, UnionType)
            else data_point_type.default_category()
        )
        return cast(
            tuple[_DATA_POINT_T, ...],
            self.central.query_facade.get_data_points(
                category=category,
                exclude_no_create=True,
                registered=False,
            ),
        )

    def get_new_hub_data_points(
        self,
        *,
        data_point_type: type[_DATA_POINT_T],
    ) -> tuple[_DATA_POINT_T, ...]:
        """Return all data points by type."""
        return cast(
            tuple[_DATA_POINT_T, ...],
            self.central.hub_coordinator.get_hub_data_points(
                category=data_point_type.default_category(),
                registered=False,
            ),
        )

    async def start_central(self) -> None:
        """Start the central unit."""
        # Clean up stale callback repair issues from previous sessions
        # (e.g., from PingPong race condition bug fixed in aiohomematic 2026.1.3)
        self._cleanup_callback_issues()

        # Subscribe to integration events (5 focused subscriptions)
        _LOGGER.debug("Subscribing to integration events")
        self._unsubscribe_callbacks.append(
            self._central.event_bus.subscribe(
                event_type=SystemStatusChangedEvent,
                event_key=None,
                handler=self._on_system_status,
            )
        )
        self._unsubscribe_callbacks.append(
            self._central.event_bus.subscribe(
                event_type=DeviceLifecycleEvent,
                event_key=None,
                handler=self._on_device_lifecycle,
            )
        )
        self._unsubscribe_callbacks.append(
            self._central.event_bus.subscribe(
                event_type=DataPointsCreatedEvent,
                event_key=None,
                handler=self._on_data_points_created,
            )
        )
        self._unsubscribe_callbacks.append(
            self._central.event_bus.subscribe(
                event_type=DeviceTriggerEvent,
                event_key=None,
                handler=self._on_device_trigger,
            )
        )
        self._unsubscribe_callbacks.append(
            self._central.event_bus.subscribe(
                event_type=OptimisticRollbackEvent,
                event_key=None,
                handler=self._on_optimistic_rollback,
            )
        )
        self._async_add_central_to_device_registry()
        await super().start_central()
        if self._enable_mqtt:
            self._mqtt_consumer = MQTTConsumer(hass=self._hass, central=self._central, mqtt_prefix=self._mqtt_prefix)
            await self._mqtt_consumer.subscribe()

    async def stop_central(self, *args: Any) -> None:
        """Stop the central unit."""
        if self._mqtt_consumer:
            self._mqtt_consumer.unsubscribe()

        for unregister in self._unsubscribe_callbacks:
            if unregister is not None:
                unregister()

        await super().stop_central(*args)

    @callback
    def _async_add_central_to_device_registry(self) -> None:
        """Add the central to device registry."""
        device_registry = dr.async_get(self._hass)
        device_registry.async_get_or_create(
            config_entry_id=self._entry_id,
            identifiers={
                (
                    DOMAIN,
                    self._central.name,
                )
            },
            manufacturer=Manufacturer.EQ3,
            model=self._central.model,
            sw_version=self._central.version,
            name=self._central.name,
            entry_type=DeviceEntryType.SERVICE,
            configuration_url=self._central.url,
        )

    @callback
    def _async_add_virtual_remotes_to_device_registry(self) -> None:
        """Add the virtual remotes to device registry."""
        if not self._central.client_coordinator.has_clients:
            _LOGGER.error(
                "Cannot create ControlUnit %s virtual remote devices. No clients",
                self._instance_name,
            )
            return

        device_registry = dr.async_get(self._hass)
        for virtual_remote in self._central.device_coordinator.get_virtual_remotes():
            device_registry.async_get_or_create(
                config_entry_id=self._entry_id,
                identifiers={
                    (
                        DOMAIN,
                        virtual_remote.identifier,
                    )
                },
                manufacturer=Manufacturer.EQ3,
                name=virtual_remote.name,
                model=virtual_remote.model,
                sw_version=virtual_remote.firmware,
                # Link to the Homematic control unit.
                via_device=(DOMAIN, self._central.name),
            )

    @callback
    def _async_get_device_entry(self, *, device_address: str) -> DeviceEntry | None:
        """Return the device of the ha device."""
        if (hm_device := self._central.device_coordinator.get_device(address=device_address)) is None:
            return None
        device_registry = dr.async_get(self._hass)
        return device_registry.async_get_device(
            identifiers={
                (
                    DOMAIN,
                    hm_device.identifier,
                )
            }
        )

    @callback
    def _cleanup_callback_issues(self) -> None:
        """Clean up stale callback repair issues from previous sessions."""
        for interface_name in self._config.interface_config:
            interface_id = f"{self._instance_name}-{interface_name}"
            async_delete_issue(
                hass=self._hass,
                domain=DOMAIN,
                issue_id=f"{self._entry_id}_callback_{interface_id}",
            )

    @callback
    def _fire_device_availability_event(self, *, device_address: str, available: bool) -> None:
        """Fire device availability event to HA event bus."""
        hm_device = self._central.device_coordinator.get_device(address=device_address)
        if hm_device is None:
            _LOGGER.debug("Cannot fire availability event: device %s not found", device_address)
            return

        # Build base event data
        event_data: dict[str, Any] = {
            EVENT_INTERFACE_ID: hm_device.interface_id,
            EVENT_ADDRESS: device_address,
            EVENT_CHANNEL_NO: 0,  # Availability is per device, not channel
            EVENT_MODEL: hm_device.model,
            EVENT_PARAMETER: "AVAILABILITY",
        }

        # Lookup device for device_id and name
        name: str | None = None
        if device_entry := self._async_get_device_entry(device_address=device_address):
            name = device_entry.name_by_user or device_entry.name
            event_data[EVENT_DEVICE_ID] = device_entry.id
            event_data[EVENT_NAME] = name

        title = f"{DOMAIN.upper()} Device {'Available' if available else 'Unavailable'}"
        availability_message = (
            f"{name}/{device_address} on interface {hm_device.interface_id}: "
            f"{'available' if available else 'unavailable'}"
        )

        event_data.update(
            {
                EVENT_IDENTIFIER: f"{device_address}_availability",
                EVENT_TITLE: title,
                EVENT_MESSAGE: availability_message,
                EVENT_UNAVAILABLE: not available,
            }
        )

        if is_valid_event(event_data=event_data, schema=DEVICE_AVAILABILITY_EVENT_SCHEMA):
            self._hass.bus.async_fire(
                event_type=EVENT_TYPE_DEVICE_AVAILABILITY,
                event_data=event_data,
            )

    def _handle_degraded_state(self, event: SystemStatusChangedEvent, issue_id_degraded: str) -> bool:
        """Handle DEGRADED central state. Return True if reauth was triggered."""
        # Check if any degraded interface has an authentication failure
        auth_failed_interfaces: list[str] = []
        if event.degraded_interfaces:
            for interface_id, reason in event.degraded_interfaces.items():
                if reason == FailureReason.AUTH:
                    auth_failed_interfaces.append(interface_id)
                    _LOGGER.warning(
                        "Interface %s in DEGRADED state due to authentication error",
                        interface_id,
                    )

        # If any interface has AUTH failure, trigger reauth
        if auth_failed_interfaces:
            _LOGGER.warning(
                "Central %s DEGRADED due to authentication error on interfaces: %s. Triggering reauthentication flow",
                self._instance_name,
                ", ".join(auth_failed_interfaces),
            )
            # Get config entry and trigger reauth
            if entry := self._hass.config_entries.async_get_entry(self._entry_id):
                entry.async_start_reauth(self._hass)
            return True

        # No AUTH failures - create normal degraded warning if enabled
        if self._enable_system_notifications:
            ir.async_create_issue(
                hass=self._hass,
                domain=DOMAIN,
                issue_id=issue_id_degraded,
                is_fixable=False,
                severity=ir.IssueSeverity.WARNING,
                translation_key="central_degraded",
                translation_placeholders={
                    "instance_name": self._instance_name,
                    "reason": "Some interfaces disconnected",
                },
            )
            _LOGGER.warning("Central %s is DEGRADED - some interfaces disconnected", self._instance_name)
        else:
            # Also delete DEGRADED issue if notifications are disabled
            async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id_degraded)
            _LOGGER.debug("SYSTEM NOTIFICATION disabled for DEGRADED state")
        return False

    def _handle_failed_state(self, event: SystemStatusChangedEvent, issue_id_failed: str) -> bool:
        """Handle FAILED central state. Return True if reauth was triggered."""
        # Check if failure is due to authentication issue
        if event.failure_reason == FailureReason.AUTH:
            # Trigger reauth flow for authentication failures
            _LOGGER.warning(
                "Central %s FAILED due to authentication error. Triggering reauthentication flow",
                self._instance_name,
            )
            # Get config entry and trigger reauth
            if entry := self._hass.config_entries.async_get_entry(self._entry_id):
                entry.async_start_reauth(self._hass)
            return True

        # For non-auth failures, create appropriate repair issue
        if self._enable_system_notifications:
            translation_key = "central_failed"
            reason_text = "All recovery attempts exhausted"

            # Customize message based on failure reason
            if event.failure_reason == FailureReason.NETWORK:
                translation_key = "central_failed_network"
                reason_text = "Network connectivity issue"
            elif event.failure_reason == FailureReason.TIMEOUT:
                translation_key = "central_failed_timeout"
                reason_text = "Connection timeout"
            elif event.failure_reason == FailureReason.INTERNAL:
                translation_key = "central_failed_internal"
                reason_text = "CCU internal error"

            ir.async_create_issue(
                hass=self._hass,
                domain=DOMAIN,
                issue_id=issue_id_failed,
                is_fixable=False,
                severity=ir.IssueSeverity.ERROR,
                translation_key=translation_key,
                translation_placeholders={
                    "instance_name": self._instance_name,
                    "reason": reason_text,
                    "interface_id": event.failure_interface_id or "Unknown",
                },
            )
            _LOGGER.error(
                "Central %s FAILED - %s (interface: %s)",
                self._instance_name,
                reason_text,
                event.failure_interface_id or "Unknown",
            )
        else:
            # Also delete FAILED issue if notifications are disabled
            async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id_failed)
            _LOGGER.debug("SYSTEM NOTIFICATION disabled for FAILED state")
        return False

    async def _on_data_points_created(self, event: DataPointsCreatedEvent) -> None:
        """Handle data points created event from aiohomematic (Entity discovery)."""
        for category, data_points in event.new_data_points.items():
            if data_points and len(data_points) > 0:
                async_dispatcher_send(
                    self._hass,
                    signal_new_data_point(entry_id=self._entry_id, platform=category),
                    data_points,
                )

    async def _on_device_lifecycle(self, event: DeviceLifecycleEvent) -> None:
        """Handle device lifecycle event from aiohomematic (Device lifecycle + availability)."""
        if event.event_type == DeviceLifecycleEventType.CREATED:
            _LOGGER.debug("Devices created: %s", event.device_addresses)
            if event.includes_virtual_remotes:
                self._async_add_virtual_remotes_to_device_registry()

        elif event.event_type == DeviceLifecycleEventType.DELAYED:
            _LOGGER.debug("Devices delayed: %s on interface %s", event.device_addresses, event.interface_id)
            interface_id = event.interface_id
            if not interface_id:
                return

            # Check if we're in auto-confirm window (initial setup)
            if self._auto_confirm_until is not None and time.time() < self._auto_confirm_until:
                _LOGGER.debug(
                    "Auto-confirming devices during initial setup: %s on interface %s",
                    event.device_addresses,
                    interface_id,
                )
                # Directly add devices without creating repair issues
                await self._central.device_coordinator.add_new_devices_manually(
                    interface_id=interface_id,
                    address_names=dict.fromkeys(event.device_addresses, ""),
                )
                return

            # Check which devices already exist in HA device registry (e.g., after cache clear)
            # These should be auto-confirmed without creating repair issues
            device_registry = dr.async_get(self._hass)
            existing_addresses: list[str] = []
            new_addresses: list[str] = []

            for address in event.device_addresses:
                # Device identifier format is: {address}@{interface_id}
                expected_identifier = f"{address}@{interface_id}"
                if device_registry.async_get_device(identifiers={(DOMAIN, expected_identifier)}):
                    existing_addresses.append(address)
                else:
                    new_addresses.append(address)

            # Auto-confirm devices that already exist in HA (cache was cleared but devices are known)
            if existing_addresses:
                _LOGGER.debug(
                    "Auto-confirming existing devices after cache clear: %s on interface %s",
                    existing_addresses,
                    interface_id,
                )
                await self._central.device_coordinator.add_new_devices_manually(
                    interface_id=interface_id,
                    address_names=dict.fromkeys(existing_addresses, ""),
                )

            # Create repair issues only for truly new devices
            for address in new_addresses:
                issue_id = f"devices_delayed|{interface_id}|{address}"

                async def _fix_callback(*, device_name: str, _interface_id: str, _address: str) -> None:
                    """Rename, accept inbox device, and trigger manual add of the delayed device."""
                    if not _interface_id:
                        return
                    # Trigger manual add of the device
                    await self._central.device_coordinator.add_new_devices_manually(
                        interface_id=_interface_id, address_names={_address: device_name}
                    )

                REPAIR_CALLBACKS[issue_id] = partial(_fix_callback, _interface_id=interface_id, _address=address)

                ir.async_create_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=issue_id,
                    is_fixable=True,
                    severity=ir.IssueSeverity.WARNING,
                    translation_key="devices_delayed",
                    translation_placeholders={
                        "instance_name": self._instance_name,
                        "interface_id": interface_id,
                        "address": address,
                    },
                )

        elif event.event_type == DeviceLifecycleEventType.AVAILABILITY_CHANGED:
            for device_address, available in event.availability_changes:
                _LOGGER.debug("Device %s availability: %s", device_address, available)

                # Fire HA event for automations (e.g., blueprints)
                self._fire_device_availability_event(
                    device_address=device_address,
                    available=available,
                )

    async def _on_device_trigger(self, event: DeviceTriggerEvent) -> None:
        """Handle device trigger event from aiohomematic (Device triggers for HA event bus)."""

        device_address = event.device_address
        # Build base event data
        event_data: dict[str, Any] = {
            EVENT_INTERFACE_ID: event.interface_id,
            EVENT_ADDRESS: device_address,
            EVENT_CHANNEL_NO: event.channel_no,
            EVENT_MODEL: event.model,
            EVENT_PARAMETER: event.parameter,
            EVENT_VALUE: event.value,
        }

        # Lookup device for device_id and name
        name: str | None = None
        if device_entry := self._async_get_device_entry(device_address=device_address):
            name = device_entry.name_by_user or device_entry.name
            event_data[EVENT_DEVICE_ID] = device_entry.id
            event_data[EVENT_NAME] = name

        trigger_type = event.trigger_type

        if trigger_type in (DeviceTriggerEventType.IMPULSE, DeviceTriggerEventType.KEYPRESS):
            # Transform data to match CLICK_EVENT_SCHEMA
            cleaned_event_data = cleanup_click_event_data(event_data=event_data)
            if is_valid_event(event_data=cleaned_event_data, schema=CLICK_EVENT_SCHEMA):
                self._hass.bus.async_fire(
                    event_type=trigger_type.value,
                    event_data=cleaned_event_data,
                )

        elif trigger_type == DeviceTriggerEventType.DEVICE_ERROR:
            error_parameter = event.parameter
            if error_parameter in FILTER_ERROR_EVENT_PARAMETERS:
                return

            error_parameter_display = error_parameter.replace("_", " ").title()
            title = f"{DOMAIN.upper()} Device Error"
            error_message: str = ""
            error_value = event.value
            display_error: bool = False

            if isinstance(error_value, bool):
                display_error = error_value
                error_message = f"{name}/{device_address} on interface {event.interface_id}: {error_parameter_display}"
            if isinstance(error_value, int):
                display_error = error_value != 0
                error_message = (
                    f"{name}/{device_address} on interface {event.interface_id}: "
                    f"{error_parameter_display} {error_value}"
                )

            event_data.update(
                {
                    EVENT_IDENTIFIER: f"{device_address}_{error_parameter}",
                    EVENT_TITLE: title,
                    EVENT_MESSAGE: error_message,
                    EVENT_ERROR_VALUE: error_value,
                    EVENT_ERROR: display_error,
                }
            )
            if is_valid_event(event_data=event_data, schema=DEVICE_ERROR_EVENT_SCHEMA):
                self._hass.bus.async_fire(
                    event_type=trigger_type.value,
                    event_data=event_data,
                )

    async def _on_optimistic_rollback(self, event: OptimisticRollbackEvent) -> None:
        """Handle optimistic rollback event from aiohomematic."""
        if not self._enable_system_notifications:
            return

        device_address = get_device_address(address=event.dpk.channel_address)

        # Resolve device name from HA device registry
        name: str | None = None
        if device_entry := self._async_get_device_entry(device_address=device_address):
            name = device_entry.name_by_user or device_entry.name

        display_name = name or device_address

        event_data: dict[str, Any] = {
            EVENT_INTERFACE_ID: event.dpk.interface_id,
            EVENT_ADDRESS: device_address,
            EVENT_PARAMETER: event.dpk.parameter,
            EVENT_REASON: event.reason,
            EVENT_ROLLED_BACK_VALUE: event.rolled_back_value,
            EVENT_RESTORED_VALUE: event.restored_value,
            EVENT_AGE_SECONDS: event.age_seconds,
        }

        if device_entry:
            event_data[EVENT_DEVICE_ID] = device_entry.id
            event_data[EVENT_NAME] = display_name

        if event.error:
            event_data[EVENT_ERROR] = event.error

        self._hass.bus.async_fire(
            event_type=EVENT_TYPE_OPTIMISTIC_ROLLBACK,
            event_data=event_data,
        )

        _LOGGER.warning(
            "Optimistic rollback for %s/%s: %s -> %s (reason=%s, age=%.1fs)",
            display_name,
            event.dpk.parameter,
            event.rolled_back_value,
            event.restored_value,
            event.reason,
            event.age_seconds,
        )

    async def _on_system_status(self, event: SystemStatusChangedEvent) -> None:
        """Handle system status event from aiohomematic (Infrastructure + Lifecycle)."""
        # Central state changes
        if event.central_state:
            central_state = event.central_state
            issue_id_degraded = f"{self._entry_id}_central_degraded"
            issue_id_failed = f"{self._entry_id}_central_failed"

            match central_state:
                case CentralState.RUNNING:
                    # All interfaces connected - remove any existing issues
                    async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id_degraded)
                    async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id_failed)
                    _LOGGER.info("Central %s is RUNNING - all interfaces connected", self._instance_name)

                case CentralState.DEGRADED:
                    # Some interfaces disconnected - check if any have authentication issues
                    async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id_failed)
                    if self._handle_degraded_state(event, issue_id_degraded):
                        return  # Reauth triggered, don't create repair issue

                case CentralState.RECOVERING:
                    # Active recovery in progress - no issue changes
                    _LOGGER.info("Central %s is RECOVERING - attempting reconnection", self._instance_name)

                case CentralState.FAILED:
                    # Critical error - all recovery attempts failed
                    async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id_degraded)
                    if self._handle_failed_state(event, issue_id_failed):
                        return  # Reauth triggered, don't create repair issue

            # Fire HA event for automations
            self._hass.bus.async_fire(
                event_type=f"{DOMAIN}.central_state_changed",
                event_data={
                    "instance_name": self._instance_name,
                    "new_state": central_state.value,
                },
            )

        # Connection state changes: tuple[str, bool] = (interface_id, connected)
        if event.connection_state:
            interface_id, connected = event.connection_state
            _LOGGER.debug("Connection state for %s: connected=%s", interface_id, connected)
            if not connected:
                ir.async_create_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=f"{self._entry_id}_connection_{interface_id}",
                    is_fixable=False,
                    severity=ir.IssueSeverity.ERROR,
                    translation_key="connection_failed",
                    translation_placeholders={"interface_id": interface_id},
                )
            else:
                # Connection restored - delete issue
                async_delete_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=f"{self._entry_id}_connection_{interface_id}",
                )

            # Fire HA event for automations
            self._hass.bus.async_fire(
                event_type=f"{DOMAIN}.interface_connection_changed",
                event_data={
                    "instance_name": self._instance_name,
                    "interface_id": interface_id,
                    "connected": connected,
                },
            )

        # Client state changes: tuple[str, ClientState, ClientState] = (interface_id, old_state, new_state)
        if event.client_state:
            interface_id, old_state, new_state = event.client_state
            _LOGGER.debug("Client state for %s: %s -> %s", interface_id, old_state, new_state)
            if new_state == ClientState.CONNECTED:
                # Client connected - delete issue
                async_delete_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=f"{self._entry_id}_client_{interface_id}",
                )
            elif new_state == ClientState.DISCONNECTED:
                ir.async_create_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=f"{self._entry_id}_client_{interface_id}",
                    is_fixable=False,
                    severity=ir.IssueSeverity.ERROR,
                    translation_key="client_failed",
                    translation_placeholders={"interface_id": interface_id},
                )

        # Callback state changes: tuple[str, bool] = (interface_id, alive)
        if event.callback_state:
            interface_id, alive = event.callback_state
            _LOGGER.debug("Callback state for %s: alive=%s", interface_id, alive)
            if alive:
                # Callback alive - delete issue
                async_delete_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=f"{self._entry_id}_callback_{interface_id}",
                )
            else:
                ir.async_create_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=f"{self._entry_id}_callback_{interface_id}",
                    is_fixable=False,
                    severity=ir.IssueSeverity.ERROR,
                    translation_key="callback_server_failed",
                    translation_placeholders={"interface_id": interface_id},
                )

        # Issues from aiohomematic
        for issue in event.issues:
            issue_id = f"{self._entry_id}_{issue.issue_id}"
            # For ping_pong_mismatch issues:
            # - Delete the issue when mismatch_count drops to 0 (recovery signal)
            # - Only create repair issues for ERROR severity (above threshold)
            # - WARNING severity is for telemetry only, not user-facing repair issues
            if issue.issue_type == IntegrationIssueType.PING_PONG_MISMATCH and (
                issue.mismatch_count == 0 or issue.severity == IntegrationIssueSeverity.WARNING
            ):
                async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id)
                continue
            # PARAMSET_INCONSISTENCY issues are WARNING severity but should create repair issues
            # to inform users about potential device problems after firmware updates
            if issue.issue_type == IntegrationIssueType.PARAMSET_INCONSISTENCY:
                ir.async_create_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=issue_id,
                    is_fixable=False,
                    severity=ir.IssueSeverity.WARNING,
                    learn_more_url="https://homematic-forum.de/forum/viewtopic.php?t=77531",
                    translation_key=issue.translation_key,
                    translation_placeholders=issue.translation_placeholders,
                )
                continue
            # Only create repair issues for ERROR severity
            if issue.severity == IntegrationIssueSeverity.ERROR:
                ir.async_create_issue(
                    hass=self._hass,
                    domain=DOMAIN,
                    issue_id=issue_id,
                    is_fixable=False,
                    severity=ir.IssueSeverity.ERROR,
                    translation_key=issue.translation_key,
                    translation_placeholders=issue.translation_placeholders,
                )


class ControlUnitTemp(BaseControlUnit):
    """Central unit to control a central unit for temporary usage."""

    async def stop_central(self, *args: Any) -> None:
        """Stop the control unit."""
        await self._central.cache_coordinator.clear_all()
        await super().stop_central(*args)


class ControlConfig:
    """Config for a ControlUnit."""

    def __init__(
        self,
        *,
        hass: HomeAssistant,
        entry_id: str,
        data: Mapping[str, Any],
        auto_confirm_until: float | None = None,
        default_callback_port_xml_rpc: int = PORT_ANY,
        enable_device_firmware_check: bool = DEFAULT_ENABLE_DEVICE_FIRMWARE_CHECK,
        start_direct: bool = False,
    ) -> None:
        """Create the required config for the ControlUnit."""
        self.hass: Final = hass
        self.entry_id: Final = entry_id
        self._data: Final = data
        self.auto_confirm_until: Final = auto_confirm_until
        self._default_callback_port_xml_rpc: Final = default_callback_port_xml_rpc
        self._start_direct: Final = start_direct
        self._enable_device_firmware_check: Final = enable_device_firmware_check

        # central
        self.instance_name: Final[str] = _cleanup_instance_name(instance_name=self._data[CONF_INSTANCE_NAME])
        self._host: Final[str] = self._data[CONF_HOST]
        self._username: Final[str] = self._data[CONF_USERNAME]
        self._password: Final[str] = self._data[CONF_PASSWORD]
        self._tls: Final[bool] = self._data[CONF_TLS]
        self._verify_tls: Final[bool] = self._data[CONF_VERIFY_TLS]
        self._callback_host: Final[str | None] = self._data.get(CONF_CALLBACK_HOST)
        self._callback_port_xml_rpc: Final[int | None] = self._data.get(CONF_CALLBACK_PORT_XML_RPC)
        self._json_port: Final[int | None] = self._data.get(CONF_JSON_PORT)

        # interface_config
        self._interface_config: Final[Mapping[str, Any]] = self._data.get(CONF_INTERFACE, {})
        # advanced_config
        ac = self._data.get(CONF_ADVANCED_CONFIG, {})
        self.enable_config_panel: Final[bool] = ac.get(CONF_ENABLE_CONFIG_PANEL, DEFAULT_ENABLE_CONFIG_PANEL)
        self.enable_light_last_brightness: Final[bool] = ac.get(
            CONF_ENABLE_LIGHT_LAST_BRIGHTNESS, DEFAULT_ENABLE_LIGHT_LAST_BRIGHTNESS
        )
        self.enable_mqtt: Final[bool] = ac.get(CONF_ENABLE_MQTT, DEFAULT_ENABLE_MQTT)
        self._enable_program_scan: Final[bool] = ac.get(CONF_ENABLE_PROGRAM_SCAN, DEFAULT_ENABLE_PROGRAM_SCAN)
        self.enable_sub_devices: Final[bool] = ac.get(CONF_ENABLE_SUB_DEVICES, DEFAULT_ENABLE_SUB_DEVICES)
        self.enable_system_notifications: Final[bool] = ac.get(
            CONF_ENABLE_SYSTEM_NOTIFICATIONS, DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS
        )
        self._enable_sysvar_scan: Final[bool] = ac.get(CONF_ENABLE_SYSVAR_SCAN, DEFAULT_ENABLE_SYSVAR_SCAN)
        self._listen_on_all_ip: Final[bool] = ac.get(CONF_LISTEN_ON_ALL_IP, DEFAULT_LISTEN_ON_ALL_IP)
        self.mqtt_prefix: Final[str] = ac.get(CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX)
        self._optional_settings: Final[tuple[OptionalSettings | str, ...]] = (
            optional_settings if (optional_settings := ac.get(CONF_OPTIONAL_SETTINGS)) else DEFAULT_OPTIONAL_SETTINGS
        )
        self._program_markers: Final[tuple[DescriptionMarker | str, ...]] = (
            program_markers if (program_markers := ac.get(CONF_PROGRAM_MARKERS)) else DEFAULT_PROGRAM_MARKERS
        )
        self._sys_scan_interval: Final[int] = ac.get(CONF_SYS_SCAN_INTERVAL, DEFAULT_SYS_SCAN_INTERVAL)
        self._command_throttle_interval: Final[float] = ac.get(
            CONF_COMMAND_THROTTLE_INTERVAL, DEFAULT_COMMAND_THROTTLE_INTERVAL
        )
        self._sysvar_markers: Final[tuple[DescriptionMarker | str, ...]] = (
            sysvar_markers if (sysvar_markers := ac.get(CONF_SYSVAR_MARKERS)) else DEFAULT_SYSVAR_MARKERS
        )
        self._un_ignore: Final[frozenset[str]] = frozenset(ac.get(CONF_UN_IGNORES, DEFAULT_UN_IGNORES))
        self._use_group_channel_for_cover_state: Final[bool] = ac.get(
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE, DEFAULT_USE_GROUP_CHANNEL_FOR_COVER_STATE
        )
        self._backup_path: Final[str] = ac.get(CONF_BACKUP_PATH, DEFAULT_BACKUP_PATH)

    @property
    def _temporary_config(self) -> ControlConfig:
        """Return a config for validation."""
        temporary_data: dict[str, Any] = deepcopy(dict(self._data))
        temporary_data[CONF_INSTANCE_NAME] = "temporary_instance"
        return ControlConfig(
            hass=self.hass,
            entry_id="hmip_local_temporary",
            data=temporary_data,
            start_direct=True,
        )

    @property
    def backup_directory(self) -> str:
        """Return the full path to the backup directory."""
        return f"{get_storage_directory(hass=self.hass)}/{self._backup_path}"

    @property
    def interface_config(self) -> Mapping[str, Any]:
        """Return the interface configuration."""
        return self._interface_config

    async def check_config(self) -> None:
        """Check config. Throws BaseHomematicException on failure."""
        if not self._check_instance_name_is_unique():
            raise InvalidConfig("Instance name must be unique.")
        if config_failures := await check_config(
            central_name=self.instance_name,
            host=self._host,
            username=self._username,
            password=self._password,
            callback_host=self._callback_host,
            callback_port_xml_rpc=self._callback_port_xml_rpc,
            json_port=self._json_port,
            storage_directory=get_storage_directory(hass=self.hass),
        ):
            failures = ", ".join(config_failures)
            raise InvalidConfig(failures)

    async def create_central(self) -> CentralUnit:
        """Create the central unit for ccu callbacks."""
        interface_configs: set[InterfaceConfig] = set()
        for interface_name in self._interface_config:
            interface = self._interface_config[interface_name]
            interface_type = Interface(interface_name)
            # Use configured port, fall back to default port
            # JSON-RPC-only interfaces (CUxD, CCU-Jack) don't have an XML-RPC port
            if (configured_port := interface.get(CONF_PORT)) is not None:
                port: int | None = configured_port
            else:
                port = get_interface_default_port(interface=interface_type, tls=self._tls)
            interface_configs.add(
                InterfaceConfig(
                    central_name=self.instance_name,
                    interface=interface_type,
                    port=port,
                    remote_path=interface.get(CONF_PATH),
                )
            )
        # use last 10 chars of entry_id for central_id uniqueness
        central_id = self.entry_id[-10:]
        return await CentralConfig(
            callback_host=self._callback_host if self._callback_host != IP_ANY_V4 else None,
            callback_port_xml_rpc=self._callback_port_xml_rpc if self._callback_port_xml_rpc != PORT_ANY else None,
            central_id=central_id,
            client_session=aiohttp_client.async_get_clientsession(self.hass),
            delay_new_device_creation=True,
            enable_device_firmware_check=DEFAULT_ENABLE_DEVICE_FIRMWARE_CHECK,
            enable_program_scan=self._enable_program_scan,
            enable_sysvar_scan=self._enable_sysvar_scan,
            listen_ip_addr=IP_ANY_V4 if self._listen_on_all_ip else None,
            default_callback_port_xml_rpc=self._default_callback_port_xml_rpc,
            host=self._host,
            interface_configs=frozenset(interface_configs),
            interfaces_requiring_periodic_refresh=frozenset(
                () if self.enable_mqtt else DEFAULT_INTERFACES_REQUIRING_PERIODIC_REFRESH
            ),
            json_port=self._json_port,
            locale=self.hass.config.language,
            max_read_workers=1,
            name=self.instance_name,
            optional_settings=frozenset(self._optional_settings),
            password=self._password,
            program_markers=self._program_markers,
            schedule_timer_config=ScheduleTimerConfig(sys_scan_interval=self._sys_scan_interval),
            timeout_config=TimeoutConfig(command_throttle_interval=self._command_throttle_interval),
            start_direct=self._start_direct,
            storage_directory=get_storage_directory(hass=self.hass),
            sysvar_markers=self._sysvar_markers,
            tls=self._tls,
            un_ignore_list=self._un_ignore,
            use_group_channel_for_cover_state=self._use_group_channel_for_cover_state,
            username=self._username,
            verify_tls=self._verify_tls,
        ).create_central()

    async def create_control_unit(self) -> ControlUnit:
        """Create the control unit asynchronously."""
        return await ControlUnit.async_create(control_config=self)

    async def create_control_unit_temp(self) -> ControlUnitTemp:
        """Create a temporary control unit asynchronously."""
        return await ControlUnitTemp.async_create(control_config=self._temporary_config)

    def _check_instance_name_is_unique(self) -> bool:
        """Check if instance_name is unique in HA."""
        for entry in self.hass.config_entries.async_entries(domain=DOMAIN):
            if entry.entry_id == self.entry_id or len(entry.data) == 0:
                continue
            if hasattr(entry.data, CONF_INSTANCE_NAME) and entry.data[CONF_INSTANCE_NAME] == self.instance_name:
                return False
        return True


def signal_new_data_point(*, entry_id: str, platform: DataPointCategory | str) -> str:
    """Gateway specific event to signal new device."""
    platform_value = platform.value if isinstance(platform, DataPointCategory) else platform
    return f"{DOMAIN}-new-data-point-{entry_id}-{platform_value}"


async def validate_config_and_get_system_information(
    *,
    control_config: ControlConfig,
) -> SystemInformation | None:
    """Validate the control configuration."""
    if control_unit := await control_config.create_control_unit_temp():
        return await control_unit.central.validate_config_and_get_system_information()
    return None


def get_storage_directory(*, hass: HomeAssistant) -> str:
    """Return the base path where to store files for this integration."""
    return f"{hass.config.config_dir}/{DOMAIN}"


def _cleanup_instance_name(*, instance_name: str) -> str:
    """Clean up instance name problematic characters for directories."""
    for char in ("/", "\\"):
        instance_name = instance_name.replace(char, "")
    return instance_name
