# GitHub Copilot Instructions for Homematic(IP) Local

This file provides GitHub Copilot with context-specific instructions for working with the Homematic(IP) Local integration for Home Assistant.

## Project Context

**Project**: Homematic(IP) Local for OpenCCU
**Type**: Home Assistant Custom Integration
**Language**: Python 3.13+
**Domain**: `homematicip_local`
**Architecture**: Async, event-driven, push-based state updates

## Code Generation Rules

### 1. Import Requirements

**MANDATORY**: Every Python file must start with:

```python
from __future__ import annotations
```

### 2. Type Annotations

**STRICT MODE**: All code must be fully typed (mypy strict mode enabled).

```python
# ✅ CORRECT
def get_device(self, *, address: str) -> Device | None:
    """Return device by address."""
    return self._devices.get(address)

# ❌ INCORRECT - Missing types
def get_device(self, address):
    return self._devices.get(address)
```

### 3. Keyword-Only Arguments

**ALL parameters** (except `self`/`cls`) must be keyword-only:

```python
# ✅ CORRECT
def create_entity(
    *,  # Force keyword-only
    control_unit: ControlUnit,
    data_point: DataPoint,
) -> Entity:
    """Create a new entity."""
```

### 4. Docstring Conventions

- Always end with a period (`.`)
- Use imperative mood for methods: "Return device" (not "Returns")
- Use declarative for classes: "Represents a device"
- Don't repeat type information already in annotations

```python
# ✅ CORRECT
@property
def device_address(self) -> str:
    """Return the device address."""

# ❌ INCORRECT
@property
def device_address(self) -> str:
    """Returns the address as a string"""  # Wrong tense, no period, redundant
```

### 5. Import Organization

```python
from __future__ import annotations

# 1. Standard library
import asyncio
from typing import TYPE_CHECKING

# 2. Third-party (Home Assistant)
from homeassistant.core import HomeAssistant

# 3. First-party (aiohomematic)
from aiohomematic.const import Interface

# 4. Local imports
from .const import DOMAIN

# 5. TYPE_CHECKING imports
if TYPE_CHECKING:
    from aiohomematic.central import CentralUnit
```

## Architecture Patterns

### Entity Pattern

```python
class MyEntity(AioHomematicGenericEntity[GenericDataPoint], SensorEntity):
    """Entity description."""

    _attr_has_entity_name = True
    _attr_should_poll = False  # Always False - push-based updates only

    @property
    def native_value(self) -> StateType:
        """Return the current value."""
        return self._data_point.value
```

### Service Pattern

1. Define in `services.yaml` with schema
2. Implement handler in `services.py`
3. Register with `async_register_admin_service`
4. Add translations to `strings.json`, `translations/en.json`, `translations/de.json`

### Event Pattern

Events fired by the integration:
- `homematic.keypress` - Button press events (CLICK_EVENT_SCHEMA required)
- `homematic.impulse` - Impulse events
- `homematic.device_error` - Error state notifications (DEVICE_ERROR_EVENT_SCHEMA required)

## Critical Don'ts

❌ **Never** poll for state updates - use push-based updates only
❌ **Never** use `_attr_should_poll = True`
❌ **Never** omit type annotations
❌ **Never** use bare `except:` clauses
❌ **Never** create backward compatibility shims or deprecated aliases
❌ **Never** modify device MASTER paramsets excessively (can damage device storage)
❌ **Never** skip updating docstrings when changing code behavior
❌ **Never** forget to update translations (strings.json → en.json → de.json)

## Testing Requirements

- All new code must have tests
- Use pytest with `@pytest.mark.asyncio`
- Use existing fixtures from `tests/conftest.py`
- Aim for 100% coverage on critical files

## Pre-Commit Checks

Before suggesting commits, ensure code passes:

```bash
pre-commit run --all-files
```

This includes:
- ruff (linting & formatting)
- mypy (strict type checking)
- pylint (code quality)
- codespell (spell checking)
- translation validation

## Pull Request Guidelines

### Target Branch
- **Always target**: `devel` (NOT `master`)

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example**:
```
feat(climate): Add boost mode for HmIP-eTRV-2

Implements boost mode with new service and entity attributes.

Closes #123
```

### PR Checklist

Before submitting a PR:

```
□ All tests pass (pytest --cov=custom_components tests)
□ Pre-commit hooks pass (pre-commit run --all-files)
□ Type hints complete (mypy strict mode)
□ Docstrings updated
□ Translations added (strings.json, en.json, de.json)
□ Documentation updated (README.md, CLAUDE.md, docs/*.md as needed)
□ Changelog updated (changelog.md)
□ No legacy compatibility layers or deprecated code
```

## Common Import Aliases

```python
import voluptuous as vol

from aiohomematic.central import CentralUnit as hmcu
from aiohomematic.client import Client as hmcl
from aiohomematic.model.custom import definition as hmed
from aiohomematic.support import support as hms
```

## Version Information

- **Integration Version**: 2.0.0
- **Minimum HA Version**: 2025.10.0+
- **Python Target**: 3.13+
- **aiohomematic Version**: 2025.12.41

## Documentation Structure

When suggesting documentation updates:

- **CLAUDE.md** - AI development guide (architecture, patterns, strict rules)
- **CONTRIBUTING.md** - Human contributor guide
- **README.md** - User documentation
- **docs/BEHAVIORAL_COMPATIBILITY.md** - API stability guidelines
- **docs/naming.md** - Entity/device naming conventions
- **changelog.md** - Release history (update for every PR)

## Key Files

| File | Purpose |
|------|---------|
| `__init__.py` | Integration entry point |
| `config_flow.py` | Configuration UI & validation |
| `control_unit.py` | Central control logic |
| `services.py` | Service handlers |
| `generic_entity.py` | Base entity class |
| `const.py` | Constants & enums |
| `strings.json` | UI strings (primary source) |
| `manifest.json` | Integration metadata |

## Code Review Focus Areas

When reviewing code or generating suggestions:

1. **Type Safety**: Ensure full type coverage (mypy strict)
2. **Docstrings**: Check imperative mood, periods, no redundancy
3. **Keyword-Only Args**: Verify `*,` present in all method signatures
4. **Push vs Pull**: Ensure no polling (only push-based updates)
5. **Translation Coverage**: Check strings.json → en.json → de.json
6. **Test Coverage**: Suggest tests for new functionality
7. **Documentation**: Update relevant docs when behavior changes

## Integration-Specific Patterns

### Control Unit Access
```python
# Access central instance
central = control_unit.central

# Access device coordinator
device = central.device_coordinator.get_device(address=address)

# Access client coordinator
has_client = central.client_coordinator.has_client(interface_id=interface_id)
```

### Event Data Transformation
```python
# KEYPRESS/IMPULSE events need cleanup_click_event_data
event_data = cleanup_click_event_data(event_data=event_data)
if is_valid_event(event_data=event_data, schema=CLICK_EVENT_SCHEMA):
    hass.bus.async_fire(event_type=trigger_type.value, event_data=event_data)
```

### Device Lookup
```python
# Get device entry for device_id
if device_entry := self._async_get_device_entry(device_address=device_address):
    device_id = device_entry.id
    name = device_entry.name_by_user or device_entry.name
```

## Quality Standards

This is a production-grade integration with:
- 100% test coverage on critical files
- Strict mypy enforcement
- Comprehensive pre-commit validation
- Full bilingual support (English/German)
- Behavioral compatibility guarantees

Match this quality bar when generating code suggestions.

---

**For more details**, see:
- [CLAUDE.md](../CLAUDE.md) - Comprehensive AI development guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Human contribution guidelines
- [README.md](../README.md) - User documentation
