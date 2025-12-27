"""Test the Homematic(IP) Local for OpenCCU config flow."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from aiohomematic.backend_detection import BackendDetectionResult
from aiohomematic.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    Backend,
    Interface,
    SystemInformation,
    get_interface_default_port,
)
from aiohomematic.exceptions import AuthFailure, NoConnectionException, ValidationException
from custom_components.homematicip_local.config_flow import (
    CONF_ADVANCED_CONFIG,
    CONF_BIDCOS_RF_PORT,
    CONF_BIDCOS_WIRED_PORT,
    CONF_CUSTOM_PORT_CONFIG,
    CONF_CUSTOM_PORTS,
    CONF_ENABLE_BIDCOS_RF,
    CONF_ENABLE_BIDCOS_WIRED,
    CONF_ENABLE_CCU_JACK,
    CONF_ENABLE_CUXD,
    CONF_ENABLE_HMIP_RF,
    CONF_ENABLE_VIRTUAL_DEVICES,
    CONF_HMIP_RF_PORT,
    CONF_INSTANCE_NAME,
    CONF_VIRTUAL_DEVICES_PATH,
    CONF_VIRTUAL_DEVICES_PORT,
    IF_VIRTUAL_DEVICES_PATH,
    InvalidConfig,
    _async_validate_config_and_get_system_information,
    _get_ccu_data,
    _get_instance_name,
    _get_serial,
    _update_advanced_input,
    _update_interface_input,
    get_advanced_schema,
    get_interface_schema,
)
from custom_components.homematicip_local.const import (
    CONF_ADVANCED_CONFIG as CONST_ADVANCED_CONFIG,
    CONF_CALLBACK_HOST,
    CONF_CALLBACK_PORT_XML_RPC,
    CONF_ENABLE_MQTT,
    CONF_ENABLE_PROGRAM_SCAN,
    CONF_ENABLE_SUB_DEVICES,
    CONF_ENABLE_SYSTEM_NOTIFICATIONS,
    CONF_ENABLE_SYSVAR_SCAN,
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
    DOMAIN as HMIP_DOMAIN,
)
from homeassistant import config_entries
from homeassistant.components import ssdp
from homeassistant.const import CONF_HOST, CONF_PATH, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from tests import const

# Port constants using helper function (must be after imports)
IF_HMIP_RF_PORT = get_interface_default_port(interface=Interface.HMIP_RF, tls=False)
IF_HMIP_RF_TLS_PORT = get_interface_default_port(interface=Interface.HMIP_RF, tls=True)
IF_BIDCOS_RF_PORT = get_interface_default_port(interface=Interface.BIDCOS_RF, tls=False)
IF_BIDCOS_RF_TLS_PORT = get_interface_default_port(interface=Interface.BIDCOS_RF, tls=True)
IF_BIDCOS_WIRED_PORT = get_interface_default_port(interface=Interface.BIDCOS_WIRED, tls=False)
IF_VIRTUAL_DEVICES_PORT = get_interface_default_port(interface=Interface.VIRTUAL_DEVICES, tls=False)


def _get_default_detection_result(tls: bool = False) -> BackendDetectionResult:
    """Return a default detection result for tests."""
    return BackendDetectionResult(
        backend=Backend.CCU,
        available_interfaces=(Interface.HMIP_RF, Interface.BIDCOS_RF),
        detected_port=2010 if not tls else 42010,
        tls=tls,
        host=const.HOST,
        version="3.0.0",
        auth_enabled=True,
        https_redirect_enabled=False,
    )


async def async_check_form(
    hass: HomeAssistant,
    central_data: dict[str, Any] | None = None,
    interface_data: dict[str, Any] | None = None,
    tls: bool = False,
    detection_result: BackendDetectionResult | None = None,
) -> dict[str, Any]:
    """Test we get the form."""
    if central_data is None:
        central_data = {
            CONF_INSTANCE_NAME: const.INSTANCE_NAME,
            CONF_HOST: const.HOST,
            CONF_USERNAME: const.USERNAME,
            CONF_PASSWORD: const.PASSWORD,
        }

    # Interface data should include TLS settings (moved from central step)
    # Note: The new simplified interface step only accepts TLS and interface enable flags
    # Port fields are automatically calculated from TLS setting
    if interface_data is None:
        interface_data = {}

    # Filter out port fields - they're not part of the simplified interface schema anymore
    port_fields = {
        CONF_HMIP_RF_PORT,
        CONF_BIDCOS_RF_PORT,
        CONF_BIDCOS_WIRED_PORT,
        CONF_VIRTUAL_DEVICES_PORT,
        CONF_VIRTUAL_DEVICES_PATH,
    }
    filtered_interface_data = {k: v for k, v in interface_data.items() if k not in port_fields}

    # Ensure TLS settings are included in interface_data
    if CONF_TLS not in filtered_interface_data:
        filtered_interface_data[CONF_TLS] = tls
    if CONF_VERIFY_TLS not in filtered_interface_data:
        filtered_interface_data[CONF_VERIFY_TLS] = False
    interface_data = filtered_interface_data

    # Use default detection result if none provided
    if detection_result is None:
        detection_result = _get_default_detection_result(tls=tls)

    # Create patches that will last for the entire test
    # Note: Must use AsyncMock for async functions
    with (
        patch(
            "custom_components.homematicip_local.config_flow._async_detect_backend",
            new_callable=AsyncMock,
            return_value=detection_result,
        ),
        patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            new_callable=AsyncMock,
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ),
        patch(
            "custom_components.homematicip_local.async_setup_entry",
            return_value=True,
        ),
    ):
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] is None

        # Central step: host, credentials only (TLS moved to interface step)
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
            },
        )
        await hass.async_block_till_done()

        # Handle progress step for backend detection (if detection takes time)
        # Since mock returns immediately, progress may complete before we see SHOW_PROGRESS
        # The first result might be SHOW_PROGRESS, SHOW_PROGRESS_DONE, or directly FORM
        while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
            await hass.async_block_till_done()
            result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
            await hass.async_block_till_done()

        # After progress is done, we should be at interface form
        assert result2["type"] == FlowResultType.FORM, (
            f"Expected FORM but got {result2['type']}, step={result2.get('step_id')}"
        )
        assert result2["handler"] == HMIP_DOMAIN
        assert result2["step_id"] == "interface"

        next(flow for flow in hass.config_entries.flow.async_progress() if flow["flow_id"] == result["flow_id"])

        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            interface_data,
        )
        await hass.async_block_till_done()

        # Handle new menu step for finish_or_configure
        if result3["type"] == FlowResultType.MENU:
            assert result3["step_id"] == "finish_or_configure"
            # Select finish_setup to complete the flow
            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {"next_step_id": "finish_setup"},
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.CREATE_ENTRY
        assert result3["handler"] == HMIP_DOMAIN
        assert result3["title"] == const.INSTANCE_NAME
        data = result3["data"]
        assert data[CONF_INSTANCE_NAME] == const.INSTANCE_NAME
        assert data[CONF_HOST] == const.HOST
        assert data[CONF_USERNAME] == const.USERNAME
        assert data[CONF_PASSWORD] == const.PASSWORD
        return data


async def async_check_options_form(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    central_data: dict[str, Any] | None = None,
    interface_data: dict[str, Any] | None = None,
    port_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Test we get the form."""
    if central_data is None:
        central_data = {}

    if interface_data is None:
        interface_data = {}
    mock_config_entry.add_to_hass(hass)
    result = await hass.config_entries.options.async_init(mock_config_entry.entry_id)

    # Options flow now starts with a menu
    assert result["type"] == FlowResultType.MENU
    assert result["step_id"] == "init"

    with (
        patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ),
        patch(
            "custom_components.homematicip_local.async_setup_entry",
            return_value=True,
        ),
    ):
        # If interface_data is provided, go to interfaces step
        if interface_data:
            result2 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {"next_step_id": "interfaces"},
            )
            await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == const.CONFIG_ENTRY_ID
            assert result2["step_id"] == "interfaces"

            # Configure interfaces (TLS + interface checkboxes + custom_port_config)
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                interface_data,
            )
            await hass.async_block_till_done()

            # If port_data is provided and custom_port_config was set, we should be at port config step
            if port_data:
                assert result3["type"] == FlowResultType.FORM
                assert result3["step_id"] == "interfaces_port_config"

                # Configure ports
                result3 = await hass.config_entries.options.async_configure(
                    result["flow_id"],
                    port_data,
                )
                await hass.async_block_till_done()
        else:
            # Otherwise go to connection settings
            result2 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {"next_step_id": "connection"},
            )
            await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == const.CONFIG_ENTRY_ID
            assert result2["step_id"] == "connection"

            # Configure connection settings
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                central_data,
            )
            await hass.async_block_till_done()

    assert result3["type"] == FlowResultType.CREATE_ENTRY
    assert result3["handler"] == const.CONFIG_ENTRY_ID
    assert result3["title"] == ""
    return mock_config_entry.data


class TestConfigFlowForm:
    """Tests for basic configuration flow form."""

    async def test_form(self, hass: HomeAssistant) -> None:
        """Test we get the form with only HmIP-RF enabled."""
        interface_data = {CONF_ENABLE_HMIP_RF: True, CONF_ENABLE_BIDCOS_RF: False}
        data = await async_check_form(hass=hass, interface_data=interface_data)
        interface = data["interface"]
        assert interface[Interface.HMIP_RF][CONF_PORT] == 2010
        assert interface.get(Interface.BIDCOS_RF) is None
        assert interface.get(Interface.VIRTUAL_DEVICES) is None
        assert interface.get(Interface.BIDCOS_WIRED) is None

    async def test_form_https_redirect_enables_tls(self, hass: HomeAssistant) -> None:
        """Test that https_redirect_enabled=True enables TLS even when tls=False in detection."""
        # Detection result with tls=False but https_redirect_enabled=True
        detection_result = BackendDetectionResult(
            backend=Backend.CCU,
            available_interfaces=(Interface.HMIP_RF,),
            detected_port=2010,  # Non-TLS port
            tls=False,  # Connection was not TLS
            host=const.HOST,
            version="3.0.0",
            auth_enabled=True,
            https_redirect_enabled=True,  # But HTTPS redirect is enabled on CCU
        )
        # When https_redirect is enabled, the interface schema defaults TLS to True
        # User would see TLS pre-checked and submit with TLS=True
        interface_data = {
            CONF_ENABLE_HMIP_RF: True,
            CONF_TLS: True,  # https_redirect causes TLS to be enabled
            CONF_VERIFY_TLS: False,
            CONF_HMIP_RF_PORT: 42010,  # TLS port
        }
        data = await async_check_form(
            hass=hass, interface_data=interface_data, tls=True, detection_result=detection_result
        )
        # TLS should be enabled due to https_redirect_enabled=True
        assert data[CONF_TLS] is True
        # Interface port should be TLS port
        interface = data[CONF_INTERFACE]
        assert interface[Interface.HMIP_RF][CONF_PORT] == 42010

    async def test_form_no_hmip_only_bidcos(self, hass: HomeAssistant) -> None:
        """Test we get the form with only BidCos-RF enabled (default port)."""
        # Note: Custom ports are no longer configurable in the initial setup flow
        # Ports are automatically calculated from TLS setting
        interface_data = {CONF_ENABLE_HMIP_RF: False, CONF_ENABLE_BIDCOS_RF: True}
        data = await async_check_form(hass, interface_data=interface_data)
        interface = data["interface"]
        assert interface.get(Interface.HMIP_RF) is None
        if_bidcos_rf = interface[Interface.BIDCOS_RF]
        assert if_bidcos_rf[CONF_PORT] == IF_BIDCOS_RF_PORT  # Default non-TLS port
        assert interface.get(Interface.VIRTUAL_DEVICES) is None
        assert interface.get(Interface.BIDCOS_WIRED) is None

    async def test_form_only_hs485(self, hass: HomeAssistant) -> None:
        """Test we get the form with only BidCos-Wired enabled."""
        interface_data = {
            CONF_ENABLE_HMIP_RF: False,
            CONF_ENABLE_BIDCOS_RF: False,
            CONF_ENABLE_VIRTUAL_DEVICES: False,
            CONF_ENABLE_BIDCOS_WIRED: True,
        }
        data = await async_check_form(hass, interface_data=interface_data)
        interface = data["interface"]
        assert interface.get(Interface.HMIP_RF) is None
        assert interface.get(Interface.BIDCOS_RF) is None
        assert interface.get(Interface.VIRTUAL_DEVICES) is None
        assert interface[Interface.BIDCOS_WIRED][CONF_PORT] == 2000

    async def test_form_only_virtual(self, hass: HomeAssistant) -> None:
        """Test we get the form with only Virtual Devices enabled."""
        interface_data = {
            CONF_ENABLE_HMIP_RF: False,
            CONF_ENABLE_BIDCOS_RF: False,
            CONF_ENABLE_VIRTUAL_DEVICES: True,
            CONF_ENABLE_BIDCOS_WIRED: False,
        }
        data = await async_check_form(hass, interface_data=interface_data)
        interface = data["interface"]
        assert interface.get(Interface.HMIP_RF) is None
        assert interface.get(Interface.BIDCOS_RF) is None
        assert interface.get(Interface.BIDCOS_WIRED) is None
        assert interface[Interface.VIRTUAL_DEVICES][CONF_PORT] == 9292

    async def test_form_tls(self, hass: HomeAssistant) -> None:
        """Test we get the form with tls and only HmIP-RF enabled."""
        interface_data = {CONF_ENABLE_HMIP_RF: True, CONF_ENABLE_BIDCOS_RF: False}
        data = await async_check_form(hass=hass, interface_data=interface_data, tls=True)
        interface = data[CONF_INTERFACE]
        assert interface[Interface.HMIP_RF][CONF_PORT] == 42010
        assert interface.get(Interface.BIDCOS_RF) is None
        assert interface.get(Interface.VIRTUAL_DEVICES) is None
        assert interface.get(Interface.BIDCOS_WIRED) is None


class TestOptionsFlowForm:
    """Tests for options flow form."""

    async def test_options_form(self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry) -> None:
        """Test we get the form."""
        data = await async_check_options_form(hass, mock_config_entry=mock_config_entry_v2, interface_data={})
        interface = data["interface"]
        if_hmip_rf = interface[Interface.HMIP_RF]
        assert if_hmip_rf[CONF_PORT] == 2010
        if_bidcos_rf = interface[Interface.BIDCOS_RF]
        assert if_bidcos_rf[CONF_PORT] == 2001

        assert interface.get(Interface.VIRTUAL_DEVICES) is None
        assert interface.get(Interface.BIDCOS_WIRED) is None

    async def test_options_form_all_interfaces_enabled(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test we get the form."""
        mock_config_entry_v2.data["interface"][Interface.VIRTUAL_DEVICES] = {"port": 9292}
        mock_config_entry_v2.data["interface"][Interface.BIDCOS_WIRED] = {"port": 2000}
        mock_config_entry_v2.add_to_hass(hass)

        data = await async_check_options_form(hass, mock_config_entry_v2)
        interface = data["interface"]
        assert interface[Interface.BIDCOS_RF][CONF_PORT] == 2001
        assert interface[Interface.HMIP_RF][CONF_PORT] == 2010
        assert interface[Interface.BIDCOS_WIRED][CONF_PORT] == 2000
        assert interface[Interface.VIRTUAL_DEVICES][CONF_PORT] == 9292

    async def test_options_form_no_hmip_other_bidcos_port(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test we get the form with custom port configuration."""
        # Step 1: Interface selection with custom_port_config enabled
        interface_data = {
            CONF_ENABLE_HMIP_RF: False,
            CONF_ENABLE_BIDCOS_RF: True,
            CONF_TLS: False,
            CONF_VERIFY_TLS: False,
            CONF_CUSTOM_PORT_CONFIG: True,
        }
        # Step 2: Port configuration
        port_data = {CONF_BIDCOS_RF_PORT: 5555}
        data = await async_check_options_form(
            hass, mock_config_entry=mock_config_entry_v2, interface_data=interface_data, port_data=port_data
        )
        interface = data["interface"]
        assert interface.get(Interface.HMIP_RF) is None
        if_bidcos_rf = interface[Interface.BIDCOS_RF]
        assert if_bidcos_rf[CONF_PORT] == 5555
        assert interface.get(Interface.VIRTUAL_DEVICES) is None
        assert interface.get(Interface.BIDCOS_WIRED) is None


class TestConfigFlowErrorHandling:
    """Tests for configuration flow error handling."""

    async def test_form_cannot_connect(self, hass: HomeAssistant) -> None:
        """Test we handle cannot connect error."""
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] is None

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                return_value=_get_default_detection_result(),
            ),
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                new_callable=AsyncMock,
                side_effect=NoConnectionException("no host"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection (may complete immediately with mock)
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == HMIP_DOMAIN
            assert result2["step_id"] == "interface"

            next(flow for flow in hass.config_entries.flow.async_progress() if flow["flow_id"] == result["flow_id"])

            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {},
            )
            await hass.async_block_till_done()

            # Handle new menu step for finish_or_configure
            if result3["type"] == FlowResultType.MENU:
                assert result3["step_id"] == "finish_or_configure"
                result3 = await hass.config_entries.flow.async_configure(
                    result["flow_id"],
                    {"next_step_id": "finish_setup"},
                )
                await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["errors"] == {"base": "cannot_connect"}

    async def test_form_detection_auth_failure(self, hass: HomeAssistant) -> None:
        """Test we handle auth failure during backend detection."""
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] is None

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                side_effect=AuthFailure("invalid credentials"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

        # Should return to central step with auth error
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "central"
        assert result2["errors"] == {"base": "invalid_auth"}
        assert result2["description_placeholders"]["invalid_items"] == const.HOST

    async def test_form_detection_no_backend_found(self, hass: HomeAssistant) -> None:
        """Test we handle case when no backend is found (detection failed)."""
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] is None

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                return_value=None,  # No backend found
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

        # Should return to central step with detection_failed error
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "central"
        assert result2["errors"] == {"base": "detection_failed"}

    async def test_form_detection_no_connection(self, hass: HomeAssistant) -> None:
        """Test we handle connection exception during backend detection."""
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] is None

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                side_effect=NoConnectionException("Connection refused"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

        # Should return to central step with cannot_connect error
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "central"
        assert result2["errors"] == {"base": "cannot_connect"}

    async def test_form_detection_validation_exception(self, hass: HomeAssistant) -> None:
        """Test we handle validation exception during backend detection."""
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] is None

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                side_effect=ValidationException("invalid host format"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

        # Should return to central step with invalid_config error
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "central"
        assert result2["errors"] == {"base": "invalid_config"}

    async def test_form_invalid_auth(self, hass: HomeAssistant) -> None:
        """Test we handle invalid auth during final validation."""
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] is None

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                return_value=_get_default_detection_result(),
            ),
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                new_callable=AsyncMock,
                side_effect=AuthFailure("no pw"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection (may complete immediately with mock)
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == HMIP_DOMAIN
            assert result2["step_id"] == "interface"

            next(flow for flow in hass.config_entries.flow.async_progress() if flow["flow_id"] == result["flow_id"])

            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {},
            )
            await hass.async_block_till_done()

            # Handle new menu step for finish_or_configure
            if result3["type"] == FlowResultType.MENU:
                assert result3["step_id"] == "finish_or_configure"
                result3 = await hass.config_entries.flow.async_configure(
                    result["flow_id"],
                    {"next_step_id": "finish_setup"},
                )
                await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["errors"] == {"base": "invalid_auth"}

    async def test_form_invalid_password(self, hass: HomeAssistant) -> None:
        """Test we handle invalid config during final validation."""
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] is None

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                return_value=_get_default_detection_result(),
            ),
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                new_callable=AsyncMock,
                side_effect=InvalidConfig("wrong char"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.INVALID_PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection (may complete immediately with mock)
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == HMIP_DOMAIN
            assert result2["step_id"] == "interface"

            next(flow for flow in hass.config_entries.flow.async_progress() if flow["flow_id"] == result["flow_id"])

            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {},
            )
            await hass.async_block_till_done()

            # Handle new menu step for finish_or_configure
            if result3["type"] == FlowResultType.MENU:
                assert result3["step_id"] == "finish_or_configure"
                result3 = await hass.config_entries.flow.async_configure(
                    result["flow_id"],
                    {"next_step_id": "finish_setup"},
                )
                await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        # Note: With the new simplified flow, InvalidConfig shows port_config step
        # which uses "cannot_connect" as the base error
        assert result3["errors"] == {"base": "cannot_connect"}
        assert result3["step_id"] == "port_config"


class TestOptionsFlowErrorHandling:
    """Tests for options flow error handling."""

    async def test_options_form_cannot_connect(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test we handle cannot connect error."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        # Options flow now starts with a menu
        assert result["type"] == FlowResultType.MENU
        assert result["step_id"] == "init"

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                side_effect=NoConnectionException("no host"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            # Select connection from menu
            result2 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {"next_step_id": "connection"},
            )
            await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == const.CONFIG_ENTRY_ID
            assert result2["step_id"] == "connection"

            # Submit connection form - should fail with cannot_connect
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {},
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["errors"] == {"base": "cannot_connect"}

    async def test_options_form_invalid_auth(self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry) -> None:
        """Test we handle invalid auth."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        # Options flow now starts with a menu
        assert result["type"] == FlowResultType.MENU
        assert result["step_id"] == "init"

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                side_effect=AuthFailure("no pw"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            # Select connection from menu
            result2 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {"next_step_id": "connection"},
            )
            await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == const.CONFIG_ENTRY_ID
            assert result2["step_id"] == "connection"

            # Submit connection form - should fail with invalid_auth
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["errors"] == {"base": "invalid_auth"}

    async def test_options_form_invalid_password(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test we handle invalid auth."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        # Options flow now starts with a menu
        assert result["type"] == FlowResultType.MENU
        assert result["step_id"] == "init"

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                side_effect=InvalidConfig("wrong char"),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            # Select connection from menu
            result2 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {"next_step_id": "connection"},
            )
            await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == const.CONFIG_ENTRY_ID
            assert result2["step_id"] == "connection"

            # Submit connection form - should fail with invalid_config
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.INVALID_PASSWORD,
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["errors"] == {"base": "invalid_config"}


class TestDiscoveryFlow:
    """Tests for SSDP discovery flow."""

    async def test_flow_hassio_discovery(self, hass: HomeAssistant, discovery_info: ssdp.SsdpServiceInfo) -> None:
        """Test hassio discovery flow works."""

        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            data=discovery_info,
            context={"source": config_entries.SOURCE_SSDP},
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "central"
        # Now includes step indicators
        assert result["description_placeholders"]["step_current"] == "1"
        assert result["description_placeholders"]["step_total"] == "2"

        flows = hass.config_entries.flow.async_progress()
        assert len(flows) == 1
        assert flows[0].get("context", {}) == {
            "source": "ssdp",
            "title_placeholders": {"host": const.HOST, "name": const.INSTANCE_NAME},
            "unique_id": const.CONFIG_ENTRY_UNIQUE_ID,
        }

        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                return_value=_get_default_detection_result(),
            ),
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                new_callable=AsyncMock,
                return_value=SystemInformation(
                    available_interfaces=[],
                    auth_enabled=False,
                    https_redirect_enabled=False,
                    serial=const.SERIAL,
                ),
            ),
            patch(
                "custom_components.homematicip_local.async_setup_entry",
                return_value=True,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                user_input={
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection (may complete immediately with mock)
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["handler"] == HMIP_DOMAIN
            assert result2["step_id"] == "interface"

            next(flow for flow in hass.config_entries.flow.async_progress() if flow["flow_id"] == result["flow_id"])

            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {},
            )
            await hass.async_block_till_done()

            # Handle new menu step for finish_or_configure
            if result3["type"] == FlowResultType.MENU:
                assert result3["step_id"] == "finish_or_configure"
                result3 = await hass.config_entries.flow.async_configure(
                    result["flow_id"],
                    {"next_step_id": "finish_setup"},
                )
                await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.CREATE_ENTRY
        assert result3["handler"] == HMIP_DOMAIN
        assert result3["title"] == const.INSTANCE_NAME
        data = result3["data"]
        assert data[CONF_INSTANCE_NAME] == const.INSTANCE_NAME
        assert data[CONF_HOST] == const.HOST
        assert data[CONF_USERNAME] == const.USERNAME
        assert data[CONF_PASSWORD] == const.PASSWORD

    async def test_hassio_discovery_existing_configuration(
        self,
        hass: HomeAssistant,
        mock_config_entry_v2: MockConfigEntry,
        discovery_info: ssdp.SsdpServiceInfo,
    ) -> None:
        """Test abort on an existing config entry."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            data=discovery_info,
            context={"source": config_entries.SOURCE_SSDP},
        )
        assert result["type"] == FlowResultType.ABORT


class TestConfigFlowHelpers:
    """Tests for configuration flow helper functions."""

    async def test_async_validate_config_and_get_system_information(self, hass: HomeAssistant, entry_data_v5) -> None:
        """Test backend validation."""
        with patch(
            "custom_components.homematicip_local.config_flow.validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result = await _async_validate_config_and_get_system_information(
                hass=hass, data=entry_data_v5, entry_id="test"
            )
            assert result.serial == const.SERIAL

        entry_data_v5[CONF_PASSWORD] = const.INVALID_PASSWORD

        with pytest.raises(InvalidConfig) as exc:
            await _async_validate_config_and_get_system_information(hass=hass, data=entry_data_v5, entry_id="test")
        assert exc

    def test_config_flow_helper(self) -> None:
        """Test the config flow helper."""

        assert _get_instance_name(None) is None
        assert _get_instance_name("0123456789") == "0123456789"
        assert _get_instance_name("OpenCCU - test") == "test"
        assert _get_instance_name("OpenCCU 0123456789") == "0123456789"
        assert _get_serial(None) is None
        assert _get_serial("1234") is None
        assert _get_serial(f"9876543210{const.SERIAL}") == const.SERIAL

    def test_get_advanced_schema_with_and_without_un_ignores(self) -> None:
        """Ensure advanced schema handles UN_IGNORES presence based on candidates list."""
        data: dict[str, Any] = {CONST_ADVANCED_CONFIG: {}}

        # When there are no candidates, the field is removed
        schema_no = get_advanced_schema(data=data, all_un_ignore_parameters=[])
        assert CONF_UN_IGNORES not in schema_no.schema

        # When candidates exist, the field is present and defaults filtered to existing only
        candidates = ["A", "B", "C"]
        # Pre-populate advanced config with default un-ignores that include invalid entries
        data_with = {CONST_ADVANCED_CONFIG: {CONF_UN_IGNORES: ["A", "X", "C"]}}
        schema_yes = get_advanced_schema(data=data_with, all_un_ignore_parameters=candidates)
        assert CONF_UN_IGNORES in schema_yes.schema

    def test_get_ccu_data_optional_fields(self) -> None:
        """Verify optional fields handling and whitespace trimming in _get_ccu_data."""
        # Note: TLS and json_port are now in interface step, not central step
        base: dict[str, Any] = {
            CONF_INTERFACE: {},
            CONST_ADVANCED_CONFIG: {},
            CONF_TLS: False,  # Preserved from data
            CONF_VERIFY_TLS: False,  # Preserved from data
        }
        user_input = {
            CONF_HOST: "1.2.3.4",
            CONF_USERNAME: "user",
            CONF_PASSWORD: "pass",
            CONF_CALLBACK_HOST: " ",  # should be ignored
            CONF_CALLBACK_PORT_XML_RPC: 0,  # 0 is allowed by schema optional selector
        }
        data = _get_ccu_data(data=base, user_input=user_input)
        # callback_host ignored because of whitespace only
        assert CONF_CALLBACK_HOST not in data
        # optional numeric ports are set when provided
        assert data[CONF_CALLBACK_PORT_XML_RPC] == 0
        # TLS is preserved from data (not from user_input in central step)
        assert data[CONF_TLS] is False
        assert data[CONF_VERIFY_TLS] is False

    def test_get_ccu_data_sets_callback_host(self) -> None:
        """Confirm non-empty callback host is kept in _get_ccu_data."""
        # TLS is now preserved from data (set in interface step)
        base: dict[str, Any] = {
            CONF_INTERFACE: {},
            CONST_ADVANCED_CONFIG: {},
            CONF_TLS: False,
            CONF_VERIFY_TLS: False,
        }
        user_input = {
            CONF_HOST: "1.2.3.4",
            CONF_USERNAME: "user",
            CONF_PASSWORD: "pass",
            CONF_CALLBACK_HOST: "5.6.7.8",
        }
        data = _get_ccu_data(data=base, user_input=user_input)
        assert data[CONF_CALLBACK_HOST] == "5.6.7.8"

    def test_get_interface_schema_no_advanced_config(self) -> None:
        """Ensure get_interface_schema does not include advanced_config checkbox."""
        data = {CONF_TLS: False, CONF_INTERFACE: {}}
        schema = get_interface_schema(use_tls=False, data=data)
        assert CONF_ADVANCED_CONFIG not in schema.schema

    def test_update_advanced_input_empty_dict_noop(self) -> None:
        """Ensure empty advanced_input causes no changes (early return)."""
        data: dict[str, Any] = {CONST_ADVANCED_CONFIG: {}}
        _update_advanced_input(data=data, advanced_input={})
        assert data == {CONST_ADVANCED_CONFIG: {}}

    def test_update_advanced_input_with_un_ignores(self) -> None:
        """Ensure _update_advanced_input copies all fields including optional UN_IGNORES."""
        data: dict[str, Any] = {}
        adv_input_for_helper = {
            CONF_PROGRAM_MARKERS: ["marker1"],
            CONF_ENABLE_PROGRAM_SCAN: True,
            CONF_SYSVAR_MARKERS: ["ANY"],
            CONF_ENABLE_SYSVAR_SCAN: True,
            CONF_SYS_SCAN_INTERVAL: 30,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: True,
            CONF_LISTEN_ON_ALL_IP: True,
            CONF_ENABLE_MQTT: DEFAULT_ENABLE_MQTT,
            CONF_MQTT_PREFIX: "hmip",
            CONF_ENABLE_SUB_DEVICES: True,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: True,
            CONF_OPTIONAL_SETTINGS: ["no_wakeup"],
            CONF_UN_IGNORES: ["A", "B"],
        }
        _update_advanced_input(data=data, advanced_input=adv_input_for_helper)

        assert data[CONST_ADVANCED_CONFIG][CONF_PROGRAM_MARKERS] == adv_input_for_helper[CONF_PROGRAM_MARKERS]
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_PROGRAM_SCAN] is True
        assert data[CONST_ADVANCED_CONFIG][CONF_SYSVAR_MARKERS] == adv_input_for_helper[CONF_SYSVAR_MARKERS]
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_SYSVAR_SCAN] is True
        assert data[CONST_ADVANCED_CONFIG][CONF_SYS_SCAN_INTERVAL] == 30
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_SYSTEM_NOTIFICATIONS] is True
        assert data[CONST_ADVANCED_CONFIG][CONF_LISTEN_ON_ALL_IP] is True
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_MQTT] == DEFAULT_ENABLE_MQTT
        assert data[CONST_ADVANCED_CONFIG][CONF_MQTT_PREFIX] == "hmip"
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_SUB_DEVICES] is True
        assert data[CONST_ADVANCED_CONFIG][CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE] is True
        assert data[CONST_ADVANCED_CONFIG][CONF_OPTIONAL_SETTINGS] == adv_input_for_helper[CONF_OPTIONAL_SETTINGS]
        assert data[CONST_ADVANCED_CONFIG][CONF_UN_IGNORES] == ["A", "B"]

    def test_update_interface_input_all_paths(self) -> None:
        """Verify interface flags update correctly."""
        data: dict[str, Any] = {CONST_ADVANCED_CONFIG: {"dummy": True}}
        interface_input = {
            # TLS settings (now in interface step)
            CONF_TLS: False,
            CONF_VERIFY_TLS: False,
            # all interface toggles enabled
            CONF_ENABLE_HMIP_RF: True,
            CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
            CONF_ENABLE_BIDCOS_RF: True,
            CONF_BIDCOS_RF_PORT: IF_BIDCOS_RF_PORT,
            CONF_ENABLE_VIRTUAL_DEVICES: True,
            CONF_VIRTUAL_DEVICES_PORT: IF_VIRTUAL_DEVICES_PORT,
            CONF_VIRTUAL_DEVICES_PATH: IF_VIRTUAL_DEVICES_PATH,
            CONF_ENABLE_BIDCOS_WIRED: True,
            CONF_BIDCOS_WIRED_PORT: IF_BIDCOS_WIRED_PORT,
            CONF_ENABLE_CCU_JACK: True,
            CONF_ENABLE_CUXD: True,
        }
        _update_interface_input(data=data, interface_input=interface_input)
        # Verify TLS settings are set
        assert data[CONF_TLS] is False
        assert data[CONF_VERIFY_TLS] is False
        # Verify all interfaces created
        assert data[CONF_INTERFACE]["HmIP-RF"][CONF_PORT] == IF_HMIP_RF_PORT
        assert data[CONF_INTERFACE]["BidCos-RF"][CONF_PORT] == IF_BIDCOS_RF_PORT
        assert data[CONF_INTERFACE]["VirtualDevices"][CONF_PORT] == IF_VIRTUAL_DEVICES_PORT
        assert data[CONF_INTERFACE]["VirtualDevices"][CONF_PATH] == IF_VIRTUAL_DEVICES_PATH
        assert data[CONF_INTERFACE]["BidCos-Wired"][CONF_PORT] == IF_BIDCOS_WIRED_PORT
        assert "CCU-Jack" in data[CONF_INTERFACE]
        assert "CUxD" in data[CONF_INTERFACE]
        # advanced config is preserved (not reset by interface step)
        assert data[CONST_ADVANCED_CONFIG] == {"dummy": True}

        # Verify graceful handling when interface_input is empty
        before = dict(data)
        _update_interface_input(data=data, interface_input={})
        assert data == before


class TestAdvancedConfigurationFlow:
    """Tests for advanced configuration flow."""

    @pytest.mark.asyncio
    async def test_config_flow_advanced_path_and_submit(self, hass: HomeAssistant) -> None:
        """Drive user flow into advanced step and submit advanced settings."""
        # Start flow
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        # Submit central step
        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                return_value=_get_default_detection_result(),
            ),
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                new_callable=AsyncMock,
                return_value=SystemInformation(
                    available_interfaces=[],
                    auth_enabled=False,
                    https_redirect_enabled=False,
                    serial=const.SERIAL,
                ),
            ),
        ):
            # Central step: no TLS (moved to interface step)
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    "instance_name": const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step for backend detection (may complete immediately with mock)
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "interface"

        # Submit interface step - simplified: TLS + interface enables only, no ports
        # (ports are automatically calculated from TLS setting)
        interface_input = {
            CONF_TLS: False,
            CONF_VERIFY_TLS: False,
            CONF_ENABLE_HMIP_RF: False,
            CONF_ENABLE_BIDCOS_RF: False,
            CONF_ENABLE_VIRTUAL_DEVICES: False,
            CONF_ENABLE_BIDCOS_WIRED: False,
            CONF_ENABLE_CCU_JACK: False,
            CONF_ENABLE_CUXD: False,
        }
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            new_callable=AsyncMock,
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result3 = await hass.config_entries.flow.async_configure(result["flow_id"], interface_input)
        assert result3["type"] == FlowResultType.MENU
        assert result3["step_id"] == "finish_or_configure"

        # Select "configure_advanced" from menu to go to advanced step
        result3a = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"next_step_id": "configure_advanced"}
        )
        assert result3a["type"] == FlowResultType.FORM
        assert result3a["step_id"] == "advanced"

        # Submit advanced step and finish
        advanced_input = {
            CONF_ENABLE_PROGRAM_SCAN: True,
            CONF_PROGRAM_MARKERS: [],
            CONF_ENABLE_SYSVAR_SCAN: True,
            CONF_SYSVAR_MARKERS: [],
            CONF_SYS_SCAN_INTERVAL: 30,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: True,
            CONF_LISTEN_ON_ALL_IP: False,
            CONF_ENABLE_MQTT: False,
            CONF_MQTT_PREFIX: "hmip",
            CONF_ENABLE_SUB_DEVICES: True,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
        }
        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                return_value=SystemInformation(
                    available_interfaces=[],
                    auth_enabled=False,
                    https_redirect_enabled=False,
                    serial=const.SERIAL,
                ),
            ),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            result4 = await hass.config_entries.flow.async_configure(result["flow_id"], advanced_input)
            await hass.async_block_till_done()
        assert result4["type"] == FlowResultType.CREATE_ENTRY

    @pytest.mark.asyncio
    async def test_options_flow_advanced_path_and_submit(self, hass: HomeAssistant) -> None:
        """Cover options flow advanced branch including form display and submit."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            data={
                "instance_name": const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {},
                CONST_ADVANCED_CONFIG: {},
            },
        )

        # Provide minimal runtime_data with required method for advanced schema
        class _DummyCentral:
            def get_un_ignore_candidates(self, include_master: bool) -> list[str]:  # noqa: ARG002
                return ["X", "Y"]

        class _DummyControlUnit:
            central = _DummyCentral()

        entry.runtime_data = _DummyControlUnit()
        entry.add_to_hass(hass)

        result = await hass.config_entries.options.async_init(entry.entry_id)
        # Options flow now starts with a menu
        assert result["type"] == FlowResultType.MENU
        assert result["step_id"] == "init"

        # Select advanced_settings from menu to test the advanced path
        result2 = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "advanced_settings"},
        )
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "advanced_settings"

        # advanced_settings step does NOT include program/sysvar fields (those are in programs_sysvars step)
        advanced_input = {
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: True,
            CONF_LISTEN_ON_ALL_IP: False,
            CONF_ENABLE_MQTT: False,
            CONF_MQTT_PREFIX: "hmip",
            CONF_ENABLE_SUB_DEVICES: True,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_UN_IGNORES: [],  # UN-IGNORE field
        }
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result3 = await hass.config_entries.options.async_configure(result["flow_id"], advanced_input)
            await hass.async_block_till_done()
        assert result3["type"] == FlowResultType.CREATE_ENTRY


class TestReconfigureFlow:
    """Test the reconfigure flow (two-step: connection + interface with automatic ports)."""

    async def test_reconfigure_preserves_custom_ports(self, hass: HomeAssistant) -> None:
        """Test that reconfigure preserves custom ports when using custom_port_config."""
        custom_port = 12345
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            data={
                "instance_name": const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {
                    Interface.HMIP_RF: {CONF_PORT: custom_port},  # Custom port
                    Interface.BIDCOS_RF: {CONF_PORT: IF_BIDCOS_RF_PORT},  # Standard port
                },
                CONST_ADVANCED_CONFIG: {},
            },
        )
        entry.add_to_hass(hass)

        # Step 1: Connection
        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": entry.entry_id},
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
            },
        )
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "reconfigure_interface"

        # Step 2: Enable TLS with custom_port_config to access port configuration
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_TLS: True,  # Enable TLS
                CONF_VERIFY_TLS: False,
                CONF_ENABLE_HMIP_RF: True,
                CONF_ENABLE_BIDCOS_RF: True,
                CONF_ENABLE_VIRTUAL_DEVICES: False,
                CONF_ENABLE_BIDCOS_WIRED: False,
                CONF_ENABLE_CCU_JACK: False,
                CONF_ENABLE_CUXD: False,
                CONF_CUSTOM_PORT_CONFIG: True,  # Request custom port configuration
            },
        )

        # Should proceed to port_config step
        assert result3["type"] == FlowResultType.FORM
        assert result3["step_id"] == "reconfigure_port_config"

        # Step 3: Configure custom ports
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result4 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_JSON_PORT: 0,
                    CONF_HMIP_RF_PORT: custom_port,  # Keep custom port
                    CONF_BIDCOS_RF_PORT: IF_BIDCOS_RF_TLS_PORT,  # Update to TLS port
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.ABORT
        assert result4["reason"] == "reconfigure_successful"

        # Custom port should be preserved
        assert entry.data[CONF_INTERFACE][Interface.HMIP_RF][CONF_PORT] == custom_port
        # Standard port should be updated
        assert entry.data[CONF_INTERFACE][Interface.BIDCOS_RF][CONF_PORT] == IF_BIDCOS_RF_TLS_PORT

    async def test_reconfigure_two_step_flow(self, hass: HomeAssistant) -> None:
        """Test that reconfigure flow has two steps: connection and interface (automatic ports)."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            data={
                "instance_name": const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {
                    Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT},
                },
                CONST_ADVANCED_CONFIG: {},
            },
        )
        entry.add_to_hass(hass)

        # Step 1: Connection (host, username, password)
        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": entry.entry_id},
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reconfigure"

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
            },
        )

        # Step 2: Interface (TLS and interfaces - simplified, no ports)
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "reconfigure_interface"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: True,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    # No ports - they are calculated automatically based on TLS
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.ABORT
        assert result3["reason"] == "reconfigure_successful"

        # Port should be automatically set to TLS port
        assert entry.data[CONF_INTERFACE][Interface.HMIP_RF][CONF_PORT] == IF_HMIP_RF_TLS_PORT

    async def test_reconfigure_updates_ports_when_disabling_tls(self, hass: HomeAssistant) -> None:
        """Test that reconfigure updates ports automatically when disabling TLS."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            data={
                "instance_name": const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: True,
                CONF_VERIFY_TLS: True,
                CONF_INTERFACE: {
                    Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_TLS_PORT},
                    Interface.BIDCOS_RF: {CONF_PORT: IF_BIDCOS_RF_TLS_PORT},
                },
                CONST_ADVANCED_CONFIG: {},
            },
        )
        entry.add_to_hass(hass)

        # Step 1: Connection
        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": entry.entry_id},
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reconfigure"

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
            },
        )
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "reconfigure_interface"

        # Step 2: Disable TLS - ports are updated automatically
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,  # Disable TLS
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: True,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    # No ports - they are calculated automatically based on TLS
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.ABORT
        assert result3["reason"] == "reconfigure_successful"

        # Verify ports were automatically updated to non-TLS ports
        assert entry.data[CONF_INTERFACE][Interface.HMIP_RF][CONF_PORT] == IF_HMIP_RF_PORT
        assert entry.data[CONF_INTERFACE][Interface.BIDCOS_RF][CONF_PORT] == IF_BIDCOS_RF_PORT

    async def test_reconfigure_updates_ports_when_enabling_tls(self, hass: HomeAssistant) -> None:
        """Test that reconfigure updates ports automatically when enabling TLS."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            data={
                "instance_name": const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {
                    Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT},
                    Interface.BIDCOS_RF: {CONF_PORT: IF_BIDCOS_RF_PORT},
                },
                CONST_ADVANCED_CONFIG: {},
            },
        )
        entry.add_to_hass(hass)

        # Step 1: Connection
        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": entry.entry_id},
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reconfigure"

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
            },
        )
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "reconfigure_interface"

        # Step 2: Enable TLS - ports are updated automatically
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: True,  # Enable TLS
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: True,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    # No ports - they are calculated automatically based on TLS
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.ABORT
        assert result3["reason"] == "reconfigure_successful"

        # Verify ports were automatically updated to TLS ports
        assert entry.data[CONF_INTERFACE][Interface.HMIP_RF][CONF_PORT] == IF_HMIP_RF_TLS_PORT
        assert entry.data[CONF_INTERFACE][Interface.BIDCOS_RF][CONF_PORT] == IF_BIDCOS_RF_TLS_PORT


class TestPortConfigErrorHandling:
    """Tests for port configuration step error handling."""

    async def test_port_config_auth_failure(self, hass: HomeAssistant) -> None:
        """Test port config step handles auth failure."""
        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                return_value=_get_default_detection_result(),
            ),
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                new_callable=AsyncMock,
                side_effect=NoConnectionException("connection failed"),
            ),
        ):
            result = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )

            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

            assert result2["type"] == FlowResultType.FORM
            assert result2["step_id"] == "interface"

            # Submit interface with custom_port_config checked
            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: True,
                },
            )
            await hass.async_block_till_done()

        # Should show port config step
        assert result3["type"] == FlowResultType.FORM
        assert result3["step_id"] == "port_config"

        # Now test auth failure in port config step
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            new_callable=AsyncMock,
            side_effect=AuthFailure("invalid credentials"),
        ):
            result4 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_JSON_PORT: 80,
                    CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.FORM
        assert result4["step_id"] == "port_config"
        assert result4["errors"] == {"base": "invalid_auth"}

    async def test_port_config_invalid_config(self, hass: HomeAssistant) -> None:
        """Test port config step handles InvalidConfig exception."""
        with (
            patch(
                "custom_components.homematicip_local.config_flow._async_detect_backend",
                new_callable=AsyncMock,
                return_value=_get_default_detection_result(),
            ),
            patch(
                "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
                new_callable=AsyncMock,
                side_effect=NoConnectionException("connection failed"),
            ),
        ):
            result = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )

            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: True,
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["step_id"] == "port_config"

        # Test InvalidConfig exception
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            new_callable=AsyncMock,
            side_effect=InvalidConfig("invalid config value"),
        ):
            result4 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_JSON_PORT: 80,
                    CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.FORM
        assert result4["step_id"] == "port_config"
        assert result4["errors"] == {"base": "invalid_config"}


class TestOptionsFlowProgramsSysvars:
    """Tests for Options Flow programs and sysvars step."""

    async def test_options_programs_sysvars_auth_failure(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test programs_sysvars step handles auth failure."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "programs_sysvars"},
        )
        await hass.async_block_till_done()

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=AuthFailure("auth failed"),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_ENABLE_PROGRAM_SCAN: True,
                    CONF_PROGRAM_MARKERS: [],
                    CONF_ENABLE_SYSVAR_SCAN: True,
                    CONF_SYSVAR_MARKERS: [],
                    CONF_SYS_SCAN_INTERVAL: 30,
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["errors"] == {"base": "invalid_auth"}

    async def test_options_programs_sysvars_success(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test programs_sysvars step saves settings correctly."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        assert result["type"] == FlowResultType.MENU
        assert result["step_id"] == "init"

        # Select programs_sysvars from menu
        result2 = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "programs_sysvars"},
        )
        await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "programs_sysvars"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_ENABLE_PROGRAM_SCAN: True,
                    CONF_PROGRAM_MARKERS: ["HX"],
                    CONF_ENABLE_SYSVAR_SCAN: True,
                    CONF_SYSVAR_MARKERS: ["HAHM", "MQTT"],
                    CONF_SYS_SCAN_INTERVAL: 60,
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.CREATE_ENTRY
        # Verify settings were saved
        advanced_config = mock_config_entry_v2.data.get(CONST_ADVANCED_CONFIG, {})
        assert advanced_config.get(CONF_ENABLE_PROGRAM_SCAN) is True
        assert advanced_config.get(CONF_ENABLE_SYSVAR_SCAN) is True


class TestOptionsFlowInterfacesPortConfig:
    """Tests for Options Flow interfaces port config step."""

    async def test_options_interfaces_port_config_auth_failure(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test interfaces_port_config step handles auth failure."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        assert result["type"] == FlowResultType.MENU

        # Select interfaces from menu
        result2 = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "interfaces"},
        )
        await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "interfaces"

        # Enable custom port config to go to port config step
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=NoConnectionException("connection failed"),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: True,
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["step_id"] == "interfaces_port_config"

        # Now test auth failure in port config
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=AuthFailure("auth failed"),
        ):
            result4 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_JSON_PORT: 80,
                    CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.FORM
        assert result4["step_id"] == "interfaces_port_config"
        assert result4["errors"] == {"base": "invalid_auth"}

    async def test_options_interfaces_port_config_invalid_config(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test interfaces_port_config step handles InvalidConfig exception."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "interfaces"},
        )
        await hass.async_block_till_done()

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=NoConnectionException("connection failed"),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: True,
                },
            )
            await hass.async_block_till_done()

        assert result3["step_id"] == "interfaces_port_config"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=InvalidConfig("invalid config"),
        ):
            result4 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_JSON_PORT: 80,
                    CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.FORM
        assert result4["errors"] == {"base": "invalid_config"}


class TestReconfigurePortConfigErrors:
    """Tests for reconfigure port config error handling."""

    async def test_reconfigure_port_config_auth_failure(self, hass: HomeAssistant) -> None:
        """Test reconfigure port config handles auth failure."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            data={
                "instance_name": const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {
                    Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT},
                },
                CONST_ADVANCED_CONFIG: {},
            },
        )
        entry.add_to_hass(hass)

        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": entry.entry_id},
        )

        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
            },
        )

        # Enable custom port config
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=NoConnectionException("connection failed"),
        ):
            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: True,
                },
            )
            await hass.async_block_till_done()

        assert result3["step_id"] == "reconfigure_port_config"

        # Test auth failure
        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=AuthFailure("auth failed"),
        ):
            result4 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_JSON_PORT: 80,
                    CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.FORM
        assert result4["errors"] == {"base": "invalid_auth"}

    async def test_reconfigure_port_config_invalid_config(self, hass: HomeAssistant) -> None:
        """Test reconfigure port config handles InvalidConfig exception."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            data={
                "instance_name": const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {
                    Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT},
                },
                CONST_ADVANCED_CONFIG: {},
            },
        )
        entry.add_to_hass(hass)

        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": entry.entry_id},
        )

        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
            },
        )

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=NoConnectionException("connection failed"),
        ):
            await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: True,
                },
            )
            await hass.async_block_till_done()

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=InvalidConfig("invalid config"),
        ):
            result4 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_JSON_PORT: 80,
                    CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.FORM
        assert result4["errors"] == {"base": "invalid_config"}


class TestCustomPortHandling:
    """Tests for custom port handling functions."""

    def test_get_effective_json_port_with_custom_port(self) -> None:
        """Test _get_effective_json_port returns custom port."""
        from custom_components.homematicip_local.config_flow import _get_effective_json_port

        data = {
            CONF_JSON_PORT: 8080,  # Non-default port
        }

        result = _get_effective_json_port(tls=False, data=data)
        assert result == 8080

    def test_get_effective_port_with_custom_ports(self) -> None:
        """Test _get_effective_port returns custom port from CONF_CUSTOM_PORTS."""
        from custom_components.homematicip_local.config_flow import _get_effective_port
        from custom_components.homematicip_local.const import CONF_CUSTOM_PORTS

        data = {
            CONF_CUSTOM_PORTS: {
                Interface.HMIP_RF.value: 12345,
            },
            CONF_INTERFACE: {},
        }

        result = _get_effective_port(Interface.HMIP_RF, tls=False, data=data)
        assert result == 12345

    def test_get_effective_port_with_legacy_format(self) -> None:
        """Test _get_effective_port returns custom port from legacy interface format."""
        from custom_components.homematicip_local.config_flow import _get_effective_port

        # Use a non-default port to ensure it's returned
        custom_port = 12345
        data = {
            CONF_INTERFACE: {
                Interface.HMIP_RF: {CONF_PORT: custom_port},
            },
        }

        result = _get_effective_port(Interface.HMIP_RF, tls=False, data=data)
        assert result == custom_port


class TestBackendDetectionErrors:
    """Tests for backend detection error handling."""

    async def test_detection_base_homematic_exception(self, hass: HomeAssistant) -> None:
        """Test detection handles BaseHomematicException."""
        from aiohomematic.exceptions import BaseHomematicException

        with patch(
            "custom_components.homematicip_local.config_flow._async_detect_backend",
            new_callable=AsyncMock,
            side_effect=BaseHomematicException("generic error"),
        ):
            result = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )

            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "central"
        assert result2["errors"] == {"base": "cannot_connect"}

    async def test_detection_validation_exception(self, hass: HomeAssistant) -> None:
        """Test detection handles ValidationException."""
        with patch(
            "custom_components.homematicip_local.config_flow._async_detect_backend",
            new_callable=AsyncMock,
            side_effect=ValidationException("validation error"),
        ):
            result = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )

            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                    CONF_HOST: const.HOST,
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )
            await hass.async_block_till_done()

            # Handle progress step
            while result2["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
                await hass.async_block_till_done()
                result2 = await hass.config_entries.flow.async_configure(result["flow_id"])
                await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "central"
        assert result2["errors"] == {"base": "invalid_config"}


class TestOptionsFlowInterfacesValidation:
    """Tests for Options Flow interfaces step validation without custom ports."""

    async def test_options_interfaces_no_custom_ports_auth_error(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test interfaces step shows auth error when not requesting custom ports."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "interfaces"},
        )
        await hass.async_block_till_done()

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=AuthFailure("auth failed"),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: False,
                },
            )
            await hass.async_block_till_done()

        # Should show auth error on the same step
        assert result3["type"] == FlowResultType.FORM
        assert result3["step_id"] == "interfaces"
        assert result3["errors"] == {"base": "invalid_auth"}

    async def test_options_interfaces_no_custom_ports_connection_error(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test interfaces step redirects to port_config on connection error when not requesting custom ports."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "interfaces"},
        )
        await hass.async_block_till_done()

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=NoConnectionException("cannot connect"),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: False,
                },
            )
            await hass.async_block_till_done()

        # Should redirect to port config step with validation error
        assert result3["type"] == FlowResultType.FORM
        assert result3["step_id"] == "interfaces_port_config"
        assert result3["errors"] == {"base": "cannot_connect"}

    async def test_options_interfaces_no_custom_ports_success(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test interfaces step succeeds when validation passes without custom ports."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "interfaces"},
        )
        await hass.async_block_till_done()

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=False,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_ENABLE_HMIP_RF: True,
                    CONF_ENABLE_BIDCOS_RF: False,
                    CONF_ENABLE_VIRTUAL_DEVICES: False,
                    CONF_ENABLE_BIDCOS_WIRED: False,
                    CONF_ENABLE_CCU_JACK: False,
                    CONF_ENABLE_CUXD: False,
                    CONF_CUSTOM_PORT_CONFIG: False,
                },
            )
            await hass.async_block_till_done()

        # Should complete successfully
        assert result3["type"] == FlowResultType.CREATE_ENTRY


class TestOptionsFlowProgramsSysvarsErrors:
    """Tests for Options Flow programs_sysvars step error handling."""

    async def test_options_programs_sysvars_base_exception(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test programs_sysvars step handles BaseHomematicException."""
        from aiohomematic.exceptions import BaseHomematicException

        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "programs_sysvars"},
        )
        await hass.async_block_till_done()

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=BaseHomematicException("generic error"),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_ENABLE_PROGRAM_SCAN: True,
                    CONF_PROGRAM_MARKERS: [],
                    CONF_ENABLE_SYSVAR_SCAN: True,
                    CONF_SYSVAR_MARKERS: [],
                    CONF_SYS_SCAN_INTERVAL: 30,
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["errors"] == {"base": "cannot_connect"}

    async def test_options_programs_sysvars_invalid_config(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test programs_sysvars step handles InvalidConfig."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "programs_sysvars"},
        )
        await hass.async_block_till_done()

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=InvalidConfig("config error"),
        ):
            result3 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_ENABLE_PROGRAM_SCAN: True,
                    CONF_PROGRAM_MARKERS: [],
                    CONF_ENABLE_SYSVAR_SCAN: True,
                    CONF_SYSVAR_MARKERS: [],
                    CONF_SYS_SCAN_INTERVAL: 30,
                },
            )
            await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["errors"] == {"base": "invalid_config"}


class TestOptionsFlowInterfacesPortConfigErrors:
    """Tests for Options Flow interfaces_port_config exception handling."""

    async def test_options_interfaces_port_config_base_exception(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test interfaces_port_config handles BaseHomematicException."""
        from aiohomematic.exceptions import BaseHomematicException

        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "interfaces"},
        )
        await hass.async_block_till_done()

        # Request custom port config
        result3 = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_ENABLE_HMIP_RF: True,
                CONF_ENABLE_BIDCOS_RF: False,
                CONF_ENABLE_VIRTUAL_DEVICES: False,
                CONF_ENABLE_BIDCOS_WIRED: False,
                CONF_ENABLE_CCU_JACK: False,
                CONF_ENABLE_CUXD: False,
                CONF_CUSTOM_PORT_CONFIG: True,
            },
        )
        await hass.async_block_till_done()

        assert result3["step_id"] == "interfaces_port_config"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=BaseHomematicException("generic error"),
        ):
            result4 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
                    CONF_JSON_PORT: 80,
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.FORM
        assert result4["errors"] == {"base": "cannot_connect"}

    async def test_options_interfaces_port_config_no_connection(
        self, hass: HomeAssistant, mock_config_entry_v2: MockConfigEntry
    ) -> None:
        """Test interfaces_port_config handles NoConnectionException."""
        mock_config_entry_v2.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(mock_config_entry_v2.entry_id)

        await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "interfaces"},
        )
        await hass.async_block_till_done()

        # Request custom port config
        result3 = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_ENABLE_HMIP_RF: True,
                CONF_ENABLE_BIDCOS_RF: False,
                CONF_ENABLE_VIRTUAL_DEVICES: False,
                CONF_ENABLE_BIDCOS_WIRED: False,
                CONF_ENABLE_CCU_JACK: False,
                CONF_ENABLE_CUXD: False,
                CONF_CUSTOM_PORT_CONFIG: True,
            },
        )
        await hass.async_block_till_done()

        assert result3["step_id"] == "interfaces_port_config"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            side_effect=NoConnectionException("cannot connect"),
        ):
            result4 = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
                    CONF_JSON_PORT: 80,
                },
            )
            await hass.async_block_till_done()

        assert result4["type"] == FlowResultType.FORM
        assert result4["errors"] == {"base": "cannot_connect"}


class TestHelperFunctions:
    """Tests for config flow helper functions."""

    def test_get_ccu_data_with_json_port(self) -> None:
        """Test _get_ccu_data includes JSON port when set."""
        data = {
            CONF_JSON_PORT: 8080,
        }
        user_input = {
            CONF_INSTANCE_NAME: const.INSTANCE_NAME,
            CONF_HOST: const.HOST,
            CONF_USERNAME: const.USERNAME,
            CONF_PASSWORD: const.PASSWORD,
        }

        ccu_data = _get_ccu_data(data, user_input)

        assert ccu_data[CONF_JSON_PORT] == 8080

    def test_update_advanced_input_removes_empty_callbacks(self) -> None:
        """Test _update_advanced_input removes empty callback settings."""
        from custom_components.homematicip_local.config_flow import _update_advanced_input

        data: dict[str, Any] = {
            CONF_CALLBACK_HOST: "old_host",
            CONF_CALLBACK_PORT_XML_RPC: 1234,
        }
        advanced_input = {
            CONF_LISTEN_ON_ALL_IP: True,
            CONF_PROGRAM_MARKERS: [],
            CONF_ENABLE_PROGRAM_SCAN: False,
            CONF_SYSVAR_MARKERS: [],
            CONF_ENABLE_SYSVAR_SCAN: False,
            CONF_SYS_SCAN_INTERVAL: 30,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: False,
            CONF_ENABLE_MQTT: DEFAULT_ENABLE_MQTT,
            CONF_MQTT_PREFIX: "",
            CONF_ENABLE_SUB_DEVICES: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
        }

        _update_advanced_input(data, advanced_input)

        assert CONF_CALLBACK_HOST not in data
        assert CONF_CALLBACK_PORT_XML_RPC not in data

    def test_update_advanced_input_with_callbacks(self) -> None:
        """Test _update_advanced_input handles callback settings."""
        from custom_components.homematicip_local.config_flow import _update_advanced_input

        data: dict[str, Any] = {}
        advanced_input = {
            CONF_CALLBACK_HOST: "192.168.1.100",
            CONF_CALLBACK_PORT_XML_RPC: 9292,
            CONF_LISTEN_ON_ALL_IP: True,
            CONF_PROGRAM_MARKERS: [],
            CONF_ENABLE_PROGRAM_SCAN: False,
            CONF_SYSVAR_MARKERS: [],
            CONF_ENABLE_SYSVAR_SCAN: False,
            CONF_SYS_SCAN_INTERVAL: 30,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: False,
            CONF_ENABLE_MQTT: DEFAULT_ENABLE_MQTT,
            CONF_MQTT_PREFIX: "",
            CONF_ENABLE_SUB_DEVICES: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
        }

        _update_advanced_input(data, advanced_input)

        assert data[CONF_CALLBACK_HOST] == "192.168.1.100"
        assert data[CONF_CALLBACK_PORT_XML_RPC] == 9292

    def test_update_advanced_settings_input_empty_returns_early(self) -> None:
        """Test _update_advanced_settings_input returns early with empty input."""
        from custom_components.homematicip_local.config_flow import _update_advanced_settings_input

        data: dict[str, Any] = {"key": "value"}
        _update_advanced_settings_input(data, {})
        assert data == {"key": "value"}

    def test_update_advanced_settings_input_removes_empty_callbacks(self) -> None:
        """Test _update_advanced_settings_input removes empty callback settings."""
        from custom_components.homematicip_local.config_flow import CONF_BACKUP_PATH, _update_advanced_settings_input

        data: dict[str, Any] = {
            CONF_CALLBACK_HOST: "old_host",
            CONF_CALLBACK_PORT_XML_RPC: 1234,
        }
        advanced_input = {
            CONF_LISTEN_ON_ALL_IP: True,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: False,
            CONF_ENABLE_MQTT: DEFAULT_ENABLE_MQTT,
            CONF_MQTT_PREFIX: "",
            CONF_ENABLE_SUB_DEVICES: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_BACKUP_PATH: "",
        }

        _update_advanced_settings_input(data, advanced_input)

        assert CONF_CALLBACK_HOST not in data
        assert CONF_CALLBACK_PORT_XML_RPC not in data

    def test_update_advanced_settings_input_with_callbacks(self) -> None:
        """Test _update_advanced_settings_input handles callback settings."""
        from custom_components.homematicip_local.config_flow import CONF_BACKUP_PATH, _update_advanced_settings_input

        data: dict[str, Any] = {}
        advanced_input = {
            CONF_CALLBACK_HOST: "192.168.1.100",
            CONF_CALLBACK_PORT_XML_RPC: 9292,
            CONF_LISTEN_ON_ALL_IP: True,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: False,
            CONF_ENABLE_MQTT: DEFAULT_ENABLE_MQTT,
            CONF_MQTT_PREFIX: "",
            CONF_ENABLE_SUB_DEVICES: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_BACKUP_PATH: "",
        }

        _update_advanced_settings_input(data, advanced_input)

        assert data[CONF_CALLBACK_HOST] == "192.168.1.100"
        assert data[CONF_CALLBACK_PORT_XML_RPC] == 9292

    def test_update_advanced_settings_input_with_un_ignores(self) -> None:
        """Test _update_advanced_settings_input handles un_ignores."""
        from custom_components.homematicip_local.config_flow import CONF_BACKUP_PATH, _update_advanced_settings_input

        data: dict[str, Any] = {}
        advanced_input = {
            CONF_LISTEN_ON_ALL_IP: True,
            CONF_ENABLE_SYSTEM_NOTIFICATIONS: False,
            CONF_ENABLE_MQTT: DEFAULT_ENABLE_MQTT,
            CONF_MQTT_PREFIX: "",
            CONF_ENABLE_SUB_DEVICES: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_BACKUP_PATH: "",
            CONF_UN_IGNORES: ["param1", "param2"],
        }

        _update_advanced_settings_input(data, advanced_input)

        assert data[CONST_ADVANCED_CONFIG][CONF_UN_IGNORES] == ["param1", "param2"]

    def test_update_interface_input_removes_json_port(self) -> None:
        """Test _update_interface_input removes JSON port when None."""
        from custom_components.homematicip_local.config_flow import _update_interface_input

        data: dict[str, Any] = {CONF_JSON_PORT: 8080}
        interface_input = {
            CONF_TLS: False,
            CONF_VERIFY_TLS: False,
            CONF_ENABLE_HMIP_RF: True,
            CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
            CONF_ENABLE_BIDCOS_RF: False,
            CONF_BIDCOS_RF_PORT: IF_BIDCOS_RF_PORT,
            CONF_ENABLE_VIRTUAL_DEVICES: False,
            CONF_VIRTUAL_DEVICES_PORT: IF_VIRTUAL_DEVICES_PORT,
            CONF_ENABLE_BIDCOS_WIRED: False,
            CONF_BIDCOS_WIRED_PORT: IF_BIDCOS_WIRED_PORT,
            CONF_ENABLE_CCU_JACK: False,
            CONF_ENABLE_CUXD: False,
        }

        _update_interface_input(data, interface_input)

        assert CONF_JSON_PORT not in data

    def test_update_interface_input_with_json_port(self) -> None:
        """Test _update_interface_input updates JSON port."""
        from custom_components.homematicip_local.config_flow import _update_interface_input

        data: dict[str, Any] = {}
        interface_input = {
            CONF_TLS: False,
            CONF_VERIFY_TLS: False,
            CONF_JSON_PORT: 8080,
            CONF_ENABLE_HMIP_RF: True,
            CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
            CONF_ENABLE_BIDCOS_RF: False,
            CONF_BIDCOS_RF_PORT: IF_BIDCOS_RF_PORT,
            CONF_ENABLE_VIRTUAL_DEVICES: False,
            CONF_VIRTUAL_DEVICES_PORT: IF_VIRTUAL_DEVICES_PORT,
            CONF_ENABLE_BIDCOS_WIRED: False,
            CONF_BIDCOS_WIRED_PORT: IF_BIDCOS_WIRED_PORT,
            CONF_ENABLE_CCU_JACK: False,
            CONF_ENABLE_CUXD: False,
        }

        _update_interface_input(data, interface_input)

        assert data[CONF_JSON_PORT] == 8080
        assert data[CONF_TLS] is False
        assert Interface.HMIP_RF in data[CONF_INTERFACE]

    def test_update_port_config_input_clears_empty_custom_ports(self) -> None:
        """Test _update_port_config_input removes empty custom_ports dict."""
        from custom_components.homematicip_local.config_flow import _update_port_config_input

        data: dict[str, Any] = {
            CONF_TLS: False,
            CONF_INTERFACE: {Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT}},
            CONF_CUSTOM_PORTS: {},
        }
        port_input = {
            CONF_JSON_PORT: 80,
            CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
        }

        _update_port_config_input(data, port_input)

        # Empty custom_ports should be removed
        assert CONF_CUSTOM_PORTS not in data

    def test_update_port_config_input_custom_json_port(self) -> None:
        """Test _update_port_config_input handles custom JSON port."""
        from custom_components.homematicip_local.config_flow import _update_port_config_input

        data: dict[str, Any] = {
            CONF_TLS: False,
            CONF_INTERFACE: {Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT}},
        }
        port_input = {
            CONF_JSON_PORT: 8080,  # Non-default
            CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,
        }

        _update_port_config_input(data, port_input)

        assert data[CONF_JSON_PORT] == 8080

    def test_update_port_config_input_empty_returns_early(self) -> None:
        """Test _update_port_config_input returns early with empty input."""
        from custom_components.homematicip_local.config_flow import _update_port_config_input

        data: dict[str, Any] = {"key": "value"}
        _update_port_config_input(data, {})
        assert data == {"key": "value"}

    def test_update_port_config_input_removes_default_custom_port(self) -> None:
        """Test _update_port_config_input removes custom port when switching to default."""
        from custom_components.homematicip_local.config_flow import _update_port_config_input

        data: dict[str, Any] = {
            CONF_TLS: False,
            CONF_INTERFACE: {Interface.HMIP_RF: {CONF_PORT: 12345}},
            CONF_CUSTOM_PORTS: {Interface.HMIP_RF.value: 12345},
        }
        port_input = {
            CONF_JSON_PORT: 80,  # Default for non-TLS
            CONF_HMIP_RF_PORT: IF_HMIP_RF_PORT,  # Switch to default
        }

        _update_port_config_input(data, port_input)

        # Custom port should be removed
        assert Interface.HMIP_RF.value not in data.get(CONF_CUSTOM_PORTS, {})

    def test_update_port_config_input_virtual_devices_path(self) -> None:
        """Test _update_port_config_input handles VirtualDevices path."""
        from custom_components.homematicip_local.config_flow import _update_port_config_input

        data: dict[str, Any] = {
            CONF_TLS: False,
            CONF_INTERFACE: {Interface.VIRTUAL_DEVICES: {CONF_PORT: IF_VIRTUAL_DEVICES_PORT}},
        }
        port_input = {
            CONF_JSON_PORT: 80,
            CONF_VIRTUAL_DEVICES_PORT: IF_VIRTUAL_DEVICES_PORT,
            CONF_VIRTUAL_DEVICES_PATH: "/custom/path",
        }

        _update_port_config_input(data, port_input)

        assert data[CONF_INTERFACE][Interface.VIRTUAL_DEVICES][CONF_PATH] == "/custom/path"

    def test_update_tls_interfaces_input_empty_returns_early(self) -> None:
        """Test _update_tls_interfaces_input returns early with empty input."""
        from custom_components.homematicip_local.config_flow import _update_tls_interfaces_input

        data: dict[str, Any] = {"key": "value"}
        _update_tls_interfaces_input(data, {})
        assert data == {"key": "value"}

    def test_update_tls_interfaces_input_with_custom_port(self) -> None:
        """Test _update_tls_interfaces_input uses custom ports when available."""
        from custom_components.homematicip_local.config_flow import _update_tls_interfaces_input

        data: dict[str, Any] = {CONF_CUSTOM_PORTS: {Interface.HMIP_RF.value: 12345}}
        interface_input = {
            CONF_TLS: False,
            CONF_VERIFY_TLS: False,
            CONF_ENABLE_HMIP_RF: True,
            CONF_ENABLE_BIDCOS_RF: False,
            CONF_ENABLE_VIRTUAL_DEVICES: False,
            CONF_ENABLE_BIDCOS_WIRED: False,
            CONF_ENABLE_CCU_JACK: True,
            CONF_ENABLE_CUXD: True,
        }

        _update_tls_interfaces_input(data, interface_input)

        # HMIP_RF should use custom port
        assert data[CONF_INTERFACE][Interface.HMIP_RF][CONF_PORT] == 12345
        # CCU_JACK and CUXD should be added without port
        assert Interface.CCU_JACK in data[CONF_INTERFACE]
        assert Interface.CUXD in data[CONF_INTERFACE]


class TestReauthFlow:
    """Test the reauthentication flow."""

    async def test_reauth_flow_auth_failure(self, hass: HomeAssistant) -> None:
        """Test reauthentication flow with authentication failure."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id=const.SERIAL,
            data={
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT}},
            },
        )
        entry.add_to_hass(hass)

        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_REAUTH, "entry_id": entry.entry_id},
            data=entry.data,
        )

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reauth_confirm"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            new_callable=AsyncMock,
            side_effect=AuthFailure,
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_USERNAME: "wrong_username",
                    CONF_PASSWORD: "wrong_password",
                },
            )

        # Should show form again with error
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "reauth_confirm"
        assert result2["errors"] == {"base": "invalid_auth"}

    async def test_reauth_flow_connection_failure(self, hass: HomeAssistant) -> None:
        """Test reauthentication flow with connection failure."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id=const.SERIAL,
            data={
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT}},
            },
        )
        entry.add_to_hass(hass)

        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_REAUTH, "entry_id": entry.entry_id},
            data=entry.data,
        )

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reauth_confirm"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            new_callable=AsyncMock,
            side_effect=NoConnectionException,
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )

        # Should show form again with connection error
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "reauth_confirm"
        assert result2["errors"] == {"base": "cannot_connect"}

    async def test_reauth_flow_success(self, hass: HomeAssistant) -> None:
        """Test successful reauthentication flow."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id=const.SERIAL,
            data={
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT}},
            },
        )
        entry.add_to_hass(hass)

        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_REAUTH, "entry_id": entry.entry_id},
            data=entry.data,
        )

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reauth_confirm"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            new_callable=AsyncMock,
            return_value=SystemInformation(
                available_interfaces=[],
                auth_enabled=True,
                https_redirect_enabled=False,
                serial=const.SERIAL,
            ),
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_USERNAME: "new_username",
                    CONF_PASSWORD: "new_password",
                },
            )

        assert result2["type"] == FlowResultType.ABORT
        assert result2["reason"] == "reauth_successful"

        # Verify credentials were updated
        assert entry.data[CONF_USERNAME] == "new_username"
        assert entry.data[CONF_PASSWORD] == "new_password"

    async def test_reauth_flow_validation_failure(self, hass: HomeAssistant) -> None:
        """Test reauthentication flow with validation failure."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id=const.SERIAL,
            data={
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_INTERFACE: {Interface.HMIP_RF: {CONF_PORT: IF_HMIP_RF_PORT}},
            },
        )
        entry.add_to_hass(hass)

        result = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_REAUTH, "entry_id": entry.entry_id},
            data=entry.data,
        )

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reauth_confirm"

        with patch(
            "custom_components.homematicip_local.config_flow._async_validate_config_and_get_system_information",
            new_callable=AsyncMock,
            side_effect=ValidationException,
        ):
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_USERNAME: const.USERNAME,
                    CONF_PASSWORD: const.PASSWORD,
                },
            )

        # Should show form again with error
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "reauth_confirm"
        assert result2["errors"] == {"base": "invalid_config"}
