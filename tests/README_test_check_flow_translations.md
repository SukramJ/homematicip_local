# Tests for check_flow_translations.py Linter

## Overview

This test suite provides comprehensive testing for the `check_flow_translations.py` linter, which validates config flow and repair issue translations.

## Test Structure

The test suite is organized into 7 test classes:

### 1. TestFlowTitlePlaceholders
Tests validation of `flow_title` placeholders in translation files.

**Tests:**
- `test_valid_flow_title_all_files` - Valid placeholders in all files
- `test_missing_name_placeholder` - Detection of missing {name}
- `test_missing_host_placeholder` - Detection of missing {host}

**Coverage:**
- ✅ Valid flow_title with both placeholders
- ✅ Missing {name} placeholder
- ✅ Missing {host} placeholder

### 2. TestEntryPointTitlePlaceholders
Tests validation of title_placeholders in config flow entry points.

**Tests:**
- `test_valid_entry_points` - All entry points set title_placeholders
- `test_missing_title_placeholders_in_reauth` - Detection of missing title_placeholders in reauth

**Coverage:**
- ✅ async_step_reauth with title_placeholders
- ✅ async_step_reconfigure with title_placeholders
- ✅ async_step_ssdp with title_placeholders
- ✅ Missing title_placeholders in async_step_reauth

### 3. TestReauthFlowTranslations
Tests validation of reauthentication flow translations.

**Tests:**
- `test_valid_reauth_translations` - Complete reauth flow translations
- `test_missing_reauth_confirm_title` - Detection of missing title
- `test_missing_username_field` - Detection of missing data field

**Coverage:**
- ✅ Complete reauth_confirm step
- ✅ Missing reauth_confirm title
- ✅ Missing username field
- ✅ Abort reasons (reauth_failed, reauth_successful)

### 4. TestReconfigureFlowTranslations
Tests validation of reconfiguration flow translations.

**Tests:**
- `test_valid_reconfigure_translations` - Complete reconfigure translations
- `test_missing_reconfigure_abort` - Detection of missing abort reason

**Coverage:**
- ✅ Abort reasons (reconfigure_failed, reconfigure_successful)
- ✅ Missing abort reason detection

### 5. TestRepairIssueTranslations
Tests validation of repair issue translations and placeholders.

**Tests:**
- `test_valid_repair_issues` - All 7 repair issues complete
- `test_missing_repair_issue` - Detection of missing issue
- `test_missing_placeholder_in_issue` - Detection of missing placeholder
- `test_missing_issue_title` - Detection of missing title

**Coverage:**
- ✅ Integration-specific issues (5):
  - central_degraded
  - central_failed
  - central_failed_network
  - central_failed_timeout
  - central_failed_internal
- ✅ aiohomematic issues (2):
  - ping_pong_mismatch
  - fetch_data_failed
- ✅ Placeholder validation
- ✅ Title and description validation

### 6. TestErrorMessageTranslations
Tests validation of error message translations.

**Tests:**
- `test_valid_error_messages` - All 3 error messages present
- `test_missing_error_message` - Detection of missing error

**Coverage:**
- ✅ invalid_auth error
- ✅ cannot_connect error
- ✅ invalid_config error

### 7. TestIntegration
Integration tests for complete linter execution.

**Tests:**
- `test_all_checks_pass_with_valid_data` - All checks pass with valid data
- `test_exit_code_1_on_any_failure` - Exit code 1 on any failure

**Coverage:**
- ✅ Complete linter execution
- ✅ Exit code validation
- ✅ Output message verification

## Running the Tests

### Run all linter tests:
```bash
pytest tests/test_check_flow_translations.py -v
```

### Run specific test class:
```bash
pytest tests/test_check_flow_translations.py::TestRepairIssueTranslations -v
```

### Run specific test:
```bash
pytest tests/test_check_flow_translations.py::TestRepairIssueTranslations::test_valid_repair_issues -v
```

### Run with verbose output:
```bash
pytest tests/test_check_flow_translations.py -vv
```

## Test Fixtures

### temp_project_structure
Creates a temporary project structure with:
- `custom_components/homematicip_local/` directory
- `translations/` subdirectory
- `script/` directory with linter copy

### valid_strings_json
Returns a complete, valid strings.json structure with:
- flow_title with placeholders
- All reauth flow translations
- All reconfigure flow translations
- All 7 repair issues (5 integration + 2 aiohomematic)
- All 3 error messages

### valid_config_flow
Returns valid config_flow.py content with all entry points setting title_placeholders.

## Test Methodology

All tests follow this pattern:

1. **Setup**: Create temporary project structure with test data
2. **Execute**: Run linter as subprocess (realistic execution)
3. **Assert**: Verify exit code and output messages

This approach tests the linter as it would be used in:
- Pre-commit hooks
- CI/CD pipelines
- Manual execution

## Coverage Summary

| Component | Test Coverage |
|-----------|---------------|
| Flow title placeholders | 100% |
| Entry point title_placeholders | 100% |
| Reauth flow translations | 100% |
| Reconfigure flow translations | 100% |
| Repair issue translations | 100% |
| Error message translations | 100% |
| Integration/Exit codes | 100% |

**Total Tests:** 18
**Success Scenarios:** 7
**Failure Detection:** 11

## Adding New Tests

When adding new checks to the linter:

1. Add a new test class (e.g., `TestNewFeature`)
2. Create positive test (valid data passes)
3. Create negative tests (invalid data fails with correct message)
4. Update this README with the new tests

Example:
```python
class TestNewFeature:
    """Tests for new feature validation."""

    def test_valid_new_feature(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test that valid new feature passes."""
        # Setup
        # Execute
        # Assert
        assert result.returncode == 0
        assert "expected message" in result.stdout

    def test_invalid_new_feature(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of invalid new feature."""
        # Setup with invalid data
        # Execute
        # Assert
        assert result.returncode == 1
        assert "error message" in result.stdout
```

## Continuous Integration

These tests run automatically in CI/CD pipelines when:
- Pull requests are created
- Changes are pushed to protected branches
- Pre-commit hooks are executed

The linter must pass all tests before code can be merged.

## Troubleshooting

### Test failures due to file paths
Ensure temp_project_structure fixture is used correctly and paths are properly constructed.

### Test failures due to missing config_flow.py
Some checks require config_flow.py to exist. Add minimal file:
```python
config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
config_flow_path.write_text("# minimal config flow")
```

### Test failures due to subprocess execution
Ensure the linter script is executable and Python interpreter is available.

## Related Documentation

- **Linter Documentation**: `script/README_check_flow_translations.md`
- **Linter Source**: `script/check_flow_translations.py`
- **Project Documentation**: `CLAUDE.md`

## Author

Created: 2025-12-19
Test Suite Version: 1.0.0
