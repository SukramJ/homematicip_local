"""Tests for entity_id changes, which HA applies to the integration's entities in place."""

from __future__ import annotations

import asyncio
import importlib
import inspect
import pkgutil
from unittest.mock import patch

import pytest

import custom_components.homematicip_local as integration
from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import Entity, _entity_class_requires_readd

from tests import const, helper
from tests.helper import Factory

TEST_DEVICES: dict[str, str] = {
    "VCU2128127": "HmIP-BSM.json",
}

# pylint: disable=protected-access


def _integration_entity_classes() -> list[type[Entity]]:
    """Return every entity class the integration defines."""
    classes: set[type[Entity]] = set()
    for module_info in pkgutil.iter_modules(integration.__path__):
        module = importlib.import_module(f"{integration.__name__}.{module_info.name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Entity) and obj.__module__.startswith(integration.__name__):
                classes.add(obj)
    return sorted(classes, key=lambda cls: f"{cls.__module__}.{cls.__qualname__}")


def test_every_entity_class_changes_its_entity_id_in_place() -> None:
    """
    No entity class falls back to remove and re-add on an entity_id change.

    HA keeps the old remove/re-add path for a custom class which defines an add
    or remove method without an ``async_entity_id_changed`` on that class or a
    subclass of it — a hook on a base class does not cover a subclass that
    overrides ``async_added_to_hass``. The rule is HA's own, so a new entity
    class without the hook fails here by name.
    """
    classes = _integration_entity_classes()
    assert len(classes) > 20, classes
    assert [cls.__qualname__ for cls in classes if _entity_class_requires_readd(cls)] == []


class TestEntityIdChange:
    """An entity_id change keeps the entity and its subscriptions."""

    @pytest.mark.asyncio
    async def test_renamed_entity_is_neither_removed_nor_readded(self, factory_homegear: Factory) -> None:
        """The entity stays registered with aiohomematic and keeps receiving events under its new id."""
        entity_id = "switch.hmip_bsm_vcu2128127"
        new_entity_id = "switch.renamed_switch"
        hass, control = await factory_homegear.setup_environment(TEST_DEVICES)
        helper.get_and_check_state(hass=hass, control=control, entity_id=entity_id, entity_name="HmIP-BSM_VCU2128127")

        with patch.object(
            AioHomematicGenericEntity,
            "async_will_remove_from_hass",
            autospec=True,
            side_effect=AioHomematicGenericEntity.async_will_remove_from_hass,
        ) as will_remove:
            er.async_get(hass).async_update_entity(entity_id, new_entity_id=new_entity_id)
            await hass.async_block_till_done()

        will_remove.assert_not_called()
        assert hass.states.get(entity_id) is None
        assert hass.states.get(new_entity_id).state == STATE_OFF

        await control.central.event_coordinator.data_point_event(
            interface_id=const.INTERFACE_ID, channel_address="VCU2128127:4", parameter="STATE", value=1
        )
        await hass.async_block_till_done()
        await asyncio.sleep(0.1)
        await hass.async_block_till_done()
        assert hass.states.get(new_entity_id).state == STATE_ON
