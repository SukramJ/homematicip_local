"""Tests for Homematic(IP) Local blueprints."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from homeassistant.components.automation import DOMAIN as AUTOMATION_DOMAIN
from homeassistant.components.automation.config import AUTOMATION_BLUEPRINT_SCHEMA
from homeassistant.components.blueprint.errors import MissingInput
from homeassistant.components.blueprint.models import Blueprint, BlueprintInputs
from homeassistant.core import HomeAssistant, SupportsResponse
from homeassistant.setup import async_setup_component
from homeassistant.util.yaml import load_yaml_dict

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).parent.parent
_AUTOMATION_DIR = _REPO_ROOT / "blueprints" / "automation"
_COMMUNITY_DIR = _REPO_ROOT / "blueprints" / "community"

_ALL_BLUEPRINT_FILES: list[Path] = sorted(list(_AUTOMATION_DIR.glob("*.yaml")) + list(_COMMUNITY_DIR.glob("*.yaml")))

_BUTTON_BLUEPRINT_FILES: list[Path] = [p for p in _ALL_BLUEPRINT_FILES if "actions-for" in p.name]


# ---------------------------------------------------------------------------
# Helpers – reusable foundation for blueprint tests
# ---------------------------------------------------------------------------
def load_blueprint(*, path: Path) -> Blueprint:
    """Load a blueprint YAML file and return a validated Blueprint object."""
    data = load_yaml_dict(str(path))
    return Blueprint(
        data,
        path=path.name,
        expected_domain="automation",
        schema=AUTOMATION_BLUEPRINT_SCHEMA,
    )


def make_inputs(
    *,
    blueprint: Blueprint,
    overrides: dict[str, Any] | None = None,
) -> BlueprintInputs:
    """
    Create BlueprintInputs for *blueprint*, filling required inputs with safe dummy values.

    ``overrides`` lets individual tests supply specific values.
    """
    dummy_values = _dummy_values_for(blueprint=blueprint)
    if overrides:
        dummy_values.update(overrides)
    config: dict[str, Any] = {
        "use_blueprint": {
            "path": blueprint.metadata.get("source_url", "test.yaml"),
            "input": dummy_values,
        },
    }
    return BlueprintInputs(blueprint, config)


def resolve_config(
    *,
    blueprint: Blueprint,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the fully-substituted automation config for *blueprint*."""
    bp_inputs = make_inputs(blueprint=blueprint, overrides=overrides)
    bp_inputs.validate()
    return bp_inputs.async_substitute()


async def setup_automation_from_blueprint(
    *,
    hass: HomeAssistant,
    blueprint: Blueprint,
    overrides: dict[str, Any] | None = None,
    automation_id: str = "test_bp",
) -> dict[str, Any]:
    """Register a HA automation backed by *blueprint* and return the resolved config."""
    config = resolve_config(blueprint=blueprint, overrides=overrides)
    config["id"] = automation_id
    assert await async_setup_component(
        hass,
        AUTOMATION_DOMAIN,
        {AUTOMATION_DOMAIN: [config]},
    )
    await hass.async_block_till_done()
    return config


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
_SELECTOR_DUMMY_MAP: dict[str, Any] = {
    "device": "dummy_device_id",
    "entity": "sensor.dummy",
    "text": "dummy_text",
    "number": 0,
    "boolean": False,
    "action": [],
    "select": "",
    "target": {},
    "area": "dummy_area",
    "time": "12:00:00",
}


def _dummy_for_selector(*, selector: dict[str, Any]) -> Any:
    """Return a safe dummy value for a given HA selector."""
    selector_type = next(iter(selector))
    return _SELECTOR_DUMMY_MAP.get(selector_type, "dummy")


def _dummy_values_for(*, blueprint: Blueprint) -> dict[str, Any]:
    """Generate dummy input values for all *required* inputs (those without a default)."""
    values: dict[str, Any] = {}
    for name, definition in blueprint.inputs.items():
        if definition is None:
            values[name] = "dummy"
            continue
        if "default" not in definition:
            selector = definition.get("selector", {})
            if selector:
                values[name] = _dummy_for_selector(selector=selector)
            else:
                values[name] = "dummy"
    return values


# ---------------------------------------------------------------------------
# Parametrize helpers
# ---------------------------------------------------------------------------
def _bp_id(path: Path) -> str:
    """Return a short test-id from a blueprint path."""
    return path.stem


# ═══════════════════════════════════════════════════════════════════════════
# 1. Schema validation – every blueprint must load without errors
# ═══════════════════════════════════════════════════════════════════════════
class TestBlueprintSchemaValidation:
    """Validate that every blueprint YAML passes HA's schema validation."""

    @pytest.mark.parametrize("path", _ALL_BLUEPRINT_FILES, ids=_bp_id)
    def test_blueprint_has_min_version(self, *, path: Path) -> None:
        """Every blueprint must declare a minimum HA version."""
        bp = load_blueprint(path=path)
        meta = bp.metadata
        assert "homeassistant" in meta, f"{path.name}: missing 'homeassistant' key"
        assert "min_version" in meta["homeassistant"], f"{path.name}: missing 'min_version'"

    @pytest.mark.parametrize("path", _ALL_BLUEPRINT_FILES, ids=_bp_id)
    def test_blueprint_has_required_metadata(self, *, path: Path) -> None:
        """Every blueprint must have name, domain, and source_url."""
        bp = load_blueprint(path=path)
        meta = bp.metadata
        assert "name" in meta
        assert meta["domain"] == "automation"
        assert "source_url" in meta

    @pytest.mark.parametrize("path", _ALL_BLUEPRINT_FILES, ids=_bp_id)
    def test_blueprint_loads_successfully(self, *, path: Path) -> None:
        """Blueprint YAML must parse and pass AUTOMATION_BLUEPRINT_SCHEMA."""
        bp = load_blueprint(path=path)
        assert bp.name
        assert bp.domain == "automation"


# ═══════════════════════════════════════════════════════════════════════════
# 2. Input validation – defaults, required inputs, missing inputs
# ═══════════════════════════════════════════════════════════════════════════
class TestBlueprintInputValidation:
    """Validate input definitions and default handling."""

    @pytest.mark.parametrize("path", _BUTTON_BLUEPRINT_FILES, ids=_bp_id)
    def test_action_inputs_default_to_empty_list(self, *, path: Path) -> None:
        """All action_* inputs on button blueprints must default to []."""
        bp = load_blueprint(path=path)
        for name, definition in bp.inputs.items():
            if name.startswith("action_"):
                assert definition is not None, f"'{name}' has no definition"
                assert "default" in definition, f"'{name}' has no default"
                assert definition["default"] == [], f"'{name}' default is not []"

    @pytest.mark.parametrize("path", _ALL_BLUEPRINT_FILES, ids=_bp_id)
    def test_defaults_are_applied(self, *, path: Path) -> None:
        """Inputs with declared defaults must appear in inputs_with_default."""
        bp = load_blueprint(path=path)
        bp_inputs = make_inputs(blueprint=bp)
        merged = bp_inputs.inputs_with_default

        for name, definition in bp.inputs.items():
            if definition and "default" in definition:
                assert name in merged, f"Default for '{name}' not in merged inputs"

    @pytest.mark.parametrize("path", _ALL_BLUEPRINT_FILES, ids=_bp_id)
    def test_inputs_with_defaults_validate(self, *, path: Path) -> None:
        """Providing only required inputs (relying on defaults for the rest) must pass."""
        bp = load_blueprint(path=path)
        bp_inputs = make_inputs(blueprint=bp)
        bp_inputs.validate()  # Must not raise

    @pytest.mark.parametrize("path", _BUTTON_BLUEPRINT_FILES, ids=_bp_id)
    def test_missing_required_device_raises(self, *, path: Path) -> None:
        """Omitting the required 'remote' device input must raise MissingInput."""
        bp = load_blueprint(path=path)
        config: dict[str, Any] = {
            "use_blueprint": {
                "path": path.name,
                "input": {},  # No inputs at all
            },
        }
        bp_inputs = BlueprintInputs(bp, config)
        with pytest.raises(MissingInput):
            bp_inputs.validate()


# ═══════════════════════════════════════════════════════════════════════════
# 3. Template substitution – resolved config structure checks
# ═══════════════════════════════════════════════════════════════════════════
class TestBlueprintSubstitution:
    """Verify that resolved configs have the expected structure."""

    @pytest.mark.parametrize("path", _BUTTON_BLUEPRINT_FILES, ids=_bp_id)
    def test_button_blueprints_trigger_on_keypress(self, *, path: Path) -> None:
        """All button blueprints must trigger on homematic.keypress."""
        bp = load_blueprint(path=path)
        config = resolve_config(blueprint=bp)
        triggers = config.get("triggers", config.get("trigger", []))
        trigger = triggers[0] if isinstance(triggers, list) else triggers
        assert trigger["event_type"] == "homematic.keypress"

    @pytest.mark.parametrize("path", _BUTTON_BLUEPRINT_FILES, ids=_bp_id)
    def test_button_blueprints_use_parallel_mode(self, *, path: Path) -> None:
        """Button blueprints must use parallel mode."""
        bp = load_blueprint(path=path)
        config = resolve_config(blueprint=bp)
        assert config.get("mode") == "parallel"

    @pytest.mark.parametrize(
        ("filename", "event_type"),
        [
            ("homematicip_local_show_device_error.yaml", "homematic.device_error"),
            ("homematicip_local_persistent_notification.yaml", "homematic.device_availability"),
            ("homematicip_local_reactivate_single_device.yaml", "homematic.device_availability"),
            ("homematicip_local_reactivate_device_by_model.yaml", "homematic.device_availability"),
            ("homematicip_local_reactivate_device_full.yaml", "homematic.device_availability"),
        ],
    )
    def test_event_trigger_type(self, *, filename: str, event_type: str) -> None:
        """The resolved trigger must listen to the correct event type."""
        bp = load_blueprint(path=_AUTOMATION_DIR / filename)
        config = resolve_config(blueprint=bp)
        triggers = config.get("triggers", config.get("trigger", []))
        trigger = triggers[0] if isinstance(triggers, list) else triggers
        assert trigger["event_type"] == event_type

    def test_reactivate_delay_substitution(self) -> None:
        """The delay_seconds input must appear in the resolved delay action."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local_reactivate_device_full.yaml")
        config = resolve_config(blueprint=bp, overrides={"delay_seconds": 42})
        actions = config.get("actions", config.get("action", []))
        delay_action = actions[0]
        assert delay_action == {"delay": {"seconds": 42}}

    @pytest.mark.parametrize("path", _ALL_BLUEPRINT_FILES, ids=_bp_id)
    def test_substitution_produces_valid_config(self, *, path: Path) -> None:
        """async_substitute() must return a dict with 'triggers' and 'actions'."""
        bp = load_blueprint(path=path)
        config = resolve_config(blueprint=bp)
        assert "triggers" in config or "trigger" in config
        assert "actions" in config or "action" in config


# ═══════════════════════════════════════════════════════════════════════════
# 4. Full-flow tests – fire events and verify actions
# ═══════════════════════════════════════════════════════════════════════════
class TestBlueprintFullFlow:
    """End-to-end tests: set up automation from blueprint, fire event, assert service call."""

    @pytest.mark.asyncio
    async def test_2button_ignores_other_device(
        self,
        hass: HomeAssistant,
    ) -> None:
        """A keypress from a non-selected device must be ignored."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        test_calls = async_mock_service(hass, "test", "action_top_short")

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["selected_device"],
                "action_top_short": [{"action": "test.action_top_short"}],
            },
        )

        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "XXXXXX",
                "device_id": "wrong_device",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 0

    @pytest.mark.asyncio
    async def test_2button_short_press_top(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Pressing top button short on 2-button device must execute the configured action."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        # Register a mock service that the blueprint action will call
        test_calls = async_mock_service(hass, "test", "action_top_short")

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["test_device_id"],
                "action_top_short": [{"action": "test.action_top_short"}],
            },
        )

        # Also mock get_link_peers (called by the direct-link check)
        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "test_device_id",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_4button_krca_subtype_mapping(
        self,
        hass: HomeAssistant,
    ) -> None:
        """KRCA 4-button uses non-sequential subtypes (2,1,4,3). Verify button 1 maps to subtype 2."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-key_ring_remote_control.yaml")

        test_calls = async_mock_service(hass, "test", "btn1")
        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["krca"],
                "action_1_short": [{"action": "test.btn1"}],
            },
        )

        # Button 1 on KRCA = subtype 2
        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "krca",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_6button_long_press_right_middle(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Long-pressing right-middle on 6-button must execute the configured action."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-6-button.yaml")

        test_calls = async_mock_service(hass, "test", "right_middle_long")
        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev6"],
                "action_right_middle_long": [{"action": "test.right_middle_long"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev6",
                "type": "press_long",
                "subtype": 4,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_8button_press_button_5(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Short-pressing button 5 on 8-button device must execute the correct action."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-8-button.yaml")

        test_calls = async_mock_service(hass, "test", "btn5")
        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev8"],
                "action_5_short": [{"action": "test.btn5"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev8",
                "type": "press_short",
                "subtype": 5,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_button_multi_device_support(
        self,
        hass: HomeAssistant,
    ) -> None:
        """A blueprint configured with multiple devices must respond to all of them."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        test_calls = async_mock_service(hass, "test", "multi")
        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["device_a", "device_b"],
                "action_top_short": [{"action": "test.multi"}],
            },
        )

        # Device A
        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "AAA",
                "device_id": "device_a",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()
        assert len(test_calls) == 1

        # Device B
        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "BBB",
                "device_id": "device_b",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()
        assert len(test_calls) == 2

    @pytest.mark.asyncio
    async def test_button_no_action_when_empty(
        self,
        hass: HomeAssistant,
    ) -> None:
        """When no action is configured for a button, nothing must happen."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        # All actions default to [] – no overrides
        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={"remote": ["dev"]},
        )

        # Fire a keypress – nothing should be called (no crash either)
        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

    @pytest.mark.asyncio
    async def test_persistent_notification_dismissed_on_available(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Device becoming available again must dismiss the notification."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local_persistent_notification.yaml")
        await setup_automation_from_blueprint(hass=hass, blueprint=bp)

        dismiss_calls = async_mock_service(hass, "persistent_notification", "dismiss")

        hass.bus.async_fire(
            "homematic.device_availability",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "unavailable": False,
                "identifier": "0001D3C99C5A72_availability",
                "title": "HOMEMATICIP_LOCAL Device Availability",
                "message": "",
            },
        )
        await hass.async_block_till_done()

        assert len(dismiss_calls) == 1

    @pytest.mark.asyncio
    async def test_persistent_notification_on_unavailable(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Device becoming unavailable must trigger a persistent notification."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local_persistent_notification.yaml")
        await setup_automation_from_blueprint(hass=hass, blueprint=bp)

        create_calls = async_mock_service(hass, "persistent_notification", "create")

        hass.bus.async_fire(
            "homematic.device_availability",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "unavailable": True,
                "identifier": "0001D3C99C5A72_availability",
                "title": "HOMEMATICIP_LOCAL Device Availability",
                "message": "Device 0001D3C99C5A72 is not available",
            },
        )
        await hass.async_block_till_done()

        assert len(create_calls) == 1
        assert create_calls[0].data["notification_id"] == "0001D3C99C5A72_availability"

    @pytest.mark.asyncio
    async def test_reactivate_by_model_filters_correctly(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Reactivate-by-model must only react to the configured model."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local_reactivate_device_by_model.yaml")
        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={"model": "HmIP-BROLL", "delay_seconds": 0},
        )

        force_calls = async_mock_service(hass, "homematicip_local", "force_device_availability")

        # Wrong model
        hass.bus.async_fire(
            "homematic.device_availability",
            {
                "interface_id": "hmip_rf",
                "address": "OTHER",
                "device_id": "dev1",
                "model": "HmIP-BSM",
                "unavailable": True,
                "identifier": "OTHER_availability",
                "title": "test",
                "message": "test",
            },
        )
        await hass.async_block_till_done()
        assert len(force_calls) == 0

        # Correct model
        hass.bus.async_fire(
            "homematic.device_availability",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev2",
                "model": "HmIP-BROLL",
                "unavailable": True,
                "identifier": "0001D3C99C5A72_availability",
                "title": "test",
                "message": "test",
            },
        )
        await hass.async_block_till_done()
        assert len(force_calls) == 1
        assert force_calls[0].data["device_id"] == "dev2"

    @pytest.mark.asyncio
    async def test_reactivate_full_calls_force_availability(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Unavailability event must trigger force_device_availability after delay."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local_reactivate_device_full.yaml")
        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={"delay_seconds": 0},
        )

        force_calls = async_mock_service(hass, "homematicip_local", "force_device_availability")

        hass.bus.async_fire(
            "homematic.device_availability",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "abc123",
                "unavailable": True,
                "identifier": "0001D3C99C5A72_availability",
                "title": "test",
                "message": "test",
            },
        )
        await hass.async_block_till_done()

        assert len(force_calls) == 1
        assert force_calls[0].data["device_id"] == "abc123"

    @pytest.mark.asyncio
    async def test_reactivate_single_only_triggers_for_selected_device(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Reactivate-single must only react to the configured device_id."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local_reactivate_single_device.yaml")
        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={"device_id": "my_device", "delay_seconds": 0},
        )

        force_calls = async_mock_service(hass, "homematicip_local", "force_device_availability")

        # Fire for a *different* device – must NOT trigger
        hass.bus.async_fire(
            "homematic.device_availability",
            {
                "interface_id": "hmip_rf",
                "address": "OTHER",
                "device_id": "other_device",
                "unavailable": True,
                "identifier": "OTHER_availability",
                "title": "test",
                "message": "test",
            },
        )
        await hass.async_block_till_done()
        assert len(force_calls) == 0

        # Fire for the correct device – must trigger
        hass.bus.async_fire(
            "homematic.device_availability",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "my_device",
                "unavailable": True,
                "identifier": "0001D3C99C5A72_availability",
                "title": "test",
                "message": "test",
            },
        )
        await hass.async_block_till_done()
        assert len(force_calls) == 1

    @pytest.mark.asyncio
    async def test_show_device_error_creates_notification(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Firing a device_error event with error=true must call persistent_notification.create."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local_show_device_error.yaml")
        await setup_automation_from_blueprint(hass=hass, blueprint=bp)

        create_calls = async_mock_service(hass, "persistent_notification", "create")

        hass.bus.async_fire(
            "homematic.device_error",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "type": "STICKY_UN_REACH",
                "value": True,
                "error": True,
                "identifier": "0001D3C99C5A72_STICKY_UN_REACH",
                "title": "HOMEMATICIP_LOCAL Device Error",
                "message": "TestDevice/0001D3C99C5A72 on interface hmip_rf: Sticky Un Reach",
                "error_value": True,
            },
        )
        await hass.async_block_till_done()

        assert len(create_calls) == 1
        assert create_calls[0].data["notification_id"] == "0001D3C99C5A72_STICKY_UN_REACH"
        assert "TestDevice" in create_calls[0].data["message"]

    @pytest.mark.asyncio
    async def test_show_device_error_dismisses_notification(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Firing a device_error event with error=false must dismiss the notification."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local_show_device_error.yaml")
        await setup_automation_from_blueprint(hass=hass, blueprint=bp)

        dismiss_calls = async_mock_service(hass, "persistent_notification", "dismiss")

        hass.bus.async_fire(
            "homematic.device_error",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "type": "STICKY_UN_REACH",
                "value": False,
                "error": False,
                "identifier": "0001D3C99C5A72_STICKY_UN_REACH",
                "title": "HOMEMATICIP_LOCAL Device Error",
                "message": "",
                "error_value": False,
            },
        )
        await hass.async_block_till_done()

        assert len(dismiss_calls) == 1
        assert dismiss_calls[0].data["notification_id"] == "0001D3C99C5A72_STICKY_UN_REACH"


# ═══════════════════════════════════════════════════════════════════════════
# 5. Direct-link detection tests
# ═══════════════════════════════════════════════════════════════════════════
class TestDirectLinkDetection:
    """Test the CCU direct-link warning and skip features on button blueprints."""

    @pytest.mark.asyncio
    async def test_direct_link_no_notification_when_no_action_configured(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Even with peers, no notification if the pressed button has no configured action."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        notify_calls = async_mock_service(hass, "persistent_notification", "create")

        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={"0001D3C99C5A72:2": ["0002AABB112233:1"]},
            supports_response=SupportsResponse.OPTIONAL,
        )

        # action_top_short is NOT configured (defaults to [])
        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev"],
                "notify_on_direct_links": True,
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

        # No notification because no action is configured for that button
        assert len(notify_calls) == 0

    @pytest.mark.asyncio
    async def test_direct_link_notification_when_peers_exist(
        self,
        hass: HomeAssistant,
    ) -> None:
        """When get_link_peers returns peers and notify is enabled, a notification must be created."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        notify_calls = async_mock_service(hass, "persistent_notification", "create")
        test_calls = async_mock_service(hass, "test", "my_action")

        # Mock get_link_peers returning actual peers
        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={"0001D3C99C5A72:2": ["0002AABB112233:1"]},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev"],
                "notify_on_direct_links": True,
                "skip_actions_when_direct_link": False,
                "action_top_short": [{"action": "test.my_action"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

        # Notification must have been created
        assert len(notify_calls) == 1
        assert "direct" in notify_calls[0].data["title"].lower()
        # Action must still execute (skip is off)
        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_direct_link_on_4button_krca_blueprint(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Direct-link skip must also work on the KRCA 4-button blueprint."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-key_ring_remote_control.yaml")

        test_calls = async_mock_service(hass, "test", "btn1")
        async_mock_service(hass, "persistent_notification", "create")

        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={"0001D3C99C5A72:2": ["PEER:1"]},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["krca"],
                "skip_actions_when_direct_link": True,
                "action_1_short": [{"action": "test.btn1"}],
            },
        )

        # Button 1 on KRCA = subtype 2
        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "krca",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 0

    @pytest.mark.asyncio
    async def test_direct_link_on_6button_blueprint(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Direct-link skip must also work on the 6-button blueprint."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-6-button.yaml")

        test_calls = async_mock_service(hass, "test", "skip_me")
        async_mock_service(hass, "persistent_notification", "create")

        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={"0001D3C99C5A72:3": ["0002AABB112233:1"]},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev6"],
                "skip_actions_when_direct_link": True,
                "action_left_middle_short": [{"action": "test.skip_me"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev6",
                "type": "press_short",
                "subtype": 3,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 0

    @pytest.mark.asyncio
    async def test_direct_link_on_8button_blueprint(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Direct-link notification must also work on the 8-button blueprint."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-8-button.yaml")

        notify_calls = async_mock_service(hass, "persistent_notification", "create")
        test_calls = async_mock_service(hass, "test", "btn3")

        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={"0001D3C99C5A72:3": ["PEER:1"]},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev8"],
                "notify_on_direct_links": True,
                "skip_actions_when_direct_link": False,
                "action_3_short": [{"action": "test.btn3"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev8",
                "type": "press_short",
                "subtype": 3,
            },
        )
        await hass.async_block_till_done()

        assert len(notify_calls) == 1
        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_direct_link_skip_prevents_action(
        self,
        hass: HomeAssistant,
    ) -> None:
        """When skip_actions_when_direct_link is true and peers exist, the action must be skipped."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        test_calls = async_mock_service(hass, "test", "should_not_run")
        async_mock_service(hass, "persistent_notification", "create")

        # Mock get_link_peers returning actual peers
        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={"0001D3C99C5A72:2": ["0002AABB112233:1"]},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev"],
                "notify_on_direct_links": False,
                "skip_actions_when_direct_link": True,
                "action_top_short": [{"action": "test.should_not_run"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

        # Action must NOT have been called
        assert len(test_calls) == 0

    @pytest.mark.asyncio
    async def test_no_direct_link_no_notification(
        self,
        hass: HomeAssistant,
    ) -> None:
        """When get_link_peers returns empty, no notification must be created."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        notify_calls = async_mock_service(hass, "persistent_notification", "create")
        test_calls = async_mock_service(hass, "test", "my_action")

        # Mock get_link_peers returning NO peers
        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev"],
                "notify_on_direct_links": True,
                "skip_actions_when_direct_link": True,
                "action_top_short": [{"action": "test.my_action"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": "press_short",
                "subtype": 2,
            },
        )
        await hass.async_block_till_done()

        # No notification (no peers)
        assert len(notify_calls) == 0
        # Action still executes (no peers → no skip)
        assert len(test_calls) == 1


# ═══════════════════════════════════════════════════════════════════════════
# 6. Community blueprint full-flow tests
# ═══════════════════════════════════════════════════════════════════════════
class TestCommunityBlueprints:
    """Full-flow tests for community-contributed blueprints."""

    @pytest.mark.asyncio
    async def test_12button_press_button_12(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Long-pressing button 12 on 12-button device must execute the configured action."""
        bp = load_blueprint(path=_COMMUNITY_DIR / "homematicip_local-actions-for-12-button.yaml")

        test_calls = async_mock_service(hass, "test", "btn12_long")

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": "dev12",
                "action_12_long": [{"action": "test.btn12_long"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev12",
                "type": "press_long",
                "subtype": 12,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_4button_fm_press_button_3(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Short-pressing button 3 on 4-button flush mount must execute the configured action."""
        bp = load_blueprint(path=_COMMUNITY_DIR / "homematicip_local-actions-for-4-button-fm.yaml")

        test_calls = async_mock_service(hass, "test", "btn3_short")

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": "dev_fm",
                "action_3_short": [{"action": "test.btn3_short"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev_fm",
                "type": "press_short",
                "subtype": 3,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_6button_ho_executes_without_direct_links(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Community 6-button-ho: without direct links the action must execute."""
        bp = load_blueprint(path=_COMMUNITY_DIR / "homematicip_local-actions-for-6-button-ho.yaml")

        test_calls = async_mock_service(hass, "test", "right_bottom")

        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev_ho"],
                "action_right_bottom_short": [{"action": "test.right_bottom"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev_ho",
                "type": "press_short",
                "subtype": 6,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    async def test_6button_ho_multi_device_with_direct_link_skip(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Community 6-button-ho: multi-device + direct-link skip must work."""
        bp = load_blueprint(path=_COMMUNITY_DIR / "homematicip_local-actions-for-6-button-ho.yaml")

        test_calls = async_mock_service(hass, "test", "left_top")
        async_mock_service(hass, "persistent_notification", "create")

        async_mock_service(
            hass,
            "homematicip_local",
            "get_link_peers",
            response={"0001D3C99C5A72:1": ["PEER:1"]},
            supports_response=SupportsResponse.OPTIONAL,
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev_a", "dev_b"],
                "skip_actions_when_direct_link": True,
                "action_left_top_short": [{"action": "test.left_top"}],
            },
        )

        # Device A – has direct link → action skipped
        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev_a",
                "type": "press_short",
                "subtype": 1,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 0


# ═══════════════════════════════════════════════════════════════════════════
# 7. Exhaustive button-subtype mapping tests
# ═══════════════════════════════════════════════════════════════════════════
class TestAllButtonSubtypes:
    """Verify every button/press-type combination triggers the correct action."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("action_name", "subtype", "press_type"),
        [
            ("action_top_short", 2, "press_short"),
            ("action_top_long", 2, "press_long"),
            ("action_bottom_short", 1, "press_short"),
            ("action_bottom_long", 1, "press_long"),
        ],
    )
    async def test_2button_all_subtypes(
        self,
        hass: HomeAssistant,
        *,
        action_name: str,
        subtype: int,
        press_type: str,
    ) -> None:
        """Every 2-button combination must map to the correct action."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-2-button.yaml")

        test_calls = async_mock_service(hass, "test", action_name)
        async_mock_service(
            hass, "homematicip_local", "get_link_peers", response={}, supports_response=SupportsResponse.OPTIONAL
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev"],
                action_name: [{"action": f"test.{action_name}"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": press_type,
                "subtype": subtype,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("action_name", "subtype", "press_type"),
        [
            ("action_1_short", 2, "press_short"),
            ("action_1_long", 2, "press_long"),
            ("action_2_short", 1, "press_short"),
            ("action_2_long", 1, "press_long"),
            ("action_3_short", 4, "press_short"),
            ("action_3_long", 4, "press_long"),
            ("action_4_short", 3, "press_short"),
            ("action_4_long", 3, "press_long"),
        ],
    )
    async def test_4button_krca_all_subtypes(
        self,
        hass: HomeAssistant,
        *,
        action_name: str,
        subtype: int,
        press_type: str,
    ) -> None:
        """Every KRCA 4-button combination must map to the correct (non-sequential) subtype."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-key_ring_remote_control.yaml")

        test_calls = async_mock_service(hass, "test", action_name)
        async_mock_service(
            hass, "homematicip_local", "get_link_peers", response={}, supports_response=SupportsResponse.OPTIONAL
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev"],
                action_name: [{"action": f"test.{action_name}"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": press_type,
                "subtype": subtype,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("action_name", "subtype", "press_type"),
        [
            ("action_left_top_short", 1, "press_short"),
            ("action_left_top_long", 1, "press_long"),
            ("action_right_top_short", 2, "press_short"),
            ("action_right_top_long", 2, "press_long"),
            ("action_left_middle_short", 3, "press_short"),
            ("action_left_middle_long", 3, "press_long"),
            ("action_right_middle_short", 4, "press_short"),
            ("action_right_middle_long", 4, "press_long"),
            ("action_left_bottom_short", 5, "press_short"),
            ("action_left_bottom_long", 5, "press_long"),
            ("action_right_bottom_short", 6, "press_short"),
            ("action_right_bottom_long", 6, "press_long"),
        ],
    )
    async def test_6button_all_subtypes(
        self,
        hass: HomeAssistant,
        *,
        action_name: str,
        subtype: int,
        press_type: str,
    ) -> None:
        """Every 6-button combination must map to the correct action."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-6-button.yaml")

        test_calls = async_mock_service(hass, "test", action_name)
        async_mock_service(
            hass, "homematicip_local", "get_link_peers", response={}, supports_response=SupportsResponse.OPTIONAL
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev"],
                action_name: [{"action": f"test.{action_name}"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": press_type,
                "subtype": subtype,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("action_name", "subtype", "press_type"),
        [
            ("action_1_short", 1, "press_short"),
            ("action_1_long", 1, "press_long"),
            ("action_2_short", 2, "press_short"),
            ("action_2_long", 2, "press_long"),
            ("action_3_short", 3, "press_short"),
            ("action_3_long", 3, "press_long"),
            ("action_4_short", 4, "press_short"),
            ("action_4_long", 4, "press_long"),
            ("action_5_short", 5, "press_short"),
            ("action_5_long", 5, "press_long"),
            ("action_6_short", 6, "press_short"),
            ("action_6_long", 6, "press_long"),
            ("action_7_short", 7, "press_short"),
            ("action_7_long", 7, "press_long"),
            ("action_8_short", 8, "press_short"),
            ("action_8_long", 8, "press_long"),
        ],
    )
    async def test_8button_all_subtypes(
        self,
        hass: HomeAssistant,
        *,
        action_name: str,
        subtype: int,
        press_type: str,
    ) -> None:
        """Every 8-button combination must map to the correct action."""
        bp = load_blueprint(path=_AUTOMATION_DIR / "homematicip_local-actions-for-8-button.yaml")

        test_calls = async_mock_service(hass, "test", action_name)
        async_mock_service(
            hass, "homematicip_local", "get_link_peers", response={}, supports_response=SupportsResponse.OPTIONAL
        )

        await setup_automation_from_blueprint(
            hass=hass,
            blueprint=bp,
            overrides={
                "remote": ["dev"],
                action_name: [{"action": f"test.{action_name}"}],
            },
        )

        hass.bus.async_fire(
            "homematic.keypress",
            {
                "interface_id": "hmip_rf",
                "address": "0001D3C99C5A72",
                "device_id": "dev",
                "type": press_type,
                "subtype": subtype,
            },
        )
        await hass.async_block_till_done()

        assert len(test_calls) == 1
