# CLAUDE.md - AI Assistant Guide for Homematic(IP) Local Integration

This document provides comprehensive guidance for AI assistants working with the Homematic(IP) Local for OpenCCU codebase.

## Project Overview

**Project Name:** Homematic(IP) Local for OpenCCU
**Type:** Home Assistant Custom Integration
**Version:** 2.0.0
**Primary Language:** Python 3.13+
**Domain:** `homematicip_local`

This is a production-quality Home Assistant custom integration that enables local communication with Homematic and HomematicIP smart home devices through various hubs (CCU2/3, OpenCCU, Debmatic, Homegear). It provides bi-directional communication using XML-RPC for device control and push state updates, and JSON-RPC for fetching device names and room information.

## Repository Structure

```
homematicip_local/
├── custom_components/homematicip_local/  # Main integration code (~7,752 lines)
│   ├── __init__.py                       # Integration setup & entry point
│   ├── config_flow.py                    # Configuration UI & validation (26.8K lines)
│   ├── control_unit.py                   # Central control logic (33.9K lines)
│   ├── services.py                       # Service registration (42.1K lines)
│   ├── services.yaml                     # Service schema definitions
│   ├── generic_entity.py                 # Base entity class (21.8K lines)
│   ├── entity_helpers.py                 # Entity creation utilities (44.4K lines)
│   ├── const.py                          # Constants & enums
│   ├── support.py                        # Helper functions
│   │
│   ├── Platform Implementations (entity types):
│   │   ├── binary_sensor.py, button.py
│   │   ├── climate.py                    # Thermostat/climate (18.5K lines)
│   │   ├── cover.py, light.py, lock.py
│   │   ├── number.py, select.py, sensor.py
│   │   ├── siren.py, switch.py, text.py
│   │   ├── update.py, valve.py
│   │
│   ├── Integration Features:
│   │   ├── device_action.py              # Device automation actions
│   │   ├── device_trigger.py             # Device automation triggers
│   │   ├── event.py                      # Custom event handling
│   │   ├── mqtt.py                       # MQTT integration
│   │   ├── logbook.py                    # Logbook integration
│   │   ├── diagnostics.py                # Diagnostic data export
│   │   ├── repairs.py                    # Issue registry integration
│   │
│   ├── Configuration:
│   │   ├── manifest.json                 # Integration metadata
│   │   ├── strings.json                  # Translatable strings (52K+ lines)
│   │   ├── translations/                 # Language files (en.json, de.json)
│   │   ├── icons.json                    # Custom icon mappings
│   │   └── quality_scale.yaml            # HACS quality score
│   │
├── tests/                                # Test suite (~1,898 lines, pytest-based)
│   ├── conftest.py                       # Test fixtures & mocks
│   ├── test_config_flow.py               # Configuration flow tests (38K+ lines)
│   ├── test_init.py                      # Integration initialization tests
│   ├── test_*.py                         # Platform-specific tests
│   │
├── .github/workflows/                    # CI/CD pipelines
│   ├── test-run.yaml                     # Main test pipeline (Python 3.13, 3.14)
│   ├── pre-commit.yml                    # Code quality gate
│   ├── hacs_validate.yaml                # HACS validation
│   └── hassfest.yaml                     # HA manifest validation
│   │
├── blueprints/automation/                # HA automation blueprints
├── script/                               # Development helper scripts
│   ├── bootstrap                         # Initialize dev environment
│   ├── setup                             # Setup script
│   ├── run-in-env.sh                     # Run commands in virtualenv
│   ├── sort_class_members.py             # Class member ordering
│   └── check_translations.py             # Translation validation
│   │
├── Configuration Files:
│   ├── pyproject.toml                    # Project config (Python, testing, linting)
│   ├── .pre-commit-config.yaml           # Pre-commit hooks
│   ├── .yamllint                         # YAML linting rules
│   ├── codecov.yml                       # Code coverage config
│   ├── requirements_test.txt             # Testing dependencies
│   ├── Dockerfile.dev                    # Development container
│   └── .devcontainer/                    # VS Code DevContainer setup
│
├── docs/                                 # Additional documentation
├── README.md                             # Comprehensive user documentation (1,295 lines)
└── changelog.md                          # Release history
```

## Key Technologies & Dependencies

### Runtime Dependencies
- **aiohomematic** (v2025.12.18) - Core async library for Homematic device communication
- **Home Assistant Core** - Minimum version: 2025.10.0+
- **Python 3.13+** (target version for development)

### Development Dependencies
- **pytest-homeassistant-custom-component** (0.13.300) - HA test framework
- **mypy** (1.18.2) - Static type checker (strict mode)
- **pylint** (4.0.4) - Code linting
- **ruff** (0.14.8) - Fast Python linter and formatter
- **pre-commit** (4.5.0) - Git hooks manager
- **aiohomematic-test-support** (2025.12.18) - Mock test data
- **async-upnp-client** (0.46.0) - UPnP discovery
- **uv** - Fast Python package installer (preferred over pip)

## Development Workflows

### Setting Up Development Environment

1. **Using DevContainer (Recommended):**
   ```bash
   # Open in VS Code with DevContainer extension
   # Container will auto-configure with script/setup and script/bootstrap
   ```

2. **Manual Setup:**
   ```bash
   # Install dependencies
   pip install -r requirements_test.txt

   # Or use uv (faster)
   uv pip install -r requirements_test.txt

   # Setup pre-commit hooks
   pre-commit install
   ```

### Code Quality Standards

#### Python Code Conventions

1. **Imports:**
   - First import: `from __future__ import annotations`
   - Import order: stdlib → third-party → local
   - Common aliases: `hmcu`, `hmcl`, `hmexp`, `hmed`, `hmce`, `hmd`, `hme`, `hmge`, `hms`

2. **Type Hints (Required):**
   - Full type annotations required (mypy strict mode)
   - Use `Final` for constants
   - Type aliases: `HomematicConfigEntry: TypeAlias = ConfigEntry[ControlUnit]`
   - Generic types with TypeVar for data points

3. **Async/Await:**
   - All public async methods prefixed with `async_`
   - Use `@callback` decorator for sync callbacks
   - Proper exception handling with `BaseHomematicException`

4. **Naming Conventions:**
   - Constants: `UPPER_SNAKE_CASE`
   - Private attributes: `_attr_` or `_` prefix
   - Classes: `PascalCase`
   - Functions: `snake_case`

5. **Class Structure:**
   - Use `@dataclass` with `kw_only=True, slots=True`
   - Proper `__init__` signatures with type annotations
   - Use `Generic[T]` for generic entity classes

#### Pre-commit Hooks (Run on Every Commit)

The following hooks run automatically before each commit:

1. **sort-class-members** - Enforces class member ordering
2. **ruff** - Linting and auto-formatting
3. **codespell** - Spell checking
4. **bandit** - Security linting
5. **yamllint** - YAML validation
6. **prettier** - Code formatting
7. **mypy** - Type checking (strict mode)
8. **pylint** - Code linting
9. **check-translations** - String/translation validation

**To run all hooks manually:**
```bash
pre-commit run --all-files
```

### Testing

#### Running Tests

```bash
# Run all tests with coverage
pytest --cov=custom_components tests

# Run with asyncio mode (as in CI)
pytest --cov=custom_components tests --asyncio-mode=legacy

# Run specific test file
pytest tests/test_config_flow.py

# Run with verbose output
pytest -v tests/
```

#### Test Configuration
- Framework: pytest with pytest-homeassistant-custom-component
- Test location: `/tests/`
- Asyncio mode: `auto` (default), `legacy` (CI)
- Coverage requirements:
  - **100% coverage required** for: config_flow.py, device_action.py, device_trigger.py, diagnostics.py, logbook.py
  - Default patch threshold: 0.09%

#### Test Fixtures (conftest.py)
- Mock configuration entries (v1, v2 migrations)
- SSDP discovery fixtures
- Control unit mocks
- SessionPlayer for replay-based testing
- Recorder integration fixtures

### Code Style & Linting

#### Ruff Configuration
- Target: Python 3.13
- Line length: 120
- Enabled rules: B, C, D, E, F, G, I, LOG, PT, SIM, and more
- Auto-fix enabled in pre-commit

#### Pylint Configuration
- Target: Python 3.13
- Extensions: code_style, typing, pylint_strict_informational
- Line length suggestion: 120
- 300+ disabled rules (handled by ruff/mypy)

#### MyPy Configuration (Strict Mode)
- `check_untyped_defs: true`
- `disallow_incomplete_defs: true`
- `warn_unused_ignores: true`
- Full type annotations required

## Architectural Patterns

### Entity Base Class Pattern

All entities inherit from `AioHomematicGenericEntity`:

```python
class SomeEntity(AioHomematicGenericEntity[GenericDataPoint], SomePlatformMixin):
    """Entity description with docstring."""

    _attr_has_entity_name = True
    _attr_should_poll = False  # Push-based updates

    def __init__(self, control_unit: ControlUnit, data_point: GenericDataPoint) -> None:
        super().__init__(control_unit, data_point)
        # Platform-specific initialization

    @property
    def current_state(self) -> StateType:
        """Return current value."""
        return self._data_point.value
```

### Control Unit Architecture

- **BaseControlUnit** - Base class
- **ControlUnit** - Main control instance managing one CCU/hub
- **ControlConfig** - Configuration wrapper
- Central handles XML-RPC callbacks, device state management

### Configuration Flow Pattern

The integration uses a modern, user-friendly multi-step configuration flow with the following features:

**Flow Steps:**
1. **Central** (Step 1/2): CCU connection settings (host, credentials, TLS)
2. **Interface** (Step 2/2): Device interface selection (HmIP-RF, BidCos-RF, etc.)
3. **Menu** (finish_or_advanced): Choose between completing setup or configuring advanced options
4. **Advanced** (optional): System variables, MQTT, device behavior settings
5. **Reconfigure** (entry point): Quick updates to CCU connection settings without full re-setup

**Key Features Implemented:**

- ✅ **Early Validation** (config_flow.py:344-364): Connection validated immediately after credential entry, not after all steps
- ✅ **Enhanced Error Messages**: All errors include `error_detail` and `retry_hint` placeholders for user guidance
- ✅ **Progress Indicators**: Each step shows "Step X of Y" via description_placeholders
- ✅ **Menu-Based Navigation**: Clear choice between finishing setup or accessing advanced options (no checkbox)
- ✅ **Reconfigure Flow**: Update connection settings (host, password, TLS) without deleting and re-adding integration

**Important Implementation Details:**

```python
# Early validation helper (config_flow.py:344-364)
async def _async_validate_connection(
    hass: HomeAssistant, data: ConfigType, entry_id: str
) -> tuple[dict[str, str], dict[str, str]]:
    """Validate connection and return errors and description placeholders."""
    errors: dict[str, str] = {}
    description_placeholders: dict[str, str] = {}

    try:
        await _async_validate_config_and_get_system_information(...)
    except AuthFailure:
        errors["base"] = "invalid_auth"
        description_placeholders["error_detail"] = "Authentication failed..."
        description_placeholders["retry_hint"] = "Verify credentials and try again."
    # ... handle other exceptions

    return errors, description_placeholders
```

```python
# Menu-based flow (config_flow.py:429-438)
async def async_step_finish_or_advanced(self, user_input: ConfigType | None = None):
    """Show menu to choose between finishing setup or configuring advanced options."""
    return self.async_show_menu(
        step_id="finish_or_advanced",
        menu_options=["finish", "advanced"],
    )
```

```python
# Reconfigure flow (config_flow.py:460-512)
async def async_step_reconfigure(self, user_input: ConfigType | None = None):
    """Handle reconfiguration of the integration."""
    entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
    # ... validate and update with async_update_reload_and_abort()
```

**Translation Structure:**

All user-facing strings require entries in three files:
- `strings.json` - Base definitions
- `translations/en.json` - English translations
- `translations/de.json` - German translations

Example structure for error messages:
```json
{
  "error": {
    "cannot_connect": "Failed to connect: [{invalid_items}].\n\n{error_detail}\n\n{retry_hint}"
  }
}
```

**Testing Patterns:**

Configuration flow tests (test_config_flow.py) follow these patterns:

1. **Helper Functions**: `async_check_form()` handles the complete flow including menu step
2. **Error Tests**: Verify errors appear in correct step with proper placeholders
3. **Validation Tests**: Test `_async_validate_connection()` helper with all exception types
4. **Reconfigure Tests**: Test success, connection errors, and auth failures

**Data Structure Compatibility:**

✅ **No migration required** for these changes - config entry data structure unchanged:
- All improvements are UI/UX only
- `CONF_ADVANCED_CONFIG` checkbox removed from UI but not from stored data
- Behavioral changes (preserving advanced settings) don't affect data schema

### Service Registration Pattern

```python
async_register_admin_service(
    hass,
    DOMAIN,
    service_name,
    async_service_handler,
    schema=SERVICE_SCHEMA,
    supports_response=SupportsResponse.OPTIONAL
)
```

### Event System

Events fired by the integration:
- `homematic.keypress` - Button press events
- `homematic.device_availability` - Device online/offline
- `homematic.device_error` - Error state notifications

## CI/CD Workflows

### GitHub Actions Pipelines

1. **test-run.yaml** - Main Test Pipeline
   - Triggered on: PRs, manual dispatch
   - Matrix: Python 3.13, 3.14
   - Steps: Setup timezone → Checkout → Setup Python → Install deps → pytest with coverage
   - Command: `pytest --cov=custom_components tests --asyncio-mode=legacy`

2. **pre-commit.yml** - Code Quality Gate
   - Runs on: PRs (excluding devel/master), pushes (excluding tags)
   - Executes all pre-commit hooks with --all-files

3. **hacs_validate.yaml** - HACS Validation
   - Schedule: Daily + manual/push/PR
   - Validates integration against HACS standards

4. **hassfest.yaml** - Home Assistant Manifest Validation
   - Schedule: Daily + manual/push/PR
   - Validates manifest.json against HA schema

## Important Files to Know

### Core Integration Files

1. **`__init__.py`** (custom_components/homematicip_local/__init__.py)
   - Integration entry point
   - Contains `async_setup_entry`, `async_unload_entry`
   - Platform loading and initialization

2. **`config_flow.py`** (26.8K lines)
   - All UI configuration flows
   - Multi-step setup wizard
   - Validation logic
   - SSDP auto-discovery handling

3. **`control_unit.py`** (33.9K lines)
   - Central control logic
   - Device management
   - XML-RPC callback handling
   - Connection management

4. **`services.py`** (42.1K lines)
   - All service definitions
   - Service handlers
   - Over 30 custom services for device control

5. **`entity_helpers.py`** (44.4K lines)
   - Entity creation utilities
   - Platform-specific entity factories
   - Device mapping logic

6. **`generic_entity.py`** (21.8K lines)
   - Base entity class `AioHomematicGenericEntity`
   - Common entity functionality
   - State management
   - Attribute handling

### Configuration Files

1. **`manifest.json`**
   - Integration metadata
   - Version: 2.0.0
   - Dependencies: aiohomematic==2025.12.18
   - Integration type: hub
   - IoT class: local_push

2. **`strings.json`** (52K+ lines)
   - All UI strings
   - Configuration flow text
   - Service descriptions
   - Error messages

3. **`services.yaml`** (14K lines)
   - Service schema definitions
   - Service parameter descriptions
   - Used for service documentation

4. **`README.md`** (1,400+ lines)
   - Comprehensive user documentation
   - Installation and configuration guides
   - Service reference and examples
   - Troubleshooting and FAQs
   - **Recently improved** with user-friendly tables, quick-start guides, and structured sections

## Documentation Standards

The project maintains high-quality documentation for both developers (this file) and users (README.md).

### README.md Best Practices

**Structure and Organization:**
- Use clear hierarchical sections with descriptive headings
- Group related information together
- Provide table of contents for long sections
- Separate beginner and advanced topics

**User-Friendly Writing:**
- Use tables for comparisons and option listings
- Include visual indicators (✅, ❌, ⚠️) for quick scanning
- Provide complete, copy-paste examples with real values
- Explain "why" not just "what"
- Include "when to use" guidance
- Add step-by-step instructions for processes

**Content Standards:**
- **Configuration guides:** Show both simple and advanced setups with complete examples
- **Troubleshooting:** Include symptoms, causes, and solutions
- **Examples:** Use realistic device names, IP addresses, and configurations
- **Tables:** Align columns, use consistent formatting
- **Code blocks:** Always specify language for syntax highlighting

**Recent README Improvements (2025-11):**

The following sections were comprehensively rewritten with user-focused improvements:

1. **Configuration Variables**
   - Reorganized by config flow steps (Step 1, 2, 3)
   - Added comparison tables with "When to Use" columns
   - Included Quick Setup Guides for beginners and power users
   - Added Docker-specific networking guidance
   - Documented new reconfigure flow

2. **System Variables & Programs**
   - Clear explanation of DEFAULT vs EXTENDED modes
   - Visual comparison table of all CCU variable types
   - Step-by-step marker filtering guide with practical example
   - Separate quick-start guides for different user levels

3. **Additional Information**
   - Reorganized into topical subsections
   - Added `value_state` attribute reference table
   - Device renaming comparison table with 4 methods
   - Clear button event setup with 3 options
   - Improved troubleshooting with structured problem/solution format

4. **Firmware Updates**
   - Process overview with clear steps
   - Update check schedule table
   - Status meanings explained
   - Step-by-step HA update instructions

5. **CUxD, CCU-Jack & MQTT**
   - Communication methods comparison
   - Two setup options with complete instructions
   - Prerequisites checklist
   - Troubleshooting guide

**Documentation Update Workflow:**

When making user-facing changes:
1. Update `strings.json` (base definitions)
2. Update `translations/en.json` (English)
3. Update `translations/de.json` (German)
4. Update `README.md` if user-visible
5. Run `script/check_translations.py` to verify

## Making Code Changes

### When Adding New Features

1. **Check existing patterns first:**
   - Review similar entity platforms (binary_sensor.py, sensor.py, etc.)
   - Follow the established entity base class pattern
   - Maintain consistency with existing code structure

2. **Type hints are mandatory:**
   - All functions must have full type annotations
   - Use `from __future__ import annotations`
   - Pass mypy strict mode checks

3. **Write tests:**
   - Add tests in `/tests/` directory
   - Aim for 100% coverage for critical files
   - Use existing test fixtures from conftest.py

4. **Update documentation:**
   - Update strings.json for UI text
   - Update services.yaml for new services
   - Consider updating README.md if user-facing

5. **Run quality checks before committing:**
   ```bash
   # Run pre-commit hooks
   pre-commit run --all-files

   # Run tests
   pytest --cov=custom_components tests
   ```

### When Modifying Entity Platforms

Entity platform files (binary_sensor.py, sensor.py, climate.py, etc.):

1. **Inherit from the correct base class:**
   ```python
   class MyEntity(AioHomematicGenericEntity[GenericDataPoint], SensorEntity):
   ```

2. **Set required attributes:**
   ```python
   _attr_has_entity_name = True
   _attr_should_poll = False
   ```

3. **Implement required properties:**
   - Platform-specific properties (e.g., `state` for sensors, `is_on` for binary sensors)
   - Use `@property` decorators
   - Return proper types

4. **Handle state updates:**
   - Integration uses push-based updates (no polling)
   - State updates come via XML-RPC callbacks
   - Don't fetch state manually unless absolutely necessary

### When Adding New Services

1. **Define service in services.yaml:**
   - Add schema definition
   - Include description and field descriptions
   - Specify response type if applicable

2. **Implement service handler in services.py:**
   - Follow existing pattern
   - Use proper validation
   - Handle errors gracefully

3. **Register service:**
   - Use `async_register_admin_service` for admin services
   - Use appropriate service domain

4. **Add to strings.json:**
   - Add service title and description
   - Add field labels and descriptions

5. **Write tests:**
   - Add service tests in `/tests/`
   - Test success and failure cases

## Common Pitfalls to Avoid

1. **Don't poll for state updates:**
   - This integration uses push-based updates
   - State comes via XML-RPC callbacks
   - Only system variables are polled (every 30s)

2. **Don't skip type hints:**
   - Mypy strict mode is enforced
   - All functions need full type annotations
   - Will fail CI if types are missing

3. **Don't ignore pre-commit hooks:**
   - Hooks enforce code quality
   - Fix issues before committing
   - Use `--no-verify` only in emergencies

4. **Don't create entities that poll:**
   - Set `_attr_should_poll = False`
   - Integration is designed for push updates

5. **Don't modify paramsets excessively:**
   - Warning in docs: "Too much writing to device MASTER paramset could kill device's storage"
   - Be cautious with `put_paramset` operations

6. **Don't forget translation files:**
   - Update strings.json
   - Sync with translations/en.json and translations/de.json
   - Run check-translations hook

## Debugging & Troubleshooting

### Common Issues

1. **Import errors:**
   - Ensure `from __future__ import annotations` is first import
   - Check import order: stdlib → third-party → local

2. **Type errors:**
   - Run `mypy custom_components/homematicip_local/`
   - Check for missing type annotations
   - Verify generic types are properly specified

3. **Test failures:**
   - Check test fixtures in conftest.py
   - Ensure async/await patterns are correct
   - Verify mock data is properly configured

4. **Pre-commit hook failures:**
   - Run specific hook: `pre-commit run <hook-id> --all-files`
   - Check hook output for specific errors
   - Fix issues and try again

### Logging

The integration uses standard Home Assistant logging:

```python
import logging
_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("Debug message")
_LOGGER.info("Info message")
_LOGGER.warning("Warning message")
_LOGGER.error("Error message")
```

Logger name: `aiohomematic` (set in manifest.json)

## Integration-Specific Patterns

### Handling Device Parameters

Devices have parameters that can be:
- **Ignored** - Not created as entities (filtered for better UX)
- **Deactivated** - Created but disabled by default
- **Activated** - Created and enabled by default
- **Unignored** - Previously ignored parameters enabled via config

### System Variables

- Fetched every 30s from CCU
- Initially created as **deactivated** entities
- Support two modes:
  - **DEFAULT** (no `HAHM` marker): Read-only sensors
  - **EXTENDED** (`HAHM` marker in description): Writable entities (select, number, switch, text)

### MQTT Support (Optional)

- Required for CUxD and CCU-Jack devices
- Enables push events for system variables with `MQTT` marker
- Requires CCU-Jack or MQTT bridge setup

### Firmware Updates

- Update entities per device
- Queried every 6 hours (or on demand via service)
- Installation triggers when firmware ready

### Config Entry Migrations

**When migrations are required:**

Config entry migrations (`async_migrate_entry` in `__init__.py`) are **only needed** when the **data structure** stored in config entries changes.

**Current version:** 12 (as of 2025-12)

**Migration is required when:**
- ✅ Adding new keys to config entry data
- ✅ Removing keys from config entry data
- ✅ Changing data types of existing keys
- ✅ Restructuring nested data dictionaries

**Migration is NOT required for:**
- ❌ UI/UX changes (new flow steps, different input methods)
- ❌ Changing how data is displayed or collected
- ❌ Adding/removing UI elements (checkboxes, menus)
- ❌ Behavioral changes that don't affect stored data
- ❌ Translation updates

**Example: Recent Config Flow Improvements (No Migration Needed)**

The following changes were made without requiring migration:
- Added early validation (validates earlier in flow)
- Enhanced error messages (UI presentation only)
- Progress indicators (description_placeholders, not stored)
- Menu-based navigation (removed checkbox from UI, but not from data)
- Reconfigure flow (updates existing data, doesn't change structure)

**Verification checklist before implementing changes:**

```python
# 1. Check current config entry structure
entry.data = {
    CONF_INSTANCE_NAME: str,
    CONF_HOST: str,
    CONF_USERNAME: str,
    CONF_PASSWORD: str,
    CONF_TLS: bool,
    CONF_VERIFY_TLS: bool,
    CONF_INTERFACE: dict,
    CONF_ADVANCED_CONFIG: dict,
    # ... optional fields
}

# 2. Will your change add/remove/modify these keys? → Migration needed
# 3. Will your change only affect how these are collected? → No migration needed
```

**Migration best practices:**
- Always increment version number in migration
- Handle all previous versions in migration chain
- Test migration path from each previous version
- Document migration in changelog
- Never skip version numbers

## File Naming & Location Conventions

1. **Entity platforms:** `custom_components/homematicip_local/<platform>.py`
   - E.g., `sensor.py`, `binary_sensor.py`, `climate.py`

2. **Tests:** `tests/test_<module>.py`
   - E.g., `test_sensor.py`, `test_config_flow.py`

3. **Helper scripts:** `script/<script_name>`
   - Must be executable
   - Use shebang if needed

4. **Blueprints:** `blueprints/automation/<name>.yaml`
   - Follow existing naming pattern

## Version Information

- **Current Version:** 2.0.0
- **Minimum HA Version:** 2025.10.0+
- **Python Target:** 3.13+ (CI tests on 3.13, 3.14)
- **aiohomematic Version:** 2025.12.18

## External Resources

- **Main Documentation:** https://github.com/sukramj/homematicip_local
- **Wiki:** https://github.com/sukramj/aiohomematic/wiki
- **Issues:** https://github.com/sukramj/aiohomematic/issues
- **Discussions:** https://github.com/sukramj/aiohomematic/discussions
- **Changelog:** https://github.com/sukramj/homematicip_local/blob/master/changelog.md
- **HACS:** Integration available via HACS

## Quick Reference Commands

```bash
# Setup development environment
script/setup
script/bootstrap

# Install dependencies
pip install -r requirements_test.txt
# Or with uv (faster)
uv pip install -r requirements_test.txt

# Run tests
pytest --cov=custom_components tests

# Run pre-commit hooks
pre-commit run --all-files

# Run specific hook
pre-commit run mypy --all-files
pre-commit run ruff --all-files

# Type checking
mypy custom_components/homematicip_local/

# Linting
pylint custom_components/homematicip_local/

# Format code
ruff format custom_components/homematicip_local/

# Auto-fix linting issues
ruff check --fix custom_components/homematicip_local/
```

## Summary for AI Assistants

When working with this codebase:

### Code Quality & Standards
1. **Always maintain type hints** - Strict mypy mode is enforced, all functions need full type annotations
2. **Follow async/await patterns** - Prefix async functions with `async_`, use `@callback` for sync callbacks
3. **Write comprehensive tests** - Aim for 100% coverage on critical files (config_flow.py, device_action.py, etc.)
4. **Run pre-commit hooks** - All quality gates must pass before committing
5. **Test with Python 3.13 and 3.14** - CI tests both versions, ensure compatibility

### Architecture & Patterns
6. **Don't poll** - Use push-based updates via XML-RPC callbacks (except system variables)
7. **Use the correct entity base classes** - Inherit from `AioHomematicGenericEntity`
8. **Check existing patterns** - Review similar code (e.g., other platform files) before implementing new features
9. **Follow config flow patterns** - Use helper functions, validate early, provide detailed error messages

### Documentation & Translations
10. **Update documentation systematically**:
    - `strings.json` (base definitions)
    - `translations/en.json` (English)
    - `translations/de.json` (German)
    - `README.md` (if user-facing changes)
    - Run `script/check_translations.py` to verify

11. **Write user-friendly documentation**:
    - Use tables for comparisons
    - Include visual indicators (✅, ❌, ⚠️)
    - Provide complete examples with real values
    - Explain "why" and "when to use"
    - Add step-by-step instructions

### Config Flow & Migrations
12. **Understand migration requirements**:
    - ✅ Migration needed: Data structure changes (add/remove/modify keys)
    - ❌ No migration needed: UI/UX changes, flow reorganization, translation updates
    - Current version: 12 - always increment when migrating

13. **Config flow best practices**:
    - Validate early (immediately after credential entry)
    - Provide detailed error messages with `error_detail` and `retry_hint`
    - Use progress indicators (`step_current`, `step_total`)
    - Support reconfiguration for quick updates

### Safety & Production Standards
14. **Be cautious with device writes** - Excessive writes to MASTER paramset can damage device storage
15. **Handle errors gracefully** - Use `BaseHomematicException` and subclasses, provide actionable guidance
16. **Maintain backwards compatibility** - Don't break existing automations or configurations without migration

### Recent Improvements to Reference (2025-11)
- ✅ Early validation pattern in config flow
- ✅ Enhanced error messages with placeholders
- ✅ Menu-based navigation (finish_or_advanced)
- ✅ Reconfigure flow implementation
- ✅ Progress indicators in multi-step flows
- ✅ Comprehensive README documentation with tables and examples

This integration is production-quality, well-tested, and follows Home Assistant best practices. Maintain these standards in all contributions. When in doubt, check existing patterns in similar files and consult this guide.
