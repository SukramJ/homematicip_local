# CLAUDE.md - AI Assistant Guide for Homematic(IP) Local Integration

This document provides comprehensive guidance for AI assistants working with the Homematic(IP) Local for OpenCCU codebase.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Key Technologies & Dependencies](#key-technologies--dependencies)
4. [Development Environment Setup](#development-environment-setup)
5. [Code Quality & Standards](#code-quality--standards)
6. [Docstring Standards](#docstring-standards)
7. [Testing Guidelines](#testing-guidelines)
8. [Architecture & Design Patterns](#architecture--design-patterns)
9. [Common Development Tasks](#common-development-tasks)
10. [Git Workflow](#git-workflow)
11. [Implementation Policy](#implementation-policy)
12. [Tips for AI Assistants](#tips-for-ai-assistants)
13. [Quick Reference](#quick-reference)

---

## Project Overview

**Project Name:** Homematic(IP) Local for OpenCCU
**Type:** Home Assistant Custom Integration
**Version:** 2.12.4
**Primary Language:** Python 3.14+
**Domain:** `homematicip_local`

This is a production-quality Home Assistant custom integration that enables local communication with Homematic and HomematicIP smart home devices through various hubs (CCU2/3, OpenCCU, Debmatic, Homegear). It provides bi-directional communication using XML-RPC for device control and push state updates, and JSON-RPC for fetching device names and room information.

---

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
│   ├── test-run.yaml                     # Main test pipeline (Python 3.14)
│   ├── e2e-parity.yaml                   # Three-way backend parity gate (see tests/e2e/README.md)
│   ├── pre-commit.yml                    # Code quality gate
│   ├── issue-analyzer.yml                # Issue triage (.github/scripts/analyze_issue.py)
│   ├── validate-issue-template.yml       # Closes issues that bypass the form; skips transferred ones
│   ├── close-insufficient-info.yml       # Manual close when diagnostics are missing
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
│   ├── Makefile                          # Entry point for all dev tasks (`make help`)
│   ├── pyproject.toml                    # Project config (Python, testing, linting)
│   ├── .pre-commit-config.yaml           # Pre-commit hooks
│   ├── .yamllint                         # YAML linting rules
│   ├── codecov.yml                       # Code coverage config
│   ├── requirements_test.txt             # Testing dependencies
│   ├── Dockerfile.dev                    # Development container
│   └── .devcontainer/                    # VS Code DevContainer setup
│
├── docs/                                 # Additional documentation
│   ├── naming.md                         # Device and entity naming conventions
│
├── Documentation:
│   ├── README.md                         # Comprehensive user documentation (1,295 lines)
│   ├── CLAUDE.md                         # AI Assistant development guide
│   ├── CONTRIBUTING.md                   # Contribution guidelines
│   └── changelog.md                      # Release history
```

---

## Key Technologies & Dependencies

### Runtime Dependencies

- **aiohomematic** (v2026.11.5) - Core async library for Homematic device communication
- **aiohomematic-config** (v2026.11.1) - Device configuration metadata
- **openccu-data** (v2026.9.1) - CCU configuration metadata (translations, easymodes, link profiles); pulled in by aiohomematic and pinned in the manifest, not imported here
- **openccu-loom-client** (v2026.11.8) - Client for the openccu-loom backend (Beta)
- **Home Assistant Core** - Minimum version: 2026.11.0+
- **Python 3.14+** (target version for development)

### Development Dependencies

- **pytest-homeassistant** (2026.11.0) - Home Assistant's official pytest plugin for custom integrations (HA core `packages/pytest-homeassistant`, pinned to the matching HA release)
- **mypy** (`<=2.4.0`, a ceiling rather than a pin; 2.1.0 installed) - Static type checker (strict mode)
- **pylint** (4.1.3) - Code linting
- **ruff** (0.17.3) - Fast Python linter and formatter
- **prek** (0.5.9) - Git hooks manager (Rust-based pre-commit alternative)
- **aiohomematic-test-support** (2026.11.5) - Mock test data
- **async-upnp-client** (0.49.0) - UPnP discovery
- **uv** - Fast Python package installer (preferred over pip)

---

## Development Environment Setup

### Prerequisites

- **Python**: 3.14 or higher
- **Package Manager**: pip, uv (recommended)
- **Git**: For version control

### Initial Setup

1. **Using DevContainer (Recommended):**

   ```bash
   # Open in VS Code with DevContainer extension
   # Container will auto-configure with script/setup and script/bootstrap
   ```

2. **Manual Setup:**

   ```bash
   # Clone the repository
   git clone https://github.com/sukramj/homematicip_local.git
   cd homematicip_local

   # Create virtual environment (./venv, Python 3.14)
   make venv

   # Install dependencies and prek hooks
   make setup
   ```

### The Makefile

The `Makefile` is the entry point for every development task; `make help` lists all
targets grouped by topic (setup, code quality, tests, validation, run, housekeeping).

Targets run through `script/run-in-env.sh`, which activates `./venv` (or `.venv`) if
present, so they work with or without an activated virtual environment. The command
examples throughout this document use `make`; the underlying commands still work if
run directly.

---

## Code Quality & Standards

### Type Checking (mypy - STRICT MODE)

**CRITICAL**: This project uses mypy in **strict mode**. All code MUST be fully typed.

```python
# pyproject.toml settings:
strict = true
check_untyped_defs = true
disallow_incomplete_defs = true
warn_unused_ignores = true
```

#### Type Annotation Requirements

```python
# ✅ CORRECT - All parameters and return types annotated
def get_device_by_address(self, address: str) -> Device | None:
    """Return device by address."""
    return self._devices.get(address)

# ❌ INCORRECT - Missing type annotations
def get_device_by_address(self, address):
    return self._devices.get(address)

# ✅ CORRECT - Complex types properly annotated
async def fetch_devices(
    self,
    *,
    include_internal: bool = False,
) -> dict[str, DeviceDescription]:
    """Fetch all device descriptions."""
    ...

# ✅ CORRECT - Using TYPE_CHECKING for imports
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiohomematic.central import CentralUnit
```

### Import Requirements

**MANDATORY**: Every Python file MUST start with:

```python
from __future__ import annotations
```

This is enforced by ruff's `required-imports` setting.

#### Import Sorting (isort via ruff)

```python
# Correct import order:
from __future__ import annotations

# 1. Standard library
import asyncio
from collections.abc import Callable
from typing import TYPE_CHECKING

# 2. Third-party
from homeassistant.core import HomeAssistant

# 3. First-party (aiohomematic)
from aiohomematic.const import Interface

# 4. Local imports
from .const import DOMAIN

# 5. TYPE_CHECKING imports (to avoid circular imports)
if TYPE_CHECKING:
    from aiohomematic.central import CentralUnit
```

#### Common Import Aliases

```python
import probatio as vol

from aiohomematic.central import CentralUnit as hmcu
from aiohomematic.client import Client as hmcl
from aiohomematic.model.custom import definition as hmed
from aiohomematic.support import support as hms
```

### Code Style Conventions

```python
# Use keyword-only arguments for ALL parameters (excluding self/cls)
def create_entity(
    *,  # Force keyword-only
    control_unit: ControlUnit,
    data_point: DataPoint,
) -> Entity:
    """Create a new entity."""
    ...

# Even single parameter must be keyword-only
def get_device(self, *, address: str) -> Device | None:
    """Return device by address."""
    ...

# Docstrings required for all public classes and methods
class HmipDevice:
    """Representation of a Homematic device."""

    def get_channel(self, channel_no: int) -> Channel | None:
        """Return channel by number."""
        ...

# Use descriptive variable names (avoid single letters except in comprehensions)
# ✅ CORRECT
for device_address in device_addresses:
    ...

# ⚠️ ACCEPTABLE only in simple comprehensions
devices = [d for d in all_devices if d.is_ready]
```

### Linting (ruff + pylint)

#### Ruff Configuration

- **Target**: Python 3.14
- **Line Length**: 120 characters
- **Enabled Rules**: B, C, D, E, F, G, I, LOG, PT, SIM, and more
- **Auto-fix enabled** in prek

```bash
# Auto-format and auto-fix all code (ruff format + ruff check --fix)
make format

# Lint code without auto-fix
make lint

# Check formatting without changes
make format-check
```

### Prek Hooks (Run on Every Commit)

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
10. **check-flow-translations** - Config flow & repair translation validation

**To run all hooks manually:**

```bash
make prek
```

**Bypass hooks** (NOT recommended):

```bash
git commit --no-verify -m "message"
```

---

## Docstring Standards

**IMPORTANT**: All code must follow the project's docstring conventions for consistency and maintainability.

### Key Principles

1. **Short and Precise**: Docstrings should be concise yet informative
2. **Programmer-Focused**: Write for developers using or maintaining the code
3. **Type Hints First**: Rely on type annotations; avoid repeating type information
4. **Consistency**: Follow established patterns for similar constructs

### Quick Rules

**Punctuation**: Always end docstrings with a period (`.`)

**Verb Usage**:

- Functions/Methods: Use imperative mood ("Return the device", not "Returns" or "Gets")
- Classes: Use declarative statements ("Represents a device")

### Method Docstrings

```python
# Simple methods (one-line)
def get_device(self, address: str) -> Device | None:
    """Return device by address."""

# Complex methods (with Args/Returns)
def create_device(
    self,
    *,
    interface_id: str,
    device_address: str,
) -> Device:
    """
    Create and register a new device instance.

    Args:
        interface_id: Interface identifier.
        device_address: Unique device address.

    Returns:
        Created device instance.
    """
```

### Property Docstrings

```python
@property
def device_address(self) -> str:
    """Return the device address."""
```

### Common Anti-Patterns to Avoid

❌ **Don't repeat type information**:

```python
# Bad
def get_address(self) -> str:
    """Return the address as a string."""

# Good
def get_address(self) -> str:
    """Return the device address."""
```

❌ **Don't use inconsistent verbs**:

```python
# Bad
def get_device(...): """Gets device."""
def fetch_value(...): """Fetches value."""

# Good
def get_device(...): """Return device by address."""
def fetch_value(...): """Return parameter value."""
```

❌ **Don't forget periods**:

```python
# Bad
"""Clear the cache"""

# Good
"""Clear the cache."""
```

---

## Testing Guidelines

### Running Tests

```bash
# Run all tests
make test

# Run all tests with coverage
make test-cov

# Run exactly as in CI (asyncio-mode=legacy)
make test-ci

# Run specific test file
make test-file FILE=tests/test_config_flow.py

# Pass extra pytest arguments
make test PYTEST_ARGS="-x -vv"

# Generate HTML coverage report (htmlcov/index.html)
make test-cov-html

# Run the opt-in three-way parity e2e tests (see tests/e2e/README.md)
make test-e2e
```

### Test Configuration

- Framework: pytest with pytest-homeassistant (HA's official plugin; loads itself, no `pytest_plugins` line, the `hass` fixture enables custom integrations)
- Test location: `/tests/`
- Asyncio mode: `auto` (default), `legacy` (CI)
- Coverage requirements:
  - **100% coverage required** for: config_flow.py, device_action.py, device_trigger.py, diagnostics.py, logbook.py
  - Default patch threshold: 0.09%

### Test Fixtures (conftest.py)

Key fixtures available:

- Mock configuration entries (v1, v2 migrations)
- SSDP discovery fixtures
- Control unit mocks
- SessionPlayer for replay-based testing
- Recorder integration fixtures

### Writing Tests

```python
"""Test for config flow."""

from __future__ import annotations

import pytest

from homeassistant.core import HomeAssistant

from custom_components.homematicip_local.const import DOMAIN


@pytest.mark.asyncio
async def test_config_flow_user_init(
    hass: HomeAssistant,
) -> None:
    """Test user-initiated config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
    )

    assert result["type"] == "form"
    assert result["step_id"] == "central"
```

---

## Architecture & Design Patterns

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

The integration uses a modern, user-friendly multi-step configuration flow:

**Flow Steps:**

1. **Central** (Step 1/2): CCU connection settings (host, credentials, TLS)
2. **Interface** (Step 2/2): Device interface selection (HmIP-RF, BidCos-RF, etc.)
3. **Menu** (finish_or_advanced): Choose between completing setup or configuring advanced options
4. **Advanced** (optional): System variables, MQTT, device behavior settings
5. **Reconfigure** (entry point): Quick updates to CCU connection settings without full re-setup

**Key Features:**

- ✅ **Early Validation**: Connection validated immediately after credential entry
- ✅ **Enhanced Error Messages**: All errors include `error_detail` and `retry_hint` placeholders
- ✅ **Progress Indicators**: Each step shows "Step X of Y"
- ✅ **Menu-Based Navigation**: Clear choice between finishing setup or accessing advanced options
- ✅ **Reconfigure Flow**: Update connection settings without deleting and re-adding integration
- ✅ **Relevance-Gated Loom Backend**: There is no master switch for the openccu-loom backend. `_loom_is_relevant()` decides whether `async_step_user` shows the backend menu: it returns `True` when a loom entry is already configured or a daemon discovery flow is in progress (`async_progress_by_handler(DOMAIN, match_context={"source": SOURCE_ZEROCONF})`). Setups without a daemon go straight to `central` and never see a backend choice. `async_step_zeroconf` is ungated — an announcing daemon always produces a discovery card. Do **not** reintroduce a compile-time flag, and do not use `show_advanced_options` as a gate (deprecated in HA, returns `True` unconditionally, removal in 2027.6)
- ✅ **Loom Beta Marking**: The loom backend is marked Beta at every entry point — `TITLE_BACKEND_LOOM = "openccu-loom Beta"` (discovery card, reauth, reconfigure) plus `(Beta)` titles and a leading Beta note on `user.menu_options.loom`, `step.loom`, `step.loom_credentials` and `step.loom_token` in `strings.json`/`en.json`/`de.json`. Steps that act on an existing entry stay unmarked — `options.step.loom_connection`, `step.reauth_loom`, `step.reauth_loom_box` and `step.reconfigure_loom`; their dialogs carry Beta through the `{backend}` flow title. Remove the marking only when the client consumes the full daemon wire surface — see `docs/architecture-comparison-aiohomematic-vs-loom.md` §10
- ✅ **Backend-Aware Flow Titles**: `flow_title` carries a `{backend}` placeholder (`aiohomematic` / `openccu-loom Beta`), so discovery cards (SSDP vs. mDNS), reauth and reconfigure dialogs show which backend a flow targets
- ✅ **Backend-Neutral Device Identifiers**: The HA device identifier is composed by the integration — `ControlUnit.device_identifier()` / `support.get_device_identifier()` build `<address>@<instance_name>-<interface>` from the interface *type*, never from a backend's own `interface_id`. The two backends disagree on that id's leading component (aiohomematic uses the HA instance name, the openccu-loom daemon its own CCU name), so keying devices on it re-created every device entry on a backend switch and lost the `device_id` with its area and automations. For the direct-CCU backend the composed value is byte-identical to `Device.identifier`. `_async_migrate_device_identifiers` moves legacy entries over before the platforms are forwarded (plain rename; merge into the older entry when both exist). **Never key a device on `hm_device.identifier` again, and never parse an interface id back out of an identifier** — device actions/triggers/services resolve the device by address and read `interface_id` off the device
- ✅ **In-Place Backend Switch**: Setting up a CCU whose serial is already configured on the *other* backend switches the existing entry in place (abort reason `backend_switched`) instead of aborting with `already_configured`. The entry keeps its entry_id, instance name and advanced config (incl. `sub_devices_enabled`). An entry holds only its own backend's credentials: the switch drops the other set (`CCU_CREDENTIAL_KEYS` / `LOOM_CREDENTIAL_KEYS` in `const.py`), and a switch back asks for them in that backend's setup flow. **Never carry a credential across a switch** — openccu-loom-client refuses any credential beside a box token (`box_token is the only credential behind the box`), which left a switched entry in `SETUP_ERROR` (openccu-lite#20); the v17 → v18 migration cleans entries switched earlier. Non-credential keys such as the daemon port stay
- ✅ **Loom Sub-Device Toggle**: The openccu-loom setup flow (manual form and discovered-daemon token step) offers `sub_devices_enabled` directly, defaulting to enabled (`DEFAULT_LOOM_ENABLE_SUB_DEVICES`)
- ✅ **Serial-Keyed Manual Loom Setup**: The manual loom form validates the daemon, lists its CCUs and routes into the shared CCU-selection step, so manual entries get the same serial-based dedup and in-place backend switch as discovered daemons (the user-chosen instance name is kept)
- ✅ **Single-Reload Entry Updates**: `_async_update_reload_and_abort_entry` / `_async_update_entry_and_reload` (used by reauth, reconfigure, both backend-switch paths and the mDNS host follow-up) schedule a reload only when the entry's update listener will not already reload it — never use `ConfigFlow.async_update_reload_and_abort` here (double reload, deprecated with HA 2026.12)
- ✅ **Loom Discovery Dedup**: `async_step_zeroconf` suppresses the daemon card once it is configured — per CCU serial when the daemon announces them (TXT key `ccus`, incl. automatic host/port follow-up on IP change; a serial on the CCU backend keeps the card as the backend-switch path), with a host/port fallback for pre-`ccus` daemons; `_async_create_loom_entry` clears lingering passive cards of the daemon it just handled

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

---

## Common Development Tasks

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
   # Run prek hooks and tests with coverage
   make check
   ```

### When Modifying Entity Platforms

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

### Adding a Translation

**IMPORTANT**: `strings.json` is the **primary source** for all translation keys.

1. **Add to translation files** (in this order):

   ```bash
   # Step 1: Add key to strings.json (PRIMARY SOURCE)
   # Step 2: Add to translations/en.json
   # Step 3: Add German translation to translations/de.json
   ```

2. **Validate translations**:

   ```bash
   # Validate strings.json / en.json / de.json (use `make translations-fix` to sort and sync)
   make translations

   # Validate config flow & repair translations
   make flow-translations
   ```

### Updating Documentation

**MANDATORY**: When making significant changes, verify and update all relevant documentation.

#### Documentation Update Checklist

After any major feature, refactoring, or API change, check:

```
□ 1. Module/Class/Method Docstrings - Updated with current behavior
□ 2. CLAUDE.md - Version numbers, dependencies, architecture changes
□ 3. CONTRIBUTING.md - Development process, workflow changes
□ 4. README.md - User-facing features, setup instructions
□ 5. docs/*.md - Relevant technical documentation
□ 6. changelog.md - Version entry with breaking changes
```

#### Key Documentation Files

| File | Update When |
|------|------------|
| **Module/Class/Method docstrings** | Code behavior changes |
| **CLAUDE.md** | Architecture, dependencies, dev processes |
| **CONTRIBUTING.md** | Git workflow, contribution process |
| **README.md** | User features, setup, troubleshooting |
| **docs/naming.md** | Entity/device naming logic |
| **changelog.md** | Every release, every breaking change |

#### When to Update Documentation

**Always update when:**
- ✅ Adding new features or services
- ✅ Changing public APIs (events, services, entity attributes)
- ✅ Modifying configuration flow
- ✅ Updating dependencies (aiohomematic, Home Assistant minimum version)
- ✅ Changing architecture or design patterns
- ✅ Breaking backward compatibility

**Documentation update workflow:**

1. **Update code docstrings** (inline with code changes)
2. **Update CLAUDE.md** (if dev process/architecture changed)
3. **Update README.md** (if user-facing changes)
4. **Update docs/*.md** (if relevant to that topic)
5. **Update changelog.md** (required for all releases)

**Verify documentation:**

```bash
# Check for outdated version numbers
grep -r "2025.12.33" CLAUDE.md README.md docs/

# Check for broken internal references
grep -r "TODO\|FIXME\|XXX" *.md docs/*.md

# Validate markdown formatting
make prettier
```

---

## Git Workflow

### Branch Structure

- **Default Branch**: `main` (protected)
- **Feature Branches**: `feature/description`
- **Bug Fix Branches**: `fix/description`

### Commit Messages

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:

```bash
feat(climate): Add support for new thermostat device

Implements custom entity class for HmIP-eTRV-2 with support for
boost mode and window open detection.

Closes #123
```

```bash
fix(config_flow): Handle connection timeout gracefully

Added retry logic with exponential backoff for validation calls.
```

### Pull Request Process

1. **Create feature branch** from `main`
2. **Make changes** with tests
3. **Run the quality gate**: `make check` (prek hooks + tests with coverage)
4. **Commit changes** with descriptive messages
5. **Push to remote**: `git push -u origin feature/branch-name`
6. **Create Pull Request** to `main` branch
7. **Wait for CI** to pass
8. **Request review** from maintainers

---

## Implementation Policy

This section defines mandatory rules for all implementations in this project.

### Refactoring Completion Checklist

**MANDATORY**: Every refactoring or feature implementation MUST complete ALL items before merging:

```
□ 1. Clean Code    - No legacy compatibility layers, deprecated aliases, or shims
□ 2. Tests         - make test passes without errors
□ 3. Linting       - make prek passes without errors
□ 4. Documentation - Docstrings, CLAUDE.md, README.md, docs/*.md updated as needed
□ 5. Changelog     - changelog.md updated with version entry
```

### Implementation Plan Requirements

**CRITICAL**: An implementation plan is a brief for the `impl` agent (Opus, see [Which model does which work](#which-model-does-which-work)) and MUST be executable without questions; a stop condition reported back is a successful outcome, a guess is not.

A valid implementation plan must:

1. **Resolve ALL Ambiguities Upfront**

   - No "decide later" or "TBD" items
   - Every decision point must have a concrete answer
   - If multiple approaches exist, one MUST be selected and documented

2. **Provide Exact File Paths**

   - Full paths to all files to be created/modified
   - Example: `custom_components/homematicip_local/new_platform.py` (not just "create a new file")

3. **Include Complete Code Snippets**

   - Entire function/class implementations, not partial examples
   - All imports required for each file
   - Exact method signatures with full type annotations

4. **Specify Exact Locations for Edits**

   - Line numbers or unique context strings for modifications
   - Before/after code blocks for changes
   - Example: "In `control_unit.py`, replace lines 145-150 with..."

5. **Document Dependencies and Order**

   - Which steps depend on which
   - Exact execution order
   - Files that must exist before others can be created

6. **Include Test Requirements**
   - Specific test cases to add
   - Expected test file locations
   - Test function names and what they verify

### Clean Code Policy

When implementing new features or refactoring existing code:

1. **No Legacy Code**: After implementation, the codebase must be clean without any legacy compatibility layers, deprecated aliases, or backward-compatibility shims introduced during the change.

2. **No Backward Compatibility Layers**: Do not create:
   - Type aliases for old names
   - Re-exports of renamed symbols
   - Deprecation warnings for removed APIs
   - Compatibility adapters or wrappers
   - `# TODO: remove after migration` comments

3. **Complete Migration**: All usages of changed APIs must be updated in a single change. Partial migrations that leave legacy code are not acceptable.

4. **Documentation Updates**: All changes must include:
   - Updated docstrings for modified classes/methods
   - Updated `*.md` documentation files

### Quality Gate Commands

Run these commands before considering any implementation complete:

```bash
# 1. Run all prek hooks (ruff, mypy, pylint, etc.) and tests with coverage
make check

# 2. Verify no TODO/FIXME related to migration
grep -r "TODO.*migration\|FIXME.*migration\|TODO.*remove\|TODO.*deprecated" custom_components/

# 3. Check for unused imports/code
ruff check --select F401,F841 custom_components/
```

### Config Entry Migrations

**When migrations are required:**

Config entry migrations (`async_migrate_entry` in `__init__.py`) are **only needed** when the **data structure** stored in config entries changes.

**Current version:** 18 (as of 2026-11)

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

**Migration best practices:**

- Always increment version number in migration
- Handle all previous versions in migration chain
- Test migration path from each previous version
- Document migration in changelog
- Never skip version numbers

---

## Which model does which work

Set by the owner for the go-fabric family on 2026-10-10 (go-fabric's
`CLAUDE.md`); the review split of 2026-11-08 (go-fabric #456) likewise.
Adopted here on 2026-11-08. A statement about Home Assistant, aiohomematic or openccu-loom behaviour that
lands in this repo is cited later as fact — a comment that names a caller
or a consumer, a docstring that states what the other side does, a
`changelog.md` line — so the work that produces such statements gets
the strongest model, and the work a guard checks may use a cheaper one. The
agents in [Sub-Agent Delegation](#sub-agent-delegation) carry a default
model each; the rows below decide when a call overrides it (`model:` on the
Agent tool). Implementation defaults to Opus.

| Work | Model |
| --- | --- |
| Analysis, planning, reviews of design, audits; anything written into `docs/`, `changelog.md` or `AI_POLICY.md`, or a comment that names a Home Assistant core, aiohomematic, openccu-loom-client or CCU behaviour; the config flow with its credentials and TLS (`config_flow.py`, the loom credential and token steps) and the WebSocket API payloads the frontend consumes (`websocket_api.py`); *which* guard gets built and its bite line; rebases and merge conflicts where `main` may have overtaken the change | **Fable** (the default for this repo; also the `hunt` agent) |
| Implementation of a finished plan with guards behind it: a platform entity once the pattern exists, a translation key with `make translations`, a test on an existing fixture, a `changelog.md` entry for a finished diff | **Opus** (the `impl` default; also what fast mode runs on) |
| **Review of a slice's pull request, split (owner decision 2026-11-08, go-fabric #456).** The code review — correctness, concurrency, error paths, tests, the fixed report shape — is **Opus**. On top of it **Fable** reads, bounded: every new comment or docstring that names a Home Assistant core, aiohomematic, openccu-loom-client or CCU behaviour against Home Assistant core at the minimum version, aiohomematic and openccu-loom-client at the pins in `manifest.json`, every line that enters `docs/`, `changelog.md` or `AI_POLICY.md`, the paths of the first row, and the brief's decisions against the reference — the behavioural gaps a code review does not see. The load-bearing claims of the Opus review are verified before they reach the implementer. | **Opus**, then **Fable** |
| Work a test or generator checks immediately: `make translations`, `make prek`, `ruff format`, a table case on an existing pattern; search and first reading of a tree whose result a stronger model or the owner reads again | **Sonnet** (the `guard` default; `impl` with `model: "sonnet"`) |
| Mechanical inventories whose answer is a list the caller can re-grep: which files reference X, which links are dead, which entries lack a counterpart | **Haiku** (`sweep` default) |

Sonnet never writes a claim about a Home Assistant core, aiohomematic, openccu-loom-client or CCU behaviour into the repo, and
never touches the paths named in the first row. Haiku returns lists, never
verdicts. When in doubt about which row a task is in, it is in the first.

---

## Sub-Agent Delegation

As go-fabric's and openccu-loom's rule (owner, 2026-10-10). The main
conversation owns planning, contract and wire decisions, guard
specifications, sub-agent steering, and final verification. It does not own
typing.

**Delegate what a gate can prove; keep what only a reader can accept.**
Delegate freely: table cases, fakes, scaffolding, fixture updates, doc and
link cleanups, version bumps across the changelog set, inventories and grep
sweeps. Never delegate: the config flow and credential handling, the WebSocket API payloads, the aiohomematic / openccu-loom-client pins and the capability handshake, and *which* guard gets
built. Locating is delegable; reading is not.

| Agent | Default model | Use for |
|---|---|---|
| `impl` | Opus | scoped implementation with a stated acceptance command |
| `guard` | Sonnet | tests from a caller-written guard spec, plus the bite proof |
| `sweep` | Haiku | read-only inventories and grep sweeps, high fan-out |
| `hunt` | Fable | adversarial read-only defect hunt, ranked candidates |

Each default is one row of
[Which model does which work](#which-model-does-which-work); a call that
falls into another row passes `model:` on the Agent tool — `impl` with
`model: "sonnet"` for work a generator or formatter checks immediately.

**Size CPU-bound fan-out from the host, never from a constant** — the owner
works from a 4-core box and a 14-core box:

```sh
cores=$(nproc); agents=$(( (cores - 1) / share ))   # share = cores per agent
```

Check the 1-minute load first; if it is at or above the core count, run one
CPU-bound agent and queue the rest. Eight concurrent agents is a practical
ceiling whatever the core count. Every CPU-bound agent must **pin** its share
in the command it runs (`pytest tests/<area>` — one process is one core; never a parallel run from a sub-agent) — handing out a number without
pinning it changes nothing. Read-only agents cost no core worth counting;
6–8 is a practical ceiling there.

Two hard rules: **no sub-agent runs the full gate (`make check` (prek + tests with coverage), `make ci`) or a
repo-wide lint** — the full gate runs once, in the main conversation, at the
end of the slice — and **no two writing agents in the same package**
(disjoint file sets, or `isolation: "worktree"`).

Every brief carries five things: the files and public surface plus one style
reference; the acceptance command the agent runs itself; the invariants it
touches; **stop conditions** (new dependency, API or wire change, credential
handling, an ADR-shaped decision — a stop is a successful outcome); and a
report format ≤ 250 words, large artefacts to the scratchpad as a path.

**A report is a claim.** Read the diff, run the gate yourself. For `guard`,
the acceptance artefact is not a green test but the **bite proof**: the named
production line removed, the test observed red with its message, the line
restored, green again.

---

## Token use

Set by the owner on 2026-10-14 (efficient use of the tokens matters to the
owner), as go-fabric's rule of the same date. A slice costs on
the order of half a million to a million tokens per implementing agent
before the owner's review; the rules below are what keeps that from
doubling.

- **Read slices, not files.** `sed -n a,bp`, `grep -n` with a tight
  pattern and `head`; a whole file only when the task is the file. Never
  re-read what is already in context; cite the earlier read.
- **Delegate first reads.** A source tree's inventory (Home Assistant core, aiohomematic, openccu-loom-client, this repo)
  is a `sweep` or Sonnet read written to the scratchpad with `file:line`
  for every fact; the owner spot-checks the load-bearing lines and verifies
  every fact about Home Assistant, aiohomematic or openccu-loom behaviour before it enters a brief or
  `docs/`, `changelog.md` or `AI_POLICY.md` — the agent's result is a map, never a citation.
- **Logs by their summary.** The gate (`make check` (prek + tests with coverage), `make ci`) runs in the
  background with a summary file (one line per gate, `FAIL`/`ok` lines
  only); read the summary, and open a log only on failure, with `grep` for
  the failure markers and the error strings — never `cat`. The same for CI:
  the job log is fetched once to a file and grepped.
- **One turn, every independent call.** Reads, checks and background
  starts that do not depend on each other go out together; a wait is a
  `Monitor` or an `until` loop in the background, not polling by hand.
- **Short artefacts.** A brief names files, decisions and the acceptance
  command, not prose; a report follows the fixed shape of
  [Sub-Agent Delegation](#sub-agent-delegation) (≤ 250 words, large
  artefacts as a scratchpad path); status messages to the owner are short,
  outcome first, in German.
- **Skip what cannot have changed.** No regeneration for a comment change;
  no second gate run for a notes-only commit — say what was skipped and
  why.
- **Edit by script.** Several replacements in several files are one
  scripted call with asserted anchors, not a chain of interactive edits;
  a generated file (the bundled frontend under `custom_components/homematicip_local/frontend/`, the translation files) is regenerated, never patched.
- **Agents read what the brief names.** An implementing agent gets the
  file list and the pinned sources in the brief, reads those, and reports
  in the fixed shape; it does not survey the tree. One agent per brief;
  two agents only on disjoint paths, at most one Opus agent at a time.
- **Push, pull request and tag are the session's own calls.** An
  implementing agent works locally — branch, commits, guards — and
  reports; the owner's session reads the diff, runs the gate, pushes,
  opens the pull request and tags the merge commit; the owner merges. A
  delegated push, pull request or tag is refused by the auto-mode
  classifier ("Create Public Surface", 2026-11-07), and the review in
  [Which model does which work](#which-model-does-which-work) sits
  between the agent's report and the push anyway.

---

## Tips for AI Assistants

### Interaction Protocol

These rules govern how the AI assistant communicates and works with the developer:

1. **Describe before coding**: Before writing any code, describe the planned approach and wait for explicit approval.
2. **Clarify ambiguities first**: If requirements are ambiguous or incomplete, ask clarifying questions before writing any code.
3. **Suggest edge cases after coding**: After finishing any code change, list edge cases and suggest test cases to cover them.
4. **Bug fix = test first**: When fixing a bug, start by writing a test that reproduces it, then fix the code until the test passes.
5. **Learn from corrections**: When corrected, reflect on what went wrong and describe a concrete plan to avoid repeating the mistake.

### Do's

✅ **Always** include `from __future__ import annotations` at the top of Python files
✅ **Always** provide complete type annotations for all functions and methods
✅ **Always** run prek hooks before committing
✅ **Always** write tests for new functionality
✅ **Always** update documentation when changing public APIs (see "Updating Documentation")
✅ **Always** check and update module/class/method docstrings after code changes
✅ **Always** use keyword-only arguments for ALL parameters (excluding self/cls)
✅ **Always** use descriptive variable names
✅ **Always** handle exceptions with proper context
✅ **Always** complete the Refactoring Completion Checklist before finishing
✅ **Always** update changelog.md with breaking changes
✅ **Always** create implementation plans the `impl` agent can execute without questions
✅ **Always** verify docs/*.md files are current after major changes
✅ **Always** describe your approach and wait for approval before writing code
✅ **Always** ask clarifying questions when requirements are ambiguous

### Don'ts

❌ **Never** commit without type annotations
❌ **Never** skip prek hooks
❌ **Never** commit to `main` directly
❌ **Never** use `Any` type without justification
❌ **Never** use bare `except:` clauses
❌ **Never** break backward compatibility without major version bump
❌ **Never** leave legacy compatibility layers or deprecated aliases
❌ **Never** create plans with ambiguities or "TBD" items
❌ **Never** poll for state updates (use push-based updates)
❌ **Never** create entities that poll (`_attr_should_poll = False`)
❌ **Never** start coding without describing the approach first
❌ **Never** assume ambiguous requirements — ask instead

### Common Pitfalls to Avoid

1. **Don't poll for state updates:**
   - This integration uses push-based updates
   - State comes via XML-RPC callbacks
   - Only system variables are polled (every 30s)

2. **Don't skip type hints:**
   - Mypy strict mode is enforced
   - All functions need full type annotations
   - Will fail CI if types are missing

3. **Don't ignore prek hooks:**
   - Hooks enforce code quality
   - Fix issues before committing
   - Use `--no-verify` only in emergencies

4. **Don't modify paramsets excessively:**
   - Warning: "Too much writing to device MASTER paramset could kill device's storage"
   - Be cautious with `put_paramset` operations

5. **Don't forget translation files:**
   - Update strings.json
   - Sync with translations/en.json and translations/de.json
   - Run check-translations hook

6. **Don't reorder `manifest.json` requirements — keep `aiohomematic` LAST:**
   - The `aiohomematic==...` pin MUST remain the final entry in the `requirements` list.
   - HA installs each requirement as its own `uv pip install --upgrade <req>` call (no
     atomic resolve, no `--constraint`). The sub-packages `aiohomematic-config` and
     `openccu-loom-client` depend on `aiohomematic` via open, upper-bound-less `>=` ranges,
     so a sibling install can pull a *newer* aiohomematic than the manifest pin. Whichever
     `aiohomematic` line runs LAST wins, so keeping the exact pin last lets it override any
     newer transitively-pulled version.
   - Moving it earlier reopens the dependency-version bug fixed in aiohomematic#2981 (and
     related to the version gate in `__init__.py`, see aiohomematic#3275).
   - The version gate in `async_setup_entry` is a **minimum-version** check: setup is only
     blocked when the installed aiohomematic is *older* than the manifest pin; a newer patch
     is allowed.
   - `manifest.json` and `requirements_test.txt` must declare the same versions —
     `tests/test_dependency_pins.py` fails by name when they drift, so a dependency bump
     always touches both files. CI runs against `requirements_test.txt`, so without that
     test a release can ship a pin nothing ever tested.

7. **`vol` is not voluptuous — don't rely on marker-replacement in `Schema.extend`:**
   - From HA 2026.9 on, `homeassistant/__init__.py` calls `install_as_voluptuous()`, so
     `import voluptuous` resolves to the **probatio** shim (`probatio._vol_shim`), not to
     voluptuous. The two disagree on marker identity: in voluptuous
     `Remove("x") == Required("x")` is `True` (measured on 0.13.1 … 0.16.0), in probatio
     0.11.3 it is `False` and `Remove` carries its own `__hash__`.
   - Consequence: `BASE.extend({vol.Remove("x"): …})` **keeps both markers** under probatio,
     so a key the schema was meant to drop stays `Required`. `Required` → `Optional` still
     replaces correctly; only `Remove` is affected.
   - Build a schema that differs structurally from its base by spelling it out, not by
     extending the base and undoing parts of it. See `CLICK_EVENT_SCHEMA` in `support.py`
     and aiohomematic#3374, where this silently stopped every `homematic.keypress` event.
   - Validation failures on the event path are DEBUG-level and non-fatal, so a broken schema
     produces no error and no trace — cover such paths end to end (payload → schema → bus),
     never each half on its own.

8. **The button blueprints trigger on event entities, the other blueprints on the bus event:**
   - `blueprints/automation/*actions-for-*` use HA's `event.received` entity trigger with the
     selected devices as `target.device_id` and `options.event_type: [press_short, press_long]`.
     They read `trigger.to_state.attributes.channel_no` / `event_type` and resolve the device
     with `device_id(trigger.entity_id)` — there is no `trigger.event.data` any more, and no
     device condition. `min_version` is 2026.8.0 (purpose-specific triggers left HA Labs in
     2026.7). `blueprints/community/*` still use `homematic.keypress`; both paths are supported
     and both are covered in `tests/test_blueprints.py`.
   - A device target is expanded through the device **and entity registry**, so a test needs a
     real device entry plus registered event entities (`register_remote()` in
     `tests/test_blueprints.py`); firing a bus event with an invented `device_id` no longer
     reaches anything. HA skips hidden entities and entities with an `entity_category` on that
     expansion (`helpers/target.py`), which is why event entities must keep neither.
   - `channel_no` is derived in `event.py` from `channel.address`, never read off the channel:
     aiohomematic spells it `ChannelProtocol.no`, the loom client's compat channel `.number`.
     The address is the one value both backends carry in `<address>:<no>` form.

9. **A repair issue outlives the object that would withdraw it:**
   - The issue registry survives a reload, a reconfigure and a restart; the per-session
     objects that take a repair back do not. `CentralConnectionState` publishes the
     `connected=True` event only for an interface it holds and is rebuilt empty with the
     central, and a client's `_is_callback_alive` starts `True`, so a healthy fresh client
     never reports its callback as restored. A repair of that shape is therefore permanent
     once its session ends — which is why `_STALE_ISSUE_TYPES` in `__init__.py` withdraws
     `connection` and `callback` on every setup of the entry. Before adding a type there,
     check that a fault which is still present raises it again after the start; `client`
     is not in the list because a fresh client's CONNECTED transition withdraws it anyway.
   - Compose every interface-scoped repair id with `support.get_issue_id()` and sweep with
     `support.async_delete_issues()`, which matches the prefix that helper produces. Do not
     rebuild an id from `{instance_name}-{interface}`: that is the aiohomematic interface
     id, while the loom daemon names the leading component itself. The trailing part is not
     always an interface id either — a JSON-RPC session issue carries the url there.
   - Cover such a path end to end (raise the repair through the handler, then sweep), never
     each half on its own: the type token in the id is the only thing that links them, and
     the issue registry does not persist the translation key.

### Refactoring Workflow

When performing a refactoring task, follow this workflow:

1. **Plan**: Create a detailed implementation plan (see Implementation Plan Requirements)
2. **Clarify**: Resolve ALL ambiguities before starting implementation
3. **Implement**: Make all changes following the exact plan
4. **Clean**: Remove all legacy code, aliases, and compatibility shims
5. **Test**: Run `make test` - all tests must pass
6. **Lint**: Run `make prek` - no errors allowed
7. **Document**: Update changelog.md
8. **Verify**: Check for leftover TODOs related to migration

### Implementation Plan Quality Standard

**A plan is only complete when the `impl` agent (Opus) can execute it without asking questions.**

Before finalizing any implementation plan, verify:

- [ ] Every file path is absolute and correct
- [ ] Every code block is complete (not "..." or "similar to above")
- [ ] Every import statement is explicitly listed
- [ ] Every type annotation is complete
- [ ] Every step has a clear verification method
- [ ] No decisions are deferred to implementation time

### When in Doubt

1. **Check existing patterns**: Review similar code in the codebase
2. **Run the tests**: `make test`
3. **Check the type hints**: `make mypy` will guide you
4. **Review the changelog**: `changelog.md` for recent changes

---

## Quick Reference

### Running Common Commands

All development tasks run via the `Makefile`. `make help` lists every target.

```bash
# Show all available targets
make help

# Setup development environment (dependencies + prek hooks)
make setup

# (Re-)install dependencies via uv
make install

# Format and auto-fix code
make format

# Lint code
make lint

# Type check (mypy strict)
make mypy

# Run all prek hooks
make prek

# Run tests with coverage
make test-cov

# Run specific test file
make test-file FILE=tests/test_config_flow.py

# Check translations
make translations

# Full quality gate (prek + tests with coverage)
make check

# Validate manifest/repository like CI (requires Docker)
make validate

# Start Home Assistant against the local ./config directory
make hass
```

### Important Files Reference

| File                      | Purpose                              |
| ------------------------- | ------------------------------------ |
| `__init__.py`             | Integration entry point              |
| `config_flow.py`          | Configuration UI & validation        |
| `control_unit.py`         | Central control logic                |
| `services.py`             | Service definitions & handlers       |
| `generic_entity.py`       | Base entity class                    |
| `entity_helpers.py`       | Entity creation utilities            |
| `const.py`                | Constants & enums                    |
| `manifest.json`           | Integration metadata                 |
| `strings.json`            | UI strings (primary source)          |
| `services.yaml`           | Service schema definitions           |

### Version Information

- **Current Version:** 2.12.4
- **Minimum HA Version:** 2026.11.0+
- **Python Target:** 3.14+ (CI tests on 3.14)
- **aiohomematic Version:** 2026.11.5
- **openccu-loom-client Version:** 2026.11.8. Its wire layer is generated against daemon API `16.3.4`
  (`openccu_loom_client.wire.const.DAEMON_API_VERSION`), but that number no longer gates the
  connection: `_report_api_version` **logs and never raises** — a warning when the majors differ,
  an info line when only the minors do. Refusing on it was wrong in both directions, because the
  daemon's major moved 7 → 8 → 9 → 10 → 11 inside one release window without touching surface this
  client calls, and because HACS updates the integration before the operator updates the daemon,
  so `minor(daemon) < minor(types)` is the ordinary state of an additive daemon release. The hard
  compatibility gate is the **capability handshake** (`_assert_capabilities`), which raises
  `LoomIncompatibleVersionError` when the daemon does not advertise a feature the caller declared
  as required; the schema digest is likewise only logged. Do not reintroduce a version-number
  gate here. `openccu-loom-types` is not a separate dependency, it is folded into the client

### External Resources

- **Main Documentation:** https://github.com/sukramj/homematicip_local
- **Contributing Guide:** See CONTRIBUTING.md
- **Issues:** https://github.com/sukramj/homematicip_local/issues
- **Discussions:** https://github.com/sukramj/homematicip_local/discussions
- **Changelog:** [changelog.md](changelog.md)
- **HACS:** Integration available via HACS

---

**Last Updated**: 2026-11-07
**Version**: 2.12.4
