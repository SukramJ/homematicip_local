"""Helpers for tests."""

from __future__ import annotations

import contextlib
from datetime import datetime
import inspect
import logging
from types import FunctionType, MethodType
from typing import Any, Final, TypeVar
from unittest.mock import MagicMock, Mock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from aiohomematic.central.event_bus import BackendParameterEvent, BackendSystemEventData, HomematicEvent
from aiohomematic.interfaces import BaseParameterDataPointProtocol, CustomDataPointProtocol
from aiohomematic_test_support.factory import FactoryWithClient
from aiohomematic_test_support.mock import SessionPlayer
from custom_components.homematicip_local import HAHM_VERSION as _HAHM_VERSION
from custom_components.homematicip_local.control_unit import ControlUnit
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

EXCLUDE_METHODS_FROM_MOCKS: Final = [
    "default_category",
    "event",
    "get_event_data",
    "load_data_point_value",
    "publish_data_point_updated_event",
    "publish_device_removed_event",
    "subscribe_to_data_point_updated",
    "subscribe_to_device_removed",
    "subscribe_to_internal_data_point_updated",
    "write_value",
    "write_temporary_value",
]
T = TypeVar("T")

# pylint: disable=protected-access


class Factory:
    """Factory for a central with one local client."""

    def __init__(self, hass: HomeAssistant, mock_config_entry: MockConfigEntry, player: SessionPlayer):
        """Init the central factory."""
        self._hass = hass
        self._player = player
        self._backend_factory = FactoryWithClient(player=self._player)
        self.mock_config_entry = mock_config_entry
        self.system_event_mock = MagicMock()
        self.entity_event_mock = MagicMock()
        self.ha_event_mock = MagicMock()

    async def setup_environment(
        self,
        address_device_translation: dict[str, str],
        ignore_devices_on_create: list[str] | None = None,
        un_ignore_list: list[str] | None = None,
    ) -> tuple[HomeAssistant, ControlUnit]:
        """Return a central based on give address_device_translation."""
        central = await self._backend_factory.init(
            address_device_translation=address_device_translation,
            ignore_devices_on_create=ignore_devices_on_create,
            un_ignore_list=un_ignore_list,
        ).get_default_central(start=False)

        central.event_bus.subscribe(event_type=BackendSystemEventData, event_key=None, handler=self.system_event_mock)
        central.event_bus.subscribe(event_type=BackendParameterEvent, event_key=None, handler=self.entity_event_mock)
        central.event_bus.subscribe(event_type=HomematicEvent, event_key=None, handler=self.ha_event_mock)
        await central.start()
        await central.hub_coordinator.init_hub()

        patch("custom_components.homematicip_local.find_free_port", return_value=8765).start()
        patch(
            "custom_components.homematicip_local.control_unit.ControlConfig.create_central",
            return_value=central,
        ).start()
        patch(
            "custom_components.homematicip_local.generic_entity.get_data_point",
            side_effect=get_data_point_mock,
        ).start()
        patch(
            "homeassistant.helpers.entity.Entity.entity_registry_enabled_default",
            return_value=True,
        ).start()
        # Ensure version check in async_setup_entry passes by returning current package version
        patch(
            "custom_components.homematicip_local.get_aiohomematic_version",
            return_value=_HAHM_VERSION,
        ).start()

        # Start integration in hass
        self.mock_config_entry.add_to_hass(self._hass)
        await self._hass.config_entries.async_setup(self.mock_config_entry.entry_id)
        await self._hass.async_block_till_done()
        assert self.mock_config_entry.state == ConfigEntryState.LOADED

        control: ControlUnit = self.mock_config_entry.runtime_data
        await self._hass.async_block_till_done()
        await self._hass.async_block_till_done()
        return self._hass, control


def get_and_check_state(hass: HomeAssistant, control: ControlUnit, entity_id: str, entity_name: str):
    """Get and test basic device."""
    ha_state = hass.states.get(entity_id)
    assert ha_state is not None
    # assert ha_state.name == entity_name
    data_point = get_data_point(control=control, entity_id=entity_id)

    return ha_state, data_point


def get_data_point(control: ControlUnit, entity_id: str):
    """Get the data point by entity id."""
    for dp in control.central.get_data_points():
        if dp.custom_id == entity_id:
            return dp
    for dp in control.central.hub_coordinator.get_hub_data_points():
        if dp.custom_id == entity_id:
            return dp


def get_mock(instance, **kwargs):
    """Create a mock and copy instance attributes over mock."""
    if isinstance(instance, Mock):
        instance.__dict__.update(instance._mock_wraps.__dict__)
        return instance

    mock = MagicMock(spec=instance, wraps=instance, **kwargs)
    mock.__dict__.update(instance.__dict__)
    return mock


def get_data_point_mock[DP](data_point: DP) -> DP:
    """Return the mocked Homematic entity."""
    try:
        for method_name in _get_mockable_method_names(data_point):
            with contextlib.suppress(AttributeError):
                fn = _get_full_qualname(obj=data_point, method_name=method_name)
                if not fn.startswith("unitest.mock"):
                    patch(fn).start()

        if isinstance(data_point, CustomDataPointProtocol):
            for g_entity in data_point._data_points.values():
                g_entity._set_modified_at(modified_at=datetime.now())
        elif isinstance(data_point, BaseParameterDataPointProtocol):
            data_point._set_modified_at(modified_at=datetime.now())
        if hasattr(data_point, "is_valid"):
            assert data_point.is_valid is True
        # patch.object(data_point, "is_valid", return_value=True).start()
    except Exception:
        pass
    finally:
        return data_point


def _get_full_qualname(obj: Any, method_name: str) -> str:
    """Return the fully qualified name of a method."""
    try:
        attr = getattr(obj, method_name)
    except AttributeError as e:
        raise ValueError(f"Object of type {type(obj)} has no attribute '{method_name}'") from e

    # Attempt to resolve the module name
    module = inspect.getmodule(attr)
    module_name = module.__name__ if module else obj.__class__.__module__

    # Resolve the qualified name
    if isinstance(attr, (FunctionType, MethodType)):
        # For functions or methods
        qualname = attr.__qualname__
    else:
        # For properties or other descriptors, fallback to class-based qualname
        qualname = f"{obj.__class__.__qualname__}.{method_name}"

    return f"{module_name}.{qualname}"


def _get_mockable_method_names(data_point: Any) -> list[str]:
    """Return all relevant method names for mocking."""
    method_list: list[str] = []
    for attribute in dir(data_point):
        # Get the attribute value
        attribute_value = getattr(data_point, attribute, None)
        # Check that it is callable
        if (
            callable(attribute_value)
            and attribute.startswith("_") is False
            and attribute not in EXCLUDE_METHODS_FROM_MOCKS
        ):
            method_list.append(attribute)
    return method_list
