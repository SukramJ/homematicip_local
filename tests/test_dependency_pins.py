"""
Guard the backend pins that are maintained in two files at once.

`manifest.json` is what Home Assistant installs for a user. `requirements_test.txt`
is what CI installs before running this suite. A package pinned exactly in both must
name the same version, or every test here runs against one version while users get
another — the suite stays green and the release ships broken.

That is not hypothetical. The `aiohomematic` pin sat at `2026.8.7` in the manifest
while CI ran `2026.8.8`, across the release that adopted 2026.8.8's re-keying of
system variables and programs. The registry migration added for it was therefore
tested against a backend that had re-keyed and shipped against one that had not.

The sister repository `openccu-loom-client` carries the same guard for the same
reason (`tests/unit/test_dependency_pins.py` there); this is its counterpart.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

_ROOT = Path(__file__).resolve().parents[1]
_MANIFEST = _ROOT / "custom_components" / "homematicip_local" / "manifest.json"
_TEST_REQUIREMENTS = _ROOT / "requirements_test.txt"


def _exact_pins(requirements: list[str]) -> dict[str, str]:
    """Map distribution name -> version for every ``name==version`` requirement."""
    out: dict[str, str] = {}
    for raw in requirements:
        if (line := raw.strip()) and not line.startswith("#") and "==" in line:
            name, version = line.split("==", 1)
            out[name.strip().lower()] = version.strip()
    return out


def _manifest_pins() -> dict[str, str]:
    return _exact_pins(json.loads(_MANIFEST.read_text(encoding="utf-8"))["requirements"])


def _test_requirement_pins() -> dict[str, str]:
    return _exact_pins(_TEST_REQUIREMENTS.read_text(encoding="utf-8").splitlines())


class TestBackendPinsAgree:
    """A package pinned in both files must name one version."""

    def test_shared_pins_match(self) -> None:
        manifest = _manifest_pins()
        ci = _test_requirement_pins()
        shared = sorted(set(manifest) & set(ci))
        assert shared, (
            "no package is pinned exactly in both files — either the guard's parsing "
            "broke or the pins moved, and it would pass vacuously either way"
        )
        for dist in shared:
            assert manifest[dist] == ci[dist], (
                f"{dist} pin drifted: manifest.json says {manifest[dist]}, "
                f"requirements_test.txt says {ci[dist]}. Home Assistant installs the "
                f"manifest; CI tests the other — so a mismatch ships untested code."
            )

    def test_the_two_backends_are_pinned_in_the_manifest(self) -> None:
        """
        Both backends stay exactly pinned rather than floored.

        This integration is the application at the top of the chain, so an exact pin
        here conflicts with nobody, and the two backends re-key entities between
        releases — an accidental range would migrate a registry against a version
        this suite never ran.
        """
        manifest = _manifest_pins()
        for dist in ("aiohomematic", "openccu-loom-client"):
            assert dist in manifest, f"{dist} is no longer pinned exactly in manifest.json"
            assert re.fullmatch(r"\d{4}\.\d+\.\d+", manifest[dist]), (
                f"{dist} pin {manifest[dist]!r} is not a calendar version"
            )
