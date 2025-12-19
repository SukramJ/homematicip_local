"""Tests for the check_flow_translations.py linter."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import pytest


@pytest.fixture
def temp_project_structure(tmp_path: Path) -> dict[str, Path]:
    """Create temporary project structure for testing."""
    # Create directory structure
    custom_components = tmp_path / "custom_components" / "homematicip_local"
    translations = custom_components / "translations"
    script_dir = tmp_path / "script"

    custom_components.mkdir(parents=True)
    translations.mkdir()
    script_dir.mkdir()

    # Copy the linter script
    linter_source = Path("script/check_flow_translations.py")
    linter_dest = script_dir / "check_flow_translations.py"
    linter_dest.write_text(linter_source.read_text())

    return {
        "root": tmp_path,
        "custom_components": custom_components,
        "translations": translations,
        "script": script_dir,
    }


@pytest.fixture
def valid_strings_json() -> dict[str, Any]:
    """Return valid strings.json structure."""
    return {
        "config": {
            "flow_title": "{name}/{host}",
            "step": {
                "reauth_confirm": {
                    "title": "Reauthenticate",
                    "description": "Enter credentials",
                    "data": {
                        "username": "Username",
                        "password": "Password",
                    },
                }
            },
            "abort": {
                "reauth_failed": "Reauth failed",
                "reauth_successful": "Reauth successful",
                "reconfigure_failed": "Reconfigure failed",
                "reconfigure_successful": "Reconfigure successful",
            },
            "error": {
                "invalid_auth": "Invalid credentials",
                "cannot_connect": "Cannot connect",
                "invalid_config": "Invalid config",
            },
        },
        "issues": {
            "central_degraded": {
                "title": "Connection degraded",
                "description": "Instance {instance_name} is degraded. Reason: {reason}",
            },
            "central_failed": {
                "title": "Connection failed",
                "description": "Instance {instance_name} failed. Reason: {reason}",
            },
            "central_failed_network": {
                "title": "Network error",
                "description": "Instance {instance_name} on {interface_id}",
            },
            "central_failed_timeout": {
                "title": "Timeout error",
                "description": "Instance {instance_name} on {interface_id}",
            },
            "central_failed_internal": {
                "title": "Internal error",
                "description": "Instance {instance_name} on {interface_id}",
            },
            "ping_pong_mismatch": {
                "title": "Ping-pong mismatch on {interface_id}",
                "description": "Mismatch on {interface_id}: {mismatch_type} - {mismatch_count}",
            },
            "fetch_data_failed": {
                "title": "Fetch failed",
                "description": "Failed on {interface_id}",
            },
        },
    }


@pytest.fixture
def valid_config_flow() -> str:
    """Return valid config_flow.py content."""
    return '''"""Config flow."""
from __future__ import annotations

from homeassistant.config_entries import ConfigFlowResult


class ConfigFlow:
    """Config flow."""

    async def async_step_reauth(self, entry_data: dict) -> ConfigFlowResult:
        """Handle reauth."""
        self.context["title_placeholders"] = {
            "name": "test",
            "host": "test",
        }
        return self.async_step_reauth_confirm()

    async def async_step_reconfigure(self, user_input: dict | None = None) -> ConfigFlowResult:
        """Handle reconfigure."""
        self.context["title_placeholders"] = {
            "name": "test",
            "host": "test",
        }
        return self.async_show_form()

    async def async_step_ssdp(self, discovery_info: dict) -> ConfigFlowResult:
        """Handle SSDP discovery."""
        self.context["title_placeholders"] = {"name": "test", "host": "test"}
        return self.async_step_user()
'''


class TestFlowTitlePlaceholders:
    """Tests for flow_title placeholder checking."""

    def test_missing_host_placeholder(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing {host} placeholder."""
        invalid_strings = valid_strings_json.copy()
        invalid_strings["config"]["flow_title"] = "{name}"

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "flow_title missing required placeholders" in result.stdout

    def test_missing_name_placeholder(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing {name} placeholder."""
        invalid_strings = valid_strings_json.copy()
        invalid_strings["config"]["flow_title"] = "{host}"

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "flow_title missing required placeholders" in result.stdout

    def test_valid_flow_title_all_files(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test that valid flow_title passes in all files."""
        for filename in ["strings.json", "en.json", "de.json"]:
            if filename == "strings.json":
                filepath = temp_project_structure["custom_components"] / filename
            else:
                filepath = temp_project_structure["translations"] / filename

            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py (needed for entry point checks)
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal config flow")

        # Run linter
        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "flow_title has {name}/{host} placeholders" in result.stdout


class TestEntryPointTitlePlaceholders:
    """Tests for entry point title_placeholders checking."""

    def test_missing_title_placeholders_in_reauth(
        self,
        temp_project_structure: dict[str, Path],
        valid_strings_json: dict[str, Any],
    ) -> None:
        """Test detection of missing title_placeholders in reauth."""
        # Create translation files
        for filename in ["strings.json", "en.json", "de.json"]:
            if filename == "strings.json":
                filepath = temp_project_structure["custom_components"] / filename
            else:
                filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create config_flow.py WITHOUT title_placeholders in reauth
        invalid_config_flow = '''"""Config flow."""
from __future__ import annotations

from homeassistant.config_entries import ConfigFlowResult


class ConfigFlow:
    """Config flow."""

    async def async_step_reauth(self, entry_data: dict) -> ConfigFlowResult:
        """Handle reauth."""
        # No title_placeholders here
        return self.async_step_reauth_confirm()

    async def async_step_reconfigure(self, user_input: dict | None = None) -> ConfigFlowResult:
        """Handle reconfigure."""
        self.context["title_placeholders"] = {
            "name": "test",
            "host": "test",
        }
        return self.async_show_form()

    async def async_step_ssdp(self, discovery_info: dict) -> ConfigFlowResult:
        """Handle SSDP discovery."""
        self.context["title_placeholders"] = {"name": "test", "host": "test"}
        return self.async_step_user()
'''

        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text(invalid_config_flow)

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "async_step_reauth: Missing title_placeholders" in result.stdout

    def test_valid_entry_points(
        self,
        temp_project_structure: dict[str, Path],
        valid_strings_json: dict[str, Any],
        valid_config_flow: str,
    ) -> None:
        """Test that valid entry points pass."""
        # Create translation files
        for filename in ["strings.json", "en.json", "de.json"]:
            if filename == "strings.json":
                filepath = temp_project_structure["custom_components"] / filename
            else:
                filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text(valid_config_flow)

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "async_step_reauth: Sets title_placeholders" in result.stdout
        assert "async_step_reconfigure: Sets title_placeholders" in result.stdout
        assert "async_step_ssdp: Sets title_placeholders" in result.stdout


class TestReauthFlowTranslations:
    """Tests for reauth flow translation checking."""

    def test_missing_reauth_confirm_title(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing reauth_confirm title."""
        invalid_strings = valid_strings_json.copy()
        del invalid_strings["config"]["step"]["reauth_confirm"]["title"]

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "reauth_confirm step title" in result.stdout

    def test_missing_username_field(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing username field."""
        invalid_strings = valid_strings_json.copy()
        del invalid_strings["config"]["step"]["reauth_confirm"]["data"]["username"]

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "username field" in result.stdout

    def test_valid_reauth_translations(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test that valid reauth translations pass."""
        for filename in ["strings.json", "en.json", "de.json"]:
            if filename == "strings.json":
                filepath = temp_project_structure["custom_components"] / filename
            else:
                filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal config flow")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Checking reauth flow translations" in result.stdout


class TestRepairIssueTranslations:
    """Tests for repair issue translation checking."""

    def test_missing_issue_title(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing issue title."""
        invalid_strings = valid_strings_json.copy()
        del invalid_strings["issues"]["fetch_data_failed"]["title"]

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "fetch_data_failed (missing title)" in result.stdout

    def test_missing_placeholder_in_issue(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing placeholder in issue."""
        invalid_strings = valid_strings_json.copy()
        # Remove mismatch_count placeholder
        invalid_strings["issues"]["ping_pong_mismatch"]["description"] = "Mismatch on {interface_id}: {mismatch_type}"

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "mismatch_count" in result.stdout

    def test_missing_repair_issue(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing repair issue."""
        invalid_strings = valid_strings_json.copy()
        del invalid_strings["issues"]["ping_pong_mismatch"]

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "ping_pong_mismatch (missing)" in result.stdout

    def test_valid_repair_issues(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test that valid repair issues pass."""
        for filename in ["strings.json", "en.json", "de.json"]:
            if filename == "strings.json":
                filepath = temp_project_structure["custom_components"] / filename
            else:
                filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "All 7 repair issues complete (5 integration + 2 aiohomematic)" in result.stdout


class TestErrorMessageTranslations:
    """Tests for error message translation checking."""

    def test_missing_error_message(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing error message."""
        invalid_strings = valid_strings_json.copy()
        del invalid_strings["config"]["error"]["invalid_auth"]

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "invalid_auth" in result.stdout

    def test_valid_error_messages(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test that valid error messages pass."""
        for filename in ["strings.json", "en.json", "de.json"]:
            if filename == "strings.json":
                filepath = temp_project_structure["custom_components"] / filename
            else:
                filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "All 3 error messages present" in result.stdout


class TestReconfigureFlowTranslations:
    """Tests for reconfigure flow translation checking."""

    def test_missing_reconfigure_abort(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test detection of missing reconfigure abort."""
        invalid_strings = valid_strings_json.copy()
        del invalid_strings["config"]["abort"]["reconfigure_successful"]

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "reconfigure_successful" in result.stdout

    def test_valid_reconfigure_translations(
        self, temp_project_structure: dict[str, Path], valid_strings_json: dict[str, Any]
    ) -> None:
        """Test that valid reconfigure translations pass."""
        for filename in ["strings.json", "en.json", "de.json"]:
            if filename == "strings.json":
                filepath = temp_project_structure["custom_components"] / filename
            else:
                filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create minimal config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text("# minimal")

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Checking reconfigure flow translations" in result.stdout


class TestIntegration:
    """Integration tests for the complete linter."""

    def test_all_checks_pass_with_valid_data(
        self,
        temp_project_structure: dict[str, Path],
        valid_strings_json: dict[str, Any],
        valid_config_flow: str,
    ) -> None:
        """Test that all checks pass with completely valid data."""
        # Create all translation files
        for filename in ["strings.json", "en.json", "de.json"]:
            if filename == "strings.json":
                filepath = temp_project_structure["custom_components"] / filename
            else:
                filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text(valid_config_flow)

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "ALL CHECKS PASSED" in result.stdout
        assert "flow_title has {name}/{host} placeholders" in result.stdout
        assert "async_step_reauth: Sets title_placeholders" in result.stdout
        assert "All 7 repair issues complete" in result.stdout
        assert "All 3 error messages present" in result.stdout

    def test_exit_code_1_on_any_failure(
        self,
        temp_project_structure: dict[str, Path],
        valid_strings_json: dict[str, Any],
        valid_config_flow: str,
    ) -> None:
        """Test that exit code is 1 when any check fails."""
        # Create invalid strings.json (missing flow_title placeholder)
        invalid_strings = valid_strings_json.copy()
        invalid_strings["config"]["flow_title"] = "{name}"  # Missing {host}

        filepath = temp_project_structure["custom_components"] / "strings.json"
        filepath.write_text(json.dumps(invalid_strings, indent=2))

        # Create valid en.json and de.json
        for filename in ["en.json", "de.json"]:
            filepath = temp_project_structure["translations"] / filename
            filepath.write_text(json.dumps(valid_strings_json, indent=2))

        # Create config_flow.py
        config_flow_path = temp_project_structure["custom_components"] / "config_flow.py"
        config_flow_path.write_text(valid_config_flow)

        result = subprocess.run(
            [sys.executable, "script/check_flow_translations.py"],
            cwd=temp_project_structure["root"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "CHECK(S) FAILED" in result.stdout
