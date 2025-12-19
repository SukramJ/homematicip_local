#!/usr/bin/env python3
"""
Linter to verify config flow and repair issue translations are complete.

This script checks:
1. All config flow entry points set required title_placeholders
2. All repair issues have translations in all language files
3. All translation placeholders are present

Usage:
    python script/check_flow_translations.py

Exit codes:
    0: All checks passed
    1: Translation issues found
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

# Color codes for terminal output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def load_json(file_path: Path) -> dict[str, Any]:
    """Load and parse JSON file."""
    with file_path.open() as f:
        return json.load(f)


def check_flow_title_placeholders() -> bool:
    """Verify flow_title has {name} and {host} placeholders in all translation files."""
    print(f"\n{BOLD}1. Checking flow_title placeholders{RESET}")
    print("-" * 70)

    files = {
        "strings.json": Path("custom_components/homematicip_local/strings.json"),
        "en.json": Path("custom_components/homematicip_local/translations/en.json"),
        "de.json": Path("custom_components/homematicip_local/translations/de.json"),
    }

    all_ok = True
    for file_name, file_path in files.items():
        data = load_json(file_path)
        flow_title = data.get("config", {}).get("flow_title", "")

        if "{name}" in flow_title and "{host}" in flow_title:
            print(f"{GREEN}✓{RESET} {file_name}: flow_title has {{name}}/{{host}} placeholders")
        else:
            print(f"{RED}✗{RESET} {file_name}: flow_title missing required placeholders {{name}}/{{host}}")
            all_ok = False

    return all_ok


def check_entry_point_title_placeholders() -> bool:
    """Verify config flow entry points set title_placeholders in context."""
    print(f"\n{BOLD}2. Checking config flow entry points{RESET}")
    print("-" * 70)

    config_flow_path = Path("custom_components/homematicip_local/config_flow.py")
    content = config_flow_path.read_text()

    # Entry points that need to set title_placeholders
    entry_points = {
        "async_step_reauth": "Reauthentication flow",
        "async_step_reconfigure": "Reconfiguration flow",
        "async_step_ssdp": "SSDP discovery flow",
    }

    all_ok = True
    for method_name, description in entry_points.items():
        # Find the method definition
        method_pattern = rf"async def {method_name}\([^)]*\)[^:]*:.*?(?=\n    async def |\Z)"
        match = re.search(method_pattern, content, re.DOTALL)

        if not match:
            print(f"{YELLOW}?{RESET} {method_name}: Method not found (may have been renamed)")
            continue

        method_body = match.group(0)

        # Check if title_placeholders is set
        has_title_placeholders = 'context["title_placeholders"]' in method_body

        if has_title_placeholders:
            print(f"{GREEN}✓{RESET} {method_name}: Sets title_placeholders")
        else:
            print(f"{RED}✗{RESET} {method_name}: Missing title_placeholders - {description}")
            all_ok = False

    return all_ok


def check_reauth_flow_translations() -> bool:
    """Verify reauth flow translations are complete."""
    print(f"\n{BOLD}3. Checking reauth flow translations{RESET}")
    print("-" * 70)

    files = {
        "strings.json": Path("custom_components/homematicip_local/strings.json"),
        "en.json": Path("custom_components/homematicip_local/translations/en.json"),
        "de.json": Path("custom_components/homematicip_local/translations/de.json"),
    }

    all_ok = True
    for file_name, file_path in files.items():
        data = load_json(file_path)

        step = data.get("config", {}).get("step", {}).get("reauth_confirm", {})
        abort = data.get("config", {}).get("abort", {})

        checks = [
            (step.get("title"), "reauth_confirm step title"),
            (step.get("description"), "reauth_confirm description"),
            (step.get("data", {}).get("username"), "username field"),
            (step.get("data", {}).get("password"), "password field"),
            (abort.get("reauth_failed"), "reauth_failed abort"),
            (abort.get("reauth_successful"), "reauth_successful abort"),
        ]

        missing = [desc for value, desc in checks if not value]

        if not missing:
            print(f"{GREEN}✓{RESET} {file_name}: Complete")
        else:
            print(f"{RED}✗{RESET} {file_name}: Missing {len(missing)} item(s)")
            for desc in missing:
                print(f"    - {desc}")
            all_ok = False

    return all_ok


def check_reconfigure_flow_translations() -> bool:
    """Verify reconfigure flow translations are complete."""
    print(f"\n{BOLD}4. Checking reconfigure flow translations{RESET}")
    print("-" * 70)

    files = {
        "strings.json": Path("custom_components/homematicip_local/strings.json"),
        "en.json": Path("custom_components/homematicip_local/translations/en.json"),
        "de.json": Path("custom_components/homematicip_local/translations/de.json"),
    }

    all_ok = True
    for file_name, file_path in files.items():
        data = load_json(file_path)

        abort = data.get("config", {}).get("abort", {})

        checks = [
            (abort.get("reconfigure_failed"), "reconfigure_failed abort"),
            (abort.get("reconfigure_successful"), "reconfigure_successful abort"),
        ]

        missing = [desc for value, desc in checks if not value]

        if not missing:
            print(f"{GREEN}✓{RESET} {file_name}: Complete")
        else:
            print(f"{RED}✗{RESET} {file_name}: Missing {len(missing)} item(s)")
            for desc in missing:
                print(f"    - {desc}")
            all_ok = False

    return all_ok


def check_repair_issue_translations() -> bool:
    """Verify repair issue translations are complete with correct placeholders."""
    print(f"\n{BOLD}5. Checking repair issue translations{RESET}")
    print("-" * 70)

    files = {
        "strings.json": Path("custom_components/homematicip_local/strings.json"),
        "en.json": Path("custom_components/homematicip_local/translations/en.json"),
        "de.json": Path("custom_components/homematicip_local/translations/de.json"),
    }

    # Integration-specific repair issues
    repair_keys = [
        "central_degraded",
        "central_failed",
        "central_failed_network",
        "central_failed_timeout",
        "central_failed_internal",
    ]

    # Issues from aiohomematic (translation_key="issue.*")
    aiohomematic_issues = [
        "ping_pong_mismatch",
        "fetch_data_failed",
    ]

    # Combine all issues
    all_repair_keys = repair_keys + aiohomematic_issues

    placeholder_requirements = {
        # Integration-specific issues
        "central_degraded": ["instance_name", "reason"],
        "central_failed": ["instance_name", "reason"],
        "central_failed_network": ["instance_name", "interface_id"],
        "central_failed_timeout": ["instance_name", "interface_id"],
        "central_failed_internal": ["instance_name", "interface_id"],
        # aiohomematic issues
        "ping_pong_mismatch": ["interface_id", "mismatch_type", "mismatch_count"],
        "fetch_data_failed": ["interface_id"],
    }

    all_ok = True
    for file_name, file_path in files.items():
        data = load_json(file_path)
        issues = data.get("issues", {})
        missing = []

        for key in all_repair_keys:
            if key not in issues:
                missing.append(f"{key} (missing)")
            else:
                # Verify required placeholders
                desc = issues[key].get("description", "")
                title = issues[key].get("title", "")

                if not title:
                    missing.append(f"{key} (missing title)")

                if not desc:
                    missing.append(f"{key} (missing description)")

                # Check placeholders
                required = placeholder_requirements[key]
                missing_placeholders = [p for p in required if f"{{{p}}}" not in desc]

                if missing_placeholders:
                    missing.append(f"{key} (missing placeholders: {', '.join(missing_placeholders)})")

        if not missing:
            print(
                f"{GREEN}✓{RESET} {file_name}: All {len(all_repair_keys)} repair issues complete ({len(repair_keys)} integration + {len(aiohomematic_issues)} aiohomematic)"
            )
        else:
            print(f"{RED}✗{RESET} {file_name}: {len(missing)} issue(s) incomplete or missing")
            for item in missing:
                print(f"    - {item}")
            all_ok = False

    return all_ok


def check_error_message_translations() -> bool:
    """Verify error message translations are complete."""
    print(f"\n{BOLD}6. Checking error message translations{RESET}")
    print("-" * 70)

    files = {
        "strings.json": Path("custom_components/homematicip_local/strings.json"),
        "en.json": Path("custom_components/homematicip_local/translations/en.json"),
        "de.json": Path("custom_components/homematicip_local/translations/de.json"),
    }

    error_keys = ["invalid_auth", "cannot_connect", "invalid_config"]

    all_ok = True
    for file_name, file_path in files.items():
        data = load_json(file_path)
        errors = data.get("config", {}).get("error", {})
        missing = [key for key in error_keys if key not in errors]

        if not missing:
            print(f"{GREEN}✓{RESET} {file_name}: All {len(error_keys)} error messages present")
        else:
            print(f"{RED}✗{RESET} {file_name}: Missing {len(missing)} error message(s)")
            for key in missing:
                print(f"    - {key}")
            all_ok = False

    return all_ok


def main() -> int:
    """Run all translation checks."""
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}Config Flow & Repair Translation Linter{RESET}")
    print(f"{BOLD}{'=' * 70}{RESET}")

    # Run all checks
    checks = [
        check_flow_title_placeholders(),
        check_entry_point_title_placeholders(),
        check_reauth_flow_translations(),
        check_reconfigure_flow_translations(),
        check_repair_issue_translations(),
        check_error_message_translations(),
    ]

    # Summary
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    if all(checks):
        print(f"{GREEN}{BOLD}✅ ALL CHECKS PASSED{RESET}")
        print(f"{BOLD}{'=' * 70}{RESET}\n")
        return 0
    failed_count = sum(1 for check in checks if not check)
    print(f"{RED}{BOLD}✗ {failed_count} CHECK(S) FAILED{RESET}")
    print(f"{BOLD}{'=' * 70}{RESET}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
