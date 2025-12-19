# Config Flow & Repair Translation Linter

## Overview

The `check_flow_translations.py` linter ensures that all config flows and repair issues have complete translations with proper placeholders.

## What it Checks

### 1. Flow Title Placeholders
- Verifies that `flow_title` in all translation files contains `{name}` and `{host}` placeholders
- Checked in: `strings.json`, `en.json`, `de.json`

### 2. Config Flow Entry Points
- Ensures that config flow entry points set `title_placeholders` in the context
- Checks these methods in `config_flow.py`:
  - `async_step_reauth()` - Reauthentication flow
  - `async_step_reconfigure()` - Reconfiguration flow
  - `async_step_ssdp()` - SSDP discovery flow

### 3. Reauth Flow Translations
- Verifies complete translations for the reauth flow:
  - Step: `reauth_confirm` (title, description, data fields)
  - Abort reasons: `reauth_failed`, `reauth_successful`
  - Required fields: `username`, `password`

### 4. Reconfigure Flow Translations
- Verifies complete translations for the reconfigure flow:
  - Abort reasons: `reconfigure_failed`, `reconfigure_successful`

### 5. Repair Issue Translations
- Checks all repair issues are translated with correct placeholders:
  - `central_degraded` (requires: `instance_name`, `reason`)
  - `central_failed` (requires: `instance_name`, `reason`)
  - `central_failed_network` (requires: `instance_name`, `interface_id`)
  - `central_failed_timeout` (requires: `instance_name`, `interface_id`)
  - `central_failed_internal` (requires: `instance_name`, `interface_id`)

### 6. Error Message Translations
- Verifies all error messages are present:
  - `invalid_auth`
  - `cannot_connect`
  - `invalid_config`

## Usage

### Standalone

Run the linter directly from the command line:

```bash
python script/check_flow_translations.py
```

### Pre-commit Hook

The linter is automatically run as a pre-commit hook when you modify:
- `custom_components/homematicip_local/config_flow.py`
- `custom_components/homematicip_local/strings.json`
- `custom_components/homematicip_local/translations/en.json`
- `custom_components/homematicip_local/translations/de.json`

To run manually:

```bash
pre-commit run check-flow-translations --all-files
```

### CI/CD Integration

The linter returns:
- **Exit code 0**: All checks passed
- **Exit code 1**: Translation issues found

This makes it suitable for CI/CD pipelines:

```yaml
- name: Check translations
  run: python script/check_flow_translations.py
```

## Output Example

### Success

```
======================================================================
Config Flow & Repair Translation Linter
======================================================================

1. Checking flow_title placeholders
----------------------------------------------------------------------
✓ strings.json: flow_title has {name}/{host} placeholders
✓ en.json: flow_title has {name}/{host} placeholders
✓ de.json: flow_title has {name}/{host} placeholders

2. Checking config flow entry points
----------------------------------------------------------------------
✓ async_step_reauth: Sets title_placeholders
✓ async_step_reconfigure: Sets title_placeholders
✓ async_step_ssdp: Sets title_placeholders

...

======================================================================
✅ ALL CHECKS PASSED
======================================================================
```

### Failure

```
======================================================================
Config Flow & Repair Translation Linter
======================================================================

1. Checking flow_title placeholders
----------------------------------------------------------------------
✓ strings.json: flow_title has {name}/{host} placeholders
✓ en.json: flow_title has {name}/{host} placeholders
✗ de.json: flow_title missing required placeholders {name}/{host}

2. Checking config flow entry points
----------------------------------------------------------------------
✗ async_step_reauth: Missing title_placeholders - Reauthentication flow
✓ async_step_reconfigure: Sets title_placeholders
✓ async_step_ssdp: Sets title_placeholders

...

======================================================================
✗ 2 CHECK(S) FAILED
======================================================================
```

## When to Run

Run this linter:
1. **Before committing** translation changes
2. **After adding** new config flow entry points
3. **After adding** new repair issues
4. **When modifying** config flow methods that display titles

## Common Issues and Solutions

### Missing title_placeholders in Entry Point

**Issue:**
```
✗ async_step_reauth: Missing title_placeholders - Reauthentication flow
```

**Solution:**
Add title_placeholders setup at the beginning of the method:

```python
async def async_step_reauth(self, entry_data: ConfigType) -> ConfigFlowResult:
    """Handle reauthorization request."""
    entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
    if entry is None:
        return self.async_abort(reason="reauth_failed")

    # Set title placeholders for flow title display
    self.context["title_placeholders"] = {
        CONF_NAME: entry.data.get(CONF_INSTANCE_NAME, ""),
        CONF_HOST: entry.data.get(CONF_HOST, ""),
    }

    # ... rest of method
```

### Missing Repair Issue Translation

**Issue:**
```
✗ strings.json: 1 issue(s) incomplete or missing
    - central_failed_network (missing)
```

**Solution:**
Add the translation to all three files (strings.json, en.json, de.json):

```json
"issues": {
    "central_failed_network": {
        "title": "CCU network connection failed",
        "description": "The CCU connection for **{instance_name}** has failed.\n\nInterface: {interface_id}\n\n..."
    }
}
```

### Missing Placeholder in Translation

**Issue:**
```
✗ strings.json: 1 issue(s) incomplete or missing
    - central_failed_network (missing placeholders: interface_id)
```

**Solution:**
Add the missing placeholder to the description:

```json
"description": "The CCU connection for **{instance_name}** has failed.\n\nInterface: {interface_id}\n\n..."
```

## Related Scripts

- **check_translations.py** - Validates translation file structure and completeness
- **sort_class_members.py** - Sorts class members according to project standards

## Maintenance

When adding new features:

1. **New config flow entry point** → Update `entry_points` dict in `check_entry_point_title_placeholders()`
2. **New repair issue** → Add key to `repair_keys` and `placeholder_requirements` in `check_repair_issue_translations()`
3. **New error message** → Add key to `error_keys` in `check_error_message_translations()`

## Technical Details

- **Language**: Python 3.13+
- **Dependencies**: Standard library only (no external dependencies)
- **Execution time**: < 1 second
- **Files checked**: 4 (config_flow.py, strings.json, en.json, de.json)

## Author

Created: 2025-12-19
Maintained by: @SukramJ
