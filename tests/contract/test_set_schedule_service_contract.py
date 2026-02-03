"""
Contract tests for schedule services.

STABILITY GUARANTEE
-------------------
These tests define the stable API contract for the schedule services.
Any change that breaks these tests requires a MAJOR version bump.

The contract ensures that:
1. Domain-specific services are registered (e.g., switch_set_schedule, light_get_schedule)
2. Entity method async_set_schedule/async_get_schedule exists with stable signature
3. Service schema is consistent across platforms
4. Required parameters are validated
"""

from __future__ import annotations

import inspect

import pytest

from custom_components.homematicip_local.const import DOMAIN, HmipLocalServices
from custom_components.homematicip_local.generic_entity import AioHomematicGenericEntity
from homeassistant.core import HomeAssistant

# =============================================================================
# Contract: Domain-Specific set_schedule Service Registration
# =============================================================================


class TestSetScheduleServiceRegistrationContract:
    """Contract: set_schedule services must be registered per domain."""

    DOMAIN_SERVICE_MAPPING = {
        "cover": HmipLocalServices.COVER_SET_SCHEDULE,
        "light": HmipLocalServices.LIGHT_SET_SCHEDULE,
        "switch": HmipLocalServices.SWITCH_SET_SCHEDULE,
        "valve": HmipLocalServices.VALVE_SET_SCHEDULE,
    }

    @pytest.mark.asyncio
    async def test_service_name_constants_exist(self) -> None:
        """Contract: Domain-specific SET_SCHEDULE constants exist in HmipLocalServices enum."""
        assert hasattr(HmipLocalServices, "COVER_SET_SCHEDULE")
        assert hasattr(HmipLocalServices, "LIGHT_SET_SCHEDULE")
        assert hasattr(HmipLocalServices, "SWITCH_SET_SCHEDULE")
        assert hasattr(HmipLocalServices, "VALVE_SET_SCHEDULE")

        assert HmipLocalServices.COVER_SET_SCHEDULE == "cover_set_schedule"
        assert HmipLocalServices.LIGHT_SET_SCHEDULE == "light_set_schedule"
        assert HmipLocalServices.SWITCH_SET_SCHEDULE == "switch_set_schedule"
        assert HmipLocalServices.VALVE_SET_SCHEDULE == "valve_set_schedule"

    def test_service_schema_has_schedule_data_field(self) -> None:
        """Contract: Each set_schedule service schema requires schedule_data field."""
        from pathlib import Path

        import yaml

        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )

        with services_yaml_path.open() as f:
            services_data = yaml.safe_load(f)

        for service_name in self.DOMAIN_SERVICE_MAPPING.values():
            assert service_name in services_data, f"{service_name} not in services.yaml"
            service_def = services_data[service_name]
            assert "fields" in service_def, f"{service_name} has no fields"
            assert "schedule_data" in service_def["fields"], f"{service_name} missing schedule_data field"

            schedule_data_field = service_def["fields"]["schedule_data"]
            assert schedule_data_field["required"] is True
            assert "selector" in schedule_data_field
            assert "object" in schedule_data_field["selector"]

    @pytest.mark.asyncio
    async def test_services_are_registered_per_domain(self, hass: HomeAssistant) -> None:
        """Contract: Domain-specific set_schedule services are registered."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Each domain should have its own service
        for entity_domain, service_name in self.DOMAIN_SERVICE_MAPPING.items():
            assert hass.services.has_service(DOMAIN, service_name), (
                f"Service {service_name} not registered for domain {entity_domain}"
            )

    def test_services_target_correct_domains(self) -> None:
        """Contract: Each set_schedule service targets its specific domain."""
        from pathlib import Path

        import yaml

        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )

        with services_yaml_path.open() as f:
            services_data = yaml.safe_load(f)

        for entity_domain, service_name in self.DOMAIN_SERVICE_MAPPING.items():
            service_def = services_data[service_name]
            assert "target" in service_def
            assert "entity" in service_def["target"]
            assert "domain" in service_def["target"]["entity"]

            target_domain = service_def["target"]["entity"]["domain"]
            assert target_domain == entity_domain, f"{service_name} targets {target_domain}, expected {entity_domain}"


# =============================================================================
# Contract: AioHomematicGenericEntity.async_set_schedule Method
# =============================================================================


class TestAsyncSetScheduleMethodContract:
    """Contract: async_set_schedule method must exist with stable signature."""

    def test_async_set_schedule_accepts_dict_parameter(self) -> None:
        """Contract: async_set_schedule accepts schedule_data as dict."""
        method = getattr(AioHomematicGenericEntity, "async_set_schedule")
        sig = inspect.signature(method)

        schedule_data_param = sig.parameters["schedule_data"]
        # Annotation should be dict[int, dict[Any, Any]] or compatible
        annotation_str = str(schedule_data_param.annotation)
        assert "dict" in annotation_str.lower()

    def test_async_set_schedule_is_async(self) -> None:
        """Contract: async_set_schedule is an async method."""
        method = getattr(AioHomematicGenericEntity, "async_set_schedule")
        assert inspect.iscoroutinefunction(method)

    def test_async_set_schedule_method_exists(self) -> None:
        """Contract: async_set_schedule method exists on AioHomematicGenericEntity."""
        assert hasattr(AioHomematicGenericEntity, "async_set_schedule")

    def test_async_set_schedule_return_type(self) -> None:
        """Contract: async_set_schedule returns None."""
        method = getattr(AioHomematicGenericEntity, "async_set_schedule")
        sig = inspect.signature(method)

        # Return annotation should be None
        return_annotation = sig.return_annotation
        assert return_annotation is None or str(return_annotation) == "None"

    def test_async_set_schedule_signature(self) -> None:
        """Contract: async_set_schedule has stable signature."""
        method = getattr(AioHomematicGenericEntity, "async_set_schedule")
        sig = inspect.signature(method)

        # Check parameters
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "schedule_data" in params

        # Check schedule_data parameter type
        schedule_data_param = sig.parameters["schedule_data"]
        assert schedule_data_param.annotation != inspect.Parameter.empty


# =============================================================================
# Contract: Service Implementation in services.py
# =============================================================================


class TestSetScheduleServiceImplementationContract:
    """Contract: set_schedule service implementation must be stable."""

    def test_attr_schedule_data_constant_exists(self) -> None:
        """Contract: ATTR_SCHEDULE_DATA constant exists."""
        from custom_components.homematicip_local import generic_entity

        assert hasattr(generic_entity, "ATTR_SCHEDULE_DATA")
        assert generic_entity.ATTR_SCHEDULE_DATA == "schedule_data"

    def test_domain_specific_services_registered_inline(self) -> None:
        """Contract: Domain-specific set_schedule services are registered inline."""
        from pathlib import Path

        services_py_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.py"
        )

        with services_py_path.open() as f:
            content = f.read()

        # Check that domain-specific set_schedule services are registered
        assert "async_register_platform_entity_service" in content
        assert "HmipLocalServices.COVER_SET_SCHEDULE" in content
        assert "HmipLocalServices.LIGHT_SET_SCHEDULE" in content
        assert "HmipLocalServices.SWITCH_SET_SCHEDULE" in content
        assert "HmipLocalServices.VALVE_SET_SCHEDULE" in content


# =============================================================================
# Contract: Entity Support for Schedules
# =============================================================================


class TestScheduleSupportContract:
    """Contract: Entities must properly check for schedule support."""

    def test_async_set_schedule_calls_week_profile_set_schedule(self) -> None:
        """Contract: async_set_schedule delegates to data_point.set_schedule."""
        from pathlib import Path

        generic_entity_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "generic_entity.py"
        )

        with generic_entity_path.open() as f:
            content = f.read()

        # Check that data_point.set_schedule is called
        assert "await self._data_point.set_schedule(schedule_data=schedule_data)" in content

    def test_async_set_schedule_checks_custom_data_point(self) -> None:
        """Contract: async_set_schedule validates CustomDataPointProtocol."""
        from pathlib import Path

        generic_entity_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "generic_entity.py"
        )

        with generic_entity_path.open() as f:
            content = f.read()

        # Check for CustomDataPointProtocol validation
        assert "CustomDataPointProtocol" in content
        assert "not isinstance(self._data_point, CustomDataPointProtocol)" in content

    def test_async_set_schedule_checks_has_schedule(self) -> None:
        """Contract: async_set_schedule checks has_schedule property."""
        from pathlib import Path

        generic_entity_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "generic_entity.py"
        )

        with generic_entity_path.open() as f:
            content = f.read()

        # Check for has_schedule validation
        assert "has_schedule" in content
        assert "not self._data_point.has_schedule" in content

    def test_async_set_schedule_checks_week_profile(self) -> None:
        """Contract: async_set_schedule uses data_point.set_schedule."""
        from pathlib import Path

        generic_entity_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "generic_entity.py"
        )

        with generic_entity_path.open() as f:
            content = f.read()

        # Check that data_point.set_schedule is used (no direct week_profile access needed)
        assert "self._data_point.set_schedule" in content


# =============================================================================
# Contract: Supported Domains
# =============================================================================


class TestSupportedDomainsContract:
    """Contract: set_schedule must support specific entity domains."""

    SUPPORTED_DOMAINS = {"switch", "light", "cover", "valve"}

    def test_climate_domain_has_separate_services(self) -> None:
        """Contract: climate domain uses different schedule services (not *_set_schedule)."""
        from pathlib import Path

        import yaml

        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )

        with services_yaml_path.open() as f:
            services_data = yaml.safe_load(f)

        # Climate should not have a climate_set_schedule service
        # It uses set_schedule_profile and set_schedule_weekday instead
        assert "climate_set_schedule" not in services_data
        assert "set_schedule_simple_profile" in services_data
        assert "set_schedule_simple_weekday" in services_data

    def test_supported_domains_have_services(self) -> None:
        """Contract: All supported domains have their own set_schedule service."""
        from pathlib import Path

        import yaml

        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )

        with services_yaml_path.open() as f:
            services_data = yaml.safe_load(f)

        for domain in self.SUPPORTED_DOMAINS:
            service_name = f"{domain}_set_schedule"
            assert service_name in services_data, f"Service {service_name} not found in services.yaml"


# =============================================================================
# Contract: Domain-Specific get_schedule Service Registration
# =============================================================================


class TestGetScheduleServiceRegistrationContract:
    """Contract: get_schedule services must be registered per domain."""

    DOMAIN_SERVICE_MAPPING = {
        "cover": HmipLocalServices.COVER_GET_SCHEDULE,
        "light": HmipLocalServices.LIGHT_GET_SCHEDULE,
        "switch": HmipLocalServices.SWITCH_GET_SCHEDULE,
        "valve": HmipLocalServices.VALVE_GET_SCHEDULE,
    }

    @pytest.mark.asyncio
    async def test_service_name_constants_exist(self) -> None:
        """Contract: Domain-specific GET_SCHEDULE constants exist in HmipLocalServices enum."""
        assert hasattr(HmipLocalServices, "COVER_GET_SCHEDULE")
        assert hasattr(HmipLocalServices, "LIGHT_GET_SCHEDULE")
        assert hasattr(HmipLocalServices, "SWITCH_GET_SCHEDULE")
        assert hasattr(HmipLocalServices, "VALVE_GET_SCHEDULE")

        assert HmipLocalServices.COVER_GET_SCHEDULE == "cover_get_schedule"
        assert HmipLocalServices.LIGHT_GET_SCHEDULE == "light_get_schedule"
        assert HmipLocalServices.SWITCH_GET_SCHEDULE == "switch_get_schedule"
        assert HmipLocalServices.VALVE_GET_SCHEDULE == "valve_get_schedule"

    @pytest.mark.asyncio
    async def test_services_are_registered_per_domain(self, hass: HomeAssistant) -> None:
        """Contract: Domain-specific get_schedule services are registered."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Each domain should have its own service
        for entity_domain, service_name in self.DOMAIN_SERVICE_MAPPING.items():
            assert hass.services.has_service(DOMAIN, service_name), (
                f"Service {service_name} not registered for domain {entity_domain}"
            )

    @pytest.mark.asyncio
    async def test_services_in_services_yaml(self) -> None:
        """Contract: Domain-specific get_schedule services are defined in services.yaml."""
        from pathlib import Path

        import yaml

        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )

        with services_yaml_path.open() as f:
            services_data = yaml.safe_load(f)

        for entity_domain, service_name in self.DOMAIN_SERVICE_MAPPING.items():
            assert service_name in services_data, f"{service_name} not in services.yaml"

            service_def = services_data[service_name]
            assert "target" in service_def
            assert "entity" in service_def["target"]

            target_domain = service_def["target"]["entity"]["domain"]
            assert target_domain == entity_domain


# =============================================================================
# Contract: async_get_schedule Method Signature
# =============================================================================


class TestAsyncGetScheduleMethodSignatureContract:
    """Contract: async_get_schedule method must have stable signature."""

    @pytest.mark.asyncio
    async def test_method_exists(self) -> None:
        """Contract: async_get_schedule method exists on AioHomematicGenericEntity."""
        assert hasattr(AioHomematicGenericEntity, "async_get_schedule")
        assert callable(getattr(AioHomematicGenericEntity, "async_get_schedule"))

    @pytest.mark.asyncio
    async def test_method_is_coroutine(self) -> None:
        """Contract: async_get_schedule is a coroutine function."""
        method = getattr(AioHomematicGenericEntity, "async_get_schedule")
        assert inspect.iscoroutinefunction(method)

    @pytest.mark.asyncio
    async def test_method_signature(self) -> None:
        """Contract: async_get_schedule has stable signature."""
        method = getattr(AioHomematicGenericEntity, "async_get_schedule")
        sig = inspect.signature(method)

        # Return type must be ServiceResponse
        return_annotation = sig.return_annotation
        assert return_annotation is not inspect.Signature.empty
        # Check that return annotation is the expected type string
        assert "ServiceResponse" in str(return_annotation)


# =============================================================================
# Contract: Service Response Support
# =============================================================================


class TestGetScheduleServiceResponseContract:
    """Contract: get_schedule services support response data."""

    @pytest.mark.asyncio
    async def test_services_support_response(self, hass: HomeAssistant) -> None:
        """Contract: get_schedule services are registered with response support."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # All domain-specific get_schedule services should be registered
        for service_name in [
            HmipLocalServices.COVER_GET_SCHEDULE,
            HmipLocalServices.LIGHT_GET_SCHEDULE,
            HmipLocalServices.SWITCH_GET_SCHEDULE,
            HmipLocalServices.VALVE_GET_SCHEDULE,
        ]:
            assert hass.services.has_service(DOMAIN, service_name)
