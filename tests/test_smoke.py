"""
Smoke tests to contribute to coverage.

These tests perform minimal imports and basic assertions to ensure the
integration package is importable and exposes expected constants. They also
serve to validate the test setup and increase overall coverage as requested.
"""

from __future__ import annotations

from custom_components.homematicip_local.const import DOMAIN


def test_domain_constant() -> None:
    """Ensure the integration exposes the expected DOMAIN string."""
    assert DOMAIN == "homematicip_local"
