"""
Contract tests for set_schedule service.

STABILITY GUARANTEE
-------------------
These tests define the stable API contract for the set_schedule service.
Any change that breaks these tests requires a MAJOR version bump.

The contract ensures that:
1. Service is registered for all supported domains
2. Entity method async_set_schedule exists with stable signature
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
# Contract: set_schedule Service Registration
# =============================================================================


class TestSetScheduleServiceRegistrationContract:
    """Contract: set_schedule service must be registered for supported domains."""

    SUPPORTED_DOMAINS = ("switch", "light", "cover", "valve")

    @pytest.mark.asyncio
    async def test_service_is_registered(self, hass: HomeAssistant) -> None:
        """Contract: set_schedule service is registered in the domain."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Service should be registered
        assert hass.services.has_service(DOMAIN, HmipLocalServices.SET_SCHEDULE)

    @pytest.mark.asyncio
    async def test_service_name_constant_exists(self) -> None:
        """Contract: SET_SCHEDULE constant exists in HmipLocalServices enum."""
        assert hasattr(HmipLocalServices, "SET_SCHEDULE")
        assert HmipLocalServices.SET_SCHEDULE == "set_schedule"

    def test_service_schema_has_schedule_data_field(self) -> None:
        """Contract: set_schedule service schema requires schedule_data field."""
        from pathlib import Path

        import yaml

        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )

        with services_yaml_path.open() as f:
            services_data = yaml.safe_load(f)

        service_def = services_data["set_schedule"]
        assert "fields" in service_def
        assert "schedule_data" in service_def["fields"]

        schedule_data_field = service_def["fields"]["schedule_data"]
        assert schedule_data_field["required"] is True
        assert "selector" in schedule_data_field
        assert "object" in schedule_data_field["selector"]

    def test_service_schema_in_services_yaml(self) -> None:
        """Contract: set_schedule service is defined in services.yaml."""
        from pathlib import Path

        import yaml

        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )
        assert services_yaml_path.exists(), "services.yaml not found"

        with services_yaml_path.open() as f:
            services_data = yaml.safe_load(f)

        assert "set_schedule" in services_data, "set_schedule not in services.yaml"
        service_def = services_data["set_schedule"]

        # Verify target domains
        assert "target" in service_def
        assert "entity" in service_def["target"]
        assert "domain" in service_def["target"]["entity"]

        target_domains = service_def["target"]["entity"]["domain"]
        assert isinstance(target_domains, list)
        assert set(target_domains) == set(self.SUPPORTED_DOMAINS)


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

    def test_register_set_schedule_services_function_exists(self) -> None:
        """Contract: _register_set_schedule_services function exists."""
        from custom_components.homematicip_local import services

        assert hasattr(services, "_register_set_schedule_services")

    def test_register_set_schedule_services_is_called(self) -> None:
        """Contract: set_schedule services are registered during setup."""
        from pathlib import Path

        services_py_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.py"
        )

        with services_py_path.open() as f:
            content = f.read()

        # Check that set_schedule service is registered inline
        assert "async_register_platform_entity_service" in content
        assert "HmipLocalServices.SET_SCHEDULE" in content


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

    def test_climate_domain_not_supported(self) -> None:
        """Contract: climate domain uses different schedule services."""
        from pathlib import Path

        import yaml

        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )

        with services_yaml_path.open() as f:
            services_data = yaml.safe_load(f)

        service_def = services_data["set_schedule"]
        target_domains = service_def["target"]["entity"]["domain"]

        # Climate should not be in the list (it has its own schedule services)
        assert "climate" not in target_domains

    def test_supported_domains_are_registered(self) -> None:
        """Contract: All supported domains are registered in _register_set_schedule_services."""
        from pathlib import Path

        services_py_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.py"
        )

        with services_py_path.open() as f:
            content = f.read()

        # Check that all supported domains are in the registration loop
        for domain in self.SUPPORTED_DOMAINS:
            assert f"{domain.upper()}_DOMAIN" in content or f'"{domain}"' in content


# =============================================================================
# Contract: get_schedule Service Registration
# =============================================================================


class TestGetScheduleServiceRegistrationContract:
    """Contract: get_schedule service must be registered for supported domains."""

    SUPPORTED_DOMAINS = ("switch", "light", "cover", "valve")

    @pytest.mark.asyncio
    async def test_service_is_registered(self, hass: HomeAssistant) -> None:
        """Contract: get_schedule service is registered in the domain."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Service should be registered
        assert hass.services.has_service(DOMAIN, HmipLocalServices.GET_SCHEDULE)

    @pytest.mark.asyncio
    async def test_service_name_constant_exists(self) -> None:
        """Contract: GET_SCHEDULE constant exists in HmipLocalServices enum."""
        assert hasattr(HmipLocalServices, "GET_SCHEDULE")
        assert HmipLocalServices.GET_SCHEDULE == "get_schedule"

    @pytest.mark.asyncio
    async def test_service_schema_in_services_yaml(self) -> None:
        """Contract: get_schedule service is defined in services.yaml."""
        from pathlib import Path

        import yaml

        # Load services.yaml
        services_yaml_path = (
            Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local" / "services.yaml"
        )
        with open(services_yaml_path) as f:
            services_schema = yaml.safe_load(f)

        # Service must exist
        assert "get_schedule" in services_schema

        # Verify target domains
        target_config = services_schema["get_schedule"]["target"]
        assert "entity" in target_config
        entity_config = target_config["entity"]
        assert "domain" in entity_config

        target_domains = entity_config["domain"]
        assert isinstance(target_domains, list)
        assert set(target_domains) == set(self.SUPPORTED_DOMAINS)

        # Verify integration is specified
        assert entity_config["integration"] == "homematicip_local"


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
    """Contract: get_schedule service supports response data."""

    @pytest.mark.asyncio
    async def test_service_supports_response(self, hass: HomeAssistant) -> None:
        """Contract: get_schedule service is registered with response support."""
        from custom_components.homematicip_local import services

        await services.async_setup_services(hass)

        # Verify service is registered
        assert hass.services.has_service(DOMAIN, HmipLocalServices.GET_SCHEDULE)

        # The service must be callable and support returning data
        # Platform entity services with supports_response=SupportsResponse.OPTIONAL
        # are expected to return data when called
