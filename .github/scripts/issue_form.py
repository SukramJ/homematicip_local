#!/usr/bin/env python3
"""
Shared helpers for parsing GitHub issue-form bodies.

Used by both CI issue scripts:

- ``analyze_issue.py`` — deterministic triage plus a short LLM summary.
- ``check_issue_template.py`` — verifies that the issue form was actually honored.

Everything in here is deterministic and free of third-party dependencies so the two
scripts can share it without pulling each other's imports.
"""

from __future__ import annotations

from collections.abc import Mapping
import re
from typing import Final

# =============================================================================
# Issue-form parsing
# =============================================================================

# Value GitHub inserts for empty issue-form fields
FORM_NO_RESPONSE: Final = "_No response_"

# Substring markers (casefold) identifying the integration-version form field in
# both template languages. The "last working version" field does not match these.
VERSION_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "what version of homematic",
    "bei welcher version von homematic",
)

# Substring markers (casefold) identifying the "did you use an AI tool" form field.
AI_TOOL_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "did you use an ai tool",
    "ki-tool eingesetzt",
)


def parse_form_fields(issue_body: str) -> dict[str, str]:
    """
    Parse a GitHub issue-form body into a mapping of field label to value.

    Issue forms render each field as a "### <label>" heading followed by the value.
    Empty fields ("_No response_") are normalized to an empty string.
    """
    fields: dict[str, str] = {}
    if not issue_body:
        return fields

    chunks = re.split(r"^### ", issue_body, flags=re.MULTILINE)
    for chunk in chunks[1:]:
        label, _, value = chunk.partition("\n")
        value = value.strip()
        if value == FORM_NO_RESPONSE:
            value = ""
        fields[label.strip()] = value

    return fields


def get_form_field(fields: Mapping[str, str], *, markers: tuple[str, ...]) -> str | None:
    """
    Return the value of the first form field whose label contains one of the markers.

    Returns None when no matching field exists (e.g. the issue was created without
    the template), and an empty string when the field exists but was left blank.
    """
    for label, value in fields.items():
        lowered = label.casefold()
        if any(marker in lowered for marker in markers):
            return value
    return None


# =============================================================================
# Label normalization
# =============================================================================

_MARKDOWN_LINK_PATTERN: Final = re.compile(r"\[([^\]]*)\]\([^)]*\)")
# Only "*" and backticks are stripped: "_" occurs inside identifiers such as
# "custom_component" and "homematicip_local_frontend" that appear in the labels.
_MARKDOWN_EMPHASIS_PATTERN: Final = re.compile(r"[*`]+")
_WHITESPACE_PATTERN: Final = re.compile(r"\s+")


def normalize_label(text: str) -> str:
    """
    Normalize a checkbox or field label for comparison against a template label.

    Markdown links are reduced to their link text, emphasis markers are dropped and
    whitespace is collapsed, so a label survives GitHub's rendering unchanged. The
    result is casefolded — comparisons are deliberately case-insensitive, since only
    structural changes (rewritten or omitted labels) should be flagged.
    """
    without_links = _MARKDOWN_LINK_PATTERN.sub(r"\1", text or "")
    without_emphasis = _MARKDOWN_EMPHASIS_PATTERN.sub("", without_links)
    return _WHITESPACE_PATTERN.sub(" ", without_emphasis).strip().casefold()


# =============================================================================
# Attachment / screenshot detection (deterministic)
# =============================================================================


def extract_attachment_urls(issue_body: str) -> tuple[list[str], list[str]]:
    """
    Extract URLs to attached diagnostic and log files from issue body.

    Returns tuple of (json_urls, log_urls).
    """
    # GitHub user-attachments pattern for uploaded files
    attachment_pattern = r"https://github\.com/user-attachments/files/\d+/[^\s\)\]\"']+"

    # Also match direct links to .json and .log files
    json_pattern = r"https://[^\s\)\]\"']+\.json(?:\?[^\s\)\]\"']*)?"
    log_pattern = r"https://[^\s\)\]\"']+\.log(?:\?[^\s\)\]\"']*)?"

    all_attachments = re.findall(attachment_pattern, issue_body)
    json_direct = re.findall(json_pattern, issue_body)
    log_direct = re.findall(log_pattern, issue_body)

    json_urls: list[str] = []
    log_urls: list[str] = []

    # Categorize attachments by extension or content type hint
    for url in all_attachments:
        url_lower = url.lower()
        if "config" in url_lower or "diagnostic" in url_lower or url_lower.endswith(".json"):
            json_urls.append(url)
        elif "log" in url_lower or "home-assistant" in url_lower or url_lower.endswith(".log"):
            log_urls.append(url)
        elif ".json" in url_lower:
            json_urls.append(url)
        elif ".log" in url_lower or ".txt" in url_lower:
            log_urls.append(url)

    # Add direct matches
    json_urls.extend(json_direct)
    log_urls.extend(log_direct)

    # Remove duplicates while preserving order
    json_urls = list(dict.fromkeys(json_urls))
    log_urls = list(dict.fromkeys(log_urls))

    return json_urls, log_urls


def detect_attachments(issue_body: str) -> tuple[bool, bool]:
    """
    Detect whether diagnostics and log data are attached to the issue.

    Returns tuple of (has_diagnostics, has_logs). Both require an uploaded file: a log
    excerpt pasted into a fenced code block does not count, because it is by definition
    a selection the reporter made, and the selection usually drops exactly the context
    the analysis needs. AI_POLICY.md states the same rule for reporters.
    """
    json_urls, log_urls = extract_attachment_urls(issue_body or "")
    return bool(json_urls), bool(log_urls)


def has_uploaded_file(issue_body: str) -> bool:
    """
    Return True if the body links at least one file uploaded through the GitHub UI.

    Stricter than :func:`detect_attachments`: an inline excerpt pasted into a fenced
    block does not count, only an actual uploaded file does.
    """
    json_urls, log_urls = extract_attachment_urls(issue_body or "")
    return bool(json_urls or log_urls)


_SCREENSHOT_PATTERN: Final = re.compile(
    r"user-attachments/assets/|!\[[^\]]*\]\(|\.(?:png|jpe?g|gif|webp)\b", re.IGNORECASE
)


def detect_screenshots(issue_body: str) -> bool:
    """Return True if the issue body contains screenshots or other images."""
    return bool(_SCREENSHOT_PATTERN.search(issue_body or ""))


# =============================================================================
# Template language detection
# =============================================================================

# German template markers - if any of these are found, the issue uses the German template
GERMAN_TEMPLATE_MARKERS: Final[tuple[str, ...]] = (
    "Ich stimme dem Folgenden zu",
    "Das Problem",
    "Bei welcher Version",
    "Welche Art von Installation",
    "Dieses Formular dient ausschließlich",
    "Diagnoseinformationen (keine Protokolle hier!)",
    "Protokolldatei (am besten DEBUG-Log)",
    "Welche Schnittstellen werden verwendet?",
)


def detect_template_language(issue_body: str) -> str:
    """
    Detect which template language was used based on template-specific markers.

    Returns "de" if German template markers are found, "en" otherwise.
    """
    if not issue_body:
        return "en"

    # Check for German template markers
    for marker in GERMAN_TEMPLATE_MARKERS:
        if marker in issue_body:
            return "de"

    return "en"
