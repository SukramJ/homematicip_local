"""Test the Homematic(IP) Local for OpenCCU config flow."""

from __future__ import annotations

import asyncio
from collections.abc import Iterator
from ipaddress import ip_address
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry, flush_store

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
    CONF_LOOM_BASE_PATH,
    CONF_LOOM_DAEMON,
    CONF_LOOM_DEPLOY,
    CONF_VIRTUAL_DEVICES_PATH,
    CONF_VIRTUAL_DEVICES_PORT,
    IF_VIRTUAL_DEVICES_PATH,
    LOOM_MANUAL_DAEMON,
    ZEROCONF_TYPE,
    DomainConfigFlow,
    InvalidConfig,
    LoomLoginMode,
    LoomLoginOffer,
    _async_browse_loom_daemons,
    _async_loom_list_ccus,
    _async_validate_config_and_get_system_information,
    _get_ccu_data,
    _get_instance_name,
    _get_loom_data,
    _get_serial,
    _import_loom_list_ccus,
    _update_advanced_input,
    _update_interface_input,
    _update_loom_advanced_settings_input,
    get_advanced_schema,
    get_interface_schema,
    get_loom_advanced_settings_schema,
    get_loom_credentials_schema,
    get_loom_options_schema,
    get_loom_schema,
    get_loom_token_schema,
    loom_login_offer,
)
from custom_components.homematicip_local.const import (
    BACKEND_CCU,
    BACKEND_LOOM,
    CONF_ADVANCED_CONFIG as CONST_ADVANCED_CONFIG,
    CONF_BACKEND,
    CONF_CALLBACK_HOST,
    CONF_CALLBACK_PORT_XML_RPC,
    CONF_COMMAND_THROTTLE_INTERVAL,
    CONF_DISABLE_CONFIG_PANEL,
    CONF_ENABLE_LIGHT_LAST_BRIGHTNESS,
    CONF_ENABLE_MQTT,
    CONF_ENABLE_PROGRAM_SCAN,
    CONF_ENABLE_SUB_DEVICES,
    CONF_ENABLE_SYSTEM_NOTIFICATIONS,
    CONF_ENABLE_SYSVAR_SCAN,
    CONF_INTERFACE,
    CONF_JSON_PORT,
    CONF_LISTEN_ON_ALL_IP,
    CONF_LOOM_BOX,
    CONF_LOOM_BOX_PASSWORD,
    CONF_LOOM_BOX_TOKEN,
    CONF_LOOM_BOX_USERNAME,
    CONF_LOOM_PAIR,
    CONF_LOOM_PORT,
    CONF_LOOM_TOKEN,
    CONF_MQTT_PREFIX,
    CONF_OPTIONAL_SETTINGS,
    CONF_PROGRAM_MARKERS,
    CONF_SYS_SCAN_INTERVAL,
    CONF_SYSVAR_MARKERS,
    CONF_TLS,
    CONF_UN_IGNORES,
    CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE,
    CONF_VERIFY_TLS,
    DEFAULT_COMMAND_THROTTLE_INTERVAL,
    DEFAULT_DISABLE_CONFIG_PANEL,
    DEFAULT_ENABLE_MQTT,
    DOMAIN as HMIP_DOMAIN,
)
from homeassistant import config_entries
from homeassistant.components import ssdp
from homeassistant.const import CONF_HOST, CONF_PATH, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo

from tests import const

# Port constants using helper function (must be after imports)
IF_HMIP_RF_PORT = get_interface_default_port(interface=Interface.HMIP_RF, tls=False)
IF_HMIP_RF_TLS_PORT = get_interface_default_port(interface=Interface.HMIP_RF, tls=True)
IF_BIDCOS_RF_PORT = get_interface_default_port(interface=Interface.BIDCOS_RF, tls=False)
IF_BIDCOS_RF_TLS_PORT = get_interface_default_port(interface=Interface.BIDCOS_RF, tls=True)
IF_BIDCOS_WIRED_PORT = get_interface_default_port(interface=Interface.BIDCOS_WIRED, tls=False)
IF_VIRTUAL_DEVICES_PORT = get_interface_default_port(interface=Interface.VIRTUAL_DEVICES, tls=False)

_PROBE = "openccu_loom_client.probe_daemon"


def _daemon_probe(*, kind: str | None = None, paths: frozenset[str] = frozenset()) -> Any:
    """Return the probe answer of a daemon describing itself with ``kind`` and ``paths``."""
    from openccu_loom_client import DaemonProbe, ProbeOutcome

    # A daemon older than API 13.5 sends no deployment and no login paths.
    api_version = "13.5.0" if kind is not None or paths else "13.4.0"
    return DaemonProbe(reached=ProbeOutcome.DAEMON, api_version=api_version, deployment_kind=kind, login_paths=paths)


def _box_gate_probe() -> Any:
    """Return the probe answer of an openccu-lite box's gate."""
    from openccu_loom_client import DaemonProbe, ProbeOutcome

    return DaemonProbe(reached=ProbeOutcome.BOX_GATE)


def _probe_unreachable() -> Exception:
    """Return the error the probe raises when nothing usable answered."""
    from openccu_loom_client import LoomTransportError

    return LoomTransportError("connection refused")


@pytest.fixture(autouse=True)
def _legacy_loom_probe() -> Iterator[AsyncMock]:
    """Answer every loom probe as a daemon older than 0.86 unless a test patches its own.

    The loom flow asks the daemon what it offers before it shows credential
    fields; without a stand-in each loom flow test would reach for the
    network. A daemon that does not describe itself gets today's full field
    set, so tests that do not care about the offer drive the unchanged form.
    """
    with patch(_PROBE, AsyncMock(return_value=_daemon_probe())) as probe:
        yield probe


def _get_default_detection_result(
    tls: bool = False,
    interfaces: tuple[Interface, ...] | None = None,
) -> BackendDetectionResult:
    """Return a default detection result for tests."""
    return BackendDetectionResult(
        backend=Backend.CCU,
        available_interfaces=interfaces or (Interface.HMIP_RF, Interface.BIDCOS_RF),
        detected_port=2010 if not tls else 42010,
        tls=tls,
        host=const.HOST,
        version="3.0.0",
        auth_enabled=True,
        https_redirect_enabled=False,
    )


async def _async_init_user_flow_at_central(hass: HomeAssistant) -> Any:
    """Start a user flow and reach the central form.

    Robust against the loom backend gate: when the loom backend is
    relevant the user step shows a backend menu (navigate to ``central``);
    otherwise the user step skips straight to the central form.
    """
    result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
    if result["type"] == FlowResultType.MENU:
        result = await hass.config_entries.flow.async_configure(result["flow_id"], {"next_step_id": "central"})
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "central"
    return result


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
        result = await _async_init_user_flow_at_central(hass)
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
        # Include BidCos-Wired in detection result so it's considered available
        detection_result = _get_default_detection_result(interfaces=(Interface.BIDCOS_WIRED,))
        data = await async_check_form(hass, interface_data=interface_data, detection_result=detection_result)
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
        # Include VirtualDevices in detection result so it's considered available
        detection_result = _get_default_detection_result(interfaces=(Interface.VIRTUAL_DEVICES,))
        data = await async_check_form(hass, interface_data=interface_data, detection_result=detection_result)
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
        result = await _async_init_user_flow_at_central(hass)
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
        result = await _async_init_user_flow_at_central(hass)
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

        # Should proceed to interface step with graceful degradation
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "interface"
        # No errors shown on interface page - user can manually configure

    async def test_form_detection_no_backend_found(self, hass: HomeAssistant) -> None:
        """Test we handle case when no backend is found (detection failed)."""
        result = await _async_init_user_flow_at_central(hass)
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

        # Should proceed to interface step with graceful degradation
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "interface"
        # No errors shown - user can manually configure

    async def test_form_detection_no_connection(self, hass: HomeAssistant) -> None:
        """Test we handle connection exception during backend detection."""
        result = await _async_init_user_flow_at_central(hass)
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

        # Should proceed to interface step with graceful degradation
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "interface"
        # No errors shown - user can manually configure

    async def test_form_detection_validation_exception(self, hass: HomeAssistant) -> None:
        """Test we handle validation exception during backend detection."""
        result = await _async_init_user_flow_at_central(hass)
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

        # Should proceed to interface step with graceful degradation
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "interface"
        # No errors shown - user can manually configure

    async def test_form_invalid_auth(self, hass: HomeAssistant) -> None:
        """Test we handle invalid auth during final validation."""
        result = await _async_init_user_flow_at_central(hass)
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
        result = await _async_init_user_flow_at_central(hass)
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
        # Note: Validation errors now stay on interface page so user can disable
        # problematic interfaces (e.g., CUxD not running)
        assert result3["errors"] == {"base": "cannot_connect"}
        assert result3["step_id"] == "interface"


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
            "title_placeholders": {
                "host": const.HOST,
                "name": const.INSTANCE_NAME,
                "backend": "aiohomematic",
            },
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
            CONF_DISABLE_CONFIG_PANEL: DEFAULT_DISABLE_CONFIG_PANEL,
            CONF_ENABLE_LIGHT_LAST_BRIGHTNESS: True,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: True,
            CONF_OPTIONAL_SETTINGS: ["no_wakeup"],
            CONF_COMMAND_THROTTLE_INTERVAL: DEFAULT_COMMAND_THROTTLE_INTERVAL,
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
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_LIGHT_LAST_BRIGHTNESS] is True
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
        result = await _async_init_user_flow_at_central(hass)
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
        class _DummyQueryFacade:
            def get_un_ignore_candidates(self, include_master: bool) -> list[str]:
                return ["X", "Y"]

        class _DummyCentral:
            query_facade = _DummyQueryFacade()

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

    @pytest.fixture(autouse=True)
    def _mock_setup_entry(self):
        """Mock async_setup_entry to prevent central startup after reconfigure."""
        with patch(
            "custom_components.homematicip_local.async_setup_entry",
            return_value=True,
        ):
            yield


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
            result = await _async_init_user_flow_at_central(hass)

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
            result = await _async_init_user_flow_at_central(hass)

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
            result = await _async_init_user_flow_at_central(hass)

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

        # Should proceed to interface step with graceful degradation
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "interface"
        # No errors shown - user can manually configure

    async def test_detection_validation_exception(self, hass: HomeAssistant) -> None:
        """Test detection handles ValidationException."""
        with patch(
            "custom_components.homematicip_local.config_flow._async_detect_backend",
            new_callable=AsyncMock,
            side_effect=ValidationException("validation error"),
        ):
            result = await _async_init_user_flow_at_central(hass)

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

        # Should proceed to interface step with graceful degradation
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "interface"
        # No errors shown - user can manually configure


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
            CONF_DISABLE_CONFIG_PANEL: DEFAULT_DISABLE_CONFIG_PANEL,
            CONF_ENABLE_LIGHT_LAST_BRIGHTNESS: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_COMMAND_THROTTLE_INTERVAL: DEFAULT_COMMAND_THROTTLE_INTERVAL,
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
            CONF_DISABLE_CONFIG_PANEL: DEFAULT_DISABLE_CONFIG_PANEL,
            CONF_ENABLE_LIGHT_LAST_BRIGHTNESS: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_COMMAND_THROTTLE_INTERVAL: DEFAULT_COMMAND_THROTTLE_INTERVAL,
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
            CONF_DISABLE_CONFIG_PANEL: DEFAULT_DISABLE_CONFIG_PANEL,
            CONF_ENABLE_LIGHT_LAST_BRIGHTNESS: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_COMMAND_THROTTLE_INTERVAL: DEFAULT_COMMAND_THROTTLE_INTERVAL,
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
            CONF_DISABLE_CONFIG_PANEL: DEFAULT_DISABLE_CONFIG_PANEL,
            CONF_ENABLE_LIGHT_LAST_BRIGHTNESS: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_COMMAND_THROTTLE_INTERVAL: DEFAULT_COMMAND_THROTTLE_INTERVAL,
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
            CONF_DISABLE_CONFIG_PANEL: DEFAULT_DISABLE_CONFIG_PANEL,
            CONF_ENABLE_LIGHT_LAST_BRIGHTNESS: False,
            CONF_USE_GROUP_CHANNEL_FOR_COVER_STATE: False,
            CONF_OPTIONAL_SETTINGS: [],
            CONF_COMMAND_THROTTLE_INTERVAL: DEFAULT_COMMAND_THROTTLE_INTERVAL,
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
            await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.ABORT
        assert result2["reason"] == "reauth_successful"

        # Verify credentials were updated
        assert entry.data[CONF_USERNAME] == "new_username"
        assert entry.data[CONF_PASSWORD] == "new_password"

        # The entry update schedules a delayed config-entry store write; flush it so
        # the pending timer does not linger into teardown.
        await flush_store(hass.config_entries._store)

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

    @pytest.fixture(autouse=True)
    def _mock_setup_entry(self):
        """Mock async_setup_entry to prevent central startup after reauth."""
        with patch(
            "custom_components.homematicip_local.async_setup_entry",
            return_value=True,
        ):
            yield


_LOOM_RELEVANT = "custom_components.homematicip_local.config_flow.DomainConfigFlow._loom_is_relevant"


class TestLoomBackendGate:
    """The user step offers the loom backend only when it is relevant.

    Relevance is derived from real state — a configured loom entry or a
    daemon discovery flow in progress — so these tests drive the gate
    through that state rather than patching it.
    """

    async def test_ccu_entry_alone_skips_backend_menu(self, hass: HomeAssistant) -> None:
        """A direct-CCU entry is no evidence for loom — no menu."""
        MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            data={CONF_INSTANCE_NAME: const.INSTANCE_NAME, CONF_HOST: "ccu.local"},
        ).add_to_hass(hass)
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "central"

    async def test_configured_loom_entry_shows_backend_menu(self, hass: HomeAssistant) -> None:
        """An existing loom entry makes the backend menu appear."""
        MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            data={CONF_BACKEND: BACKEND_LOOM, CONF_HOST: "daemon.local"},
        ).add_to_hass(hass)
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.MENU
        assert set(result["menu_options"]) == {"central", "loom"}

    async def test_no_evidence_skips_backend_menu(self, hass: HomeAssistant) -> None:
        """Without a daemon or loom entry a fresh flow goes straight to central."""
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "central"

    async def test_pending_zeroconf_flow_shows_backend_menu(self, hass: HomeAssistant) -> None:
        """A daemon discovery flow in progress makes the backend menu appear."""
        discovery = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=_loom_zeroconf_info()
        )
        assert discovery["step_id"] == "loom_token"
        result = await hass.config_entries.flow.async_init(HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER})
        assert result["type"] == FlowResultType.MENU
        assert set(result["menu_options"]) == {"central", "loom"}


class TestOptionsFlowLoom:
    """Options flow for the openccu-loom backend (backend-aware steps)."""

    @staticmethod
    def _loom_entry(advanced_config: dict[str, object] | None = None, *, box: bool = False) -> MockConfigEntry:
        """Return a loom entry: direct with a daemon token, or through a box with a box token."""
        credential = {CONF_LOOM_BOX_TOKEN: _BOX_TOKEN} if box else {CONF_LOOM_TOKEN: "old-token"}
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            entry_id=const.CONFIG_ENTRY_ID,
            unique_id=const.CONFIG_ENTRY_UNIQUE_ID,
            data={
                CONF_BACKEND: BACKEND_LOOM,
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: const.HOST,
                CONF_LOOM_PORT: 8443,
                CONF_TLS: True,
                CONF_VERIFY_TLS: True,
                **credential,
                CONST_ADVANCED_CONFIG: advanced_config or {},
            },
        )
        entry.runtime_data = "123"
        return entry

    async def test_loom_advanced_settings_reduced(self, hass: HomeAssistant) -> None:
        """The loom advanced step exposes only the HA-side toggles and persists them."""
        entry = self._loom_entry()
        entry.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(entry.entry_id)

        form = await hass.config_entries.options.async_configure(
            result["flow_id"], {"next_step_id": "advanced_settings"}
        )
        assert form["type"] == FlowResultType.FORM
        assert form["step_id"] == "advanced_settings"
        keys = {str(k.schema) for k in form["data_schema"].schema}
        # The config-panel toggle is absent: loom entries register no panel.
        assert keys == {CONF_ENABLE_SYSTEM_NOTIFICATIONS, CONF_ENABLE_SUB_DEVICES}

        done = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {
                CONF_ENABLE_SYSTEM_NOTIFICATIONS: False,
                CONF_ENABLE_SUB_DEVICES: True,
            },
        )
        await hass.async_block_till_done()

        assert done["type"] == FlowResultType.CREATE_ENTRY
        advanced = entry.data[CONST_ADVANCED_CONFIG]
        assert advanced[CONF_ENABLE_SYSTEM_NOTIFICATIONS] is False
        assert advanced[CONF_ENABLE_SUB_DEVICES] is True

    async def test_loom_connection_invalid(self, hass: HomeAssistant) -> None:
        """An invalid loom connection surfaces an error and re-shows the form."""
        entry = self._loom_entry()
        entry.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(entry.entry_id)

        with patch("custom_components.homematicip_local.config_flow.ControlConfig") as control_config:
            control_config.return_value.check_config = AsyncMock(side_effect=InvalidConfig("bad token"))
            await hass.config_entries.options.async_configure(result["flow_id"], {"next_step_id": "loom_connection"})
            failed = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {CONF_HOST: const.HOST, CONF_TLS: True, CONF_VERIFY_TLS: True},
            )
            await hass.async_block_till_done()

        assert failed["type"] == FlowResultType.FORM
        assert failed["errors"] == {"base": "invalid_config"}

    async def test_loom_connection_success(self, hass: HomeAssistant) -> None:
        """A valid loom connection update is persisted to the entry data."""
        entry = self._loom_entry()
        entry.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(entry.entry_id)

        with patch("custom_components.homematicip_local.config_flow.ControlConfig") as control_config:
            control_config.return_value.check_config = AsyncMock(return_value=None)
            menu = await hass.config_entries.options.async_configure(
                result["flow_id"], {"next_step_id": "loom_connection"}
            )
            assert menu["type"] == FlowResultType.FORM
            assert menu["step_id"] == "loom_connection"
            # A direct entry edits its daemon token; the box token is not offered.
            assert _schema_keys(menu) == {CONF_HOST, CONF_LOOM_PORT, CONF_TLS, CONF_VERIFY_TLS, CONF_LOOM_TOKEN}

            done = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {
                    CONF_HOST: "daemon.local",
                    CONF_LOOM_PORT: 9999,
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_LOOM_TOKEN: "new-token",
                },
            )
            await hass.async_block_till_done()

        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert entry.data[CONF_HOST] == "daemon.local"
        assert entry.data[CONF_LOOM_PORT] == 9999
        assert entry.data[CONF_TLS] is False
        assert entry.data[CONF_LOOM_TOKEN] == "new-token"

    async def test_loom_menu_omits_ccu_only_steps(self, hass: HomeAssistant) -> None:
        """The loom menu drops interfaces and programs_sysvars (daemon-owned)."""
        entry = self._loom_entry()
        entry.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(entry.entry_id)
        assert result["type"] == FlowResultType.MENU
        assert result["menu_options"] == ["loom_connection", "advanced_settings", "permissions"]


class TestLoomFlowHelpers:
    """Unit tests for the loom flow schema/data helpers."""

    def test_get_loom_advanced_settings_schema_fields(self) -> None:
        schema = get_loom_advanced_settings_schema(data={})
        keys = {str(k.schema) for k in schema.schema}
        # No config-panel toggle: the panel is not registered for loom
        # entries at all, so the switch would offer a choice that does not
        # exist. Device pages link at the daemon's Config UI instead.
        assert keys == {CONF_ENABLE_SYSTEM_NOTIFICATIONS, CONF_ENABLE_SUB_DEVICES}

    def test_get_loom_data_sets_and_clears(self) -> None:
        base = {CONF_LOOM_PORT: 1, CONF_LOOM_TOKEN: "x"}
        # blank port + token are removed; tls/verify default to True
        cleared = _get_loom_data(base, user_input={CONF_HOST: "h"})
        assert cleared[CONF_HOST] == "h"
        assert CONF_LOOM_PORT not in cleared
        assert CONF_LOOM_TOKEN not in cleared
        assert cleared[CONF_TLS] is True
        # explicit port + token are set
        filled = _get_loom_data({}, user_input={CONF_HOST: "h", CONF_LOOM_PORT: 7, CONF_LOOM_TOKEN: "t"})
        assert filled[CONF_LOOM_PORT] == 7
        assert filled[CONF_LOOM_TOKEN] == "t"
        # absent in both input and existing data → keys simply stay absent
        absent = _get_loom_data({}, user_input={CONF_HOST: "h"})
        assert CONF_LOOM_PORT not in absent
        assert CONF_LOOM_TOKEN not in absent

    def test_get_loom_options_schema_fields(self) -> None:
        """A direct entry edits the daemon token; a box entry edits only the box token."""
        direct = get_loom_options_schema(data={CONF_BACKEND: BACKEND_LOOM, CONF_LOOM_TOKEN: "t"})
        assert {str(k.schema) for k in direct.schema} == {
            CONF_HOST,
            CONF_LOOM_PORT,
            CONF_TLS,
            CONF_VERIFY_TLS,
            CONF_LOOM_TOKEN,
        }
        box = get_loom_options_schema(data={CONF_BACKEND: BACKEND_LOOM, CONF_LOOM_BOX_TOKEN: "b"})
        assert {str(k.schema) for k in box.schema} == {
            CONF_HOST,
            CONF_LOOM_PORT,
            CONF_TLS,
            CONF_VERIFY_TLS,
            CONF_LOOM_BOX_TOKEN,
        }

    def test_update_loom_advanced_settings_input(self) -> None:
        data: dict[str, object] = {CONST_ADVANCED_CONFIG: {"keep_me": 1}}
        _update_loom_advanced_settings_input(
            data,
            advanced_input={
                CONF_ENABLE_SYSTEM_NOTIFICATIONS: True,
                CONF_ENABLE_SUB_DEVICES: True,
                CONF_DISABLE_CONFIG_PANEL: False,
            },
        )
        advanced = data[CONST_ADVANCED_CONFIG]
        assert advanced["keep_me"] == 1  # existing keys preserved
        assert advanced[CONF_ENABLE_SYSTEM_NOTIFICATIONS] is True
        assert advanced[CONF_ENABLE_SUB_DEVICES] is True
        # empty input is a no-op
        _update_loom_advanced_settings_input(data, advanced_input={})
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_SYSTEM_NOTIFICATIONS] is True


def _loom_zeroconf_info(
    *,
    properties: dict[str, str] | None = None,
    port: int = 8080,
    name: str = "Loom._openccu-loom._tcp.local.",
) -> ZeroconfServiceInfo:
    return ZeroconfServiceInfo(
        ip_address=ip_address("192.168.1.50"),
        ip_addresses=[ip_address("192.168.1.50")],
        port=port,
        hostname="daemon.local.",
        type="_openccu-loom._tcp.local.",
        name=name,
        properties=properties if properties is not None else {"instance": "Loom", "path": "/api/v1", "tls": "0"},
    )


_LOOM_LIST = "custom_components.homematicip_local.config_flow._async_loom_list_ccus"


class TestLoomZeroconfDiscovery:
    """mDNS (zeroconf) discovery of an openccu-loom daemon."""

    async def test_already_configured_aborts_with_serial(self, hass: HomeAssistant) -> None:
        """A CCU already configured on the loom backend aborts and renders the serial placeholder."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            data={CONF_BACKEND: BACKEND_LOOM, CONF_HOST: "daemon.local"},
        )
        existing.add_to_hass(hass)
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        with (
            patch(_LOOM_LIST, return_value=ccus),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            result = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "tok"})
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "already_configured"
        assert result["description_placeholders"] == {"serial": "ABC123"}

    async def test_announced_serial_on_ccu_backend_keeps_card(self, hass: HomeAssistant) -> None:
        """A serial configured on the CCU backend keeps the card (backend-switch path)."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            version=DomainConfigFlow.VERSION,
            data={CONF_INSTANCE_NAME: const.INSTANCE_NAME, CONF_HOST: "ccu.local"},
        )
        existing.add_to_hass(hass)
        result = await self._init_zeroconf(hass, _loom_zeroconf_info(properties={"instance": "Loom", "ccus": "ABC123"}))
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "loom_token"

    async def test_announced_serials_all_configured_aborts(self, hass: HomeAssistant) -> None:
        """The card is suppressed once every announced CCU is set up on loom."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            version=DomainConfigFlow.VERSION,
            data={CONF_BACKEND: BACKEND_LOOM, CONF_HOST: "192.168.1.50", CONF_LOOM_PORT: 8080},
        )
        existing.add_to_hass(hass)
        result = await self._init_zeroconf(hass, _loom_zeroconf_info(properties={"instance": "Loom", "ccus": "ABC123"}))
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "already_configured"
        assert result["description_placeholders"] == {"serial": "ABC123"}

    async def test_announced_serials_follow_daemon_host(self, hass: HomeAssistant) -> None:
        """A configured loom entry follows the daemon's announced endpoint."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            version=DomainConfigFlow.VERSION,
            data={CONF_BACKEND: BACKEND_LOOM, CONF_HOST: "old.local", CONF_LOOM_PORT: 9999},
        )
        existing.add_to_hass(hass)
        with (
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            result = await self._init_zeroconf(
                hass, _loom_zeroconf_info(properties={"instance": "Loom", "ccus": "ABC123"})
            )
            await hass.async_block_till_done()
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "already_configured"
        assert existing.data[CONF_HOST] == "192.168.1.50"
        assert existing.data[CONF_LOOM_PORT] == 8080

    async def test_announced_serials_partially_configured_keeps_card(self, hass: HomeAssistant) -> None:
        """With an unconfigured CCU on the daemon the card stays offered."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="AAA",
            version=DomainConfigFlow.VERSION,
            data={CONF_BACKEND: BACKEND_LOOM, CONF_HOST: "192.168.1.50", CONF_LOOM_PORT: 8080},
        )
        existing.add_to_hass(hass)
        result = await self._init_zeroconf(
            hass, _loom_zeroconf_info(properties={"instance": "Loom", "ccus": "AAA,BBB"})
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "loom_token"

    async def test_cannot_connect(self, hass: HomeAssistant) -> None:
        with (
            patch(_LOOM_LIST, side_effect=NoConnectionException("unreachable")),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            result = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "x"})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "cannot_connect"}

    async def test_ccu_entry_switched_to_loom_in_place(self, hass: HomeAssistant) -> None:
        """A serial configured on the CCU backend is switched to loom in place."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            title=const.INSTANCE_NAME,
            version=DomainConfigFlow.VERSION,
            data={
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: "ccu.local",
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONST_ADVANCED_CONFIG: {CONF_ENABLE_SUB_DEVICES: False, CONF_ENABLE_MQTT: True},
            },
        )
        existing.add_to_hass(hass)
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        with (
            patch(_LOOM_LIST, return_value=ccus),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            result = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            await hass.async_block_till_done()
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "backend_switched"
        data = existing.data
        assert data[CONF_BACKEND] == BACKEND_LOOM
        assert data[CONF_HOST] == "192.168.1.50"
        assert data[CONF_LOOM_PORT] == 8080
        assert data[CONF_LOOM_TOKEN] == "tok"
        # Instance name and CCU credentials survive for a lossless switch back.
        assert data[CONF_INSTANCE_NAME] == const.INSTANCE_NAME
        assert data[CONF_USERNAME] == const.USERNAME
        assert data[CONF_PASSWORD] == const.PASSWORD
        # The entry's explicit advanced config wins over the form default.
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_SUB_DEVICES] is False
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_MQTT] is True

    async def test_daemon_endpoint_already_configured_aborts(self, hass: HomeAssistant) -> None:
        """Without announced serials the daemon endpoint dedups the card."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            version=DomainConfigFlow.VERSION,
            data={CONF_BACKEND: BACKEND_LOOM, CONF_HOST: "192.168.1.50", CONF_LOOM_PORT: 8080},
        )
        existing.add_to_hass(hass)
        result = await self._init_zeroconf(hass, _loom_zeroconf_info())
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "already_configured"
        assert result["description_placeholders"] == {"serial": "ABC123"}

    async def test_empty_token_omits_token_in_entry(self, hass: HomeAssistant) -> None:
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        with (
            patch(_LOOM_LIST, return_value=ccus),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            done = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: ""})
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert CONF_LOOM_TOKEN not in done["result"].data

    async def test_entry_creation_aborts_stale_daemon_card(self, hass: HomeAssistant) -> None:
        """Setting up the daemon via the user flow clears its lingering discovery card."""
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        with (
            patch(_LOOM_LIST, return_value=ccus),
            patch(_BROWSE, return_value=[_loom_daemon("192.168.1.50", 8080, "Loom")]),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            card = await self._init_zeroconf(hass, _loom_zeroconf_info())
            assert card["type"] == FlowResultType.FORM
            user = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            token = await hass.config_entries.flow.async_configure(user["flow_id"], {"next_step_id": "loom"})
            assert token["step_id"] == "loom_token"
            done = await hass.config_entries.flow.async_configure(token["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert not [f for f in hass.config_entries.flow.async_progress() if f["flow_id"] == card["flow_id"]]

    async def test_incompatible_version(self, hass: HomeAssistant) -> None:
        """A daemon speaking another API generation gets its own error, not cannot_connect."""
        from openccu_loom_client import LoomIncompatibleVersionError

        with (
            patch(_LOOM_LIST, side_effect=LoomIncompatibleVersionError("daemon api 9 vs client api 3")),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            result = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "x"})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "incompatible_version"}

    async def test_invalid_auth(self, hass: HomeAssistant) -> None:
        with (
            patch(_LOOM_LIST, side_effect=AuthFailure("bad token")),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            result = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "x"})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "invalid_auth"}

    async def test_missing_port_aborts(self, hass: HomeAssistant) -> None:
        result = await self._init_zeroconf(hass, _loom_zeroconf_info(port=0))
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "invalid_discovery_info"

    async def test_multi_ccu_selection(self, hass: HomeAssistant) -> None:
        ccus = [
            {"name": "Home", "serial": "AAA", "host": "h1", "model": "CCU3", "available": True},
            {"name": "Office", "serial": "BBB", "host": "h2", "model": "CCU3", "available": True},
        ]
        with (
            patch(_LOOM_LIST, return_value=ccus),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            form = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            assert form["type"] == FlowResultType.FORM
            assert form["step_id"] == "loom_select_ccu"
            done = await hass.config_entries.flow.async_configure(form["flow_id"], {"serial": "BBB"})
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        entry = done["result"]
        assert entry.unique_id == "BBB"
        assert entry.data[CONF_INSTANCE_NAME] == "Office"

    async def test_no_ccus(self, hass: HomeAssistant) -> None:
        with (
            patch(_LOOM_LIST, return_value=[]),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            result = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "x"})
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "no_ccus"}

    async def test_parallel_ssdp_discovery_does_not_block_loom(
        self, hass: HomeAssistant, discovery_info: ssdp.SsdpServiceInfo
    ) -> None:
        """A concurrent SSDP discovery of the same CCU must not abort the loom setup as already_in_progress."""
        ssdp_flow = await hass.config_entries.flow.async_init(
            HMIP_DOMAIN, data=discovery_info, context={"source": config_entries.SOURCE_SSDP}
        )
        assert ssdp_flow["type"] == FlowResultType.FORM
        ccus = [
            {
                "name": "Home",
                "serial": const.CONFIG_ENTRY_UNIQUE_ID,
                "host": "ccu.local",
                "model": "CCU3",
                "available": True,
            }
        ]
        with (
            patch(_LOOM_LIST, return_value=ccus),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            done = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert done["result"].unique_id == const.CONFIG_ENTRY_UNIQUE_ID
        # Creating the loom entry auto-aborts the now-redundant SSDP discovery card.
        assert not hass.config_entries.flow.async_progress()

    async def test_shows_token_form(self, hass: HomeAssistant) -> None:
        result = await self._init_zeroconf(hass, _loom_zeroconf_info())
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "loom_token"

    async def test_single_ccu_creates_entry(self, hass: HomeAssistant) -> None:
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        with (
            patch(_LOOM_LIST, return_value=ccus),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            done = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert done["title"] == "Home"
        entry = done["result"]
        assert entry.unique_id == "ABC123"
        assert entry.data[CONF_BACKEND] == BACKEND_LOOM
        assert entry.data[CONF_INSTANCE_NAME] == "Home"
        assert entry.data[CONF_HOST] == "192.168.1.50"
        assert entry.data[CONF_LOOM_PORT] == 8080
        assert entry.data[CONF_LOOM_TOKEN] == "tok"
        # Sub-device entities default to enabled on the loom backend.
        assert entry.data[CONST_ADVANCED_CONFIG] == {CONF_ENABLE_SUB_DEVICES: True}

    async def test_switch_of_loaded_entry_skips_schedule_reload(self, hass: HomeAssistant) -> None:
        """A loaded entry reloads via its update listener - no extra schedule."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            version=DomainConfigFlow.VERSION,
            data={CONF_INSTANCE_NAME: const.INSTANCE_NAME, CONF_HOST: "ccu.local"},
        )
        existing.add_to_hass(hass)
        existing.mock_state(hass, config_entries.ConfigEntryState.LOADED)
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        with (
            patch(_LOOM_LIST, return_value=ccus),
            patch.object(hass.config_entries, "async_schedule_reload") as schedule_reload,
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            result = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            await hass.async_block_till_done()
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "backend_switched"
        schedule_reload.assert_not_called()

    async def test_token_step_can_disable_sub_devices(self, hass: HomeAssistant) -> None:
        """Unchecking the sub-device toggle in the token step is persisted."""
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        with (
            patch(_LOOM_LIST, return_value=ccus),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            init = await self._init_zeroconf(hass, _loom_zeroconf_info())
            done = await hass.config_entries.flow.async_configure(
                init["flow_id"], {CONF_LOOM_TOKEN: "tok", CONF_ENABLE_SUB_DEVICES: False}
            )
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert done["result"].data[CONST_ADVANCED_CONFIG] == {CONF_ENABLE_SUB_DEVICES: False}

    async def _init_zeroconf(self, hass: HomeAssistant, info: ZeroconfServiceInfo) -> dict:
        return await hass.config_entries.flow.async_init(
            HMIP_DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=info
        )


class TestBackendSwitchToCcu:
    """The central flow switches an existing loom entry back to the CCU backend in place."""

    async def test_central_flow_same_backend_still_aborts(self, hass: HomeAssistant) -> None:
        """A serial already configured on the CCU backend keeps aborting with already_configured."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id=const.SERIAL,
            version=DomainConfigFlow.VERSION,
            data={CONF_INSTANCE_NAME: const.INSTANCE_NAME, CONF_HOST: const.HOST},
        )
        existing.add_to_hass(hass)
        result3 = await self._run_central_flow(hass)
        assert result3["type"] == FlowResultType.ABORT
        assert result3["reason"] == "already_configured"
        assert result3["description_placeholders"] == {"serial": const.SERIAL}

    async def test_loom_entry_switched_to_ccu_in_place(self, hass: HomeAssistant) -> None:
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id=const.SERIAL,
            title=const.INSTANCE_NAME,
            version=DomainConfigFlow.VERSION,
            data={
                CONF_BACKEND: BACKEND_LOOM,
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: "daemon.local",
                CONF_LOOM_PORT: 8443,
                CONF_LOOM_TOKEN: "tok",
                CONST_ADVANCED_CONFIG: {CONF_ENABLE_SUB_DEVICES: True},
            },
        )
        existing.add_to_hass(hass)
        result3 = await self._run_central_flow(hass)
        assert result3["type"] == FlowResultType.ABORT
        assert result3["reason"] == "backend_switched"
        data = existing.data
        assert data[CONF_BACKEND] == BACKEND_CCU
        assert data[CONF_HOST] == const.HOST
        assert data[CONF_USERNAME] == const.USERNAME
        assert data[CONF_PASSWORD] == const.PASSWORD
        # The instance name keys entity naming and stays stable on a switch.
        assert data[CONF_INSTANCE_NAME] == const.INSTANCE_NAME
        # Loom connection keys survive for a lossless switch back.
        assert data[CONF_LOOM_PORT] == 8443
        assert data[CONF_LOOM_TOKEN] == "tok"
        # The entry's advanced config (incl. sub_devices_enabled) is migrated.
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_SUB_DEVICES] is True

    async def _run_central_flow(self, hass: HomeAssistant) -> dict:
        """Drive a fresh central flow (serial const.SERIAL) up to its final result."""
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
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            result = await _async_init_user_flow_at_central(hass)
            result2 = await hass.config_entries.flow.async_configure(
                result["flow_id"],
                {
                    CONF_INSTANCE_NAME: "Fresh Name",
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
            assert result2["step_id"] == "interface"
            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"], {CONF_TLS: False, CONF_VERIFY_TLS: False}
            )
            await hass.async_block_till_done()
            if result3["type"] == FlowResultType.MENU:
                result3 = await hass.config_entries.flow.async_configure(
                    result["flow_id"], {"next_step_id": "finish_setup"}
                )
                await hass.async_block_till_done()
            return result3


class TestAsyncLoomListCcus:
    """The `_async_loom_list_ccus` helper maps loom-client errors."""

    def test_import_helper_returns_callable(self) -> None:
        assert callable(_import_loom_list_ccus())

    async def test_incompatible_version_is_not_collapsed_into_no_connection(self, hass: HomeAssistant) -> None:
        """The version mismatch reaches the flow step as itself, not as a connection failure."""
        from openccu_loom_client import LoomIncompatibleVersionError

        fake = AsyncMock(side_effect=LoomIncompatibleVersionError("daemon api 9 vs client api 3"))
        with (
            patch(_LOOM_LIST.replace("_async_loom_list_ccus", "_import_loom_list_ccus"), return_value=fake),
            pytest.raises(LoomIncompatibleVersionError),
        ):
            await _async_loom_list_ccus(hass, host="h", port=1, tls=False, token="t", base_path="/api/v1")

    async def test_maps_auth_error(self, hass: HomeAssistant) -> None:
        from openccu_loom_client import LoomAuthError

        fake = AsyncMock(side_effect=LoomAuthError(status=401))
        with (
            patch(_LOOM_LIST.replace("_async_loom_list_ccus", "_import_loom_list_ccus"), return_value=fake),
            pytest.raises(AuthFailure),
        ):
            await _async_loom_list_ccus(hass, host="h", port=1, tls=False, token="t", base_path="/api/v1")

    async def test_maps_other_error(self, hass: HomeAssistant) -> None:
        fake = AsyncMock(side_effect=RuntimeError("boom"))
        with (
            patch(_LOOM_LIST.replace("_async_loom_list_ccus", "_import_loom_list_ccus"), return_value=fake),
            pytest.raises(NoConnectionException),
        ):
            await _async_loom_list_ccus(hass, host="h", port=1, tls=False, token="t", base_path="/api/v1")

    async def test_returns_result(self, hass: HomeAssistant) -> None:
        fake = AsyncMock(return_value=[{"serial": "X", "name": "n", "host": "h", "model": "m", "available": True}])
        with patch(_LOOM_LIST.replace("_async_loom_list_ccus", "_import_loom_list_ccus"), return_value=fake):
            result = await _async_loom_list_ccus(hass, host="h", port=1, tls=False, token="t", base_path="/api/v1")
        assert result == [{"serial": "X", "name": "n", "host": "h", "model": "m", "available": True}]


_BROWSE = "custom_components.homematicip_local.config_flow._async_browse_loom_daemons"

# Fields the manual flow's first step (connection) takes; the rest belong to
# the credentials step that follows the probe.
_MANUAL_CONNECTION_KEYS = frozenset(
    {CONF_INSTANCE_NAME, CONF_HOST, CONF_LOOM_PORT, CONF_TLS, CONF_VERIFY_TLS, CONF_ENABLE_SUB_DEVICES}
)


def _split_manual_input(user_input: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Split one manual loom input into the connection step's and the credentials step's part."""
    connection = {k: v for k, v in user_input.items() if k in _MANUAL_CONNECTION_KEYS}
    credentials = {k: v for k, v in user_input.items() if k not in _MANUAL_CONNECTION_KEYS}
    return connection, credentials


def _schema_keys(result: Any) -> set[str]:
    """Return the field names of a form result's schema."""
    return {str(k.schema) for k in result["data_schema"].schema}


def _loom_daemon(host: str, port: int, instance: str) -> dict:
    return {
        CONF_HOST: host,
        CONF_LOOM_PORT: port,
        CONF_TLS: False,
        CONF_LOOM_BASE_PATH: "/api/v1",
        CONF_INSTANCE_NAME: instance,
    }


class TestLoomBrowseCallbackContract:
    """The mDNS browse handler must honour zeroconf's callback contract.

    ``zeroconf`` fires state changes with keyword arguments only
    (``zeroconf=``, ``service_type=``, ``name=``, ``state_change=``), and it
    fires them from the browser constructor when the shared cache already
    holds matching services — which is the normal case in Home Assistant,
    since the integration's manifest makes HA browse this service type. A
    mismatched parameter name therefore raises synchronously inside the
    config-flow step rather than being swallowed in a background task.
    """

    async def test_handler_accepts_keyword_call_from_constructor(self, hass: HomeAssistant) -> None:
        """A cache-warm constructor callback must be accepted and collected."""
        from zeroconf import ServiceStateChange

        service_name = f"Daemon.{ZEROCONF_TYPE}"

        class _CacheWarmBrowser:
            """Stand-in for AsyncServiceBrowser that fires from its constructor."""

            def __init__(self, _zc: Any, service_type: str, handlers: list[Any]) -> None:
                for handler in handlers:
                    handler(
                        zeroconf=_zc,
                        service_type=service_type,
                        name=service_name,
                        state_change=ServiceStateChange.Added,
                    )

            async def async_cancel(self) -> None:
                return None

        info = MagicMock()
        info.async_request = AsyncMock(return_value=True)
        info.parsed_addresses = MagicMock(return_value=["192.168.1.50"])
        info.port = 8119
        info.properties = {b"instance": b"Daemon", b"path": b"/api/v1", b"tls": b"0"}

        with (
            patch("zeroconf.asyncio.AsyncServiceBrowser", _CacheWarmBrowser),
            patch("zeroconf.asyncio.AsyncServiceInfo", return_value=info),
            patch("homeassistant.components.zeroconf.async_get_async_instance", return_value=MagicMock()),
            patch("custom_components.homematicip_local.config_flow.LOOM_BROWSE_SECONDS", 0),
        ):
            daemons = await _async_browse_loom_daemons(hass)

        assert daemons == [
            {
                CONF_HOST: "192.168.1.50",
                CONF_LOOM_PORT: 8119,
                CONF_TLS: False,
                CONF_LOOM_BASE_PATH: "/api/v1",
                CONF_INSTANCE_NAME: "Daemon",
            }
        ]


class TestLoomActiveBrowse:
    """User-initiated loom flow actively browses for daemons via mDNS."""

    async def test_manual_entry_auth_failure(self, hass: HomeAssistant) -> None:
        """A rejected token surfaces invalid_auth on the manual form."""
        result = await self._submit_manual(hass, loom_list=AuthFailure("bad token"))
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "invalid_auth"}

    async def test_manual_entry_cannot_connect(self, hass: HomeAssistant) -> None:
        """An unreachable daemon surfaces cannot_connect on the manual form."""
        result = await self._submit_manual(hass, loom_list=NoConnectionException("unreachable"))
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "cannot_connect"}

    async def test_manual_entry_creates_entry(self, hass: HomeAssistant) -> None:
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        done = await self._submit_manual(hass, loom_list=ccus)
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert done["title"] == "Manual Loom"
        entry = done["result"]
        # The manual path is serial-keyed via the shared CCU-selection step.
        assert entry.unique_id == "ABC123"
        assert entry.data[CONF_INSTANCE_NAME] == "Manual Loom"
        assert entry.data[CONF_HOST] == "daemon.local"
        assert entry.data[CONF_LOOM_PORT] == 8080
        assert entry.data[CONF_LOOM_TOKEN] == "tok"
        assert entry.data[CONF_VERIFY_TLS] is False
        # Sub-device entities default to enabled on the loom backend.
        assert entry.data[CONST_ADVANCED_CONFIG] == {CONF_ENABLE_SUB_DEVICES: True}

    async def test_manual_entry_incompatible_version(self, hass: HomeAssistant) -> None:
        """
        The manual form gets its own error too, not cannot_connect.

        The discovered path had a test and this one did not, so the clause here
        could have been deleted with the suite still green — and a user who
        typed the host in by hand would have been sent to debug their network
        for a mismatch that has nothing to do with reachability.
        """
        from openccu_loom_client import LoomIncompatibleVersionError

        result = await self._submit_manual(
            hass, loom_list=LoomIncompatibleVersionError("daemon is missing required capabilities")
        )
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "incompatible_version"}

    async def test_manual_entry_invalid_config(self, hass: HomeAssistant) -> None:
        """A failing config check surfaces invalid_config on the manual form."""
        result = await self._submit_manual(hass, loom_list=[], check_config=InvalidConfig("bad host"))
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "invalid_config"}

    async def test_manual_entry_no_ccus(self, hass: HomeAssistant) -> None:
        """A daemon without CCUs surfaces no_ccus on the manual form."""
        result = await self._submit_manual(hass, loom_list=[])
        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "no_ccus"}

    async def test_manual_entry_switches_existing_ccu_entry(self, hass: HomeAssistant) -> None:
        """The manual path switches an existing CCU entry to loom in place."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            title=const.INSTANCE_NAME,
            version=DomainConfigFlow.VERSION,
            data={
                CONF_INSTANCE_NAME: const.INSTANCE_NAME,
                CONF_HOST: "ccu.local",
                CONF_USERNAME: const.USERNAME,
                CONF_PASSWORD: const.PASSWORD,
                CONST_ADVANCED_CONFIG: {CONF_ENABLE_SUB_DEVICES: False},
            },
        )
        existing.add_to_hass(hass)
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        result = await self._submit_manual(hass, loom_list=ccus)
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "backend_switched"
        data = existing.data
        assert data[CONF_BACKEND] == BACKEND_LOOM
        assert data[CONF_HOST] == "daemon.local"
        # The entry keeps its instance name and explicit sub_devices choice.
        assert data[CONF_INSTANCE_NAME] == const.INSTANCE_NAME
        assert data[CONST_ADVANCED_CONFIG][CONF_ENABLE_SUB_DEVICES] is False

    async def test_manual_entry_without_port_omits_port(self, hass: HomeAssistant) -> None:
        """A blank daemon port stays absent from the entry (runtime defaults apply)."""
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        done = await self._submit_manual(
            hass,
            loom_list=ccus,
            user_input={
                CONF_INSTANCE_NAME: "Manual Loom",
                CONF_HOST: "daemon.local",
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_LOOM_TOKEN: "tok",
            },
        )
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert CONF_LOOM_PORT not in done["result"].data

    async def test_multi_daemon_pick_then_token_then_entry(self, hass: HomeAssistant) -> None:
        daemons = [_loom_daemon("h1", 8080, "D1"), _loom_daemon("h2", 8081, "D2")]
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu", "model": "CCU3", "available": True}]
        with (
            patch(_BROWSE, return_value=daemons),
            patch(_LOOM_LIST, return_value=ccus),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            pick = await self._init_loom(hass)
            assert pick["step_id"] == "loom_pick"
            token = await hass.config_entries.flow.async_configure(pick["flow_id"], {CONF_LOOM_DAEMON: "h2:8081"})
            assert token["step_id"] == "loom_token"
            done = await hass.config_entries.flow.async_configure(token["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        entry = done["result"]
        assert entry.data[CONF_HOST] == "h2"
        assert entry.data[CONF_LOOM_PORT] == 8081
        assert entry.data[CONF_INSTANCE_NAME] == "Home"
        assert entry.unique_id == "ABC123"

    async def test_no_daemons_falls_back_to_manual(self, hass: HomeAssistant) -> None:
        with patch(_LOOM_RELEVANT, return_value=True), patch(_BROWSE, return_value=[]):
            step = await self._init_loom(hass)
        assert step["type"] == FlowResultType.FORM
        assert step["step_id"] == "loom"

    async def test_pick_manual_shows_manual_form(self, hass: HomeAssistant) -> None:
        daemons = [_loom_daemon("h1", 8080, "D1"), _loom_daemon("h2", 8081, "D2")]
        with patch(_LOOM_RELEVANT, return_value=True), patch(_BROWSE, return_value=daemons):
            pick = await self._init_loom(hass)
            assert pick["step_id"] == "loom_pick"
            manual = await hass.config_entries.flow.async_configure(
                pick["flow_id"], {CONF_LOOM_DAEMON: LOOM_MANUAL_DAEMON}
            )
        assert manual["type"] == FlowResultType.FORM
        assert manual["step_id"] == "loom"

    async def test_single_daemon_auto_selects_to_token(self, hass: HomeAssistant) -> None:
        with patch(_LOOM_RELEVANT, return_value=True), patch(_BROWSE, return_value=[_loom_daemon("h1", 8080, "D1")]):
            step = await self._init_loom(hass)
        assert step["type"] == FlowResultType.FORM
        assert step["step_id"] == "loom_token"

    async def _init_loom(self, hass: HomeAssistant) -> dict:
        """Reach the loom step via the backend menu.

        The gate itself is covered by :class:`TestLoomBackendGate`; here it
        is forced open so these tests stay focused on the loom path.
        """
        with patch(_LOOM_RELEVANT, return_value=True):
            result = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            assert result["type"] == FlowResultType.MENU
            return await hass.config_entries.flow.async_configure(result["flow_id"], {"next_step_id": "loom"})

    async def _submit_manual(
        self,
        hass: HomeAssistant,
        *,
        loom_list: Any,
        check_config: Exception | None = None,
        user_input: dict | None = None,
    ) -> dict:
        """Drive the manual loom form to its result with the given backend behavior."""
        if user_input is None:
            user_input = {
                CONF_INSTANCE_NAME: "Manual Loom",
                CONF_HOST: "daemon.local",
                CONF_LOOM_PORT: 8080,
                CONF_TLS: False,
                CONF_VERIFY_TLS: False,
                CONF_LOOM_TOKEN: "tok",
            }
        loom_kwargs = {"side_effect": loom_list} if isinstance(loom_list, Exception) else {"return_value": loom_list}
        connection, credentials = _split_manual_input(user_input)
        with (
            patch(_BROWSE, return_value=[]),
            patch(_LOOM_LIST, **loom_kwargs),
            patch("custom_components.homematicip_local.config_flow.ControlConfig") as control_config,
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            control_config.return_value.check_config = AsyncMock(side_effect=check_config)
            form = await self._init_loom(hass)
            assert form["step_id"] == "loom"
            creds = await hass.config_entries.flow.async_configure(form["flow_id"], connection)
            assert creds["step_id"] == "loom_credentials"
            result = await hass.config_entries.flow.async_configure(creds["flow_id"], credentials)
            await hass.async_block_till_done()
        return result


class _FakePairingSession:
    """Stands in for openccu_loom_client.PairingSession."""

    def __init__(self, *, result: Any = None, error: Exception | None = None) -> None:
        self.code = "123456"
        self.expires_in = 300
        self.withdrawn = False
        self._result = result
        self._error = error

    async def wait(self) -> Any:
        if self._error is not None:
            raise self._error
        return self._result

    async def withdraw(self) -> None:
        self.withdrawn = True


def _pair_result(state: str, token: str | None = None) -> Any:
    return SimpleNamespace(state=state, token=token, subject="ha", role="operator")


_START_PAIRING = "openccu_loom_client.start_pairing"
_CHECK_CONFIG = "custom_components.homematicip_local.config_flow.ControlConfig.check_config"


class TestLoomPairing:
    """Pair-with-the-daemon instead of pasting a token (daemon ADR 0076)."""

    async def test_discovered_pair_approved_reaches_ccu_selection(self, hass: HomeAssistant) -> None:
        """The discovered-daemon token form pairs the same way."""
        session = _FakePairingSession(result=_pair_result("approved", token="tok-paired"))
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        daemon = _loom_daemon("daemon.local", 8119, "Loom")
        with (
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
            patch(_LOOM_RELEVANT, return_value=True),
            patch(_BROWSE, return_value=[daemon]),
            patch(_START_PAIRING, AsyncMock(return_value=session)),
            patch(_LOOM_LIST, return_value=ccus) as loom_list,
        ):
            result = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            result = await hass.config_entries.flow.async_configure(result["flow_id"], {"next_step_id": "loom"})
            assert result["step_id"] == "loom_token"
            result = await hass.config_entries.flow.async_configure(result["flow_id"], {CONF_LOOM_PAIR: True})
            result = await self._drain_progress(hass, result)
        assert result["type"] == FlowResultType.CREATE_ENTRY, result
        assert result["data"][CONF_LOOM_TOKEN] == "tok-paired"
        assert loom_list.call_args.kwargs["token"] == "tok-paired"

    async def test_manual_pair_approved_reaches_ccu_selection(self, hass: HomeAssistant) -> None:
        """The approved token re-enters the manual step and validates as a pasted one."""
        session = _FakePairingSession(result=_pair_result("approved", token="tok-paired"))
        ccus = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
        start = AsyncMock(return_value=session)
        with (
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
            patch(_START_PAIRING, start),
            patch(_CHECK_CONFIG, AsyncMock(return_value=None)),
            patch(_LOOM_LIST, return_value=ccus) as loom_list,
        ):
            step = await self._init_manual_loom(
                hass, {CONF_INSTANCE_NAME: "Loom", CONF_HOST: "daemon.local", CONF_TLS: False, CONF_VERIFY_TLS: False}
            )
            result = await hass.config_entries.flow.async_configure(step["flow_id"], {CONF_LOOM_PAIR: True})
            result = await self._drain_progress(hass, result)
        assert result["type"] == FlowResultType.CREATE_ENTRY, result
        assert result["data"][CONF_LOOM_TOKEN] == "tok-paired"
        assert start.await_args.kwargs["role"] == "operator"
        assert start.await_args.kwargs["host"] == "daemon.local"
        assert loom_list.call_args.kwargs["token"] == "tok-paired"

    async def test_manual_pair_expired_returns_with_error(self, hass: HomeAssistant) -> None:
        session = _FakePairingSession(result=_pair_result("expired"))
        with patch(_START_PAIRING, AsyncMock(return_value=session)):
            step = await self._init_manual_loom(hass, {CONF_INSTANCE_NAME: "Loom", CONF_HOST: "daemon.local"})
            result = await hass.config_entries.flow.async_configure(step["flow_id"], {CONF_LOOM_PAIR: True})
            result = await self._drain_progress(hass, result)
        assert result["errors"] == {"base": "pairing_expired"}

    async def test_manual_pair_rejected_returns_with_error(self, hass: HomeAssistant) -> None:
        session = _FakePairingSession(result=_pair_result("rejected"))
        with patch(_START_PAIRING, AsyncMock(return_value=session)):
            step = await self._init_manual_loom(hass, {CONF_INSTANCE_NAME: "Loom", CONF_HOST: "daemon.local"})
            result = await hass.config_entries.flow.async_configure(step["flow_id"], {CONF_LOOM_PAIR: True})
            result = await self._drain_progress(hass, result)
        assert result["type"] == FlowResultType.FORM
        # The pairing returns to the credentials step it started from.
        assert result["step_id"] == "loom_credentials"
        assert result["errors"] == {"base": "pairing_rejected"}

    async def test_pairing_off_shows_actionable_error(self, hass: HomeAssistant) -> None:
        from openccu_loom_client import LoomPairingOffError

        with patch(_START_PAIRING, AsyncMock(side_effect=LoomPairingOffError(status=503, method="POST", url="x"))):
            step = await self._init_manual_loom(hass, {CONF_INSTANCE_NAME: "Loom", CONF_HOST: "daemon.local"})
            result = await hass.config_entries.flow.async_configure(step["flow_id"], {CONF_LOOM_PAIR: True})
            result = await self._drain_progress(hass, result)
        assert result["step_id"] == "loom_credentials"
        assert result["errors"] == {"base": "pairing_off"}

    async def _drain_progress(self, hass: HomeAssistant, result: dict) -> dict:
        while result["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
            await hass.async_block_till_done()
            result = await hass.config_entries.flow.async_configure(result["flow_id"])
            await hass.async_block_till_done()
        return result

    async def _init_manual_loom(self, hass: HomeAssistant, connection: dict[str, Any]) -> dict:
        """Submit the manual connection step and return the credentials step that follows."""
        with patch(_LOOM_RELEVANT, return_value=True), patch(_BROWSE, return_value=[]):
            result = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            assert result["type"] == FlowResultType.MENU
            step = await hass.config_entries.flow.async_configure(result["flow_id"], {"next_step_id": "loom"})
            assert step["step_id"] == "loom"
            step = await hass.config_entries.flow.async_configure(step["flow_id"], connection)
        assert step["step_id"] == "loom_credentials"
        return step


_BOX_TOKEN = "olt_0123456789abcdef0123456789abcdef"
_BOX = {CONF_LOOM_BOX_TOKEN: _BOX_TOKEN}
_BOX_KWARGS = {"box_token": _BOX_TOKEN}
_LEGACY_BOX = {CONF_LOOM_BOX_USERNAME: "boxadmin", CONF_LOOM_BOX_PASSWORD: "boxpw"}
_BOX_CCUS = [{"name": "Home", "serial": "ABC123", "host": "ccu.local", "model": "CCU3", "available": True}]
_START_BOX_PAIRING = "openccu_loom_client.start_box_pairing"


def _box_pair_result(state: str, token: str | None = None) -> Any:
    return SimpleNamespace(state=state, token=token or "", name="homeassistant", scopes=("addon:openccu-loom",))


class TestLoomBoxIngress:
    """Reaching the daemon through an openccu-lite box's web server with a box token."""

    async def test_async_loom_list_ccus_direct_passes_no_box_kwargs(self, hass: HomeAssistant) -> None:
        """A direct daemon listing carries no box_* keyword at all."""
        fake = AsyncMock(return_value=_BOX_CCUS)
        with patch(_LOOM_LIST.replace("_async_loom_list_ccus", "_import_loom_list_ccus"), return_value=fake):
            await _async_loom_list_ccus(hass, host="h", port=1, tls=False, token="t", base_path="/api/v1")
        assert not any(key.startswith("box_") for key in fake.await_args.kwargs)

    async def test_async_loom_list_ccus_forwards_box_kwargs(self, hass: HomeAssistant) -> None:
        """The box token reaches the client's list_ccus as its box_* keyword."""
        fake = AsyncMock(return_value=_BOX_CCUS)
        with patch(_LOOM_LIST.replace("_async_loom_list_ccus", "_import_loom_list_ccus"), return_value=fake):
            await _async_loom_list_ccus(hass, host="box", port=None, tls=True, token="", base_path=None, box=_BOX)
        fake.assert_awaited_once_with(host="box", port=None, tls=True, token="", base_path=None, **_BOX_KWARGS)

    async def test_box_gate_refusal_lists_as_invalid_auth(self, hass: HomeAssistant) -> None:
        """The box refusing the box token is a credential verdict, not a connection failure."""
        from openccu_loom_client import LoomBoxTokenError

        fake = AsyncMock(side_effect=LoomBoxTokenError("revoked"))
        with (
            patch(_LOOM_LIST.replace("_async_loom_list_ccus", "_import_loom_list_ccus"), return_value=fake),
            pytest.raises(AuthFailure),
        ):
            await _async_loom_list_ccus(hass, host="box", port=None, tls=True, token="", base_path=None, box=_BOX)

    @pytest.mark.parametrize(
        ("code", "key"),
        [
            ("pairing-off", "loom_box_pairing_off"),
            ("not-local", "loom_box_pairing_not_local"),
            ("invalid", "loom_box_pairing_invalid"),
            ("limit", "loom_box_pairing_refused"),
        ],
    )
    async def test_box_pairing_refusal_returns_with_error_and_switch_on(
        self, hass: HomeAssistant, code: str, key: str
    ) -> None:
        from openccu_loom_client import LoomBoxPairingError

        start = AsyncMock(side_effect=LoomBoxPairingError(message="no", code=code, status=403))
        with patch(_START_BOX_PAIRING, start):
            result, loom_list = await self._submit_manual(hass, {CONF_LOOM_BOX: True}, drain=True)
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "loom_credentials"
        assert result["errors"] == {"base": key}
        loom_list.assert_not_awaited()
        # The form comes back with the box switch still on.
        box_marker = next(k for k in result["data_schema"].schema if str(k.schema) == CONF_LOOM_BOX)
        assert box_marker.default() is True

    async def test_daemon_token_beside_the_box_is_rejected(self, hass: HomeAssistant) -> None:
        """Behind the box the box token is the only credential; a daemon token is refused, not dropped."""
        result, loom_list = await self._submit_manual(hass, {CONF_LOOM_BOX: True, CONF_LOOM_TOKEN: "tok"})
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "loom_credentials"
        assert result["errors"] == {"base": "loom_box_daemon_token"}
        loom_list.assert_not_awaited()

    async def test_discovered_form_pairs_with_the_box(self, hass: HomeAssistant) -> None:
        """The discovered-daemon form takes the box switch instead of a token."""
        session = _FakePairingSession(result=_box_pair_result("approved", _BOX_TOKEN))
        with (
            patch(_LOOM_LIST, return_value=_BOX_CCUS) as loom_list,
            patch(_START_BOX_PAIRING, AsyncMock(return_value=session)),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            init = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=_loom_zeroconf_info()
            )
            assert init["step_id"] == "loom_token"
            keys = {str(k.schema) for k in init["data_schema"].schema}
            assert CONF_LOOM_BOX in keys
            done = await hass.config_entries.flow.async_configure(init["flow_id"], {CONF_LOOM_BOX: True})
            done = await self._drain(hass, done)
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert loom_list.await_args.kwargs["box"] == _BOX
        assert loom_list.await_args.kwargs["token"] == ""
        assert done["result"].data[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN
        assert CONF_LOOM_TOKEN not in done["result"].data

    def test_get_loom_data_sets_and_clears_box(self) -> None:
        """The options flow stores a pasted box token and drops it, and any box web account, when cleared."""
        filled = _get_loom_data({**_LEGACY_BOX}, user_input={CONF_HOST: "box", **_BOX})
        assert filled[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN
        assert not set(filled) & {CONF_LOOM_BOX_USERNAME, CONF_LOOM_BOX_PASSWORD}
        cleared = _get_loom_data(filled, user_input={CONF_HOST: "h", CONF_LOOM_TOKEN: "t"})
        assert CONF_LOOM_BOX_TOKEN not in cleared

    async def test_manual_form_pairs_with_the_box_and_stores_the_token(self, hass: HomeAssistant) -> None:
        """Switching the box on pairs with the box; the entry stores its token and no daemon token."""
        session = _FakePairingSession(result=_box_pair_result("approved", _BOX_TOKEN))
        start = AsyncMock(return_value=session)
        with patch(_START_BOX_PAIRING, start):
            result, loom_list = await self._submit_manual(hass, {CONF_LOOM_BOX: True}, drain=True)
        assert result["type"] == FlowResultType.CREATE_ENTRY
        # Paired at the box's own web server: its host and TLS, no daemon port.
        assert start.await_args.kwargs["host"] == "box.local"
        assert start.await_args.kwargs["tls"] is True
        assert "port" not in start.await_args.kwargs
        kwargs = loom_list.await_args.kwargs
        assert kwargs["box"] == _BOX
        assert kwargs["token"] == ""
        data = result["result"].data
        assert data[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN
        assert CONF_LOOM_TOKEN not in data
        assert not set(data) & {CONF_LOOM_BOX, CONF_LOOM_BOX_USERNAME, CONF_LOOM_BOX_PASSWORD}

    async def test_manual_form_with_a_pasted_box_token_skips_pairing(self, hass: HomeAssistant) -> None:
        """A box token pasted in the setup form is used as is; no box pairing starts."""
        start = AsyncMock()
        with patch(_START_BOX_PAIRING, start):
            result, loom_list = await self._submit_manual(hass, {CONF_LOOM_BOX: True, **_BOX})
        assert result["type"] == FlowResultType.CREATE_ENTRY
        start.assert_not_awaited()
        assert loom_list.await_args.kwargs["box"] == _BOX
        assert result["result"].data[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN

    async def test_options_connection_box_entry_keeps_its_token_when_left_empty(self, hass: HomeAssistant) -> None:
        """An emptied box token field keeps the stored one: switching to direct is not done here."""
        entry = TestOptionsFlowLoom()._loom_entry(box=True)
        entry.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(entry.entry_id)
        with patch("custom_components.homematicip_local.config_flow.ControlConfig") as control_config:
            control_config.return_value.check_config = AsyncMock(return_value=None)
            await hass.config_entries.options.async_configure(result["flow_id"], {"next_step_id": "loom_connection"})
            done = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {CONF_HOST: "box2.local", CONF_TLS: True, CONF_VERIFY_TLS: True, CONF_LOOM_BOX_TOKEN: ""},
            )
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert entry.data[CONF_HOST] == "box2.local"
        assert entry.data[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN
        assert CONF_LOOM_TOKEN not in entry.data

    async def test_options_connection_box_token(self, hass: HomeAssistant) -> None:
        """A box entry's options edit only the box token and persist a newly pasted one."""
        entry = TestOptionsFlowLoom()._loom_entry(box=True)
        entry.add_to_hass(hass)
        result = await hass.config_entries.options.async_init(entry.entry_id)
        new_token = "olt_" + "e" * 32
        with patch("custom_components.homematicip_local.config_flow.ControlConfig") as control_config:
            control_config.return_value.check_config = AsyncMock(return_value=None)
            form = await hass.config_entries.options.async_configure(
                result["flow_id"], {"next_step_id": "loom_connection"}
            )
            assert _schema_keys(form) == {CONF_HOST, CONF_LOOM_PORT, CONF_TLS, CONF_VERIFY_TLS, CONF_LOOM_BOX_TOKEN}
            done = await hass.config_entries.options.async_configure(
                result["flow_id"],
                {CONF_HOST: "box.local", CONF_TLS: True, CONF_VERIFY_TLS: True, CONF_LOOM_BOX_TOKEN: new_token},
            )
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert entry.data[CONF_LOOM_BOX_TOKEN] == new_token
        assert CONF_LOOM_TOKEN not in entry.data
        # The validation ran against the data carrying the box token.
        assert control_config.call_args.kwargs["data"][CONF_LOOM_BOX_TOKEN] == new_token

    async def test_reauth_box_pairing_failure_stays_on_the_reauth_form(self, hass: HomeAssistant) -> None:
        from openccu_loom_client import LoomBoxPairingError

        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            title="Box Loom",
            version=DomainConfigFlow.VERSION,
            data={CONF_BACKEND: BACKEND_LOOM, CONF_INSTANCE_NAME: "Box Loom", CONF_HOST: "box.local", **_LEGACY_BOX},
        )
        entry.add_to_hass(hass)
        start = AsyncMock(side_effect=LoomBoxPairingError(message="off", code="pairing-off", status=403))
        with patch(_START_BOX_PAIRING, start):
            result = await entry.start_reauth_flow(hass)
            result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
            result = await self._drain(hass, result)
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reauth_loom_box"
        assert result["errors"] == {"base": "loom_box_pairing_off"}
        assert entry.data[CONF_LOOM_BOX_USERNAME] == "boxadmin"

    @pytest.mark.parametrize("box_data", [_LEGACY_BOX, _BOX], ids=["legacy box account", "refused box token"])
    async def test_reauth_pairs_with_the_box(self, hass: HomeAssistant, box_data: dict[str, str]) -> None:
        """Reauthentication of a box entry pairs with the box and replaces the credential."""
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            title="Box Loom",
            version=DomainConfigFlow.VERSION,
            data={
                CONF_BACKEND: BACKEND_LOOM,
                CONF_INSTANCE_NAME: "Box Loom",
                CONF_HOST: "box.local",
                CONF_TLS: True,
                CONF_VERIFY_TLS: True,
                **box_data,
            },
        )
        entry.add_to_hass(hass)
        session = _FakePairingSession(result=_box_pair_result("approved", "olt_" + "f" * 32))
        with (
            patch(_START_BOX_PAIRING, AsyncMock(return_value=session)) as start,
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            result = await entry.start_reauth_flow(hass)
            assert result["type"] == FlowResultType.FORM
            assert result["step_id"] == "reauth_loom_box"
            result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
            result = await self._drain(hass, result)
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "reauth_successful"
        assert start.await_args.kwargs["host"] == "box.local"
        assert entry.data[CONF_LOOM_BOX_TOKEN] == "olt_" + "f" * 32
        assert not set(entry.data) & {CONF_LOOM_BOX_USERNAME, CONF_LOOM_BOX_PASSWORD}

    async def test_rejected_box_pairing_returns_with_error(self, hass: HomeAssistant) -> None:
        session = _FakePairingSession(result=_box_pair_result("rejected"))
        with patch(_START_BOX_PAIRING, AsyncMock(return_value=session)):
            result, _ = await self._submit_manual(hass, {CONF_LOOM_BOX: True}, drain=True)
        assert result["errors"] == {"base": "pairing_rejected"}

    async def test_setup_forms_show_the_box_switch_and_token(self, hass: HomeAssistant) -> None:
        """Only for a daemon that does not describe itself both credential forms carry the box switch and token.

        A box (gate or lite-addon) gets the box token alone, a self-describing
        direct daemon no box field at all, and no offer ever carries box
        account fields.
        """
        legacy = loom_login_offer(deployment_kind=None, login_paths=frozenset(), box_gate=False)
        box = loom_login_offer(deployment_kind="lite-addon", login_paths=frozenset(), box_gate=False)
        direct = loom_login_offer(deployment_kind="standalone", login_paths=frozenset({"bearer"}), box_gate=False)
        for build in (get_loom_credentials_schema, get_loom_token_schema):
            legacy_keys = {str(k.schema) for k in build(data={}, offer=legacy).schema}
            assert {CONF_LOOM_BOX, CONF_LOOM_BOX_TOKEN} <= legacy_keys
            box_keys = {str(k.schema) for k in build(data={}, offer=box).schema}
            assert CONF_LOOM_BOX_TOKEN in box_keys
            assert CONF_LOOM_BOX not in box_keys
            direct_keys = {str(k.schema) for k in build(data={}, offer=direct).schema}
            assert not direct_keys & {CONF_LOOM_BOX, CONF_LOOM_BOX_TOKEN}
            for keys in (legacy_keys, box_keys, direct_keys):
                assert not keys & {CONF_LOOM_BOX_USERNAME, CONF_LOOM_BOX_PASSWORD}

    async def test_switch_to_loom_drops_stale_box_credentials(self, hass: HomeAssistant) -> None:
        """A CCU entry carrying box credentials from an earlier loom life switches back without them."""
        existing = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            title=const.INSTANCE_NAME,
            version=DomainConfigFlow.VERSION,
            data={CONF_INSTANCE_NAME: const.INSTANCE_NAME, CONF_HOST: "ccu.local", **_BOX, **_LEGACY_BOX},
        )
        existing.add_to_hass(hass)
        result, _ = await self._submit_manual(hass, {CONF_LOOM_TOKEN: "tok"})
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "backend_switched"
        assert not set(existing.data) & {CONF_LOOM_BOX_TOKEN, CONF_LOOM_BOX_USERNAME, CONF_LOOM_BOX_PASSWORD}

    async def _drain(self, hass: HomeAssistant, result: dict) -> dict:
        while result["type"] in (FlowResultType.SHOW_PROGRESS, FlowResultType.SHOW_PROGRESS_DONE):
            await hass.async_block_till_done()
            result = await hass.config_entries.flow.async_configure(result["flow_id"])
            await hass.async_block_till_done()
        return result

    async def _submit_manual(
        self, hass: HomeAssistant, extra: dict[str, Any], *, drain: bool = False
    ) -> tuple[dict, AsyncMock]:
        """Submit the manual loom forms for a box host and return the result and the list_ccus mock.

        The probe answers as a daemon that does not describe itself, so the
        credentials step shows today's full field set incl. the box switch.
        """
        connection = {
            CONF_INSTANCE_NAME: "Box Loom",
            CONF_HOST: "box.local",
            CONF_TLS: True,
            CONF_VERIFY_TLS: True,
        }
        with (
            patch(_LOOM_RELEVANT, return_value=True),
            patch(_BROWSE, return_value=[]),
            patch(_LOOM_LIST, return_value=_BOX_CCUS) as loom_list,
            patch("custom_components.homematicip_local.config_flow.ControlConfig") as control_config,
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            control_config.return_value.check_config = AsyncMock(return_value=None)
            menu = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            form = await hass.config_entries.flow.async_configure(menu["flow_id"], {"next_step_id": "loom"})
            assert form["step_id"] == "loom"
            creds = await hass.config_entries.flow.async_configure(form["flow_id"], connection)
            assert creds["step_id"] == "loom_credentials"
            result = await hass.config_entries.flow.async_configure(creds["flow_id"], extra)
            await hass.async_block_till_done()
            if drain:
                result = await self._drain(hass, result)
        return result, loom_list


class TestLoomLoginOffer:
    """One pure function decides which credential fields a loom form offers."""

    @pytest.mark.parametrize(
        ("offer", "keys"),
        [
            (
                LoomLoginOffer(mode=LoomLoginMode.LEGACY, daemon_token=True, daemon_pairing=True),
                {CONF_LOOM_TOKEN, CONF_LOOM_PAIR, CONF_LOOM_BOX, CONF_LOOM_BOX_TOKEN},
            ),
            (LoomLoginOffer(mode=LoomLoginMode.BOX), {CONF_LOOM_BOX_TOKEN}),
            (
                LoomLoginOffer(mode=LoomLoginMode.DIRECT, daemon_token=True, daemon_pairing=True),
                {CONF_LOOM_TOKEN, CONF_LOOM_PAIR},
            ),
            (LoomLoginOffer(mode=LoomLoginMode.DIRECT, daemon_token=True), {CONF_LOOM_TOKEN}),
            (LoomLoginOffer(mode=LoomLoginMode.DIRECT, daemon_pairing=True), {CONF_LOOM_PAIR}),
            (LoomLoginOffer(mode=LoomLoginMode.DIRECT), set()),
        ],
        ids=["legacy", "box", "direct both", "direct token", "direct pairing", "direct nothing"],
    )
    def test_forms_build_their_credential_fields_from_the_offer(self, offer: LoomLoginOffer, keys: set[str]) -> None:
        """The manual credentials form and the discovered form carry exactly the offered fields."""
        manual = {str(k.schema) for k in get_loom_credentials_schema(data={}, offer=offer).schema}
        assert manual == keys
        discovered = {str(k.schema) for k in get_loom_token_schema(data={}, offer=offer).schema}
        assert discovered == keys | {CONF_ENABLE_SUB_DEVICES}

    @pytest.mark.parametrize(
        ("kind", "paths", "box_gate", "mode", "token", "pair"),
        [
            # A box gate answered, or the daemon runs on an openccu-lite box: box only.
            (None, frozenset(), True, LoomLoginMode.BOX, False, False),
            ("standalone", frozenset({"bearer", "pairing"}), True, LoomLoginMode.BOX, False, False),
            ("lite-addon", frozenset({"occulite_token", "occulite_sso"}), False, LoomLoginMode.BOX, False, False),
            ("lite-addon", frozenset({"bearer", "pairing"}), False, LoomLoginMode.BOX, False, False),
            ("lite-addon", frozenset(), False, LoomLoginMode.BOX, False, False),
            # A self-describing daemon elsewhere: exactly the login paths it offers.
            ("standalone", frozenset({"bearer", "pairing"}), False, LoomLoginMode.DIRECT, True, True),
            ("standalone", frozenset({"bearer"}), False, LoomLoginMode.DIRECT, True, False),
            ("ccu-addon", frozenset({"pairing"}), False, LoomLoginMode.DIRECT, False, True),
            ("ha-addon", frozenset({"bearer", "pairing", "ha_ingress"}), False, LoomLoginMode.DIRECT, True, True),
            # An unknown deployment kind is not a box.
            ("toaster", frozenset({"bearer"}), False, LoomLoginMode.DIRECT, True, False),
            # A known kind without a usable login path cannot be signed in to.
            ("standalone", frozenset(), False, LoomLoginMode.DIRECT, False, False),
            ("standalone", frozenset({"basic", "oidc"}), False, LoomLoginMode.DIRECT, False, False),
            # Login paths alone describe the daemon too.
            (None, frozenset({"bearer"}), False, LoomLoginMode.DIRECT, True, False),
            (None, frozenset({"pairing"}), False, LoomLoginMode.DIRECT, False, True),
            (None, frozenset({"occulite_token"}), False, LoomLoginMode.DIRECT, False, False),
            # A daemon older than 0.86 says nothing about itself: today's full set.
            (None, frozenset(), False, LoomLoginMode.LEGACY, True, True),
            (None, frozenset({"basic", "oidc", "ccu"}), False, LoomLoginMode.LEGACY, True, True),
        ],
    )
    def test_offer_table(
        self,
        kind: str | None,
        paths: frozenset[str],
        box_gate: bool,
        mode: LoomLoginMode,
        token: bool,
        pair: bool,
    ) -> None:
        offer = loom_login_offer(deployment_kind=kind, login_paths=paths, box_gate=box_gate)
        assert offer == LoomLoginOffer(mode=mode, daemon_token=token, daemon_pairing=pair)
        assert offer.can_authenticate is (mode is not LoomLoginMode.DIRECT or token or pair)


_LITE_TXT = {
    "txtvers": "1",
    "instance": "Box",
    "path": "/api/v1",
    "tls": "0",
    "deploy": "lite-addon",
    "ingress": "/addons/loom",
    "auth": "occulite_token,occulite_sso",
}
_STANDALONE_TXT = {
    "txtvers": "1",
    "instance": "Loom",
    "path": "/api/v1",
    "tls": "0",
    "deploy": "standalone",
    "auth": "bearer,pairing",
}


class TestLoomDiscoveredOffer:
    """The discovered-daemon form shows only what the daemon (or its box) offers."""

    async def test_box_gate_answer_shows_box_only(self, hass: HomeAssistant) -> None:
        """A box gate answering the probe overrides a record that says standalone."""
        with patch(_PROBE, AsyncMock(return_value=_box_gate_probe())):
            form = await self._init(hass, _STANDALONE_TXT)
        assert _schema_keys(form) == {CONF_LOOM_BOX_TOKEN, CONF_ENABLE_SUB_DEVICES}

    async def test_box_only_form_pairs_with_the_box_into_a_box_entry(self, hass: HomeAssistant) -> None:
        """End to end: an empty box token pairs with the box; the entry holds the box token only."""
        session = _FakePairingSession(result=_box_pair_result("approved", _BOX_TOKEN))
        with (
            patch(_PROBE, AsyncMock(side_effect=_probe_unreachable())),
            patch(_START_BOX_PAIRING, AsyncMock(return_value=session)) as start,
            patch(_LOOM_LIST, return_value=_BOX_CCUS) as loom_list,
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            form = await self._init(hass, _LITE_TXT)
            done = await hass.config_entries.flow.async_configure(form["flow_id"], {})
            done = await TestLoomBoxIngress()._drain(hass, done)
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert start.await_args.kwargs["host"] == "192.168.1.50"
        assert loom_list.await_args.kwargs["box"] == _BOX
        assert loom_list.await_args.kwargs["token"] == ""
        data = done["result"].data
        assert data[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN
        assert CONF_LOOM_TOKEN not in data
        assert CONF_LOOM_BOX not in data

    async def test_box_only_form_takes_a_pasted_box_token(self, hass: HomeAssistant) -> None:
        start = AsyncMock()
        with (
            patch(_PROBE, AsyncMock(side_effect=_probe_unreachable())),
            patch(_START_BOX_PAIRING, start),
            patch(_LOOM_LIST, return_value=_BOX_CCUS) as loom_list,
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            form = await self._init(hass, _LITE_TXT)
            done = await hass.config_entries.flow.async_configure(form["flow_id"], {**_BOX})
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        start.assert_not_awaited()
        assert loom_list.await_args.kwargs["box"] == _BOX
        assert done["result"].data[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN

    async def test_direct_form_creates_a_direct_entry(self, hass: HomeAssistant) -> None:
        """End to end: the daemon token lands in the entry, no box token beside it."""
        probe = _daemon_probe(kind="standalone", paths=frozenset({"bearer", "pairing"}))
        with (
            patch(_PROBE, AsyncMock(return_value=probe)),
            patch(_LOOM_LIST, return_value=_BOX_CCUS) as loom_list,
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            form = await self._init(hass, _STANDALONE_TXT)
            done = await hass.config_entries.flow.async_configure(form["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            await hass.async_block_till_done()
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert loom_list.await_args.kwargs["box"] == {}
        data = done["result"].data
        assert data[CONF_LOOM_TOKEN] == "tok"
        assert CONF_LOOM_BOX_TOKEN not in data

    async def test_lite_record_with_unreachable_daemon_shows_box_only(self, hass: HomeAssistant) -> None:
        """On a lite box the daemon's port is closed: the record's hint decides, and it says box."""
        with patch(_PROBE, AsyncMock(side_effect=_probe_unreachable())) as probe:
            form = await self._init(hass, _LITE_TXT)
        assert form["step_id"] == "loom_token"
        assert _schema_keys(form) == {CONF_LOOM_BOX_TOKEN, CONF_ENABLE_SUB_DEVICES}
        # The probe asked the daemon at the announced endpoint and base path.
        assert probe.await_args.kwargs == {
            "host": "192.168.1.50",
            "port": 8080,
            "tls": False,
            "verify_tls": True,
            "base_path": "/api/v1",
        }

    async def test_no_supported_login_shows_the_error_instead_of_fields(self, hass: HomeAssistant) -> None:
        probe = _daemon_probe(kind="standalone", paths=frozenset({"oidc"}))
        with patch(_PROBE, AsyncMock(return_value=probe)), patch(_LOOM_LIST) as loom_list:
            form = await self._init(hass, _STANDALONE_TXT)
            assert form["errors"] == {"base": "loom_no_supported_login"}
            assert _schema_keys(form) == {CONF_ENABLE_SUB_DEVICES}
            again = await hass.config_entries.flow.async_configure(form["flow_id"], {})
        assert again["step_id"] == "loom_token"
        assert again["errors"] == {"base": "loom_no_supported_login"}
        loom_list.assert_not_called()

    async def test_old_record_and_legacy_probe_show_the_full_field_set(self, hass: HomeAssistant) -> None:
        form = await self._init(hass, {"instance": "Loom", "path": "/api/v1", "tls": "0"})
        assert _schema_keys(form) == {
            CONF_LOOM_TOKEN,
            CONF_LOOM_PAIR,
            CONF_LOOM_BOX,
            CONF_LOOM_BOX_TOKEN,
            CONF_ENABLE_SUB_DEVICES,
        }

    async def test_old_record_and_unreachable_probe_show_the_full_field_set(self, hass: HomeAssistant) -> None:
        with patch(_PROBE, AsyncMock(side_effect=_probe_unreachable())):
            form = await self._init(hass, {"instance": "Loom", "path": "/api/v1", "tls": "0"})
        assert CONF_LOOM_BOX in _schema_keys(form)

    async def test_picked_daemon_is_the_one_probed(self, hass: HomeAssistant) -> None:
        """The active browse probes the daemon the user picked, with the record's hint as fallback."""
        lite = {**_loom_daemon("h2", 8081, "D2"), CONF_LOOM_DEPLOY: "lite-addon"}
        daemons = [_loom_daemon("h1", 8080, "D1"), lite]
        with (
            patch(_LOOM_RELEVANT, return_value=True),
            patch(_BROWSE, return_value=daemons),
            patch(_PROBE, AsyncMock(side_effect=_probe_unreachable())) as probe,
        ):
            result = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            pick = await hass.config_entries.flow.async_configure(result["flow_id"], {"next_step_id": "loom"})
            form = await hass.config_entries.flow.async_configure(pick["flow_id"], {CONF_LOOM_DAEMON: "h2:8081"})
        assert probe.await_args.kwargs["host"] == "h2"
        assert _schema_keys(form) == {CONF_LOOM_BOX_TOKEN, CONF_ENABLE_SUB_DEVICES}

    async def test_probe_wins_over_the_record(self, hass: HomeAssistant) -> None:
        """The record says box, the daemon answers as a standalone daemon: the daemon's answer counts."""
        probe = _daemon_probe(kind="standalone", paths=frozenset({"bearer"}))
        with patch(_PROBE, AsyncMock(return_value=probe)):
            form = await self._init(hass, _LITE_TXT)
        assert _schema_keys(form) == {CONF_LOOM_TOKEN, CONF_ENABLE_SUB_DEVICES}

    async def test_standalone_record_and_probe_show_direct_fields(self, hass: HomeAssistant) -> None:
        probe = _daemon_probe(kind="standalone", paths=frozenset({"bearer", "pairing"}))
        with patch(_PROBE, AsyncMock(return_value=probe)):
            form = await self._init(hass, _STANDALONE_TXT)
        assert _schema_keys(form) == {CONF_LOOM_TOKEN, CONF_LOOM_PAIR, CONF_ENABLE_SUB_DEVICES}

    async def _init(self, hass: HomeAssistant, properties: dict[str, str]) -> dict:
        return await hass.config_entries.flow.async_init(
            HMIP_DOMAIN,
            context={"source": config_entries.SOURCE_ZEROCONF},
            data=_loom_zeroconf_info(properties=properties),
        )


_MANUAL_CONNECTION = {
    CONF_INSTANCE_NAME: "Manual Loom",
    CONF_HOST: "daemon.local",
    CONF_LOOM_PORT: 8080,
    CONF_TLS: False,
    CONF_VERIFY_TLS: False,
}


class TestLoomManualOffer:
    """The manual setup asks for the connection first, probes, then shows only the offered credentials."""

    async def test_box_pairing_failure_returns_to_the_box_only_form(self, hass: HomeAssistant) -> None:
        from openccu_loom_client import LoomBoxPairingError

        probe = AsyncMock(side_effect=[_probe_unreachable(), _box_gate_probe()])
        start = AsyncMock(side_effect=LoomBoxPairingError(message="off", code="pairing-off", status=403))
        with patch(_PROBE, probe), patch(_START_BOX_PAIRING, start):
            creds = await self._submit_connection(hass, {CONF_INSTANCE_NAME: "Box Loom", CONF_HOST: "box.local"})
            result = await hass.config_entries.flow.async_configure(creds["flow_id"], {})
            result = await TestLoomBoxIngress()._drain(hass, result)
        assert result["step_id"] == "loom_credentials"
        assert result["errors"] == {"base": "loom_box_pairing_off"}
        assert _schema_keys(result) == {CONF_LOOM_BOX_TOKEN}

    @pytest.mark.parametrize(("tls", "box_port"), [(True, 443), (False, 80)], ids=["https", "http"])
    async def test_box_path_probe_asks_the_box_web_server(self, hass: HomeAssistant, tls: bool, box_port: int) -> None:
        """The box-path probe goes to the box's web server port for the TLS flag, never the daemon port."""
        probe = AsyncMock(side_effect=_probe_by_path(direct=_probe_unreachable(), box=_box_gate_probe()))
        connection = {CONF_INSTANCE_NAME: "Box Loom", CONF_HOST: "box.local", CONF_TLS: tls, CONF_VERIFY_TLS: tls}
        with patch(_PROBE, probe):
            creds = await self._submit_connection(hass, connection)
        assert creds["step_id"] == "loom_credentials"
        assert _schema_keys(creds) == {CONF_LOOM_BOX_TOKEN}
        box_calls = [call.kwargs for call in probe.await_args_list if call.kwargs["base_path"] != "/api/v1"]
        assert box_calls == [
            {"host": "box.local", "port": box_port, "tls": tls, "verify_tls": tls, "base_path": "/addons/loom/api/v1"}
        ]

    async def test_connection_step_has_no_credential_fields(self, hass: HomeAssistant) -> None:
        connection = {
            CONF_INSTANCE_NAME,
            CONF_HOST,
            CONF_LOOM_PORT,
            CONF_TLS,
            CONF_VERIFY_TLS,
            CONF_ENABLE_SUB_DEVICES,
        }
        form = await self._open(hass)
        assert _schema_keys(form) == connection
        # Even with a token in the data the schema carries no credential field.
        assert {str(k.schema) for k in get_loom_schema(data={CONF_LOOM_TOKEN: "t"}).schema} == connection

    async def test_direct_answer_wins_when_the_box_path_answers_too(self, hass: HomeAssistant) -> None:
        """Both probes run at once; the daemon's own answer counts even when the box path answers first."""
        direct = _daemon_probe(kind="standalone", paths=frozenset({"bearer"}))
        probe = AsyncMock(side_effect=_probe_by_path(direct=direct, box=_box_gate_probe(), direct_delay=0.05))
        with patch(_PROBE, probe):
            creds = await self._submit_connection(hass, _MANUAL_CONNECTION)
        assert creds["step_id"] == "loom_credentials"
        assert _schema_keys(creds) == {CONF_LOOM_TOKEN}

    async def test_direct_daemon_offers_its_token_and_creates_a_direct_entry(self, hass: HomeAssistant) -> None:
        """End to end on the direct path: the daemon's answer decides, the entry holds the daemon token."""
        probe = AsyncMock(return_value=_daemon_probe(kind="standalone", paths=frozenset({"bearer"})))
        with (
            patch(_PROBE, probe),
            patch(_LOOM_LIST, return_value=_BOX_CCUS) as loom_list,
            patch(_CHECK_CONFIG, AsyncMock(return_value=None)),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            creds = await self._submit_connection(hass, _MANUAL_CONNECTION)
            assert creds["step_id"] == "loom_credentials"
            assert _schema_keys(creds) == {CONF_LOOM_TOKEN}
            done = await hass.config_entries.flow.async_configure(creds["flow_id"], {CONF_LOOM_TOKEN: "tok"})
            await hass.async_block_till_done()
        # The daemon was asked at the entered endpoint (the box path runs beside it).
        probe.assert_any_await(host="daemon.local", port=8080, tls=False, verify_tls=False, base_path="/api/v1")
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert loom_list.await_args.kwargs["box"] == {}
        data = done["result"].data
        assert data[CONF_INSTANCE_NAME] == "Manual Loom"
        assert data[CONF_LOOM_TOKEN] == "tok"
        assert CONF_LOOM_BOX_TOKEN not in data

    async def test_no_supported_login_shows_the_error_instead_of_fields(self, hass: HomeAssistant) -> None:
        probe = AsyncMock(return_value=_daemon_probe(kind="standalone", paths=frozenset({"basic"})))
        with patch(_PROBE, probe), patch(_LOOM_LIST) as loom_list:
            creds = await self._submit_connection(hass, _MANUAL_CONNECTION)
            assert creds["step_id"] == "loom_credentials"
            assert creds["errors"] == {"base": "loom_no_supported_login"}
            assert _schema_keys(creds) == set()
            again = await hass.config_entries.flow.async_configure(creds["flow_id"], {})
        assert again["step_id"] == "loom_credentials"
        assert again["errors"] == {"base": "loom_no_supported_login"}
        loom_list.assert_not_called()

    async def test_nothing_answers_shows_cannot_connect_on_the_connection_step(self, hass: HomeAssistant) -> None:
        probe = AsyncMock(side_effect=[_probe_unreachable(), _probe_unreachable()])
        with patch(_PROBE, probe):
            result = await self._submit_connection(hass, _MANUAL_CONNECTION)
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "loom"
        assert result["errors"] == {"base": "cannot_connect"}
        assert probe.await_count == 2

    async def test_pairing_is_offered_only_when_the_daemon_offers_it(self, hass: HomeAssistant) -> None:
        """A daemon that only pairs gets the pairing switch alone, and the paired token lands in the entry."""
        session = _FakePairingSession(result=_pair_result("approved", token="tok-paired"))
        probe = AsyncMock(return_value=_daemon_probe(kind="ccu-addon", paths=frozenset({"pairing"})))
        with (
            patch(_PROBE, probe),
            patch(_START_PAIRING, AsyncMock(return_value=session)),
            patch(_LOOM_LIST, return_value=_BOX_CCUS),
            patch(_CHECK_CONFIG, AsyncMock(return_value=None)),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            creds = await self._submit_connection(hass, _MANUAL_CONNECTION)
            assert _schema_keys(creds) == {CONF_LOOM_PAIR}
            done = await hass.config_entries.flow.async_configure(creds["flow_id"], {CONF_LOOM_PAIR: True})
            done = await TestLoomBoxIngress()._drain(hass, done)
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert done["result"].data[CONF_LOOM_TOKEN] == "tok-paired"

    async def test_probe_that_never_returns_fails_after_the_bound(self, hass: HomeAssistant) -> None:
        """A port that drops packets ends as the ordinary connection failure once the probe bound passes."""

        async def never(**_kwargs: Any) -> Any:
            await asyncio.Event().wait()

        with patch(_PROBE_TIMEOUT, 0.05), patch(_PROBE, AsyncMock(side_effect=never)):
            # Without the bound the flow would wait on the probe for good.
            async with asyncio.timeout(5):
                result = await self._submit_connection(hass, _MANUAL_CONNECTION)
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "loom"
        assert result["errors"] == {"base": "cannot_connect"}

    async def test_token_only_daemon_offers_no_pairing(self, hass: HomeAssistant) -> None:
        probe = AsyncMock(return_value=_daemon_probe(kind="ha-addon", paths=frozenset({"bearer", "ha_ingress"})))
        with patch(_PROBE, probe):
            creds = await self._submit_connection(hass, _MANUAL_CONNECTION)
        assert _schema_keys(creds) == {CONF_LOOM_TOKEN}

    async def test_unreachable_daemon_behind_a_box_gate_pairs_into_a_box_entry(self, hass: HomeAssistant) -> None:
        """End to end on the box path: the daemon's port is closed, the box's gate answers instead."""
        probe = AsyncMock(side_effect=[_probe_unreachable(), _box_gate_probe()])
        session = _FakePairingSession(result=_box_pair_result("approved", _BOX_TOKEN))
        connection = {CONF_INSTANCE_NAME: "Box Loom", CONF_HOST: "box.local", CONF_TLS: True, CONF_VERIFY_TLS: True}
        with (
            patch(_PROBE, probe),
            patch(_START_BOX_PAIRING, AsyncMock(return_value=session)) as start,
            patch(_LOOM_LIST, return_value=_BOX_CCUS) as loom_list,
            patch(_CHECK_CONFIG, AsyncMock(return_value=None)),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            creds = await self._submit_connection(hass, connection)
            assert creds["step_id"] == "loom_credentials"
            assert _schema_keys(creds) == {CONF_LOOM_BOX_TOKEN}
            done = await hass.config_entries.flow.async_configure(creds["flow_id"], {})
            done = await TestLoomBoxIngress()._drain(hass, done)
        assert probe.await_count == 2
        assert probe.await_args_list[0].kwargs == {
            "host": "box.local",
            "port": None,
            "tls": True,
            "verify_tls": True,
            "base_path": "/api/v1",
        }
        # The second probe goes through the box's web server and its ingress prefix.
        assert probe.await_args_list[1].kwargs == {
            "host": "box.local",
            "port": 443,
            "tls": True,
            "verify_tls": True,
            "base_path": "/addons/loom/api/v1",
        }
        assert done["type"] == FlowResultType.CREATE_ENTRY
        assert start.await_args.kwargs["host"] == "box.local"
        assert loom_list.await_args.kwargs["box"] == _BOX
        data = done["result"].data
        assert data[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN
        assert CONF_LOOM_TOKEN not in data
        assert CONF_LOOM_BOX not in data

    async def _open(self, hass: HomeAssistant) -> dict:
        with patch(_LOOM_RELEVANT, return_value=True), patch(_BROWSE, return_value=[]):
            menu = await hass.config_entries.flow.async_init(
                HMIP_DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            form = await hass.config_entries.flow.async_configure(menu["flow_id"], {"next_step_id": "loom"})
        assert form["step_id"] == "loom"
        return form

    async def _submit_connection(self, hass: HomeAssistant, connection: dict[str, Any]) -> dict:
        form = await self._open(hass)
        return await hass.config_entries.flow.async_configure(form["flow_id"], connection)


_PROBE_TIMEOUT = "custom_components.homematicip_local.config_flow.LOOM_PROBE_TIMEOUT_SECONDS"
_BOX_PROBE_BASE_PATH = "/addons/loom/api/v1"


def _probe_by_path(*, direct: Any, box: Any, direct_delay: float = 0.0) -> Any:
    """Return a probe stand-in that answers the daemon and the box path separately.

    An exception instance as answer is raised. The daemon's answer can be
    delayed so the box path answers first.
    """

    async def answer(**kwargs: Any) -> Any:
        if kwargs["base_path"] == _BOX_PROBE_BASE_PATH:
            outcome = box
        else:
            await asyncio.sleep(direct_delay)
            outcome = direct
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    return answer


def _direct_loom_entry(**extra: Any) -> MockConfigEntry:
    """Return a loom entry that connects to the daemon directly with a daemon token."""
    return MockConfigEntry(
        domain=HMIP_DOMAIN,
        unique_id="ABC123",
        title="Direct Loom",
        version=DomainConfigFlow.VERSION,
        data={
            CONF_BACKEND: BACKEND_LOOM,
            CONF_INSTANCE_NAME: "Direct Loom",
            CONF_HOST: "daemon.local",
            CONF_LOOM_PORT: 8119,
            CONF_TLS: False,
            CONF_VERIFY_TLS: False,
            CONF_LOOM_TOKEN: "old-token",
            **extra,
        },
    )


class TestLoomReauth:
    """Reauthentication of a loom entry that reaches the daemon directly."""

    async def test_box_answer_routes_to_the_box_pairing(self, hass: HomeAssistant) -> None:
        entry = _direct_loom_entry()
        entry.add_to_hass(hass)
        with patch(_PROBE, AsyncMock(return_value=_box_gate_probe())):
            result = await entry.start_reauth_flow(hass)
        assert result["step_id"] == "reauth_loom_box"

    async def test_ccu_entry_keeps_the_ccu_credentials_form(self, hass: HomeAssistant) -> None:
        entry = MockConfigEntry(
            domain=HMIP_DOMAIN,
            unique_id="ABC123",
            title="CCU",
            version=DomainConfigFlow.VERSION,
            data={CONF_INSTANCE_NAME: "CCU", CONF_HOST: "ccu.local", CONF_USERNAME: "u", CONF_PASSWORD: "p"},
        )
        entry.add_to_hass(hass)
        with patch(_PROBE, AsyncMock(return_value=_daemon_probe())) as probe:
            result = await entry.start_reauth_flow(hass)
        assert result["step_id"] == "reauth_confirm"
        probe.assert_not_awaited()

    async def test_empty_submission_asks_for_a_credential(self, hass: HomeAssistant) -> None:
        entry = _direct_loom_entry()
        entry.add_to_hass(hass)
        with patch(_CHECK_CONFIG, AsyncMock(return_value=None)) as check:
            form = await entry.start_reauth_flow(hass)
            result = await hass.config_entries.flow.async_configure(form["flow_id"], {CONF_LOOM_PAIR: False})
        assert result["step_id"] == "reauth_loom"
        assert result["errors"] == {"base": "loom_no_credential"}
        check.assert_not_awaited()

    async def test_no_supported_login_shows_the_error(self, hass: HomeAssistant) -> None:
        entry = _direct_loom_entry()
        entry.add_to_hass(hass)
        probe = _daemon_probe(kind="standalone", paths=frozenset({"oidc"}))
        with patch(_PROBE, AsyncMock(return_value=probe)):
            result = await entry.start_reauth_flow(hass)
        assert result["step_id"] == "reauth_loom"
        assert result["errors"] == {"base": "loom_no_supported_login"}
        assert _schema_keys(result) == set()

    async def test_pairing_failure_returns_to_the_reauth_form(self, hass: HomeAssistant) -> None:
        from openccu_loom_client import LoomPairingOffError

        entry = _direct_loom_entry()
        entry.add_to_hass(hass)
        start = AsyncMock(side_effect=LoomPairingOffError(status=503, method="POST", url="x"))
        with patch(_START_PAIRING, start):
            form = await entry.start_reauth_flow(hass)
            result = await hass.config_entries.flow.async_configure(form["flow_id"], {CONF_LOOM_PAIR: True})
            result = await TestLoomBoxIngress()._drain(hass, result)
        assert result["step_id"] == "reauth_loom"
        assert result["errors"] == {"base": "pairing_off"}
        assert entry.data[CONF_LOOM_TOKEN] == "old-token"

    async def test_pairing_replaces_the_daemon_token(self, hass: HomeAssistant) -> None:
        entry = _direct_loom_entry()
        entry.add_to_hass(hass)
        session = _FakePairingSession(result=_pair_result("approved", token="tok-paired"))
        probe = _daemon_probe(kind="ccu-addon", paths=frozenset({"pairing"}))
        with (
            patch(_PROBE, AsyncMock(return_value=probe)),
            patch(_START_PAIRING, AsyncMock(return_value=session)) as start,
            patch(_CHECK_CONFIG, AsyncMock(return_value=None)),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            form = await entry.start_reauth_flow(hass)
            assert _schema_keys(form) == {CONF_LOOM_PAIR}
            result = await hass.config_entries.flow.async_configure(form["flow_id"], {CONF_LOOM_PAIR: True})
            result = await TestLoomBoxIngress()._drain(hass, result)
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "reauth_successful"
        assert start.await_args.kwargs["host"] == "daemon.local"
        assert start.await_args.kwargs["port"] == 8119
        assert entry.data[CONF_LOOM_TOKEN] == "tok-paired"

    async def test_pasted_token_is_validated_and_stored(self, hass: HomeAssistant) -> None:
        entry = _direct_loom_entry()
        entry.add_to_hass(hass)
        probe = AsyncMock(return_value=_daemon_probe(kind="standalone", paths=frozenset({"bearer"})))
        with (
            patch(_PROBE, probe),
            patch("custom_components.homematicip_local.config_flow.ControlConfig") as control_config,
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            control_config.return_value.check_config = AsyncMock(return_value=None)
            form = await entry.start_reauth_flow(hass)
            assert form["step_id"] == "reauth_loom"
            assert _schema_keys(form) == {CONF_LOOM_TOKEN}
            result = await hass.config_entries.flow.async_configure(form["flow_id"], {CONF_LOOM_TOKEN: "new-token"})
            await hass.async_block_till_done()
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "reauth_successful"
        assert entry.data[CONF_LOOM_TOKEN] == "new-token"
        assert control_config.call_args.kwargs["data"][CONF_LOOM_TOKEN] == "new-token"
        probe.assert_awaited_once_with(host="daemon.local", port=8119, tls=False, verify_tls=False, base_path="/api/v1")

    async def test_refused_token_shows_invalid_auth(self, hass: HomeAssistant) -> None:
        entry = _direct_loom_entry()
        entry.add_to_hass(hass)
        with patch(_CHECK_CONFIG, AsyncMock(side_effect=AuthFailure("refused"))):
            form = await entry.start_reauth_flow(hass)
            result = await hass.config_entries.flow.async_configure(form["flow_id"], {CONF_LOOM_TOKEN: "bad"})
        assert result["step_id"] == "reauth_loom"
        assert result["errors"] == {"base": "invalid_auth"}
        assert entry.data[CONF_LOOM_TOKEN] == "old-token"

    @pytest.mark.parametrize("unreachable", [False, True], ids=["daemon without self-description", "probe failure"])
    async def test_undescribed_or_unreachable_daemon_gets_token_and_pairing(
        self, hass: HomeAssistant, unreachable: bool
    ) -> None:
        """Token and pairing, never the box switch, when the daemon says nothing about itself."""
        entry = _direct_loom_entry()
        entry.add_to_hass(hass)
        probe = AsyncMock(side_effect=_probe_unreachable()) if unreachable else AsyncMock(return_value=_daemon_probe())
        with patch(_PROBE, probe):
            result = await entry.start_reauth_flow(hass)
        assert result["step_id"] == "reauth_loom"
        assert _schema_keys(result) == {CONF_LOOM_TOKEN, CONF_LOOM_PAIR}


class TestLoomReconfigure:
    """Reconfiguration of a loom entry edits the daemon connection, not CCU fields."""

    async def test_box_entry_keeps_its_box_token_when_left_empty(self, hass: HomeAssistant) -> None:
        entry = TestOptionsFlowLoom()._loom_entry(box=True)
        entry.add_to_hass(hass)
        with (
            patch(_CHECK_CONFIG, AsyncMock(return_value=None)),
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            form = await entry.start_reconfigure_flow(hass)
            assert _schema_keys(form) == {CONF_HOST, CONF_LOOM_PORT, CONF_TLS, CONF_VERIFY_TLS, CONF_LOOM_BOX_TOKEN}
            result = await hass.config_entries.flow.async_configure(
                form["flow_id"],
                {CONF_HOST: "box2.local", CONF_TLS: True, CONF_VERIFY_TLS: True, CONF_LOOM_BOX_TOKEN: ""},
            )
            await hass.async_block_till_done()
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "reconfigure_successful"
        assert entry.data[CONF_HOST] == "box2.local"
        assert entry.data[CONF_LOOM_BOX_TOKEN] == _BOX_TOKEN

    async def test_direct_entry_updates_the_connection(self, hass: HomeAssistant) -> None:
        entry = TestOptionsFlowLoom()._loom_entry()
        entry.add_to_hass(hass)
        with (
            patch("custom_components.homematicip_local.config_flow.ControlConfig") as control_config,
            patch("custom_components.homematicip_local.async_setup_entry", return_value=True),
        ):
            control_config.return_value.check_config = AsyncMock(return_value=None)
            form = await entry.start_reconfigure_flow(hass)
            assert form["step_id"] == "reconfigure_loom"
            assert _schema_keys(form) == {CONF_HOST, CONF_LOOM_PORT, CONF_TLS, CONF_VERIFY_TLS, CONF_LOOM_TOKEN}
            result = await hass.config_entries.flow.async_configure(
                form["flow_id"],
                {
                    CONF_HOST: "daemon2.local",
                    CONF_LOOM_PORT: 8120,
                    CONF_TLS: False,
                    CONF_VERIFY_TLS: False,
                    CONF_LOOM_TOKEN: "new-token",
                },
            )
            await hass.async_block_till_done()
        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "reconfigure_successful"
        assert entry.data[CONF_HOST] == "daemon2.local"
        assert entry.data[CONF_LOOM_PORT] == 8120
        assert entry.data[CONF_TLS] is False
        assert entry.data[CONF_LOOM_TOKEN] == "new-token"
        assert control_config.call_args.kwargs["entry_id"] == entry.entry_id

    async def test_failed_check_stays_on_the_form(self, hass: HomeAssistant) -> None:
        entry = TestOptionsFlowLoom()._loom_entry()
        entry.add_to_hass(hass)
        with patch(_CHECK_CONFIG, AsyncMock(side_effect=InvalidConfig("daemon refused"))):
            form = await entry.start_reconfigure_flow(hass)
            result = await hass.config_entries.flow.async_configure(
                form["flow_id"], {CONF_HOST: "daemon2.local", CONF_TLS: True, CONF_VERIFY_TLS: True}
            )
        assert result["step_id"] == "reconfigure_loom"
        assert result["errors"] == {"base": "invalid_config"}
        assert entry.data[CONF_HOST] == const.HOST
