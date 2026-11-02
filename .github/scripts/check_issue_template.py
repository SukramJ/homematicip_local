#!/usr/bin/env python3
"""
Verify that a new issue actually went through the issue form.

The bug-report forms mark every item of the "I agree to the following" checklist as
``required: true``. GitHub enforces that only in the browser: an issue created through
the REST/GraphQL API (``gh issue create``, an MCP server, an agent) can carry an
arbitrary body, with the checklist shortened, reworded or left unchecked, and the
mandatory diagnostics dropped along the way.

This check is deterministic and template-driven: the required checkbox labels and the
field headings are read from ``.github/ISSUE_TEMPLATE/*.yml`` at run time, so the check
cannot drift away from the templates.

Violations detected:

- ``bypassed``  - the body carries none of the template's structure at all.
- ``rewritten`` - required checklist labels are missing or reworded.
- ``unchecked`` - required checklist labels are present but not ticked.
- ``no-raw-data`` - neither a diagnostics nor a log file is attached (uploaded file).

Behavior on violation: label the issue ``invalid-template``, post one explanatory
comment, and close it as not planned. The workflow sets AUTO_CLOSE=true unless the
repository variable AUTO_CLOSE_INVALID_TEMPLATE is "false"; then the issue stays open.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
import os
from pathlib import Path
import re
import sys
from typing import Any, Final, cast

from github import Auth, Github, GithubException, Repository
from issue_form import detect_template_language, has_uploaded_file, normalize_label
import yaml

# Directory holding the issue forms
TEMPLATE_DIR: Final = Path(".github/ISSUE_TEMPLATE")

# Template file per detected language
TEMPLATE_FILES: Final[dict[str, str]] = {"en": "bug_report.yml", "de": "bug_report_de.yml"}

# Label applied when the issue form was not honored
INVALID_TEMPLATE_LABEL: Final = "invalid-template"
INVALID_TEMPLATE_LABEL_COLOR: Final = "b60205"
INVALID_TEMPLATE_LABEL_DESCRIPTION: Final = "Issue was not filed through the issue form, or the form was modified"

# Opt-out label a maintainer can add to silence the check on a specific issue
SKIP_LABEL: Final = "skip-template-check"

# Author associations exempt from the check (maintainers legitimately use the API)
EXEMPT_ASSOCIATIONS: Final[frozenset[str]] = frozenset({"OWNER", "MEMBER", "COLLABORATOR"})

# Marker in the bot comment used to avoid duplicate comments on later edits
COMMENT_MARKER: Final = "<!-- issue-template-check -->"

# Share of required checkbox labels that must be present verbatim before the body counts
# as template-shaped at all. Below this, the body is treated as freely composed.
MIN_STRUCTURE_RATIO: Final = 0.5

# Number of missing required labels still attributable to template drift rather than to a
# rewritten checklist. Measured against the 25 most recent externally filed issues
# (2026-09): every legitimately filed one misses at most one label - the "supported hubs"
# item, added to the templates after those issues were opened - while a report composed
# outside the form misses seven.
MAX_DRIFT_MISSING: Final = 1

# Link targets used in the comment
AI_POLICY_URL: Final = "https://github.com/SukramJ/aiohomematic/blob/main/AI_POLICY.md#stop--hard-precondition-for-bug-reports"
NEW_ISSUE_URL: Final = "https://github.com/SukramJ/aiohomematic/issues/new/choose"
DISCUSSIONS_URL: Final = "https://github.com/SukramJ/aiohomematic/discussions"
DEBUG_DATA_URL: Final = "https://sukramj.github.io/aiohomematic/contributor/testing/debug_data_importance/"


# =============================================================================
# Template loading
# =============================================================================


def load_required_checkbox_labels(template_path: Path) -> list[str]:
    """
    Return the labels of all ``required: true`` checkbox options of an issue form.

    Labels are returned normalized (see :func:`issue_form.normalize_label`) so they can
    be compared against the rendered issue body.
    """
    data = cast(dict[str, Any], yaml.safe_load(template_path.read_text(encoding="utf-8")))
    labels: list[str] = []
    for block in data.get("body", []):
        if not isinstance(block, dict) or block.get("type") != "checkboxes":
            continue
        labels.extend(
            normalize_label(str(option.get("label", "")))
            for option in block.get("attributes", {}).get("options", [])
            if isinstance(option, dict) and option.get("required") is True
        )
    return [label for label in labels if label]


# =============================================================================
# Body inspection
# =============================================================================

# A rendered checklist line, e.g. "- [x] I have read the documentation"
_CHECKBOX_LINE_PATTERN: Final = re.compile(r"^\s*[-*]\s*\[( |x|X)\]\s*(.+?)\s*$")


def parse_checkbox_lines(issue_body: str) -> dict[str, bool]:
    """Return a mapping of normalized checklist label to its ticked state."""
    states: dict[str, bool] = {}
    for line in (issue_body or "").splitlines():
        if (match := _CHECKBOX_LINE_PATTERN.match(line)) is not None:
            states[normalize_label(match.group(2))] = match.group(1).lower() == "x"
    return states


@dataclass(frozen=True)
class TemplateCheck:
    """Deterministic result of comparing an issue body against its issue form."""

    language: str
    violations: tuple[str, ...] = ()
    missing_labels: tuple[str, ...] = ()
    unchecked_labels: tuple[str, ...] = ()
    required_total: int = 0
    raw_data_missing: bool = False

    @property
    def ok(self) -> bool:
        """
        Return True when the issue honored the form.

        A missing raw-data attachment alone is deliberately not a violation here: that
        case belongs to the issue analyzer, which labels it "needs-raw-data" and explains
        it. Reporting it twice would only add noise. It is listed in this check's comment
        when the form was violated as well.
        """
        return not self.violations


def check_issue_body(issue_body: str, *, required_labels: Sequence[str], language: str) -> TemplateCheck:
    """
    Compare an issue body against the required checklist of its issue form.

    A body that matches fewer than MIN_STRUCTURE_RATIO of the required labels is treated
    as freely composed ("bypassed") rather than as an edited form, because listing every
    single missing label would not help the reporter in that case.
    """
    states = parse_checkbox_lines(issue_body)
    present = [label for label in required_labels if label in states]
    missing = [label for label in required_labels if label not in states]
    unchecked = [label for label in present if not states[label]]

    violations: list[str] = []
    if required_labels and len(present) < MIN_STRUCTURE_RATIO * len(required_labels):
        violations.append("bypassed")
    elif len(missing) > MAX_DRIFT_MISSING:
        violations.append("rewritten")
    if unchecked:
        violations.append("unchecked")

    raw_data_missing = not has_uploaded_file(issue_body)
    if violations and raw_data_missing:
        violations.append("no-raw-data")

    return TemplateCheck(
        language=language,
        violations=tuple(violations),
        missing_labels=tuple(missing),
        unchecked_labels=tuple(unchecked),
        required_total=len(required_labels),
        raw_data_missing=raw_data_missing,
    )


# =============================================================================
# Comment formatting
# =============================================================================

_VIOLATION_TEXT_EN: Final[dict[str, str]] = {
    "bypassed": (
        "The issue body does not match the issue form. It looks like it was composed directly "
        "(REST/GraphQL API, `gh issue create`, an MCP server or an agent) instead of being "
        "submitted through the form, which skips the form's required-field validation."
    ),
    "rewritten": "Items of the mandatory checklist are missing or were reworded.",
    "unchecked": "Items of the mandatory checklist are not ticked.",
    "no-raw-data": (
        "No uploaded file is attached. A bug report needs the integration diagnostics (`.json`) "
        "**and** the unfiltered debug log, attached as files — a pasted excerpt is not enough."
    ),
}

_VIOLATION_TEXT_DE: Final[dict[str, str]] = {
    "bypassed": (
        "Der Issue-Text entspricht nicht dem Formular. Er wurde offenbar direkt verfasst "
        "(REST/GraphQL-API, `gh issue create`, ein MCP-Server oder ein Agent), statt über das "
        "Formular abgeschickt zu werden — dabei wird die Pflichtfeld-Prüfung des Formulars übergangen."
    ),
    "rewritten": "Punkte der Pflicht-Checkliste fehlen oder wurden umformuliert.",
    "unchecked": "Punkte der Pflicht-Checkliste sind nicht angehakt.",
    "no-raw-data": (
        "Es ist keine hochgeladene Datei angehängt. Ein Fehlerbericht braucht die Integrationsdiagnose "
        "(`.json`) **und** das unveränderte Debug-Log als Dateianhang — ein eingefügter Auszug reicht nicht."
    ),
}


def format_comment(check: TemplateCheck, *, auto_closed: bool) -> str:
    """Format the explanatory comment posted on a template violation."""
    is_german = check.language == "de"
    texts = _VIOLATION_TEXT_DE if is_german else _VIOLATION_TEXT_EN

    if auto_closed and is_german:
        comment = f"{COMMENT_MARKER}\n## 🔒 Geschlossen: Issue-Formular nicht verwendet\n\n"
        comment += (
            "Dieses Issue wurde automatisch geschlossen, weil es nicht über das Issue-Formular "
            "angelegt wurde. Das Formular stellt sicher, dass jeder Bericht die Angaben enthält, "
            "ohne die sich ein Fehler nicht nachvollziehen lässt: Versionen, die Diagnose-`.json` "
            "und das unveränderte Debug-Log.\n\nFestgestellt:\n\n"
        )
    elif auto_closed:
        comment = f"{COMMENT_MARKER}\n## 🔒 Closed: issue form not used\n\n"
        comment += (
            "This issue was closed automatically because it was not filed through the issue form. "
            "The form makes sure every report carries the information a bug cannot be traced "
            "without: versions, the diagnostics `.json` and the unfiltered debug log.\n\nFound:\n\n"
        )
    elif is_german:
        comment = f"{COMMENT_MARKER}\n## ⚠️ Issue-Formular nicht verwendet\n\n"
        comment += "Dieses Issue kann so nicht bearbeitet werden:\n\n"
    else:
        comment = f"{COMMENT_MARKER}\n## ⚠️ Issue form not used\n\n"
        comment += "This issue cannot be processed as filed:\n\n"

    for violation in check.violations:
        comment += f"- ❌ {texts[violation]}\n"
    comment += "\n"

    if check.unchecked_labels:
        header = "Nicht angehakt:" if is_german else "Not ticked:"
        comment += f"{header}\n\n"
        for label in check.unchecked_labels:
            comment += f"- `{label}`\n"
        comment += "\n"

    if auto_closed and is_german:
        comment += (
            f"**So geht es weiter:** Bitte ein **neues** Issue über das [Formular]({NEW_ISSUE_URL}) im "
            f"Browser anlegen, mit Diagnose-`.json` und unverändertem Debug-Log als Dateianhang "
            f"([warum diese Daten nötig sind]({DEBUG_DATA_URL})). Dieses Issue zu bearbeiten öffnet "
            f"es nicht wieder.\n\n"
        )
    elif auto_closed:
        comment += (
            f"**Next step:** please open a **new** issue through the [issue form]({NEW_ISSUE_URL}) in "
            f"the browser, with the diagnostics `.json` and the unfiltered debug log attached as files "
            f"([why we need that data]({DEBUG_DATA_URL})). Editing this issue does not reopen it.\n\n"
        )
    elif is_german:
        comment += (
            f"**So geht es weiter:** Bitte das [Formular]({NEW_ISSUE_URL}) im Browser ausfüllen und "
            f"absenden — mit Diagnose-`.json` und unverändertem Debug-Log als Dateianhang "
            f"([warum diese Daten nötig sind]({DEBUG_DATA_URL})).\n\n"
        )
    else:
        comment += (
            f"**Next step:** please fill in the [issue form]({NEW_ISSUE_URL}) in the browser and submit "
            f"it there — with the diagnostics `.json` and the unfiltered debug log attached as files "
            f"([why we need that data]({DEBUG_DATA_URL})).\n\n"
        )

    if is_german:
        comment += (
            f"**Falls dieser Bericht von einem KI-Werkzeug erstellt wurde:** In "
            f"[AI_POLICY.md]({AI_POLICY_URL}) steht die verbindliche Vorbedingung — ohne beide Dateien "
            f"darf das Issue nicht angelegt werden, und das Formular darf nicht umgangen oder "
            f"umformuliert werden.\n\n"
        )
    else:
        comment += (
            f"**If this report was produced by an AI tool:** "
            f"[AI_POLICY.md]({AI_POLICY_URL}) states the binding precondition — without both files the "
            f"issue must not be opened, and the form must not be bypassed or reworded.\n\n"
        )

    if auto_closed:
        comment += (
            f"_Fragen und Ideen gehören in die [Diskussionen]({DISCUSSIONS_URL})._\n"
            if is_german
            else f"_Questions and ideas belong in the [Discussions]({DISCUSSIONS_URL})._\n"
        )
    else:
        comment += (
            "_Bitte das Issue entsprechend ergänzen; es bleibt bis dahin offen._\n"
            if is_german
            else "_Please amend the issue accordingly; it stays open until then._\n"
        )

    return comment


# =============================================================================
# GitHub side effects
# =============================================================================


def ensure_label(repo: Repository.Repository, name: str, *, color: str, description: str) -> bool:
    """Ensure a label exists in the repository, creating it on demand."""
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


def label_names(issue: Any) -> set[str]:
    """Return the label names currently attached to an issue."""
    return {label.name for label in issue.labels}


def has_check_comment(issue: Any) -> bool:
    """Return True if this check already commented on the issue."""
    return any(COMMENT_MARKER in (comment.body or "") for comment in issue.get_comments())


# =============================================================================
# Main
# =============================================================================


@dataclass
class Settings:
    """Runtime configuration read from the environment."""

    github_token: str = ""
    repo_name: str = ""
    issue_number: int = 0
    author_association: str = ""
    auto_close: bool = False
    extra_exempt: frozenset[str] = field(default_factory=frozenset)


def read_settings() -> Settings:
    """Read the runtime configuration from the workflow environment."""
    return Settings(
        github_token=os.getenv("GITHUB_TOKEN") or "",
        repo_name=os.getenv("REPO_NAME") or "",
        issue_number=int(os.getenv("ISSUE_NUMBER") or "0"),
        author_association=(os.getenv("AUTHOR_ASSOCIATION") or "").upper(),
        auto_close=(os.getenv("AUTO_CLOSE") or "").strip().casefold() == "true",
    )


def resolve_required_labels(language: str) -> list[str]:
    """Return the required checkbox labels of the template for the detected language."""
    template_path = TEMPLATE_DIR / TEMPLATE_FILES[language]
    if not template_path.is_file():
        print(f"Warning: template {template_path} not found")
        return []
    return load_required_checkbox_labels(template_path)


def apply_labels(issue: Any, repo: Repository.Repository, *, add: bool) -> None:
    """Add or remove the invalid-template label, idempotently."""
    current = label_names(issue)
    if add:
        if INVALID_TEMPLATE_LABEL in current:
            return
        if not ensure_label(
            repo,
            INVALID_TEMPLATE_LABEL,
            color=INVALID_TEMPLATE_LABEL_COLOR,
            description=INVALID_TEMPLATE_LABEL_DESCRIPTION,
        ):
            return
        issue.add_to_labels(INVALID_TEMPLATE_LABEL)
        print(f"Added label '{INVALID_TEMPLATE_LABEL}'")
    elif INVALID_TEMPLATE_LABEL in current:
        issue.remove_from_labels(INVALID_TEMPLATE_LABEL)
        print(f"Removed label '{INVALID_TEMPLATE_LABEL}'")


def is_exempt(*, author_association: str, labels: Iterable[str]) -> bool:
    """Return True when the check must not run for this issue."""
    return author_association in EXEMPT_ASSOCIATIONS or SKIP_LABEL in set(labels)


def main() -> None:
    """Check the issue against its form and act on the result."""
    settings = read_settings()
    if not all([settings.github_token, settings.repo_name, settings.issue_number]):
        print("Error: Missing required environment variables")
        sys.exit(1)

    gh = Github(auth=Auth.Token(settings.github_token))
    repo = gh.get_repo(settings.repo_name)
    issue = repo.get_issue(settings.issue_number)
    issue_body = os.getenv("ISSUE_BODY") or issue.body or ""

    if is_exempt(author_association=settings.author_association, labels=label_names(issue)):
        print(f"Skipping #{settings.issue_number}: exempt (association={settings.author_association!r})")
        return

    language = detect_template_language(issue_body)
    required_labels = resolve_required_labels(language)
    if not required_labels:
        print("No required checkbox labels found in the template - nothing to check")
        return

    check = check_issue_body(issue_body, required_labels=required_labels, language=language)
    print(f"Template check for #{settings.issue_number}: language={language}, violations={check.violations}")

    if check.ok:
        apply_labels(issue, repo, add=False)
        return

    apply_labels(issue, repo, add=True)

    if has_check_comment(issue):
        print("Check already commented on this issue, skipping to avoid duplicates")
        return

    auto_closed = settings.auto_close and issue.state == "open"
    try:
        issue.create_comment(format_comment(check, auto_closed=auto_closed))
        print("Comment posted successfully")
    except GithubException as e:
        print(f"Error posting comment: {e}")
        sys.exit(1)

    if auto_closed:
        try:
            issue.edit(state="closed", state_reason="not_planned")
            print("Issue closed (AUTO_CLOSE=true)")
        except GithubException as e:
            print(f"Error closing issue: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
