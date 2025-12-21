# Contributing to Homematic(IP) Local for OpenCCU

Thank you for your interest in contributing to the Homematic(IP) Local integration! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Code Quality Standards](#code-quality-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)
- [Additional Resources](#additional-resources)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

---

## Getting Started

### Ways to Contribute

- **Report bugs**: Open an issue with detailed information
- **Suggest features**: Discuss ideas in GitHub Discussions
- **Improve documentation**: Fix typos, clarify instructions, add examples
- **Submit code**: Fix bugs or implement new features via Pull Requests

### Before You Start

1. **Check existing issues**: Search for similar issues or feature requests
2. **Discuss major changes**: For significant features, open a discussion first
3. **Review the architecture**: Read [CLAUDE.md](CLAUDE.md) for technical details

---

## Development Environment Setup

### Prerequisites

- **Python 3.13+** (required for development)
- **Git** for version control
- **pip** or **uv** (recommended) for package management

### Quick Setup

#### Option 1: DevContainer (Recommended)

If you use VS Code with the DevContainer extension:

```bash
# Open the project in VS Code
# Accept the prompt to reopen in DevContainer
# Environment will be automatically configured
```

#### Option 2: Manual Setup

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

### Verify Installation

```bash
# Run tests
pytest tests/

# Run code quality checks
pre-commit run --all-files
```

---

## Code Quality Standards

This project maintains high code quality standards. All contributions must pass automated checks.

### Type Annotations (mypy - STRICT MODE)

**All code must be fully typed.** This project uses mypy in strict mode.

```python
# ✅ CORRECT
def get_device(self, *, address: str) -> Device | None:
    """Return device by address."""
    return self._devices.get(address)

# ❌ INCORRECT - Missing type annotations
def get_device(self, address):
    return self._devices.get(address)
```

### Import Requirements

**Every Python file must start with:**

```python
from __future__ import annotations
```

#### Import Order

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

# 5. TYPE_CHECKING imports (to avoid circular imports)
if TYPE_CHECKING:
    from aiohomematic.central import CentralUnit
```

### Code Style

```python
# Use keyword-only arguments for all parameters (except self/cls)
def create_entity(
    *,  # Force keyword-only
    control_unit: ControlUnit,
    data_point: DataPoint,
) -> Entity:
    """Create a new entity."""
    ...

# Docstrings required for all public classes and methods
class HmDevice:
    """Representation of a Homematic device."""

    def get_channel(self, *, channel_no: int) -> Channel | None:
        """Return channel by number."""
        ...
```

### Docstring Standards

- **Always end with a period (`.`)**
- **Use imperative mood** for methods: "Return the device" (not "Returns" or "Gets")
- **Use declarative statements** for classes: "Represents a device"
- **Keep them concise**: Rely on type hints instead of repeating type information

```python
# ✅ CORRECT
@property
def device_address(self) -> str:
    """Return the device address."""

# ❌ INCORRECT - No period, wrong verb tense
@property
def device_address(self) -> str:
    """Returns the address as a string"""
```

### Pre-commit Hooks

Pre-commit hooks run automatically on every commit. They enforce:

- Code formatting (ruff)
- Type checking (mypy)
- Linting (ruff, pylint)
- Spell checking (codespell)
- YAML validation (yamllint)
- Translation validation

**Run manually:**

```bash
pre-commit run --all-files
```

**Do NOT bypass** hooks with `--no-verify` unless absolutely necessary.

---

## Testing

All code changes must include tests.

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=custom_components tests

# Run specific test file
pytest tests/test_config_flow.py

# Run with verbose output
pytest -v tests/

# Generate HTML coverage report
pytest --cov=custom_components --cov-report=html tests/
open htmlcov/index.html
```

### Test Requirements

- **New features**: Must include tests for all new functionality
- **Bug fixes**: Must include regression test
- **Coverage**: Aim for 100% coverage on modified files
- **All tests must pass** before submitting PR

### Test Framework

- **pytest** with pytest-homeassistant-custom-component
- **Asyncio mode**: Tests use `@pytest.mark.asyncio`
- **Fixtures**: Use existing fixtures from `tests/conftest.py`

---

## Submitting Changes

### Branch Structure

- **`master`**: Stable release branch (protected)
- **`devel`**: Development branch (protected)
- **Feature branches**: `feature/description` or `fix/description`

### Workflow

1. **Fork the repository** (external contributors) or create a branch (maintainers)

2. **Create a feature branch** from `devel`:
   ```bash
   git checkout devel
   git pull origin devel
   git checkout -b feature/my-feature
   ```

3. **Make your changes**:
   - Write code following the standards above
   - Add tests for all changes
   - Update documentation if needed

4. **Run quality checks**:
   ```bash
   # Run tests
   pytest --cov=custom_components tests

   # Run pre-commit hooks
   pre-commit run --all-files
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Add support for new device type"
   ```

6. **Push to your fork/branch**:
   ```bash
   git push -u origin feature/my-feature
   ```

7. **Create a Pull Request** to the `devel` branch

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:

```bash
feat(climate): Add boost mode support for HmIP-eTRV-2

Implements boost mode functionality with new service
and entity attributes for thermostat devices.

Closes #123
```

```bash
fix(config_flow): Handle connection timeout gracefully

Added retry logic with exponential backoff for CCU
connection validation during config flow.
```

### Pull Request Guidelines

- **Title**: Clear, descriptive title
- **Description**: Explain what and why (not how)
- **Link issues**: Reference related issues with `Closes #123`
- **Target branch**: Always target `devel`, not `master`
- **Pass CI checks**: All automated checks must pass
- **Code review**: Be responsive to feedback

### What Happens Next

1. **Automated CI checks** run (tests, linting, type checking)
2. **Code review** by maintainers
3. **Discussion and iteration** if changes are needed
4. **Merge to `devel`** once approved
5. **Release to `master`** in next version

---

## Reporting Issues

### Before Opening an Issue

1. **Search existing issues**: Your issue may already be reported
2. **Check discussions**: Feature requests often start as discussions
3. **Gather information**: Logs, Home Assistant version, device details

### Opening an Issue

Use the appropriate issue template:

- **Bug Report**: Describe the bug with reproduction steps
- **Feature Request**: Describe the feature and use case
- **Question**: Ask for help or clarification

**Include**:
- Home Assistant version
- Integration version
- CCU/hub type and version
- Device model (if device-specific)
- Relevant logs (enable debug logging if needed)

### Debug Logging

Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.homematicip_local: debug
    aiohomematic: debug
```

---

## Additional Resources

### Documentation

- **[CLAUDE.md](CLAUDE.md)**: Comprehensive technical documentation
- **[README.md](README.md)**: User documentation and setup guide
- **[changelog.md](changelog.md)**: Release history
- **[BEHAVIORAL_COMPATIBILITY.md](docs/BEHAVIORAL_COMPATIBILITY.md)**: API stability guidelines

### External Links

- **GitHub Repository**: https://github.com/sukramj/homematicip_local
- **aiohomematic Library**: https://github.com/sukramj/aiohomematic
- **Home Assistant**: https://www.home-assistant.io/
- **HACS**: https://hacs.xyz/

### Getting Help

- **GitHub Discussions**: For questions and feature discussions
- **GitHub Issues**: For bug reports
- **aiohomematic Wiki**: https://github.com/sukramj/aiohomematic/wiki

---

## Quick Reference

### Common Commands

```bash
# Format code
ruff format custom_components/homematicip_local/

# Lint code
ruff check --fix custom_components/homematicip_local/

# Type check
mypy custom_components/homematicip_local/

# Run all quality checks
pre-commit run --all-files

# Run tests
pytest --cov=custom_components tests

# Check translations
python script/check_translations.py
```

### Key Files

| File | Purpose |
|------|---------|
| `custom_components/homematicip_local/__init__.py` | Integration entry point |
| `custom_components/homematicip_local/config_flow.py` | Configuration UI |
| `custom_components/homematicip_local/control_unit.py` | Central control logic |
| `custom_components/homematicip_local/services.py` | Service handlers |
| `custom_components/homematicip_local/const.py` | Constants and enums |
| `custom_components/homematicip_local/manifest.json` | Integration metadata |
| `custom_components/homematicip_local/strings.json` | UI translations |

---

**Thank you for contributing to Homematic(IP) Local!** 🎉

Your contributions help make this integration better for everyone in the Home Assistant community.
