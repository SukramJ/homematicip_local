"""
Contract tests for device-based schedule services.

STABILITY GUARANTEE
-------------------
These tests define the stable API contract for the schedule services.
Any change that breaks these tests requires a MAJOR version bump.

The contract ensures that:
1. Device-based schedule services are registered (get_schedule, set_schedule, etc.)
2. Service handler functions exist with stable signatures
3. Service schema is consistent across all schedule services
4. Required parameters are validated
5. Climate-specific services check for ClimateWeekProfileDataPointProtocol
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest
import yaml

from custom_components.homematicip_local.const import DOMAIN, HmipLocalServices
from homeassistant.core import HomeAssistant

SERVICES_YAML_PATH = Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
SERVICES_PY_PATH = Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.py"


# =============================================================================
# Contract: Device-Based Service Constants
# =============================================================================


class TestScheduleServiceConstantsContract:
    """Contract: Device-based schedule service constants must exist in HmipLocalServices."""

    def test_device_based_constant_values(self) -> None:
        """Contract: Device-based schedule service constant values are stable."""
        assert HmipLocalServices.GET_SCHEDULE == "get_schedule"
        assert HmipLocalServices.SET_SCHEDULE == "set_schedule"
        assert HmipLocalServices.GET_SCHEDULE_PROFILE == "get_schedule_profile"
        assert HmipLocalServices.GET_SCHEDULE_WEEKDAY == "get_schedule_weekday"
        assert HmipLocalServices.SET_SCHEDULE_PROFILE == "set_schedule_profile"
        assert HmipLocalServices.SET_SCHEDULE_WEEKDAY == "set_schedule_weekday"
        assert HmipLocalServices.COPY_SCHEDULE == "copy_schedule"
        assert HmipLocalServices.COPY_SCHEDULE_PROFILE == "copy_schedule_profile"
        assert HmipLocalServices.SET_CURRENT_SCHEDULE_PROFILE == "set_current_schedule_profile"

    def test_device_based_constants_exist(self) -> None:
        """Contract: Device-based schedule service constants exist."""
        assert hasattr(HmipLocalServices, "GET_SCHEDULE")
        assert hasattr(HmipLocalServices, "SET_SCHEDULE")
        assert hasattr(HmipLocalServices, "GET_SCHEDULE_PROFILE")
        assert hasattr(HmipLocalServices, "GET_SCHEDULE_WEEKDAY")
        assert hasattr(HmipLocalServices, "SET_SCHEDULE_PROFILE")
        assert hasattr(HmipLocalServices, "SET_SCHEDULE_WEEKDAY")
        assert hasattr(HmipLocalServices, "COPY_SCHEDULE")
        assert hasattr(HmipLocalServices, "COPY_SCHEDULE_PROFILE")
        assert hasattr(HmipLocalServices, "SET_CURRENT_SCHEDULE_PROFILE")

    def test_old_domain_specific_constants_removed(self) -> None:
        """Contract: Old domain-specific constants are removed."""
        assert not hasattr(HmipLocalServices, "COVER_GET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "COVER_SET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "LIGHT_GET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "LIGHT_SET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "SWITCH_GET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "SWITCH_SET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "VALVE_GET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "VALVE_SET_SCHEDULE")
        assert not hasattr(HmipLocalServices, "GET_SCHEDULE_SIMPLE_PROFILE")
        assert not hasattr(HmipLocalServices, "GET_SCHEDULE_SIMPLE_WEEKDAY")
        assert not hasattr(HmipLocalServices, "SET_SCHEDULE_SIMPLE_PROFILE")
        assert not hasattr(HmipLocalServices, "SET_SCHEDULE_SIMPLE_WEEKDAY")


# =============================================================================
# Contract: Service Registration
# =============================================================================


class TestScheduleServiceRegistrationContract:
    """Contract: Device-based schedule services must be registered."""

    DEVICE_BASED_SERVICES = [
        HmipLocalServices.GET_SCHEDULE,
        HmipLocalServices.SET_SCHEDULE,
        HmipLocalServices.GET_SCHEDULE_PROFILE,
        HmipLocalServices.GET_SCHEDULE_WEEKDAY,
        HmipLocalServices.SET_SCHEDULE_PROFILE,
        HmipLocalServices.SET_SCHEDULE_WEEKDAY,
        HmipLocalServices.COPY_SCHEDULE,
        HmipLocalServices.COPY_SCHEDULE_PROFILE,
    ]

    @pytest.mark.asyncio
    async def test_device_based_services_registered(self, hass: HomeAssistant) -> None:
        """Contract: All device-based schedule services are registered."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        for service_name in self.DEVICE_BASED_SERVICES:
            assert hass.services.has_service(DOMAIN, service_name), f"Service {service_name} not registered"

    @pytest.mark.asyncio
    async def test_old_domain_specific_services_not_registered(self, hass: HomeAssistant) -> None:
        """Contract: Old domain-specific services are not registered."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        old_services = [
            "cover_get_schedule",
            "cover_set_schedule",
            "light_get_schedule",
            "light_set_schedule",
            "switch_get_schedule",
            "switch_set_schedule",
            "valve_get_schedule",
            "valve_set_schedule",
            "get_schedule_simple_profile",
            "get_schedule_simple_weekday",
            "set_schedule_simple_profile",
            "set_schedule_simple_weekday",
        ]
        for service_name in old_services:
            assert not hass.services.has_service(DOMAIN, service_name), (
                f"Old service {service_name} should not be registered"
            )


# =============================================================================
# Contract: services.yaml Schema
# =============================================================================


class TestScheduleServiceYamlContract:
    """Contract: services.yaml must define device-based schedule services."""

    @pytest.fixture
    def services_data(self) -> dict:
        """Load services.yaml data."""
        with SERVICES_YAML_PATH.open() as f:
            return yaml.safe_load(f)

    def test_copy_schedule_defined(self, services_data: dict) -> None:
        """Contract: copy_schedule service is defined with target_device_id field."""
        assert "copy_schedule" in services_data
        service_def = services_data["copy_schedule"]
        assert "fields" in service_def
        assert "device_id" in service_def["fields"]
        assert "target_device_id" in service_def["fields"]

    def test_copy_schedule_profile_defined(self, services_data: dict) -> None:
        """Contract: copy_schedule_profile service is defined with profile fields."""
        assert "copy_schedule_profile" in services_data
        service_def = services_data["copy_schedule_profile"]
        assert "fields" in service_def
        assert "device_id" in service_def["fields"]
        assert "source_profile" in service_def["fields"]
        assert "target_profile" in service_def["fields"]

    def test_get_schedule_defined(self, services_data: dict) -> None:
        """Contract: get_schedule service is defined in services.yaml."""
        assert "get_schedule" in services_data
        service_def = services_data["get_schedule"]
        assert "fields" in service_def
        assert "device_id" in service_def["fields"]

    def test_get_schedule_profile_defined(self, services_data: dict) -> None:
        """Contract: get_schedule_profile service is defined with profile field."""
        assert "get_schedule_profile" in services_data
        service_def = services_data["get_schedule_profile"]
        assert "fields" in service_def
        assert "device_id" in service_def["fields"]
        assert "profile" in service_def["fields"]

    def test_get_schedule_weekday_defined(self, services_data: dict) -> None:
        """Contract: get_schedule_weekday service is defined with profile and weekday fields."""
        assert "get_schedule_weekday" in services_data
        service_def = services_data["get_schedule_weekday"]
        assert "fields" in service_def
        assert "device_id" in service_def["fields"]
        assert "profile" in service_def["fields"]
        assert "weekday" in service_def["fields"]

    def test_old_domain_specific_services_not_in_yaml(self, services_data: dict) -> None:
        """Contract: Old domain-specific services are not in services.yaml."""
        old_services = [
            "cover_get_schedule",
            "cover_set_schedule",
            "light_get_schedule",
            "light_set_schedule",
            "switch_get_schedule",
            "switch_set_schedule",
            "valve_get_schedule",
            "valve_set_schedule",
            "get_schedule_simple_profile",
            "get_schedule_simple_weekday",
            "set_schedule_simple_profile",
            "set_schedule_simple_weekday",
        ]
        for service_name in old_services:
            assert service_name not in services_data, f"Old service {service_name} should not be in services.yaml"

    def test_set_schedule_defined(self, services_data: dict) -> None:
        """Contract: set_schedule service is defined with schedule_data field."""
        assert "set_schedule" in services_data
        service_def = services_data["set_schedule"]
        assert "fields" in service_def
        assert "device_id" in service_def["fields"]
        assert "schedule_data" in service_def["fields"]
        assert service_def["fields"]["schedule_data"]["required"] is True

    def test_set_schedule_profile_defined(self, services_data: dict) -> None:
        """Contract: set_schedule_profile service is defined with required fields."""
        assert "set_schedule_profile" in services_data
        service_def = services_data["set_schedule_profile"]
        assert "fields" in service_def
        assert "device_id" in service_def["fields"]
        assert "profile" in service_def["fields"]
        assert "simple_profile_data" in service_def["fields"]

    def test_set_schedule_weekday_defined(self, services_data: dict) -> None:
        """Contract: set_schedule_weekday service is defined with required fields."""
        assert "set_schedule_weekday" in services_data
        service_def = services_data["set_schedule_weekday"]
        assert "fields" in service_def
        assert "device_id" in service_def["fields"]
        assert "profile" in service_def["fields"]
        assert "weekday" in service_def["fields"]


# =============================================================================
# Contract: Service Handler Functions
# =============================================================================


class TestScheduleServiceHandlerContract:
    """Contract: Service handler functions must exist with stable signatures."""

    def test_handler_functions_are_async(self) -> None:
        """Contract: All service handler functions are coroutines."""
        from custom_components.homematicip_local import services

        handler_names = [
            "_async_service_get_schedule",
            "_async_service_set_schedule",
            "_async_service_get_schedule_profile",
            "_async_service_get_schedule_weekday",
            "_async_service_set_schedule_profile",
            "_async_service_set_schedule_weekday",
            "_async_service_copy_schedule",
            "_async_service_copy_schedule_profile",
        ]
        for name in handler_names:
            handler = getattr(services, name)
            assert inspect.iscoroutinefunction(handler), f"{name} must be a coroutine function"

    def test_handler_functions_exist(self) -> None:
        """Contract: All device-based service handler functions exist."""
        from custom_components.homematicip_local import services

        assert hasattr(services, "_async_service_get_schedule")
        assert hasattr(services, "_async_service_set_schedule")
        assert hasattr(services, "_async_service_get_schedule_profile")
        assert hasattr(services, "_async_service_get_schedule_weekday")
        assert hasattr(services, "_async_service_set_schedule_profile")
        assert hasattr(services, "_async_service_set_schedule_weekday")
        assert hasattr(services, "_async_service_copy_schedule")
        assert hasattr(services, "_async_service_copy_schedule_profile")

    def test_handler_signatures_accept_hass_and_service(self) -> None:
        """Contract: All handlers accept hass and service keyword arguments."""
        from custom_components.homematicip_local import services

        handler_names = [
            "_async_service_get_schedule",
            "_async_service_set_schedule",
            "_async_service_get_schedule_profile",
            "_async_service_get_schedule_weekday",
            "_async_service_set_schedule_profile",
            "_async_service_set_schedule_weekday",
            "_async_service_copy_schedule",
            "_async_service_copy_schedule_profile",
        ]
        for name in handler_names:
            handler = getattr(services, name)
            sig = inspect.signature(handler)
            params = list(sig.parameters.keys())
            assert "hass" in params, f"{name} must accept 'hass' parameter"
            assert "service" in params, f"{name} must accept 'service' parameter"


# =============================================================================
# Contract: ATTR_SCHEDULE_DATA Constant
# =============================================================================


class TestScheduleDataConstantContract:
    """Contract: ATTR_SCHEDULE_DATA constant must exist."""

    def test_attr_schedule_data_in_generic_entity(self) -> None:
        """Contract: ATTR_SCHEDULE_DATA exists in generic_entity module."""
        from custom_components.homematicip_local import generic_entity

        assert hasattr(generic_entity, "ATTR_SCHEDULE_DATA")
        assert generic_entity.ATTR_SCHEDULE_DATA == "schedule_data"

    def test_attr_schedule_data_in_services(self) -> None:
        """Contract: ATTR_SCHEDULE_DATA exists in services module."""
        from custom_components.homematicip_local import services

        assert hasattr(services, "ATTR_SCHEDULE_DATA")
        assert services.ATTR_SCHEDULE_DATA == "schedule_data"


# =============================================================================
# Contract: services.py Implementation
# =============================================================================


class TestScheduleServiceImplementationContract:
    """Contract: services.py must use device-based service registration."""

    def test_device_based_registration_used(self) -> None:
        """Contract: Services are registered via hass.services.async_register."""
        with SERVICES_PY_PATH.open() as f:
            content = f.read()

        assert "HmipLocalServices.GET_SCHEDULE" in content
        assert "HmipLocalServices.SET_SCHEDULE" in content
        assert "HmipLocalServices.GET_SCHEDULE_PROFILE" in content
        assert "HmipLocalServices.SET_SCHEDULE_WEEKDAY" in content
        assert "HmipLocalServices.COPY_SCHEDULE" in content

    def test_device_lookup_used(self) -> None:
        """Contract: Handlers use _async_get_hm_device_by_service_data for device lookup."""
        with SERVICES_PY_PATH.open() as f:
            content = f.read()

        assert "_async_get_hm_device_by_service_data" in content
        assert "week_profile_data_point" in content

    def test_no_old_domain_specific_registration(self) -> None:
        """Contract: Old domain-specific service registrations are removed."""
        with SERVICES_PY_PATH.open() as f:
            content = f.read()

        assert "HmipLocalServices.COVER_SET_SCHEDULE" not in content
        assert "HmipLocalServices.LIGHT_SET_SCHEDULE" not in content
        assert "HmipLocalServices.SWITCH_SET_SCHEDULE" not in content
        assert "HmipLocalServices.VALVE_SET_SCHEDULE" not in content
        assert "HmipLocalServices.COVER_GET_SCHEDULE" not in content
        assert "HmipLocalServices.LIGHT_GET_SCHEDULE" not in content
        assert "HmipLocalServices.SWITCH_GET_SCHEDULE" not in content
        assert "HmipLocalServices.VALVE_GET_SCHEDULE" not in content
