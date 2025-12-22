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
11. [Release Summary Maintenance](#release-summary-maintenance)
12. [Implementation Policy](#implementation-policy)
13. [Tips for AI Assistants](#tips-for-ai-assistants)
14. [Quick Reference](#quick-reference)

---

## Project Overview

**Project Name:** Homematic(IP) Local for OpenCCU
**Type:** Home Assistant Custom Integration
**Version:** 2.0.0
**Primary Language:** Python 3.13+
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
│   ├── BEHAVIORAL_COMPATIBILITY.md       # API stability guidelines
│   └── naming.md                         # Device and entity naming conventions
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

- **aiohomematic** (v2025.12.41) - Core async library for Homematic device communication
- **Home Assistant Core** - Minimum version: 2025.10.0+
- **Python 3.13+** (target version for development)

### Development Dependencies

- **pytest-homeassistant-custom-component** (0.13.300) - HA test framework
- **mypy** (1.19.1) - Static type checker (strict mode)
- **pylint** (4.0.4) - Code linting
- **ruff** (0.14.9) - Fast Python linter and formatter
- **pre-commit** (4.5.0) - Git hooks manager
- **aiohomematic-test-support** (2025.12.41) - Mock test data
- **async-upnp-client** (0.46.1) - UPnP discovery
- **uv** - Fast Python package installer (preferred over pip)

---

## Development Environment Setup

### Prerequisites

- **Python**: 3.13 or higher
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

   # Create virtual environment
   python3.13 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements_test.txt

   # Or use uv (faster)
   uv pip install -r requirements_test.txt

   # Setup pre-commit hooks
   pre-commit install
   ```

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
import voluptuous as vol

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

- **Target**: Python 3.13
- **Line Length**: 120 characters
- **Enabled Rules**: B, C, D, E, F, G, I, LOG, PT, SIM, and more
- **Auto-fix enabled** in pre-commit

```bash
# Auto-format all code
ruff format custom_components/homematicip_local/

# Lint code
ruff check --fix custom_components/homematicip_local/

# Check formatting without changes
ruff format --check custom_components/homematicip_local/
```

### Pre-commit Hooks (Run on Every Commit)

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
pre-commit run --all-files
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
# Run all tests with coverage
pytest --cov=custom_components tests

# Run with asyncio mode (as in CI)
pytest --cov=custom_components tests --asyncio-mode=legacy

# Run specific test file
pytest tests/test_config_flow.py

# Run with verbose output
pytest -v tests/

# Generate coverage report
pytest --cov=custom_components --cov-report=html tests/

# View HTML report
open htmlcov/index.html
```

### Test Configuration

- Framework: pytest with pytest-homeassistant-custom-component
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
   # Run pre-commit hooks
   pre-commit run --all-files

   # Run tests
   pytest --cov=custom_components tests
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
   python script/check_translations.py
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
| **docs/BEHAVIORAL_COMPATIBILITY.md** | Public API changes (events, services, triggers) |
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
pre-commit run prettier --all-files
```

---

## Git Workflow

### Branch Structure

- **Main Branch**: `master` (protected)
- **Development Branch**: `devel` (protected)
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

1. **Create feature branch** from `devel`
2. **Make changes** with tests
3. **Run pre-commit hooks**: `pre-commit run --all-files`
4. **Commit changes** with descriptive messages
5. **Push to remote**: `git push -u origin feature/branch-name`
6. **Create Pull Request** to `devel` branch
7. **Wait for CI** to pass
8. **Request review** from maintainers

---

## Release Summary Maintenance

The file `release_summary.md` provides a **user-focused, high-level summary** of changes across multiple versions. This is different from the detailed `changelog.md` - it consolidates many changes into meaningful user-facing improvements.

**Important**: `release_summary.md` documents **only changes made in this integration** (homematicip_local). Changes in the underlying aiohomematic library are already documented in [aiohomematic/release_summary.md](https://github.com/sukramj/aiohomematic/blob/devel/release_summary.md) and should not be duplicated here.

### Format

```markdown
# Version 2.0.0 - 2.1.0

## What's Changed

- **Feature Category**: Brief user-focused description
- **Another Category**: What users can now do differently
```

### Release States

| State | Format | Meaning |
|-------|--------|---------|
| Open | `Version 2.0.0 -` | Collecting changes from 2.0.0 onwards |
| Closed | `Version 2.0.0 - 2.1.0` | Summary of versions 2.0.0 through 2.1.0 |

### Task: "update release summary"

When the user requests "update release summary":

1. **Read current state**:
   ```bash
   head -1 release_summary.md
   git tag --list 'v2.*' | sort -V | tail -1
   ```

2. **If release is closed** (has end version):
   - Create new open release starting from the next version
   - Example: `Version 2.0.0 - 2.1.0` → add `Version 2.1.0 -`

3. **Analyze Git commits in the version range**:
   ```bash
   # Get commits since last release tag
   git log v2.0.0..HEAD --oneline --no-merges

   # Or between two tags
   git log v2.0.0..v2.1.0 --oneline --no-merges

   # See changed files in each commit
   git log v2.0.0..HEAD --name-only --oneline --no-merges
   ```

4. **Update the open release**:
   - Analyze commit messages and changed files in the range
   - **Filter out aiohomematic dependency updates**:
     - Commits with "Bump aiohomematic", "Update aiohomematic", etc.
     - Changes only to `manifest.json` or `requirements_test.txt`
   - **Focus on integration-specific changes**:
     - New features in custom_components/homematicip_local/
     - Config flow improvements
     - Service additions/changes
     - UI/UX enhancements
     - Bug fixes specific to the integration layer
   - Summarize from **user perspective** (not developer perspective)
   - Group related changes into categories
   - Consolidate and update existing points if they evolved
   - Keep descriptions brief and action-oriented

5. **Writing Style**:
   - Focus on what users can **do** or **experience** differently
   - Avoid implementation details (no class names, method names, etc.)
   - Combine multiple related changelog entries into one summary point
   - Use categories like: New Features, Improvements, Bug Fixes, Breaking Changes

### Example Transformation

**Git commits** (developer-focused):
```
a1b2c3d Add DpActionSelect entities for siren tone/light selection
d4e5f6g Implement config entry persistence for action select values
h7i8j9k Add translations for siren selection options (strings.json, de.json, en.json)
l0m1n2o Update README with automatic select entity documentation
p3q4r5s Fix async_added_to_hass timing for value loading
t6u7v8w Use deepcopy for config entry data modification
```

**Release summary** (user-focused):
```
- **Siren Control**: Automatic select entities for tone and light pattern selection (no manual InputHelper setup required)
```

**What NOT to include**:
```
x9y0z1a Bump aiohomematic to 2025.12.42  ❌ (dependency update, documented in aiohomematic)
b2c3d4e Update manifest.json requirements  ❌ (maintenance task)
f5g6h7i Run pre-commit hooks  ❌ (development process, not user-facing)
```

---

## Implementation Policy

This section defines mandatory rules for all implementations in this project.

### Refactoring Completion Checklist

**MANDATORY**: Every refactoring or feature implementation MUST complete ALL items before merging:

```
□ 1. Clean Code    - No legacy compatibility layers, deprecated aliases, or shims
□ 2. Tests         - pytest tests/ passes without errors
□ 3. Linting       - pre-commit run --all-files passes without errors
□ 4. Documentation - Docstrings, CLAUDE.md, README.md, docs/*.md updated as needed
□ 5. Changelog     - changelog.md updated with version entry
```

### Implementation Plan Requirements

**CRITICAL**: Implementation plans created by Opus/Sonnet MUST be executable by Haiku without errors.

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
# 1. Run all tests
pytest --cov=custom_components tests

# 2. Run all pre-commit hooks (includes ruff, mypy, pylint, etc.)
pre-commit run --all-files

# 3. Verify no TODO/FIXME related to migration
grep -r "TODO.*migration\|FIXME.*migration\|TODO.*remove\|TODO.*deprecated" custom_components/

# 4. Check for unused imports/code
ruff check --select F401,F841 custom_components/
```

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

**Migration best practices:**

- Always increment version number in migration
- Handle all previous versions in migration chain
- Test migration path from each previous version
- Document migration in changelog
- Never skip version numbers

---

## Tips for AI Assistants

### Do's

✅ **Always** include `from __future__ import annotations` at the top of Python files
✅ **Always** provide complete type annotations for all functions and methods
✅ **Always** run pre-commit hooks before committing
✅ **Always** write tests for new functionality
✅ **Always** update documentation when changing public APIs (see "Updating Documentation")
✅ **Always** check and update module/class/method docstrings after code changes
✅ **Always** use keyword-only arguments for ALL parameters (excluding self/cls)
✅ **Always** use descriptive variable names
✅ **Always** handle exceptions with proper context
✅ **Always** complete the Refactoring Completion Checklist before finishing
✅ **Always** update changelog.md with breaking changes
✅ **Always** create implementation plans that are Haiku-executable
✅ **Always** verify docs/*.md files are current after major changes

### Don'ts

❌ **Never** commit without type annotations
❌ **Never** skip pre-commit hooks
❌ **Never** commit to `master` or `devel` directly
❌ **Never** use `Any` type without justification
❌ **Never** use bare `except:` clauses
❌ **Never** break backward compatibility without major version bump
❌ **Never** leave legacy compatibility layers or deprecated aliases
❌ **Never** create plans with ambiguities or "TBD" items
❌ **Never** poll for state updates (use push-based updates)
❌ **Never** create entities that poll (`_attr_should_poll = False`)

### Common Pitfalls to Avoid

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

4. **Don't modify paramsets excessively:**
   - Warning: "Too much writing to device MASTER paramset could kill device's storage"
   - Be cautious with `put_paramset` operations

5. **Don't forget translation files:**
   - Update strings.json
   - Sync with translations/en.json and translations/de.json
   - Run check-translations hook

### Refactoring Workflow

When performing a refactoring task, follow this workflow:

1. **Plan**: Create a detailed implementation plan (see Implementation Plan Requirements)
2. **Clarify**: Resolve ALL ambiguities before starting implementation
3. **Implement**: Make all changes following the exact plan
4. **Clean**: Remove all legacy code, aliases, and compatibility shims
5. **Test**: Run `pytest tests/` - all tests must pass
6. **Lint**: Run `pre-commit run --all-files` - no errors allowed
7. **Document**: Update changelog.md
8. **Verify**: Check for leftover TODOs related to migration

### Implementation Plan Quality Standard

**A plan is only complete when Haiku can execute it without asking questions.**

Before finalizing any implementation plan, verify:

- [ ] Every file path is absolute and correct
- [ ] Every code block is complete (not "..." or "similar to above")
- [ ] Every import statement is explicitly listed
- [ ] Every type annotation is complete
- [ ] Every step has a clear verification method
- [ ] No decisions are deferred to implementation time

### When in Doubt

1. **Check existing patterns**: Review similar code in the codebase
2. **Run the tests**: `pytest tests/`
3. **Check the type hints**: `mypy` will guide you
4. **Review the changelog**: `changelog.md` for recent changes

---

## Quick Reference

### Running Common Commands

```bash
# Setup development environment
script/setup
script/bootstrap

# Install dependencies
pip install -r requirements_test.txt
# Or with uv (faster)
uv pip install -r requirements_test.txt

# Format code
ruff format custom_components/homematicip_local/

# Lint code
ruff check --fix custom_components/homematicip_local/

# Type check
mypy custom_components/homematicip_local/

# Run all checks
pre-commit run --all-files

# Run tests
pytest --cov=custom_components tests

# Run specific test file
pytest tests/test_config_flow.py

# Check translations
python script/check_translations.py
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

- **Current Version:** 2.0.0
- **Minimum HA Version:** 2025.10.0+
- **Python Target:** 3.13+ (CI tests on 3.13, 3.14)
- **aiohomematic Version:** 2025.12.41

### External Resources

- **Main Documentation:** https://github.com/sukramj/homematicip_local
- **Contributing Guide:** See CONTRIBUTING.md
- **aiohomematic Wiki:** https://github.com/sukramj/aiohomematic/wiki
- **Issues:** https://github.com/sukramj/aiohomematic/issues
- **Discussions:** https://github.com/sukramj/aiohomematic/discussions
- **Changelog:** https://github.com/sukramj/homematicip_local/blob/master/changelog.md
- **HACS:** Integration available via HACS

---

**Last Updated**: 2025-12-22
**Version**: 2.0.0
