#!/usr/bin/env python3
"""
Check and maintain translation files.

- Reference: custom_components/homematicip_local/strings.json
- en.json must be an exact copy of strings.json (structure and values).
- de.json is validated against strings.json: report missing and extra keys.
- All three JSON files are kept sorted (recursively by keys). With --fix, the
  files are written back sorted; otherwise, an unsorted file will be reported.

Exit codes:
  0: Everything OK
  1: Problems found (missing/extra keys, not sorted, or en.json mismatch)

Usage:
  python3 script/check_translations.py [--fix]
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
REF_PATH = ROOT / "custom_components/homematicip_local/strings.json"
EN_PATH = ROOT / "custom_components/homematicip_local/translations/en.json"
DE_PATH = ROOT / "custom_components/homematicip_local/translations/de.json"


def load_json(path: Path) -> Any:
    """Load and parse a JSON file from the given path."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def sort_json(obj: Any) -> Any:
    """Recursively sort dictionaries by key; leave lists and scalars as-is."""
    if isinstance(obj, dict):
        return {k: sort_json(obj[k]) for k in sorted(obj.keys(), key=str)}
    if isinstance(obj, list):
        return [sort_json(i) for i in obj]
    return obj


def dumps_sorted(obj: Any) -> str:
    """Return a stable, pretty-printed JSON string with keys sorted recursively."""
    return json.dumps(sort_json(obj), ensure_ascii=False, indent=4, separators=(", ", ": ")) + "\n"


def flatten_keys(obj: Any, prefix: str = "") -> list[str]:
    """
    Return dotted key paths for all leaves in a nested dict structure.

    A leaf is anything that is not a dict (lists/values). We include the path to the
    non-dict value itself. For lists, we treat the list as a leaf at its key.
    """
    keys: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                keys.extend(flatten_keys(v, path))
            else:
                keys.append(path)
    # For top-level non-dict: just return the prefix itself
    elif prefix:
        keys.append(prefix)
    return keys


def compare_en(ref: Any, en: Any) -> tuple[bool, str, str]:
    """Return (matches, expected_str, actual_str) after sorting both."""
    expected = dumps_sorted(ref)
    actual = dumps_sorted(en)
    return expected == actual, expected, actual


def check_sorted_on_disk(path: Path, expected: str) -> bool:
    """Return True if the file exists and its content equals the expected string."""
    try:
        with path.open("r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return False
    return content == expected


def write_text(path: Path, content: str) -> None:
    """Write text content to a file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def main() -> int:
    """Entry point for the CLI that validates and optionally fixes translation files."""
    parser = argparse.ArgumentParser(description="Check and maintain translation files")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (write files sorted, sync en.json)")
    # Accept (and ignore) any filenames passed by pre-commit hooks
    parser.add_argument("paths", nargs="*", help="Optional file paths (ignored; script uses fixed locations)")
    args = parser.parse_args()

    problems: list[str] = []

    if not REF_PATH.exists():
        logger.error("Reference file not found: %s", REF_PATH)
        return 1

    ref = load_json(REF_PATH)
    en = load_json(EN_PATH) if EN_PATH.exists() else {}
    de = load_json(DE_PATH) if DE_PATH.exists() else {}

    # Prepare sorted JSON strings
    ref_sorted = dumps_sorted(ref)
    en_sorted = dumps_sorted(en)
    de_sorted = dumps_sorted(de)

    # Check sorting and write with --fix
    if not check_sorted_on_disk(REF_PATH, ref_sorted):
        if args.fix:
            write_text(REF_PATH, ref_sorted)
            logger.info("Sorted: %s", REF_PATH.relative_to(ROOT))
        else:
            problems.append(f"Not sorted: {REF_PATH.relative_to(ROOT)}")

    if not check_sorted_on_disk(DE_PATH, de_sorted):
        if args.fix:
            write_text(DE_PATH, de_sorted)
            logger.info("Sorted: %s", DE_PATH.relative_to(ROOT))
        else:
            problems.append(f"Not sorted: {DE_PATH.relative_to(ROOT)}")

    # Ensure en.json equals strings.json exactly
    matches, expected_en, _actual_en = compare_en(ref, en)
    if not matches:
        if args.fix:
            write_text(EN_PATH, expected_en)
            logger.info("Synced en.json with strings.json: %s", EN_PATH.relative_to(ROOT))
        else:
            problems.append("en.json does not match strings.json")
            # Also check if en.json itself is unsorted to provide a hint
            if not check_sorted_on_disk(EN_PATH, en_sorted):
                problems.append(f"Not sorted: {EN_PATH.relative_to(ROOT)}")

    # Compare keys for de.json
    ref_keys = sorted(flatten_keys(ref))
    de_keys = sorted(flatten_keys(de))
    missing = sorted(set(ref_keys) - set(de_keys))
    extra = sorted(set(de_keys) - set(ref_keys))

    if missing:
        problems.append("Missing keys in de.json:")
        problems.extend(f"  - {k}" for k in missing)
    if extra:
        problems.append("Extra keys in de.json:")
        problems.extend(f"  - {k}" for k in extra)

    if problems:
        logger.error("%s", "\n".join(problems))
        return 1

    logger.info("Translations OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
