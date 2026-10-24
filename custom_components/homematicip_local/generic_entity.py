"""Generic entity for the Homematic(IP) Local for OpenCCU component."""

from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any, Final, Generic, override

from aiohomematic import ccu_translations
from aiohomematic.central.events import DataPointStateChangedEvent, DeviceRemovedEvent, SubscriptionGroup
from aiohomematic.const import CallSource, DataPointCategory, DataPointUsage
from aiohomematic.interfaces import (
    CalculatedDataPointProtocol,
    CallbackDataPointProtocol,
    ChannelProtocol,
    CombinedDataPointProtocol,
    CustomDataPointProtocol,
    GenericDataPointProtocol,
    GenericHubDataPointProtocol,
    GenericProgramDataPointProtocol,
    GenericSysvarDataPointProtocol,
)
from homeassistant.const import ATTR_CONFIG_ENTRY_ID
from homeassistant.core import State, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.device_registry import ChildDeviceInfo, DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import UndefinedType

from .const import (
    ALARM_DEVICE_IDENTIFIER,
    ALARM_DEVICE_MANUFACTURER,
    ALARM_DEVICE_NAME,
    DOMAIN,
    ENTITY_TRANSLATION_KEYS,
    HmEntityState,
)
from .control_unit import ControlUnit
from .entity_helpers import get_entity_description
from .support import (
    HmGenericDataPointProtocol,
    HmGenericProgramDataPointProtocol,
    HmGenericSysvarDataPointProtocol,
    get_data_point,
)

_LOGGER = logging.getLogger(__name__)

_SCHEDULE_CATEGORIES: Final[frozenset[DataPointCategory]] = frozenset(
    {DataPointCategory.WEEK_PROFILE, DataPointCategory.SCHEDULE_SWITCH}
)
_SCHEDULE_TRANSLATION_PARAMETER: Final = "SCHEDULE_CHANNEL_SWITCH"
# The CCU translations carry no word for a channel group, so the label of an
# unnamed group is kept here; English is the fallback for every other locale.
_CHANNEL_GROUP_LABELS: Final[Mapping[str, str]] = {"de": "Gruppe", "en": "Group"}
_CHILD_SCHEDULE_SUFFIX: Final = "schedule"


def get_schedule_name(*, locale: str) -> str:
    """Return the translated schedule name for the given locale."""
    return (
        ccu_translations.get_parameter_translation(
            parameter=_SCHEDULE_TRANSLATION_PARAMETER,
            locale=locale,
        )
        or "Schedule"
    )


def get_channel_group_name(*, locale: str, group_label: str) -> str:
    """Return the name of a channel group that carries no name of its own, e.g. ``Gruppe 2``."""
    return f"{_CHANNEL_GROUP_LABELS.get(locale[:2].lower(), _CHANNEL_GROUP_LABELS['en'])} {group_label}"


ATTR_ADDRESS: Final = "address"
ATTR_DESCRIPTION: Final = "description"
ATTR_FUNCTION: Final = "function"
ATTR_INTERFACE_ID: Final = "interface_id"
ATTR_DEVICES: Final = "devices"
ATTR_MODEL: Final = "model"
ATTR_NAME: Final = "name"
ATTR_PARAMETER: Final = "parameter"
ATTR_SCHEDULE_DATA: Final = "schedule_data"
ATTR_VALUE_STATE: Final = "value_state"


class AioHomematicGenericEntity(Entity, Generic[HmGenericDataPointProtocol]):
    """Representation of the HomematicIP generic entity."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    NO_RECORDED_ATTRIBUTES = {
        ATTR_ADDRESS,
        ATTR_CONFIG_ENTRY_ID,
        ATTR_FUNCTION,
        ATTR_INTERFACE_ID,
        ATTR_MODEL,
        ATTR_PARAMETER,
        ATTR_SCHEDULE_DATA,
        ATTR_VALUE_STATE,
    }

    _unrecorded_attributes = frozenset(NO_RECORDED_ATTRIBUTES)

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: HmGenericDataPointProtocol,
    ) -> None:
        """Initialize the generic entity."""
        self._cu: ControlUnit = control_unit
        self._data_point: HmGenericDataPointProtocol = get_data_point(data_point=data_point)
        self._attr_unique_id = f"{DOMAIN}_{data_point.unique_id}"

        if entity_description := get_entity_description(data_point=data_point):
            self.entity_description = entity_description
        else:
            self._attr_entity_registry_enabled_default = data_point.enabled_default
            if (
                isinstance(
                    data_point, CalculatedDataPointProtocol | CombinedDataPointProtocol | GenericDataPointProtocol
                )
                and data_point.translation_key in ENTITY_TRANSLATION_KEYS
            ):
                self._attr_translation_key = data_point.translation_key

        hm_device = data_point.device
        device_identifier = control_unit.device_identifier(device=hm_device)
        # The physical device hangs off the central, a genuine hub relation
        # that stays a via_device link.
        device_info = DeviceInfo(
            identifiers={(DOMAIN, device_identifier)},
            configuration_url=control_unit.device_configuration_url(
                address=hm_device.address,
                interface_id=hm_device.interface_id,
            ),
            manufacturer=hm_device.manufacturer,
            model=hm_device.model,
            model_id=hm_device.model_description,
            name=hm_device.name,
            serial_number=hm_device.address,
            sw_version=hm_device.firmware,
            suggested_area=hm_device.room,
            via_device_id=control_unit.ensure_central_device_exists(),
        )

        # A channel group or the schedule is a part of that one product, so it
        # becomes a child device of it: no hardware data of its own, its area
        # inherited from the parent unless the group carries its own room.
        child_identifier: str | None = None
        child_suggested_area: str | None = None
        if control_unit.enable_sub_devices and data_point.category in _SCHEDULE_CATEGORIES:
            child_identifier = f"{device_identifier}-{_CHILD_SCHEDULE_SUFFIX}"
        elif (channel_group_master := self._channel_group_master) is not None:
            child_identifier = f"{device_identifier}-{channel_group_master.group_no}"
            child_suggested_area = channel_group_master.room

        if child_identifier is None:
            self._attr_device_info = device_info
        else:
            # The child device itself is registered by the entity platform from
            # this device info; the parent it points at has to exist first.
            self._attr_device_info = ChildDeviceInfo(
                identifiers={(DOMAIN, child_identifier)},
                name=self._ha_device_name,
                parent_device_id=control_unit.ensure_parent_device_exists(device_info=device_info),
                suggested_area=child_suggested_area,
            )

        self._static_state_attributes = self._get_static_state_attributes()
        self._subscription_group: Final[SubscriptionGroup] = control_unit.central.event_bus.create_subscription_group(
            name=f"entity_{data_point.unique_id}"
        )

        _LOGGER.debug("init: Setting up %s", data_point.full_name)
        if (
            isinstance(data_point, CalculatedDataPointProtocol | CombinedDataPointProtocol | GenericDataPointProtocol)
            and hasattr(self, "entity_description")
            and hasattr(self.entity_description, "native_unit_of_measurement")
            and data_point.unit is not None
            and self.entity_description.native_unit_of_measurement != data_point.unit
        ):
            _LOGGER.debug(
                "Different unit for entity: %s: entity_description: %s vs device: %s",
                data_point.full_name,
                self.entity_description.native_unit_of_measurement,
                data_point.unit,
            )

    @property
    def _channel_group_master(self) -> ChannelProtocol | None:
        """
        Return the group master of the channel group this entity splits off into, else None.

        data_point.channel is None for some loom-backend data points (hub
        singletons ride a different base class, but week-profile DPs can
        resolve no channel before the store is fully hydrated), and a group
        without a master has no child device to split off; both stay on the
        device.
        """
        hm_device = self._data_point.device
        if (
            self._cu.enable_sub_devices
            and hm_device.has_sub_devices
            and (dp_channel := self._data_point.channel) is not None
            and dp_channel.is_in_multi_group
        ):
            return dp_channel.group_master
        return None

    @property
    def _ha_device_name(self) -> str:
        """
        Return the name of the HA device this entity lands on.

        A child device carries its own name only — the schedule label or the
        channel group's name — never the device name as a prefix: HA composes
        the full name from parent, child and entity itself.
        """
        hm_device = self._data_point.device
        if not self._cu.enable_sub_devices:
            return hm_device.name

        locale = hm_device.config_provider.config.locale
        if self._data_point.category in _SCHEDULE_CATEGORIES:
            return get_schedule_name(locale=locale)

        if (channel_group_master := self._channel_group_master) is not None:
            if (group_name := channel_group_master.name) and not group_name.isnumeric():
                return group_name
            return get_channel_group_name(locale=locale, group_label=group_name or str(channel_group_master.group_no))

        return hm_device.name

    @property
    @override
    def available(self) -> bool:
        """Return if data point is available."""
        return self._data_point.available

    @property
    def data_point(self) -> HmGenericDataPointProtocol:
        """Return the Homematic entity."""
        return self._data_point

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the generic entity."""
        attributes: dict[str, Any] = {}
        attributes.update(self._static_state_attributes)
        attributes.update(self._data_point.additional_information)

        if (
            isinstance(self._data_point, CalculatedDataPointProtocol | GenericDataPointProtocol)
            and self._data_point.is_readable
        ) or isinstance(self._data_point, CombinedDataPointProtocol | CustomDataPointProtocol):
            if self._data_point.is_valid:
                attributes[ATTR_VALUE_STATE] = (
                    HmEntityState.UNCERTAIN if self._data_point.state_uncertain else HmEntityState.VALID
                )
            else:
                attributes[ATTR_VALUE_STATE] = HmEntityState.NOT_VALID
        if (
            isinstance(self._data_point, CustomDataPointProtocol)
            and self._data_point.usage == DataPointUsage.CDP_PRIMARY
            and (wp_dp := self._data_point.device.week_profile_data_point) is not None
            and (schedule := wp_dp.schedule) is not None
        ):
            attributes[ATTR_SCHEDULE_DATA] = schedule
        return attributes

    @property
    @override
    def name(self) -> str | UndefinedType | None:
        """
        Return the name of the entity.

        Override by CC.
        A hm entity can consist of two parts. The first part is already defined by the user,
        and the second part is the english named parameter that must be translated.
        This translated parameter will be used in the combined name.
        """
        entity_name = self._data_point.translated_name
        device_name = self._ha_device_name

        if (
            isinstance(
                self._data_point, CalculatedDataPointProtocol | CombinedDataPointProtocol | GenericDataPointProtocol
            )
            and entity_name
        ):
            if entity_name.startswith(device_name):
                entity_name = entity_name.removeprefix(device_name).strip()
            translated_name = super().name
            if self._do_remove_name():
                translated_name = ""
            if isinstance(translated_name, str) and translated_name != entity_name:
                param = self._data_point.parameter.replace("_", " ").title()
                if param != translated_name:
                    entity_name = entity_name.replace(param, translated_name)

        if isinstance(self._data_point, CustomDataPointProtocol) and entity_name:
            if entity_name.startswith(device_name):
                entity_name = entity_name.removeprefix(device_name).strip()

            translated_name = super().name
            if self._do_remove_name():
                translated_name = ""
            if isinstance(translated_name, str) and self._data_point.name_data.parameter_name:
                entity_name = entity_name.replace(
                    self._data_point.name_data.parameter_name.replace("_", " ").title(),
                    translated_name,
                )

        # For data points not handled above, delegate to HA's translation mechanism.
        if not isinstance(
            self._data_point,
            CalculatedDataPointProtocol
            | CombinedDataPointProtocol
            | CustomDataPointProtocol
            | GenericDataPointProtocol,
        ):
            if not self.platform_data:
                return self._name_internal(None, {})
            return self._name_internal(
                self._device_class_name,
                self.platform_data.platform_translations,
            )

        if device_name == entity_name:
            entity_name = ""

        if entity_name == "":
            return None
        return entity_name

    @property
    def use_device_name(self) -> bool:
        """
        Return if this entity does not have its own name.

        Override by CC.
        """
        return not self.name

    @override
    async def async_added_to_hass(self) -> None:
        """Register callbacks and load initial data."""
        if isinstance(self._data_point, CallbackDataPointProtocol):
            self._data_point.register()
            self._subscription_group.subscribe(
                event_type=DataPointStateChangedEvent,
                event_key=self._data_point.unique_id,
                handler=self._async_data_point_updated,
            )
            self._subscription_group.subscribe(
                event_type=DeviceRemovedEvent,
                event_key=self._data_point.unique_id,
                handler=self._async_device_removed,
            )
        # Init value of entity.
        if isinstance(
            self._data_point,
            CalculatedDataPointProtocol
            | CombinedDataPointProtocol
            | CustomDataPointProtocol
            | GenericDataPointProtocol,
        ):
            await self._data_point.load_data_point_value(call_source=CallSource.HA_INIT)
        if (
            isinstance(self._data_point, CalculatedDataPointProtocol | GenericDataPointProtocol)
            and not self._data_point.is_valid
            and self._data_point.is_readable
        ) or (isinstance(self._data_point, CustomDataPointProtocol) and not self._data_point.is_valid):
            _LOGGER.debug(
                "CCU did not provide initial value for %s. See README for more information",
                self._data_point.full_name,
            )

    async def async_update(self) -> None:
        """Update entities."""
        if isinstance(
            self._data_point,
            CalculatedDataPointProtocol
            | CombinedDataPointProtocol
            | CustomDataPointProtocol
            | GenericDataPointProtocol,
        ):
            await self._data_point.load_data_point_value(call_source=CallSource.MANUAL_OR_SCHEDULED)

    @override
    async def async_will_remove_from_hass(self) -> None:
        """Run when hmip device will be removed from hass."""
        if isinstance(self._data_point, CallbackDataPointProtocol):
            self._data_point.unregister()
        self._subscription_group.unsubscribe_all()

    @callback
    def _async_data_point_updated(self, *, event: DataPointStateChangedEvent) -> None:
        """Handle device state changes."""
        # Don't update disabled entities
        update_type = "updated" if self._data_point.refreshed_at == self._data_point.modified_at else "refreshed"
        if self.enabled:
            _LOGGER.debug("Device %s event emitted for %s", update_type, self._data_point.full_name)
            self.async_schedule_update_ha_state()
        else:
            _LOGGER.debug(
                "Device %s event for %s not emitted. Entity is disabled",
                update_type,
                self._data_point.full_name,
            )

    @callback
    def _async_device_removed(self, *, event: DeviceRemovedEvent) -> None:
        """Handle hm device removal."""
        # Fire-and-forget: HA tracks the task internally
        _ = self.hass.async_create_task(self.async_remove(force_remove=True))

        if not self.registry_entry:
            return

        if device_id := self.registry_entry.device_id:
            # Remove from device registry.
            device_registry = dr.async_get(self.hass)
            if device_registry.async_get(device_id) is not None:
                # This will also remove associated entities from entity registry.
                device_registry.async_remove_device(device_id)

    def _do_remove_name(self) -> bool:
        """
        Check if entity name part should be removed.

        Here we use the HA translation support to identify if the translated name is ''
        This is guarded against failure due to future HA api changes.
        """
        try:
            if (
                self._name_translation_key
                and hasattr(self, "platform_data")
                and hasattr(self.platform_data, "platform_translations")
                and (name := self.platform_data.platform_translations.get(self._name_translation_key)) is not None
            ):
                return bool(name == "")
        except Exception:  # noqa: BLE001  # guard against future HA API changes
            return False
        return False

    def _get_static_state_attributes(self) -> Mapping[str, Any]:
        """Return the static attributes of the generic entity."""
        attributes: dict[str, Any] = {
            ATTR_INTERFACE_ID: self._data_point.device.interface_id,
            ATTR_ADDRESS: self._data_point.channel.address,
            ATTR_MODEL: self._data_point.device.model,
        }
        if isinstance(
            self._data_point, CalculatedDataPointProtocol | CombinedDataPointProtocol | GenericDataPointProtocol
        ):
            attributes[ATTR_PARAMETER] = self._data_point.parameter
            if isinstance(self._data_point, CalculatedDataPointProtocol | GenericDataPointProtocol):
                attributes[ATTR_FUNCTION] = self._data_point.function

        return attributes


class AioHomematicGenericRestoreEntity(AioHomematicGenericEntity[HmGenericDataPointProtocol], RestoreEntity):
    """Representation of the HomematicIP generic restore entity."""

    _restored_state: State | None = None

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the generic entity."""
        attributes = super().extra_state_attributes
        if self.is_restored:
            attributes[ATTR_VALUE_STATE] = HmEntityState.RESTORED
        return attributes

    @property
    def is_restored(self) -> bool:
        """Return if the state is restored."""
        return (
            not self._data_point.is_valid
            and self._restored_state is not None
            and self._restored_state.state is not None
        )

    @override
    async def async_added_to_hass(self) -> None:
        """Check, if state needs to be restored."""
        await super().async_added_to_hass()
        # if not self._data_point.is_valid:
        self._restored_state = await self.async_get_last_state()


class AioHomematicGenericHubEntity(Entity):
    """Representation of the HomematicIP generic hub entity."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    NO_RECORDED_ATTRIBUTES = {
        ATTR_DESCRIPTION,
        ATTR_DEVICES,
        ATTR_NAME,
        ATTR_VALUE_STATE,
    }

    _unrecorded_attributes = frozenset(NO_RECORDED_ATTRIBUTES)

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: GenericHubDataPointProtocol,
    ) -> None:
        """Initialize the generic entity."""
        self._cu: ControlUnit = control_unit
        self._data_point = get_data_point(data_point)
        self._attr_unique_id = f"{DOMAIN}_{data_point.unique_id}"

        if entity_description := get_entity_description(data_point=data_point):
            self.entity_description = entity_description
        else:
            self._attr_entity_registry_enabled_default = data_point.enabled_default
            if isinstance(data_point, GenericSysvarDataPointProtocol):
                self._attr_translation_key = data_point.name.lower()
            elif getattr(self, "_attr_translation_key", None) is None:
                # A subclass that declares its own translation key names itself
                # out of this integration's catalogue. Setting `_attr_name` here
                # would silently win over that: `Entity.name` hands the attribute
                # back before it ever looks a key up. Entities riding another
                # entity's data point — the alarm reset button and its counter
                # ride the panel — would end up named after that data point,
                # indistinguishable from the entity they accompany.
                self._attr_name = data_point.name

        self._attr_device_info = self._get_device_info()
        self._subscription_group: Final[SubscriptionGroup] = control_unit.central.event_bus.create_subscription_group(
            name=f"hub_entity_{data_point.unique_id}"
        )
        _LOGGER.debug("init sysvar: Setting up %s", self._data_point.name)

    @property
    @override
    def available(self) -> bool:
        """Return if entity is available."""
        return self._data_point.available

    @property
    @override
    def name(self) -> str | UndefinedType | None:
        """
        Return the name of the entity.

        Override by CC.
        A hm entity can consist of two parts. The first part is already defined by the user,
        and the second part is the english named parameter that must be translated.
        This translated parameter will be used in the combined name.
        """

        # A backend may have resolved the name itself. openccu-loom is the
        # naming authority for its own hub entities and hands the localized
        # name over the wire, in the language this integration asked for.
        # Rendering it verbatim is what keeps the same words from living
        # here and in the daemon's catalogue at once, drifting apart on the
        # first edit to either. The data point keeps its English token in
        # `name`, so the entity-description lookup in __init__ still matches
        # on it and the entity keeps its icon, device class and category.
        # aiohomematic data points carry no such attribute and fall through
        # to the behaviour below unchanged.
        #
        # The isinstance check is not belt-and-braces: `getattr` on a mock
        # answers with a truthy mock, and a bare truthiness test would make
        # every mocked data point in a test suite take this branch.
        if isinstance(resolved_name := getattr(self._data_point, "resolved_name", None), str) and resolved_name:
            return resolved_name

        entity_name = self._data_point.name

        if (translated_name := super().name) is not None and not isinstance(translated_name, UndefinedType):
            entity_name = translated_name

        if not self._data_point.channel and entity_name and isinstance(entity_name, str):
            if isinstance(self._data_point, GenericSysvarDataPointProtocol) and not entity_name.lower().startswith(
                tuple({"v_", "sv_", "sv"})
            ):
                entity_name = f"SV {entity_name}"
            elif isinstance(self._data_point, GenericProgramDataPointProtocol) and not entity_name.lower().startswith(
                tuple({"p_", "prg_"})
            ):
                entity_name = f"P {entity_name}"

        if entity_name == "":
            return None
        if isinstance(entity_name, UndefinedType):
            return None
        return entity_name.replace("_", " ")

    @override
    async def async_added_to_hass(self) -> None:
        """Register callbacks and load initial data."""
        if isinstance(self._data_point, CallbackDataPointProtocol):
            self._data_point.register()
            self._subscription_group.subscribe(
                event_type=DataPointStateChangedEvent,
                event_key=self._data_point.unique_id,
                handler=self._async_hub_entity_updated,
            )
            self._subscription_group.subscribe(
                event_type=DeviceRemovedEvent,
                event_key=self._data_point.unique_id,
                handler=self._async_hub_device_removed,
            )

    @override
    async def async_will_remove_from_hass(self) -> None:
        """Run when hmip sysvar entity will be removed from hass."""
        if isinstance(self._data_point, CallbackDataPointProtocol):
            self._data_point.unregister()
        self._subscription_group.unsubscribe_all()

    @callback
    def _async_hub_device_removed(self, *, event: DeviceRemovedEvent) -> None:
        """Handle hm sysvar entity removal."""
        # Fire-and-forget: HA tracks the task internally
        _ = self.hass.async_create_task(self.async_remove(force_remove=True))

        if not self.registry_entry:
            return

        if entity_id := self.registry_entry.entity_id:
            entity_registry = er.async_get(self.hass)
            if entity_id in entity_registry.entities:
                entity_registry.async_remove(entity_id)

    @callback
    def _async_hub_entity_updated(self, *, event: DataPointStateChangedEvent) -> None:
        """Handle sysvar entity state changes."""
        # Don't update disabled entities
        if self.enabled:
            _LOGGER.debug("Sysvar changed event emitted for %s", self.name)
            self.async_schedule_update_ha_state()
        else:
            _LOGGER.debug(
                "Sysvar changed event for %s not emitted. Sysvar entity is disabled",
                self.name,
            )

    def _get_device_info(self) -> DeviceInfo | None:
        """Return device specific attributes."""
        if self._data_point.channel is None:
            return self._cu.device_info

        # suggested_area only applies at device creation — see event.py.
        return DeviceInfo(
            identifiers={(DOMAIN, self._cu.device_identifier(device=self._data_point.channel.device))},
            suggested_area=self._data_point.channel.device.room,
        )


class AioHomematicAlarmEntity(AioHomematicGenericHubEntity):
    """
    Base for every openccu-loom alarm surface (panel, reset button, counter).

    Exists for one reason: the alarm system is not part of any CCU. Its
    zones live in the daemon and may hold sensors of several centrals, so
    the hub default of attaching to the central's device states a
    belonging that does not exist — and buries the panels among dozens of
    sysvars and diagnostics while it is at it. Everything alarm-related
    goes on one device of its own instead, matching the block the daemon
    publishes over MQTT.
    """

    def _get_device_info(self) -> DeviceInfo | None:
        """Return the shared alarm device instead of the central's."""
        return DeviceInfo(
            identifiers={(DOMAIN, ALARM_DEVICE_IDENTIFIER)},
            manufacturer=ALARM_DEVICE_MANUFACTURER,
            name=ALARM_DEVICE_NAME,
        )


class AioHomematicGenericProgramEntity(AioHomematicGenericHubEntity, Generic[HmGenericProgramDataPointProtocol]):
    """Representation of the HomematicIP generic sysvar entity."""

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: GenericProgramDataPointProtocol,
    ) -> None:
        """Initialize the generic entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        self._data_point: GenericProgramDataPointProtocol = data_point
        self._static_state_attributes = {
            ATTR_NAME: self._data_point.name,
            ATTR_DESCRIPTION: self._data_point.description,
        }

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the generic entity."""
        attributes: dict[str, Any] = {}
        attributes.update(self._static_state_attributes)
        if self._data_point.is_valid:
            attributes[ATTR_VALUE_STATE] = (
                HmEntityState.UNCERTAIN if self._data_point.state_uncertain else HmEntityState.VALID
            )
        else:
            attributes[ATTR_VALUE_STATE] = HmEntityState.NOT_VALID
        return attributes


class AioHomematicGenericSysvarEntity(AioHomematicGenericHubEntity, Generic[HmGenericSysvarDataPointProtocol]):
    """Representation of the HomematicIP generic sysvar entity."""

    def __init__(
        self,
        control_unit: ControlUnit,
        data_point: GenericSysvarDataPointProtocol,
    ) -> None:
        """Initialize the generic entity."""
        super().__init__(
            control_unit=control_unit,
            data_point=data_point,
        )
        self._data_point: GenericSysvarDataPointProtocol = data_point
        self._static_state_attributes = {
            ATTR_NAME: self._data_point.name,
            ATTR_DESCRIPTION: self._data_point.description,
        }

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the generic entity."""
        attributes: dict[str, Any] = {}
        attributes.update(self._static_state_attributes)
        attributes.update(self._data_point.additional_information)
        if self._data_point.is_valid:
            attributes[ATTR_VALUE_STATE] = (
                HmEntityState.UNCERTAIN if self._data_point.state_uncertain else HmEntityState.VALID
            )
        else:
            attributes[ATTR_VALUE_STATE] = HmEntityState.NOT_VALID

        if hasattr(self._data_point, "devices"):
            attributes[ATTR_DEVICES] = [m.name for m in self._data_point.devices]
        return attributes
