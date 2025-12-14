"""Homematic(IP) Local for OpenCCU is a Python 3 module for Home Assistant and Homematic(IP) devices."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
import logging
from types import UnionType
from typing import Any, Final, TypeVar, cast

from aiohomematic import __version__ as AIOHM_VERSION
from aiohomematic.central import CentralConfig, CentralUnit, check_config
from aiohomematic.central.integration_events import (
    DataPointsCreatedEvent,
    DeviceLifecycleEvent,
    DeviceLifecycleEventType,
    DeviceTriggerEvent,
    SystemStatusEvent,
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
    DEFAULT_SYS_SCAN_INTERVAL,
    DEFAULT_SYSVAR_MARKERS,
    DEFAULT_UN_IGNORES,
    DEFAULT_USE_GROUP_CHANNEL_FOR_COVER_STATE,
    IP_ANY_V4,
    PORT_ANY,
    CentralState,
    ClientState,
    DataPointCategory,
    DescriptionMarker,
    Interface,
    Manufacturer,
    OptionalSettings,
    SystemInformation,
)
from aiohomematic.exceptions import BaseHomematicException
from aiohomematic.model.data_point import CallbackDataPoint
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
    DEFAULT_ENABLE_DEVICE_FIRMWARE_CHECK,
    DEFAULT_ENABLE_MQTT,
    DEFAULT_ENABLE_SUB_DEVICES,
    DEFAULT_ENABLE_SYSTEM_NOTIFICATIONS,
    DEFAULT_LISTEN_ON_ALL_IP,
    DEFAULT_MQTT_PREFIX,
    DOMAIN,
)
from .mqtt import MQTTConsumer
from .support import InvalidConfig

_LOGGER = logging.getLogger(__name__)

_DATA_POINT_T = TypeVar("_DATA_POINT_T", bound=CallbackDataPoint)


class BaseControlUnit:
    """Base central point to control a central unit."""

    def __init__(self, *, control_config: ControlConfig) -> None:
        """Init the control unit."""
        self._config: Final = control_config
        self._hass: Final = control_config.hass
        self._entry_id: Final = control_config.entry_id
        self._instance_name: Final = control_config.instance_name
        self._backup_directory: Final = control_config.backup_directory
        self._enable_mqtt: Final = control_config.enable_mqtt
        self._enable_sub_devices: Final = control_config.enable_sub_devices
        self._mqtt_prefix: Final = control_config.mqtt_prefix
        self._enable_system_notifications: Final = control_config.enable_system_notifications
        self._central: Final = control_config.create_central()
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
    def enable_sub_devices(self) -> bool:
        """Return if sub devices are enabled."""
        return self._enable_sub_devices

    async def start_central(self) -> None:
        """Start the central unit."""
        _LOGGER.debug(
            "Starting central unit %s",
            self._instance_name,
        )
        try:
            await self._central.start()
            _LOGGER.info("Started central unit for %s (%s)", self._instance_name, AIOHM_VERSION)
        except BaseHomematicException:
            _LOGGER.warning("START_CENTRAL: Failed to start central unit for %s", self._instance_name)

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

    def __init__(self, *, control_config: ControlConfig) -> None:
        """Init the control unit."""
        super().__init__(control_config=control_config)
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
            self.central.get_data_points(
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
        # Subscribe to integration events (4 focused subscriptions)
        _LOGGER.debug("Subscribing to integration events")
        self._unsubscribe_callbacks.append(
            self._central.event_bus.subscribe(
                event_type=SystemStatusEvent,
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

    async def _on_data_points_created(self, event: DataPointsCreatedEvent) -> None:
        """Handle data points created event from aiohomematic (Entity discovery)."""
        for category, data_points in event.new_data_points:
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

        elif event.event_type == DeviceLifecycleEventType.AVAILABILITY_CHANGED:
            for device_address, available in event.availability_changes:
                _LOGGER.debug("Device %s availability: %s", device_address, available)
                # Update device registry
                device_registry = dr.async_get(self._hass)
                if ha_device := device_registry.async_get_device(
                    identifiers={(DOMAIN, f"{device_address}{self._central.config.central_id}")}
                ):
                    device_registry.async_update_device(
                        device_id=ha_device.id,
                        disabled_by=None if available else dr.DeviceEntryDisabler.INTEGRATION,
                    )

    async def _on_device_trigger(self, event: DeviceTriggerEvent) -> None:
        """Handle device trigger event from aiohomematic (Device triggers for HA event bus)."""
        self._hass.bus.async_fire(
            event_type=f"{DOMAIN}.event",
            event_data={
                "entry_id": self._entry_id,
                "interface_id": event.interface_id,
                "channel_address": event.channel_address,
                "parameter": event.parameter,
                "value": event.value,
            },
        )

    async def _on_system_status(self, event: SystemStatusEvent) -> None:
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
                    # Some interfaces disconnected - create warning issue
                    if self._enable_system_notifications:
                        async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id_failed)
                        ir.async_create_issue(
                            hass=self._hass,
                            domain=DOMAIN,
                            issue_id=issue_id_degraded,
                            is_fixable=False,
                            severity=ir.IssueSeverity.WARNING,
                            translation_key="central_degraded",
                            translation_placeholders={"name": self._instance_name},
                        )
                        _LOGGER.warning("Central %s is DEGRADED - some interfaces disconnected", self._instance_name)
                    else:
                        _LOGGER.debug("SYSTEM NOTIFICATION disabled for DEGRADED state")

                case CentralState.RECOVERING:
                    # Active recovery in progress
                    _LOGGER.info("Central %s is RECOVERING - attempting reconnection", self._instance_name)

                case CentralState.FAILED:
                    # Critical error - all recovery attempts failed
                    if self._enable_system_notifications:
                        async_delete_issue(hass=self._hass, domain=DOMAIN, issue_id=issue_id_degraded)
                        ir.async_create_issue(
                            hass=self._hass,
                            domain=DOMAIN,
                            issue_id=issue_id_failed,
                            is_fixable=False,
                            severity=ir.IssueSeverity.ERROR,
                            translation_key="central_failed",
                            translation_placeholders={"name": self._instance_name},
                        )
                        _LOGGER.error("Central %s FAILED - recovery unsuccessful", self._instance_name)
                    else:
                        _LOGGER.debug("SYSTEM NOTIFICATION disabled for FAILED state")

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
            ir.async_create_issue(
                hass=self._hass,
                domain=DOMAIN,
                issue_id=f"{self._entry_id}_{issue.issue_id}",
                is_fixable=False,
                severity=ir.IssueSeverity.ERROR if issue.severity == "error" else ir.IssueSeverity.WARNING,
                translation_key=issue.translation_key,
                translation_placeholders=dict(issue.translation_placeholders),
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
        self._interface_config = self._data.get(CONF_INTERFACE, {})
        # advanced_config
        ac = self._data.get(CONF_ADVANCED_CONFIG, {})
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

    def check_config(self) -> None:
        """Check config. Throws BaseHomematicException on failure."""
        if not self._check_instance_name_is_unique():
            raise InvalidConfig("Instance name must be unique.")
        if config_failures := check_config(
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

    def create_central(self) -> CentralUnit:
        """Create the central unit for ccu callbacks."""
        interface_configs: set[InterfaceConfig] = set()
        for interface_name in self._interface_config:
            interface = self._interface_config[interface_name]
            interface_configs.add(
                InterfaceConfig(
                    central_name=self.instance_name,
                    interface=Interface(interface_name),
                    port=interface.get(CONF_PORT),
                    remote_path=interface.get(CONF_PATH),
                )
            )
        # use last 10 chars of entry_id for central_id uniqueness
        central_id = self.entry_id[-10:]
        return CentralConfig(
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
            interface_configs=interface_configs,
            interfaces_requiring_periodic_refresh=frozenset(
                () if self.enable_mqtt else DEFAULT_INTERFACES_REQUIRING_PERIODIC_REFRESH
            ),
            json_port=self._json_port,
            locale=self.hass.config.language,
            max_read_workers=1,
            name=self.instance_name,
            optional_settings=self._optional_settings,
            password=self._password,
            program_markers=self._program_markers,
            start_direct=self._start_direct,
            storage_directory=get_storage_directory(hass=self.hass),
            sys_scan_interval=self._sys_scan_interval,
            sysvar_markers=self._sysvar_markers,
            tls=self._tls,
            un_ignore_list=self._un_ignore,
            use_group_channel_for_cover_state=self._use_group_channel_for_cover_state,
            username=self._username,
            verify_tls=self._verify_tls,
        ).create_central()

    def create_control_unit(self) -> ControlUnit:
        """Identify the used client."""
        return ControlUnit(control_config=self)

    def create_control_unit_temp(self) -> ControlUnitTemp:
        """Identify the used client."""
        return ControlUnitTemp(control_config=self._temporary_config)

    def _check_instance_name_is_unique(self) -> bool:
        """Check if instance_name is unique in HA."""
        for entry in self.hass.config_entries.async_entries(domain=DOMAIN):
            if entry.entry_id == self.entry_id or len(entry.data) == 0:
                continue
            if hasattr(entry.data, CONF_INSTANCE_NAME) and entry.data[CONF_INSTANCE_NAME] == self.instance_name:
                return False
        return True


def signal_new_data_point(*, entry_id: str, platform: DataPointCategory) -> str:
    """Gateway specific event to signal new device."""
    return f"{DOMAIN}-new-data-point-{entry_id}-{platform.value}"


async def validate_config_and_get_system_information(
    *,
    control_config: ControlConfig,
) -> SystemInformation | None:
    """Validate the control configuration."""
    if control_unit := control_config.create_control_unit_temp():
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
