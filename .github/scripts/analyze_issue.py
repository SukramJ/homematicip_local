#!/usr/bin/env python3
"""
Issue triage script for AioHomematic and Homematic(IP) Local.

This script performs deterministic triage of newly created issues: it checks that the
required raw data (integration diagnostics, log file) is attached, validates the reported
version against the published releases, detects pasted AI analyses, and searches for
similar issues. Claude is only used for a short summary and documentation-link selection —
it does NOT diagnose root causes.

An audit of 181 bot-commented issues (2026-07) showed that LLM root-cause analyses were
fully correct in only 18% of cases and outright wrong in 24%, so all diagnosis sections
were removed in favor of deterministic checks. Do not re-add root-cause claims to the
public comment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from itertools import islice
import json
import os
import re
import sys
from typing import Any, Final, cast

from anthropic import Anthropic
from github import Auth, Github, GithubException, Repository
from issue_form import (
    AI_TOOL_FIELD_MARKERS,
    VERSION_FIELD_MARKERS,
    detect_attachments,
    detect_screenshots,
    detect_template_language,
    get_form_field,
    parse_form_fields,
)

# Integration repository for version lookups
INTEGRATION_REPO: Final = "SukramJ/homematicip_local"

# Maximum number of releases to scan when building the known-version set
MAX_RELEASES_TO_SCAN: Final = 100

# Claude model used for the triage summary (override via the ANALYZER_MODEL env var)
DEFAULT_ANALYZER_MODEL: Final = "claude-sonnet-4-5"

# Documentation links
DOCS_LINKS: Final[dict[str, str]] = {
    "main_readme": "https://sukramj.github.io/aiohomematic/",
    "homematicip_local_readme": "https://github.com/sukramj/homematicip_local#homematicip_local",
    "troubleshooting": "https://sukramj.github.io/aiohomematic/user/troubleshooting/homeassistant_troubleshooting/",
    "releases": "https://github.com/sukramj/homematicip_local/releases",
    "architecture": "https://sukramj.github.io/aiohomematic/architecture/",
    "naming": "https://sukramj.github.io/aiohomematic/contributor/coding/naming/",
    "unignore": "https://sukramj.github.io/aiohomematic/user/advanced/unignore/",
    "lifecycle": "https://sukramj.github.io/aiohomematic/developer/homeassistant_lifecycle/",
    "glossary": "https://sukramj.github.io/aiohomematic/reference/glossary/",
    "discussions": "https://github.com/sukramj/aiohomematic/discussions",
}

# Hard precondition for bug reports, quoted at AI tools that draft issues
AI_POLICY_URL: Final = "https://github.com/SukramJ/aiohomematic/blob/main/AI_POLICY.md#stop--hard-precondition-for-bug-reports"


# =============================================================================
# Version check (deterministic — compared against published releases only)
# =============================================================================


def parse_version(version_str: str) -> tuple[int, int, int, str] | None:
    """
    Parse a version string into components.

    Returns tuple of (major, minor, patch, prerelease) or None if invalid.
    """
    if not version_str:
        return None

    # Match patterns like "1.90.2", "1.91.0b32"
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(b\d+)?$", version_str.strip())
    if not match:
        return None

    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))
    prerelease = match.group(4) or ""

    return (major, minor, patch, prerelease)


@dataclass(frozen=True)
class ReleaseInfo:
    """Published release versions of the integration."""

    stable: str | None = None
    prerelease: str | None = None
    all_versions: frozenset[str] = field(default_factory=frozenset)


def fetch_release_info(gh: Github) -> ReleaseInfo:
    """
    Fetch the published release versions from the integration repository.

    Returns the latest stable version, the latest pre-release version and the set of
    all known release versions (tag names without a leading "v").
    """
    stable: str | None = None
    prerelease: str | None = None
    versions: set[str] = set()

    try:
        repo = gh.get_repo(INTEGRATION_REPO)
        for index, release in enumerate(repo.get_releases()):
            if index >= MAX_RELEASES_TO_SCAN:
                break
            if release.draft:
                continue
            tag = release.tag_name.removeprefix("v")
            versions.add(tag)
            if release.prerelease:
                if prerelease is None:
                    prerelease = tag
            elif stable is None:
                stable = tag
    except GithubException as e:
        print(f"Warning: Could not fetch releases from GitHub: {e}")

    return ReleaseInfo(stable=stable, prerelease=prerelease, all_versions=frozenset(versions))


@dataclass(frozen=True)
class VersionCheck:
    """Deterministic result of comparing the reported version against known releases."""

    # One of: "missing", "no_data", "ok", "outdated", "unknown"
    status: str
    reported: str = ""
    stable: str = ""
    prerelease: str = ""


# Leading version token inside a free-text version field, e.g. "2.11.0" in
# "2.11.0 (aiohomematic 2026.9.1) - also reproduced on 2.10.0".
_VERSION_TOKEN_PATTERN: Final = re.compile(r"\bv?(\d+\.\d+(?:\.\d+)?(?:b\d+)?)\b")


def extract_version_token(reported: str) -> str:
    """
    Return the first version-like token in a free-text version field value.

    Reporters (and AI tools filling the form) routinely add context to the field, e.g.
    "2.11.0 (aiohomematic 2026.9.1)". Matching the raw value against the release list
    then fails and the field is reported as missing, which is wrong and undermines the
    bot comment. Falls back to the stripped input when no token is found.
    """
    if (match := _VERSION_TOKEN_PATTERN.search(reported)) is not None:
        return match.group(1)
    return reported.strip().removeprefix("v")


def check_reported_version(reported: str | None, *, releases: ReleaseInfo) -> VersionCheck:
    """
    Check the version reported in the form field against the published releases.

    The check is purely deterministic: a version is only flagged as "unknown" when it
    matches none of the actually published release versions, and as "outdated" only
    when it is a known release older than the current stable one. When the release
    list could not be fetched, no statement about validity is made ("no_data").
    """
    stable = releases.stable or ""
    prerelease = releases.prerelease or ""

    if reported is None or not reported.strip():
        return VersionCheck(status="missing", stable=stable, prerelease=prerelease)

    normalized = extract_version_token(reported)

    if not releases.all_versions:
        return VersionCheck(status="no_data", reported=normalized, stable=stable, prerelease=prerelease)

    if normalized in releases.all_versions:
        rep_parsed = parse_version(normalized)
        stable_parsed = parse_version(stable) if stable else None
        if rep_parsed and stable_parsed and rep_parsed[:3] < stable_parsed[:3]:
            return VersionCheck(status="outdated", reported=normalized, stable=stable, prerelease=prerelease)
        return VersionCheck(status="ok", reported=normalized, stable=stable, prerelease=prerelease)

    # Tolerate shortened versions like "2.8" when a release "2.8.x" exists.
    if "." in normalized and any(
        version.startswith((f"{normalized}.", f"{normalized}b")) for version in releases.all_versions
    ):
        return VersionCheck(status="ok", reported=normalized, stable=stable, prerelease=prerelease)

    return VersionCheck(status="unknown", reported=normalized, stable=stable, prerelease=prerelease)


# =============================================================================
# AI-paste detection
# =============================================================================

# Markers that strongly indicate AI-authored content - any single match triggers detection.
STRONG_AI_MARKERS: Final[tuple[str, ...]] = (
    # Self-identification of the model
    "as an ai",
    "as a large language model",
    "as an llm",
    "i am an ai",
    "i'm an ai",
    "language model",
    "als ki",
    "als ein ki",
    "ich bin eine ki",
    "ich bin ein ki",
    "sprachmodell",
    # Authorship disclosure. Reports written end-to-end by an assistant increasingly
    # open with such a line instead of the self-identification markers above; a line
    # like "This report was written by <assistant>" went undetected without these.
    "ai disclosure",
    "ki-offenlegung",
    "written by claude",
    "written by chatgpt",
    "written by copilot",
    "written by gemini",
    "generated by claude",
    "generated by chatgpt",
    "generated by copilot",
    "generated by gemini",
    "geschrieben von claude",
    "verfasst von claude",
    "verfasst von chatgpt",
    "ai-generated report",
    "ki-generierter bericht",
)

# Stylistic markers typical of AI analyses - need at least MIN_WEAK_AI_MARKERS distinct matches.
WEAK_AI_MARKERS: Final[tuple[str, ...]] = (
    "based on the logs",
    "based on the provided",
    "based on the diagnostics",
    "it appears that",
    "it seems that",
    "here's a summary",
    "here is a summary",
    "here's a breakdown",
    "here is a breakdown",
    "here's an analysis",
    "here is an analysis",
    "root cause analysis",
    "probable cause",
    "likely cause",
    "possible cause",
    "possible root cause",
    "in summary,",
    "to summarize",
    "let me analyze",
    "i'll analyze",
    "recommended steps",
    "recommended actions",
    "step-by-step",
    # Source-code reasoning offered in place of the raw data
    "derivation from the source",
    "rather than a measurement",
    "a minimal fix would be",
    "ableitung aus dem quellcode",
    "ein minimaler fix",
    "auf grundlage der logs",
    "auf basis der logs",
    "es scheint, dass",
    "es sieht so aus",
    "wahrscheinliche ursache",
    "mögliche ursache",
    "wahrscheinliche ursachen",
    "mögliche ursachen",
    "zusammenfassend",
    "hier ist eine analyse",
    "hier ist eine zusammenfassung",
    "lösungsvorschlag",
    "empfohlene schritte",
    "schritt für schritt",
    "schritt-für-schritt",
)

# Minimum number of distinct weak markers required to flag a body as AI-generated.
MIN_WEAK_AI_MARKERS: Final = 2

# Marker recorded when the reporter answered the template's "did you use an AI tool" field.
DISCLOSED_IN_FORM_MARKER: Final = "disclosed-in-form"

# First token of an AI-tool form answer that denies AI use. Anything else counts as a
# disclosure - the field is free text, so only an explicit denial is treated as "no".
AI_TOOL_DENIALS: Final[frozenset[str]] = frozenset(
    {"no", "not", "none", "nope", "n/a", "na", "nein", "kein", "keine", "keins", "nö", "-", "0"}
)


def is_ai_tool_disclosed(ai_tool_field: str | None) -> bool:
    """
    Return True if the template's AI-tool field states that an AI tool was used.

    The field is optional free text ("no", "Claude wrote the text", "ChatGPT for the
    translation"), so the check is deliberately asymmetric: an empty field or an answer
    starting with an explicit denial is a "no", everything else is a disclosure.
    """
    if not ai_tool_field or not ai_tool_field.strip():
        return False

    # Split on whitespace only, then strip trailing punctuation: "n/a" must survive as
    # one token, while "No." and "Nein," must reduce to their bare denial.
    first_token = ai_tool_field.strip().casefold().split()[0].strip(",.;:!")
    return first_token not in AI_TOOL_DENIALS


def detect_ai_generated_analysis(issue_body: str, *, ai_tool_field: str | None = None) -> dict[str, Any]:
    """
    Detect whether the issue body was written by, or contains output of, an AI tool.

    Reporters increasingly paste an AI tool's interpretation instead of the raw
    diagnostics/log file. Such interpretations are frequently wrong and cannot replace
    the raw data. This heuristic flags likely AI prose so the bot can redirect the
    reporter to attach the underlying files.

    Three independent signals, in descending reliability:

    1. The reporter answered the template's AI-tool field with anything but a denial.
    2. A single strong marker (self-identification or an authorship disclosure).
    3. At least MIN_WEAK_AI_MARKERS distinct stylistic markers.

    Returns a dict with "detected" (bool), "strong" (bool), "disclosed" (bool) and
    "markers" (list of str).
    """
    result: dict[str, Any] = {"detected": False, "strong": False, "disclosed": False, "markers": []}

    disclosed = is_ai_tool_disclosed(ai_tool_field)
    lowered = (issue_body or "").lower()

    strong_hits = [marker for marker in STRONG_AI_MARKERS if marker in lowered]
    weak_hits = [marker for marker in WEAK_AI_MARKERS if marker in lowered]

    if disclosed:
        result["disclosed"] = True
        result["detected"] = True
        result["strong"] = True
        result["markers"] = [DISCLOSED_IN_FORM_MARKER, *strong_hits, *weak_hits]
    elif strong_hits:
        result["detected"] = True
        result["strong"] = True
        result["markers"] = strong_hits + weak_hits
    elif len(weak_hits) >= MIN_WEAK_AI_MARKERS:
        result["detected"] = True
        result["markers"] = weak_hits

    return result


# =============================================================================
# Search terms and similar issues
# =============================================================================

# Device model designations like "HmIP-eTRV-2", "HM-PB-2-WM55", "HB-UNI-Sen-..."
_DEVICE_MODEL_PATTERN: Final = re.compile(r"\b(?:HmIPW?|HM|HB)-[A-Za-z0-9][A-Za-z0-9-]*\b", re.IGNORECASE)

# Interface designations that match the device-model pattern but are useless as search terms
_NON_DEVICE_TERMS: Final = frozenset({"hmip-rf", "hm-rf"})


def extract_device_model(text: str) -> str | None:
    """Return the first device model designation found in the text, or None."""
    for match in _DEVICE_MODEL_PATTERN.finditer(text or ""):
        candidate = match.group(0).rstrip("-")
        if candidate.casefold() not in _NON_DEVICE_TERMS:
            return candidate
    return None


def search_similar_issues(
    gh: Github,
    *,
    repo_full_name: str,
    search_terms: list[str],
    current_issue_number: int,
) -> list[dict[str, Any]]:
    """Search for similar issues via the GitHub search API using the given terms."""
    similar_items: list[dict[str, Any]] = []
    seen: set[int] = set()

    for raw_term in search_terms[:3]:
        # Strip search-syntax characters so terms cannot break the query
        term = re.sub(r"[:\"\[\]<>()]", " ", raw_term).strip()
        if len(term) < 3:
            continue

        query = f"repo:{repo_full_name} is:issue {term}"
        try:
            results = gh.search_issues(query)
            # Do not slice the PaginatedList: slicing probes by index and raises
            # IndexError when the search returns no hits; plain iteration is safe.
            for issue in islice(results, 3):
                if issue.number == current_issue_number or issue.number in seen:
                    continue
                seen.add(issue.number)
                similar_items.append(
                    {
                        "type": "issue",
                        "number": issue.number,
                        "title": issue.title,
                        "url": issue.html_url,
                        "state": issue.state,
                        "search_term": term,
                    }
                )
        except GithubException as e:
            print(f"Warning: similar-issue search failed for '{term}': {e}")
            continue

        if len(similar_items) >= 5:
            break

    return similar_items[:5]


# =============================================================================
# Claude triage summary (no diagnosis!)
# =============================================================================

CLAUDE_TRIAGE_PROMPT = """You are a triage assistant for GitHub issues of the aiohomematic / Homematic(IP) Local projects (a Python library and Home Assistant integration for Homematic home-automation devices).

Today's date is {today}. Keep this in mind: version numbers and timestamps matching the current year are normal, not anomalies.

The issue template language is {template_language}. Write ALL output text in that language.

Your ONLY tasks (pure triage):
1. "summary": summarize the issue in at most 2 sentences (what the reporter observes, which device/feature is affected).
2. "suggested_docs": pick 0-2 documentation keys from the list below that genuinely help THIS issue. Return an empty list when none clearly applies.
3. "search_terms": 1-3 short search terms for finding duplicate issues (device model, distinctive error message fragment, feature name).
4. "is_device_related": true if the issue is about a specific device's entities, values or behavior.
5. "is_feature_request": true if this is a feature request rather than a bug report.

STRICT RULES:
- Do NOT diagnose root causes, do NOT judge versions, do NOT analyze logs, do NOT recommend fixes. Triage only.
- The summary must describe, not explain: no "probably", no "caused by", no suspected reasons.

Available documentation keys:
{docs}

Issue title: {title}

Issue body:
{body}

Respond with ONLY a JSON object of this shape:
{{"summary": "...", "suggested_docs": [{{"doc_key": "...", "reason": "..."}}], "search_terms": ["..."], "is_device_related": true, "is_feature_request": false}}"""


def get_claude_triage(
    *,
    title: str,
    body: str,
    api_key: str,
    template_language: str,
) -> dict[str, Any] | None:
    """
    Get a triage summary from Claude (summary, doc links, search terms, routing flags).

    Returns None on any failure so the deterministic triage comment can still be posted.
    """
    docs_str = "\n".join(f"- {key}: {url}" for key, url in DOCS_LINKS.items())
    prompt = CLAUDE_TRIAGE_PROMPT.format(
        today=date.today().isoformat(),
        template_language="German" if template_language == "de" else "English",
        docs=docs_str,
        title=title,
        body=(body or "(empty)")[:8000],
    )

    try:
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model=os.getenv("ANALYZER_MODEL") or DEFAULT_ANALYZER_MODEL,
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = message.content[0].text
        # Extract JSON from potential markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        triage = cast(dict[str, Any], json.loads(response_text))
    except Exception as e:
        print(f"Warning: Claude triage failed (continuing with deterministic checks only): {e}")
        return None

    return triage


# =============================================================================
# Comment formatting
# =============================================================================


@dataclass
class TriageResult:
    """Aggregated triage results used to render the issue comment."""

    language: str = "en"
    summary: str | None = None
    version_check: VersionCheck = field(default_factory=lambda: VersionCheck(status="no_data"))
    has_diagnostics: bool = False
    has_logs: bool = False
    ai_detection: dict[str, Any] = field(default_factory=dict)
    is_feature_request: bool = False
    is_device_related: bool = False
    has_screenshots: bool = False
    suggested_docs: list[dict[str, str]] = field(default_factory=list)
    similar_items: list[dict[str, Any]] = field(default_factory=list)


def has_bot_comment(issue: Any) -> bool:
    """Check if the bot has already commented on this issue."""
    for comment in issue.get_comments():
        if comment.user.type == "Bot" and "Automatische Issue-Analyse" in comment.body:
            return True
        if comment.user.type == "Bot" and "Automatic Issue Analysis" in comment.body:
            return True
    return False


def _format_version_notice(version_check: VersionCheck, *, is_german: bool) -> str:
    """
    Format a neutral, deterministic version notice.

    Only emitted for statuses that are established by comparing against the actually
    published releases ("outdated", "unknown"). Never renders a "critical" banner.
    """
    if version_check.status not in ("outdated", "unknown") or not version_check.stable:
        return ""

    releases_url = DOCS_LINKS["releases"]

    if version_check.status == "outdated":
        if is_german:
            return (
                "### ℹ️ Versionshinweis\n\n"
                f"Die gemeldete Version **{version_check.reported}** ist nicht die aktuelle stabile Version "
                f"(**{version_check.stable}**). Bitte aktualisiere zuerst auf die "
                f"[aktuelle Version]({releases_url}) und prüfe, ob das Problem weiterhin besteht.\n\n"
            )
        return (
            "### ℹ️ Version notice\n\n"
            f"The reported version **{version_check.reported}** is not the current stable version "
            f"(**{version_check.stable}**). Please update to the [latest version]({releases_url}) "
            "first and check whether the problem persists.\n\n"
        )

    if is_german:
        return (
            "### ℹ️ Versionshinweis\n\n"
            f'Die Angabe "{version_check.reported}" im Versionsfeld entspricht keiner veröffentlichten Version '
            f"von Homematic(IP) Local (aktuelle stabile Version: **{version_check.stable}**). "
            "Möglicherweise wurde versehentlich die Version von Home Assistant oder des CCU-Backends "
            "eingetragen - bitte das Feld korrigieren.\n\n"
        )
    return (
        "### ℹ️ Version notice\n\n"
        f'The value "{version_check.reported}" in the version field does not match any published version '
        f"of Homematic(IP) Local (current stable version: **{version_check.stable}**). "
        "You may have entered the Home Assistant or CCU backend version by mistake — please correct the field.\n\n"
    )


def _format_missing_required_info(
    *,
    has_diagnostics: bool,
    has_logs: bool,
    version_missing: bool,
    is_german: bool,
) -> str:
    """Format missing required information section."""
    if has_diagnostics and has_logs and not version_missing:
        return ""

    if is_german:
        result = "### ⚠️ Fehlende Pflichtinformationen\n\n"
        result += (
            "**Sinnvoller Support ist nur möglich, wenn alle erforderlichen Informationen bereitgestellt werden!**\n\n"
            "Es fehlen:\n\n"
        )
        if not has_diagnostics:
            result += "- ❌ **Integrationsdiagnose (.json-Datei)** - Herunterladen via: Einstellungen → Geräte → Integration auswählen → Diagnose herunterladen\n"
        if not has_logs:
            result += "- ❌ **Protokolldatei** - Als **Datei angehängt**, am besten ein DEBUG-Log; ein eingefügter Auszug reicht nicht. Aktivieren via: Einstellungen → Geräte → Integration auswählen → Debug-Protokollierung aktivieren. Danach Problem reproduzieren und Log herunterladen (Einstellungen → System → Protokolle → Unveränderte Protokolle laden)\n"
        if version_missing:
            result += "- ❌ **Version der Integration** - Das Versionsfeld ist leer. Bitte die Version von Homematic(IP) Local angeben (zu finden in: HACS → Integrationen)\n"
        result += (
            "\n⚠️ **Issues ohne diese Informationen können nicht bearbeitet werden und werden ggf. geschlossen.**\n\n"
        )
        result += "_Ausnahme: Bei Problemen mit der Erstinstallation sind Diagnosedaten möglicherweise noch nicht verfügbar._\n\n"
    else:
        result = "### ⚠️ Missing Required Information\n\n"
        result += "**Meaningful support is only possible if all required information is provided!**\n\nMissing:\n\n"
        if not has_diagnostics:
            result += "- ❌ **Integration diagnostics (.json file)** - Download via: Settings → Devices → Select integration → Download diagnostics\n"
        if not has_logs:
            result += "- ❌ **Log file** - **Attached as a file**, preferably a DEBUG log; a pasted excerpt is not enough. Enable via: Settings → Devices → Select integration → Enable debug logging. Then reproduce the issue and download log (Settings → System → Logs → Load unchanged logs)\n"
        if version_missing:
            result += "- ❌ **Integration version** - The version field is empty. Please provide the Homematic(IP) Local version (found in: HACS → Integrations)\n"
        result += "\n⚠️ **Issues without this information cannot be processed and may be closed.**\n\n"
        result += "_Exception: For initial setup issues, diagnostics may not be available yet._\n\n"

    return result


def _format_ai_analysis_hint(
    ai_detection: dict[str, Any],
    is_german: bool,
    *,
    raw_data_complete: bool = False,
) -> str:
    """
    Format a redirect section when the report was written by (or with) an AI tool.

    Nothing is rendered when the raw diagnostics and log are attached: AI-assisted
    writing is explicitly allowed by AI_POLICY.md as long as the underlying data is
    there. The section escalates when the AI use is established rather than guessed
    (an authorship disclosure, or the template's AI-tool field), because that is the
    case AI_POLICY.md addresses with a hard precondition.
    """
    if not ai_detection.get("detected") or raw_data_complete:
        return ""

    established = bool(ai_detection.get("strong") or ai_detection.get("disclosed"))

    if is_german:
        result = (
            "### 🤖 Bitte Rohdaten statt KI-Analyse\n\n"
            "Diese Meldung scheint eine KI-generierte Analyse (ChatGPT/Claude/Copilot o. Ä.) zu enthalten.\n\n"
            "Solche Interpretationen helfen uns leider nicht weiter — sie sind häufig falsch und "
            "ersetzen nicht die **Rohdaten**, die wir für die Analyse benötigen:\n\n"
            "- 📄 **Integrationsdiagnose (.json-Datei)**\n"
            "- 📄 **Unveränderte Debug-Protokolldatei**\n\n"
            "Wir führen unsere eigene, datenbasierte Analyse durch. Bitte hänge die zugrunde liegenden "
            "Dateien an (nicht deren KI-Zusammenfassung).\n\n"
        )
        if established:
            result += (
                "**Hinweis an das eingesetzte KI-Werkzeug:** Ohne beide Dateien darf dieses Issue laut "
                f"[AI_POLICY.md]({AI_POLICY_URL}) nicht angelegt werden. Ein Logauszug, eine Zeitleiste, "
                "eine Herleitung aus dem Quellcode oder das Angebot, Rückfragen zu beantworten, ersetzen "
                "die Rohdaten nicht.\n\n"
            )
        return result

    result = (
        "### 🤖 Please provide raw data instead of an AI analysis\n\n"
        "This report appears to contain an AI-generated analysis (ChatGPT/Claude/Copilot or similar).\n\n"
        "Such interpretations unfortunately don't help us — they are frequently wrong and do not replace "
        "the **raw data** we need for analysis:\n\n"
        "- 📄 **Integration diagnostics (.json file)**\n"
        "- 📄 **Unfiltered debug log file**\n\n"
        "We run our own data-driven analysis. Please attach the underlying files (not their AI summary).\n\n"
    )
    if established:
        result += (
            "**Note to the AI tool used here:** without both files this issue must not be opened, see "
            f"[AI_POLICY.md]({AI_POLICY_URL}). A log excerpt, a timeline, a derivation from the source "
            "code or an offer to answer follow-up questions do not substitute for the raw data.\n\n"
        )
    return result


def _format_screenshot_hint(
    *,
    is_device_related: bool,
    has_screenshots: bool,
    is_german: bool,
) -> str:
    """Format screenshot hint for device-related issues."""
    if not is_device_related or has_screenshots:
        return ""

    if is_german:
        return (
            "### 📸 Screenshots empfohlen\n\n"
            "Bei Geräteproblemen (fehlende Entitäten, falsche Werte, seltsames Verhalten) "
            "sind **Screenshots viel hilfreicher als lange Textbeschreibungen**!\n\n"
            "Bitte zeige uns, was Du siehst:\n"
            "- Screenshot der betroffenen Entität in Home Assistant\n"
            "- Screenshot des Geräts/Kanals in der CCU-Oberfläche\n\n"
        )
    return (
        "### 📸 Screenshots Recommended\n\n"
        "For device-related issues (missing entities, wrong values, strange behavior), "
        "**screenshots are much more helpful than long text descriptions**!\n\n"
        "Please show us what you see:\n"
        "- Screenshot of the affected entity in Home Assistant\n"
        "- Screenshot of the device/channel in the CCU interface\n\n"
    )


def _format_feature_request_hint(*, is_feature_request: bool, is_german: bool) -> str:
    """Format a routing hint pointing feature requests to the discussions."""
    if not is_feature_request:
        return ""

    discussions_url = DOCS_LINKS["discussions"]
    if is_german:
        return (
            "### 💡 Feature-Wunsch?\n\n"
            "Diese Meldung sieht nach einem Feature-Wunsch aus. Neue Funktionen werden in den "
            f"[Diskussionen]({discussions_url}) besprochen — dieses Issue-Formular ist für Fehlermeldungen gedacht.\n\n"
        )
    return (
        "### 💡 Feature request?\n\n"
        "This report looks like a feature request. New features are discussed in the "
        f"[discussions]({discussions_url}) — this issue form is meant for bug reports.\n\n"
    )


def format_comment(triage: TriageResult) -> str:
    """Format the triage comment to post on the issue."""
    is_german = triage.language == "de"

    # Header (kept identical to the previous bot so duplicate detection keeps working)
    if is_german:
        comment = "## Automatische Issue-Analyse\n\n"
        if triage.summary:
            comment += f"**Zusammenfassung:** {triage.summary}\n\n"
    else:
        comment = "## Automatic Issue Analysis\n\n"
        if triage.summary:
            comment += f"**Summary:** {triage.summary}\n\n"

    # Deterministic version notice (neutral, never "critical")
    comment += _format_version_notice(triage.version_check, is_german=is_german)

    # Missing required raw data (diagnostics / log / version field)
    comment += _format_missing_required_info(
        has_diagnostics=triage.has_diagnostics,
        has_logs=triage.has_logs,
        version_missing=triage.version_check.status == "missing",
        is_german=is_german,
    )

    # Redirect hint when the report contains a pasted AI-generated analysis
    comment += _format_ai_analysis_hint(
        triage.ai_detection,
        is_german,
        raw_data_complete=triage.has_diagnostics and triage.has_logs,
    )

    # Routing hint for feature requests
    comment += _format_feature_request_hint(is_feature_request=triage.is_feature_request, is_german=is_german)

    # Screenshot hint for device-related issues
    comment += _format_screenshot_hint(
        is_device_related=triage.is_device_related,
        has_screenshots=triage.has_screenshots,
        is_german=is_german,
    )

    # Suggested documentation (at most 2 links)
    suggested_docs = [doc for doc in triage.suggested_docs if doc.get("doc_key") in DOCS_LINKS][:2]
    if suggested_docs:
        if is_german:
            comment += "### Hilfreiche Dokumentation\n\n"
            comment += "Die folgenden Dokumentationsseiten könnten hilfreich sein:\n\n"
        else:
            comment += "### Helpful Documentation\n\n"
            comment += "The following documentation pages might be helpful:\n\n"

        for doc in suggested_docs:
            doc_key = doc["doc_key"]
            url = DOCS_LINKS[doc_key]
            reason = doc.get("reason", "")
            comment += f"- [{doc_key}]({url})\n"
            if reason:
                comment += f"  _{reason}_\n"
        comment += "\n"

    # Similar issues (real search-API results)
    if triage.similar_items:
        if is_german:
            comment += "### Ähnliche Issues und Diskussionen\n\n"
            comment += "Die folgenden Issues oder Diskussionen könnten relevant sein:\n\n"
        else:
            comment += "### Similar Issues and Discussions\n\n"
            comment += "The following issues or discussions might be relevant:\n\n"

        for item in triage.similar_items:
            state_emoji = "✅" if item["state"] == "closed" else "🔄"
            comment += f"- {state_emoji} #{item['number']}: [{item['title']}]({item['url']})\n"
        comment += "\n"

    # Footer
    if is_german:
        comment += "---\n"
        comment += "_Diese Analyse wurde automatisch erstellt. "
        comment += "Bei Fragen oder Problemen, bitte die [Diskussionen]({}) nutzen._\n".format(
            DOCS_LINKS["discussions"]
        )
    else:
        comment += "---\n"
        comment += "_This analysis was generated automatically. "
        comment += "For questions or support, please use the [discussions]({})._\n".format(DOCS_LINKS["discussions"])

    return comment


# =============================================================================
# Label maintenance
# =============================================================================

# Triage label applied when an issue lacks the raw data required for analysis.
NEEDS_RAW_DATA_LABEL: Final = "needs-raw-data"
NEEDS_RAW_DATA_LABEL_COLOR: Final = "d93f0b"
NEEDS_RAW_DATA_LABEL_DESCRIPTION: Final = "Issue lacks the raw diagnostics/log data required for analysis"


def ensure_label(repo: Repository.Repository, name: str, *, color: str, description: str) -> bool:
    """
    Ensure a label exists in the repository, creating it on demand.

    Returns True if the label exists (or was created), False if it could not be created.
    """
    try:
        repo.get_label(name)
    except GithubException:
        pass
    else:
        return True

    try:
        repo.create_label(name=name, color=color, description=description)
    except GithubException as e:
        print(f"Warning: could not create label '{name}': {e}")
        return False
    else:
        print(f"Created label '{name}'")
        return True


def apply_needs_raw_data_label(issue: Any, repo: Repository.Repository) -> None:
    """Add the needs-raw-data triage label to the issue (idempotent)."""
    if not ensure_label(
        repo,
        NEEDS_RAW_DATA_LABEL,
        color=NEEDS_RAW_DATA_LABEL_COLOR,
        description=NEEDS_RAW_DATA_LABEL_DESCRIPTION,
    ):
        return

    try:
        if NEEDS_RAW_DATA_LABEL in {label.name for label in issue.labels}:
            print(f"Label '{NEEDS_RAW_DATA_LABEL}' already present")
            return
        issue.add_to_labels(NEEDS_RAW_DATA_LABEL)
        print(f"Added label '{NEEDS_RAW_DATA_LABEL}'")
    except GithubException as e:
        print(f"Warning: could not add label '{NEEDS_RAW_DATA_LABEL}': {e}")


def remove_needs_raw_data_label(issue: Any) -> None:
    """Remove the needs-raw-data triage label if present (e.g. data added in a later edit)."""
    try:
        if NEEDS_RAW_DATA_LABEL not in {label.name for label in issue.labels}:
            return
        issue.remove_from_labels(NEEDS_RAW_DATA_LABEL)
        print(f"Removed label '{NEEDS_RAW_DATA_LABEL}'")
    except GithubException as e:
        print(f"Warning: could not remove label '{NEEDS_RAW_DATA_LABEL}': {e}")


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """Triage the issue and post a comment."""
    # Get environment variables
    github_token = os.getenv("GITHUB_TOKEN") or ""
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") or ""
    issue_number = int(os.getenv("ISSUE_NUMBER", "0"))
    repo_name = os.getenv("REPO_NAME", "")

    if not all([github_token, anthropic_api_key, issue_number, repo_name]):
        print("Error: Missing required environment variables")
        sys.exit(1)

    # Initialize GitHub client
    gh = Github(auth=Auth.Token(github_token))
    repo = gh.get_repo(repo_name)
    issue = repo.get_issue(issue_number)

    # Get issue details (either from env or from GitHub API)
    issue_title = os.getenv("ISSUE_TITLE") or issue.title
    issue_body = os.getenv("ISSUE_BODY") or issue.body or ""

    print(f"Triaging issue #{issue_number}: {issue_title}")

    # Deterministic checks
    fields = parse_form_fields(issue_body)
    template_language = detect_template_language(issue_body)
    print(f"Detected template language: {template_language}")

    has_diagnostics, has_logs = detect_attachments(issue_body)
    has_screenshots = detect_screenshots(issue_body)
    ai_tool_field = get_form_field(fields, markers=AI_TOOL_FIELD_MARKERS)
    ai_detection = detect_ai_generated_analysis(issue_body, ai_tool_field=ai_tool_field)
    if ai_detection["detected"]:
        print(
            f"Detected likely AI-generated analysis (strong={ai_detection['strong']}, markers={ai_detection['markers']})"
        )

    releases = fetch_release_info(gh)
    print(
        f"Known releases - stable: {releases.stable}, prerelease: {releases.prerelease}, total: {len(releases.all_versions)}"
    )

    reported_version = get_form_field(fields, markers=VERSION_FIELD_MARKERS)
    version_check = check_reported_version(reported_version, releases=releases)
    print(f"Version check: status={version_check.status}, reported={version_check.reported!r}")

    # Optional Claude triage (summary, doc links, search terms) — never blocks the comment
    triage_llm = get_claude_triage(
        title=issue_title,
        body=issue_body,
        api_key=anthropic_api_key,
        template_language=template_language,
    )

    # Build search terms: device model (deterministic) first, then LLM-provided terms
    search_terms: list[str] = []
    if (device_model := extract_device_model(f"{issue_title}\n{issue_body}")) is not None:
        search_terms.append(device_model)
    if triage_llm:
        for term in triage_llm.get("search_terms", []):
            if isinstance(term, str) and term.casefold() not in {t.casefold() for t in search_terms}:
                search_terms.append(term)

    similar_items: list[dict[str, Any]] = []
    if search_terms:
        similar_items = search_similar_issues(
            gh,
            repo_full_name=repo_name,
            search_terms=search_terms,
            current_issue_number=issue_number,
        )
        print(f"Found {len(similar_items)} similar items")

    # Maintain the needs-raw-data triage label: add it when the raw diagnostics/log data
    # is missing, and remove it once the required data has been provided (e.g. on a later
    # edit). Detected AI content alone does not earn the label - AI_POLICY.md allows an
    # AI-assisted report as long as the raw data is attached.
    missing_required_info = not has_diagnostics or not has_logs
    if missing_required_info:
        apply_needs_raw_data_label(issue, repo)
    else:
        remove_needs_raw_data_label(issue)

    # Check if bot has already commented (to avoid duplicates on edit)
    is_manual_trigger = not os.getenv("ISSUE_TITLE")  # Manual trigger doesn't have ISSUE_TITLE in env
    if has_bot_comment(issue) and not is_manual_trigger:
        print("Bot has already commented on this issue, skipping to avoid duplicates")
        return

    triage = TriageResult(
        language=template_language,
        summary=triage_llm.get("summary") if triage_llm else None,
        version_check=version_check,
        has_diagnostics=has_diagnostics,
        has_logs=has_logs,
        ai_detection=ai_detection,
        is_feature_request=bool(triage_llm and triage_llm.get("is_feature_request")),
        is_device_related=bool(triage_llm and triage_llm.get("is_device_related")),
        has_screenshots=has_screenshots,
        suggested_docs=[
            doc for doc in (triage_llm.get("suggested_docs", []) if triage_llm else []) if isinstance(doc, dict)
        ],
        similar_items=similar_items,
    )

    comment_body = format_comment(triage)

    # Only post if there's something useful to say
    has_useful_feedback = (
        version_check.status in ("outdated", "unknown", "missing")
        or missing_required_info
        or triage.is_feature_request
        or (triage.is_device_related and not has_screenshots)
        or bool(triage.suggested_docs)
        or bool(similar_items)
    )

    if has_useful_feedback:
        try:
            issue.create_comment(comment_body)
            print("Comment posted successfully")
        except GithubException as e:
            print(f"Error posting comment: {e}")
            sys.exit(1)
    else:
        print("No actionable feedback to provide, skipping comment")


if __name__ == "__main__":
    main()
