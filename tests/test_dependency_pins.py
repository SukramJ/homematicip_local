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

`.pre-commit-config.yaml` and `requirements_test_pre_commit.txt` are the second
such pair: the hook `rev` decides what prek runs, the requirements file what a
developer or CI installs, and nothing tied the two together. Both had drifted by
the time this guard was written — codespell ran at `v2.4.2` against a pinned
`2.4.3`, python-typing-update at `v0.7.3` against `v0.8.1` — which means a hook
silently disagreed with the linter the same repository claimed to use.

The sister repository `openccu-loom-client` carries the same guard for the same
reason (`tests/unit/test_dependency_pins.py` there); this is its counterpart.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

import yaml

_ROOT = Path(__file__).resolve().parents[1]
_MANIFEST = _ROOT / "custom_components" / "homematicip_local" / "manifest.json"
_TEST_REQUIREMENTS = _ROOT / "requirements_test.txt"
_PRE_COMMIT_CONFIG = _ROOT / ".pre-commit-config.yaml"
_PRE_COMMIT_REQUIREMENTS = _ROOT / "requirements_test_pre_commit.txt"

# Which hook repository ships which distribution. Spelled out rather than derived
# from the repository name: `charliermarsh/ruff-pre-commit` ships `ruff`, and
# `adrienverge/yamllint.git` carries a suffix no rule would strip reliably. A
# guessed mapping would silently skip the pair it got wrong, which is the failure
# this guard exists to catch.
_HOOK_REPO_DISTRIBUTION: dict[str, str] = {
    "https://github.com/charliermarsh/ruff-pre-commit": "ruff",
    "https://github.com/codespell-project/codespell": "codespell",
    "https://github.com/PyCQA/bandit": "bandit",
    "https://github.com/adrienverge/yamllint.git": "yamllint",
    "https://github.com/cdce8p/python-typing-update": "python-typing-update",
}


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


def _pre_commit_requirement_pins() -> dict[str, str]:
    return _exact_pins(_PRE_COMMIT_REQUIREMENTS.read_text(encoding="utf-8").splitlines())


def _hook_revisions() -> dict[str, str]:
    """Map hook repository URL -> the `rev` it is pinned at."""
    config = yaml.safe_load(_PRE_COMMIT_CONFIG.read_text(encoding="utf-8"))
    return {repo["repo"]: str(repo["rev"]) for repo in config["repos"] if "rev" in repo}


def _without_v(version: str) -> str:
    """Return the version without a leading ``v``; the two files disagree on it."""
    return version.removeprefix("v")


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


class TestPreCommitPinsAgree:
    """A tool pinned both as a hook and as a requirement must name one version."""

    def test_every_pinned_requirement_is_mapped(self) -> None:
        """
        A tool added to the requirements must be mapped, or it is never compared.

        The mapping is maintained by hand, so an unmapped distribution would make
        the guard above skip it without saying so.
        """
        mapped = set(_HOOK_REPO_DISTRIBUTION.values())
        unmapped = sorted(set(_pre_commit_requirement_pins()) - mapped)
        assert not unmapped, (
            f"{unmapped} is pinned in requirements_test_pre_commit.txt but not mapped to a "
            f"hook repository in _HOOK_REPO_DISTRIBUTION, so its revision is never checked"
        )

    def test_hook_revisions_match_the_requirements(self) -> None:
        revisions = _hook_revisions()
        requirements = _pre_commit_requirement_pins()
        checked = 0
        for repo, dist in _HOOK_REPO_DISTRIBUTION.items():
            if repo not in revisions or dist not in requirements:
                continue
            checked += 1
            assert _without_v(revisions[repo]) == _without_v(requirements[dist]), (
                f"{dist} pin drifted: .pre-commit-config.yaml runs {revisions[repo]}, "
                f"requirements_test_pre_commit.txt installs {requirements[dist]}. The "
                f"hook and the tool a developer installs would then disagree."
            )
        assert checked, "no hook was matched to a requirement — the mapping went stale"
