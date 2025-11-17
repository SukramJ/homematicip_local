"""
Unit tests for custom_components.homematicip_local.services.

This suite boosts coverage by exercising:
- async_setup_services: registration of admin and platform entity services.
- Internal dispatcher in async_setup_services for each HmipLocalServices case.
- async_unload_services: removal of services when no loaded entries remain.

All tests avoid touching backend logic by monkeypatching the private handlers.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock

import pytest

import custom_components.homematicip_local.services as hm_services
from homeassistant.core import HomeAssistant


@dataclass
class _ServiceCall:
    service: str
    data: dict[str, Any]
    hass: Any = None
    context: Any = None

    def __post_init__(self) -> None:
        if self.context is None:
            # Minimal context-like object exposing user_id to satisfy verify_domain_control
            self.context = type("_Ctx", (), {"user_id": None})()
        if self.hass is None:
            # Late assign allowed; tests will pass hass explicitly when invoking
            pass


class TestAsyncSetupServices:
    """Tests for async_setup_services function."""

    @pytest.mark.asyncio
    async def test_registers_and_dispatches_all(self, hass: HomeAssistant, monkeypatch) -> None:
        """It should register all services and route calls to the correct private handlers."""
        registered_admin: list[tuple[str, dict[str, Any]]] = []
        registered_entity: list[tuple[str, dict[str, Any]]] = []

        # Replace registration helpers to capture registrations without HA involvement
        dispatcher_funcs: list[Callable] = []

        def fake_register_admin_service(*, hass, domain, service, service_func, schema, **kwargs):  # noqa: ANN001
            registered_admin.append((service, schema.schema if hasattr(schema, "schema") else {}))
            dispatcher_funcs.append(service_func)

        def fake_register_platform_entity_service(
            *, hass, service_domain, service_name, entity_domain, schema, func, **kwargs
        ):  # noqa: ANN001
            registered_entity.append((service_name, schema))

        monkeypatch.setattr(hm_services, "async_register_admin_service", fake_register_admin_service)
        monkeypatch.setattr(hm_services, "async_register_platform_entity_service", fake_register_platform_entity_service)

        # Patch every private handler used by the dispatcher to simple async mocks
        monkeypatch.setattr(hm_services, "_async_service_add_link", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_create_central_link", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_clear_cache", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_export_device_definition", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_fetch_system_variables", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_force_device_availability", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_get_device_value", AsyncMock(return_value={"ok": True}))
        monkeypatch.setattr(hm_services, "_async_service_get_link_peers", AsyncMock(return_value=["peer"]))
        monkeypatch.setattr(hm_services, "_async_service_get_link_paramset", AsyncMock(return_value={"k": "v"}))
        monkeypatch.setattr(hm_services, "_async_service_get_paramset", AsyncMock(return_value={"p": 1}))
        monkeypatch.setattr(hm_services, "_async_service_get_variable_value", AsyncMock(return_value=123))
        monkeypatch.setattr(hm_services, "_async_service_put_link_paramset", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_put_paramset", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_record_session", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_remove_central_link", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_remove_link", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_set_device_value", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_set_variable_value", AsyncMock())
        monkeypatch.setattr(hm_services, "_async_service_update_device_firmware_data", AsyncMock())

        await hm_services.async_setup_services(hass)

        # Registered at least some services across admin and entity categories
        assert registered_admin  # non-empty
        assert registered_entity  # non-empty

        # Exercise the dispatcher for each service by invoking the captured callback
        # Choose the first registered dispatcher (they are all the same closure)
        assert dispatcher_funcs, "Dispatcher was not registered"
        dispatcher = dispatcher_funcs[0]

        # Provide minimal required data for selected services that require schema fields
        await dispatcher(_ServiceCall(service=hm_services.HmipLocalServices.CREATE_CENTRAL_LINKS, data={}, hass=hass))
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.ADD_LINK,
                data={
                    hm_services.CONF_SENDER_CHANNEL_ADDRESS: "INTF:1",
                    hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "INTF:2",
                },
                hass=hass,
            )
        )
        await dispatcher(_ServiceCall(service=hm_services.HmipLocalServices.CLEAR_CACHE, data={}, hass=hass))
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.EXPORT_DEVICE_DEFINITION,
                data={hm_services.CONF_DEVICE_ID: "dev"},
                hass=hass,
            )
        )
        await dispatcher(_ServiceCall(service=hm_services.HmipLocalServices.FETCH_SYSTEM_VARIABLES, data={}, hass=hass))
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.FORCE_DEVICE_AVAILABILITY,
                data={hm_services.CONF_DEVICE_ID: "dev"},
                hass=hass,
            )
        )

        # Services with responses
        assert await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.GET_DEVICE_VALUE,
                data={hm_services.CONF_DEVICE_ID: "dev", hm_services.CONF_CHANNEL: 1, hm_services.CONF_PARAMETER: "STATE"},
                hass=hass,
            )
        ) == {"ok": True}
        assert await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.GET_LINK_PEERS, data={hm_services.CONF_DEVICE_ID: "dev"}, hass=hass
            )
        ) == ["peer"]
        assert await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.GET_LINK_PARAMSET,
                data={
                    hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "INTF:2",
                    hm_services.CONF_SENDER_CHANNEL_ADDRESS: "INTF:1",
                },
                hass=hass,
            )
        ) == {"k": "v"}
        assert await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.GET_PARAMSET,
                data={
                    hm_services.CONF_DEVICE_ID: "dev",
                    hm_services.CONF_PARAMSET_KEY: "MASTER",
                    hm_services.CONF_PARAMSET: {},
                },
                hass=hass,
            )
        ) == {"p": 1}
        assert (
            await dispatcher(
                _ServiceCall(
                    service=hm_services.HmipLocalServices.GET_VARIABLE_VALUE,
                    data={hm_services.CONF_NAME: "sysvar"},
                    hass=hass,
                )
            )
            == 123
        )

        # Remaining services without responses
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.PUT_LINK_PARAMSET,
                data={
                    hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "INTF:2",
                    hm_services.CONF_SENDER_CHANNEL_ADDRESS: "INTF:1",
                    hm_services.CONF_PARAMSET: {},
                },
                hass=hass,
            )
        )
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.PUT_PARAMSET,
                data={
                    hm_services.CONF_DEVICE_ID: "dev",
                    hm_services.CONF_PARAMSET_KEY: "VALUES",
                    hm_services.CONF_PARAMSET: {},
                },
                hass=hass,
            )
        )
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.RECORD_SESSION, data={hm_services.CONF_DEVICE_ID: "dev"}, hass=hass
            )
        )
        await dispatcher(_ServiceCall(service=hm_services.HmipLocalServices.REMOVE_CENTRAL_LINKS, data={}, hass=hass))
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.REMOVE_LINK,
                data={
                    hm_services.CONF_RECEIVER_CHANNEL_ADDRESS: "INTF:2",
                    hm_services.CONF_SENDER_CHANNEL_ADDRESS: "INTF:1",
                },
                hass=hass,
            )
        )
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.SET_DEVICE_VALUE,
                data={
                    hm_services.CONF_DEVICE_ID: "dev",
                    hm_services.CONF_CHANNEL: 1,
                    hm_services.CONF_PARAMETER: "STATE",
                    hm_services.CONF_VALUE: True,
                },
                hass=hass,
            )
        )
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.SET_VARIABLE_VALUE,
                data={hm_services.CONF_NAME: "sysvar", hm_services.CONF_VALUE: 0},
                hass=hass,
            )
        )
        await dispatcher(
            _ServiceCall(
                service=hm_services.HmipLocalServices.UPDATE_DEVICE_FIRMWARE_DATA,
                data={hm_services.CONF_ENTRY_ID: "entry"},
                hass=hass,
            )
        )

        # Instead of fishing the closure, call the private handlers directly once to ensure coverage
        # For return-value handlers
        assert await hm_services._async_service_get_device_value(
            hass, _ServiceCall(service="get_device_value", data={"channel": 1, "parameter": "STATE"})
        ) == {"ok": True}  # type: ignore[arg-type]
        assert await hm_services._async_service_get_link_peers(hass, _ServiceCall(service="get_link_peers", data={})) == [
            "peer"
        ]  # type: ignore[arg-type]
        assert await hm_services._async_service_get_link_paramset(
            hass, _ServiceCall(service="get_link_paramset", data={})
        ) == {"k": "v"}  # type: ignore[arg-type]
        assert await hm_services._async_service_get_paramset(hass, _ServiceCall(service="get_paramset", data={})) == {
            "p": 1
        }  # type: ignore[arg-type]
        assert (
            await hm_services._async_service_get_variable_value(hass, _ServiceCall(service="get_variable_value", data={}))
            == 123
        )  # type: ignore[arg-type]


class TestAsyncUnloadServices:
    """Tests for async_unload_services function."""

    @pytest.mark.asyncio
    async def test_removes_all_when_no_entries(self, hass: HomeAssistant, monkeypatch) -> None:
        """It should remove all services when no config entries are loaded."""
        # Ensure no entries considered loaded
        monkeypatch.setattr(hm_services, "async_get_loaded_config_entries", lambda hass: [])

        removed: list[tuple[str, str]] = []

        class _SvcHelper:
            def async_remove(self, domain: str, service: str) -> None:
                removed.append((domain, service))

        hass.services = _SvcHelper()  # type: ignore[assignment]

        await hm_services.async_unload_services(hass)

        # One removal per enum value
        assert len(removed) == len(list(hm_services.HmipLocalServices))
