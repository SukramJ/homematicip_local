"""Tests for the issue-form validation used by the Validate Issue Template workflow."""

from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
import sys
import types

import pytest

_SCRIPTS_DIR = Path(__file__).resolve().parents[2] / ".github" / "scripts"
_SCRIPT_PATH = _SCRIPTS_DIR / "check_issue_template.py"
_TEMPLATE_DIR = Path(__file__).resolve().parents[2] / ".github" / "ISSUE_TEMPLATE"


def _ensure_module(name: str, **attrs: object) -> None:
    """Make ``name`` importable, preferring the real package and stubbing only if absent."""
    if name in sys.modules:
        return
    try:
        importlib.import_module(name)
    except ModuleNotFoundError:
        stub = types.ModuleType(name)
        for attr, value in attrs.items():
            setattr(stub, attr, value)
        sys.modules[name] = stub


def _load_checker() -> types.ModuleType:
    """Load the standalone checker script with PyGithub stubbed out if unavailable."""
    _ensure_module(
        "github",
        Auth=object,
        Github=object,
        GithubException=type("GithubException", (Exception,), {}),
        Repository=object,
    )
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))

    spec = importlib.util.spec_from_file_location("check_issue_template_under_test", _SCRIPT_PATH)
    if spec is None or spec.loader is None:
        pytest.fail(f"Could not load checker script from {_SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


# ---------------------------------------------------------------------------
# Template loading
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("template", "expected"), [("bug_report.yml", "documentation"), ("bug_report_de.yml", "dokumentation")]
)
def test_load_required_checkbox_labels(template: str, expected: str) -> None:
    """Read the required checklist labels straight from the shipped issue forms."""
    labels = checker.load_required_checkbox_labels(_TEMPLATE_DIR / template)
    assert len(labels) >= 8
    assert all(label == label.casefold() for label in labels)
    # Markdown links are reduced to their link text, so the label text remains matchable.
    assert any(expected in label for label in labels)


def test_load_required_checkbox_labels_ignores_optional_options(tmp_path: Path) -> None:
    """Only options marked required belong to the checklist under test."""
    template = tmp_path / "form.yml"
    template.write_text(
        "body:\n"
        "  - type: checkboxes\n"
        "    attributes:\n"
        "      options:\n"
        "        - label: Required one\n"
        "          required: true\n"
        "        - label: Optional one\n"
        "          required: false\n"
        "  - type: input\n"
        "    attributes:\n"
        "      label: Some field\n",
        encoding="utf-8",
    )
    assert checker.load_required_checkbox_labels(template) == ["required one"]


# ---------------------------------------------------------------------------
# Checkbox parsing
# ---------------------------------------------------------------------------


def test_parse_checkbox_lines_reads_state() -> None:
    """Read the ticked state of every rendered checklist line."""
    body = "- [x] I have read the documentation\n- [ ] I am aware of the release notes\n* [X] Upper case tick\n"
    states = checker.parse_checkbox_lines(body)
    assert states["i have read the documentation"] is True
    assert states["i am aware of the release notes"] is False
    assert states["upper case tick"] is True


def test_parse_checkbox_lines_ignores_prose() -> None:
    """Ignore lines that are not checklist items."""
    assert checker.parse_checkbox_lines("Just prose.\n- a list item\n") == {}


# ---------------------------------------------------------------------------
# Body check
# ---------------------------------------------------------------------------

_REQUIRED = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
_ATTACHMENT = "https://github.com/user-attachments/files/1/diagnostics.json"


def _body(labels: list[str], *, ticked: bool = True, attachment: bool = True) -> str:
    mark = "x" if ticked else " "
    body = "\n".join(f"- [{mark}] {label}" for label in labels)
    if attachment:
        body += f"\n\n### Diagnostics information\n{_ATTACHMENT}\n"
    return body


def test_check_issue_body_accepts_a_complete_form() -> None:
    """Accept a body that carries the full ticked checklist and an attachment."""
    check = checker.check_issue_body(_body(_REQUIRED), required_labels=_REQUIRED, language="en")
    assert check.ok is True
    assert check.violations == ()
    assert check.raw_data_missing is False


def test_check_issue_body_tolerates_template_drift() -> None:
    """Accept a body missing a single label - a checklist item added after it was filed."""
    check = checker.check_issue_body(_body(_REQUIRED[:-1]), required_labels=_REQUIRED, language="en")
    assert check.ok is True
    assert check.missing_labels == ("ten",)


def test_check_issue_body_flags_rewritten_checklist() -> None:
    """Flag a body whose checklist lost more labels than template drift explains."""
    check = checker.check_issue_body(_body(_REQUIRED[:7]), required_labels=_REQUIRED, language="en")
    assert check.ok is False
    assert "rewritten" in check.violations


def test_check_issue_body_flags_bypassed_form() -> None:
    """Flag a freely composed body that keeps only a fraction of the checklist."""
    check = checker.check_issue_body(_body(_REQUIRED[:3]), required_labels=_REQUIRED, language="en")
    assert check.ok is False
    assert "bypassed" in check.violations
    assert "rewritten" not in check.violations


def test_check_issue_body_flags_unchecked_required_item() -> None:
    """Flag a required checklist item that is present but not ticked."""
    body = _body(_REQUIRED[:-1]) + "\n- [ ] ten\n"
    check = checker.check_issue_body(body, required_labels=_REQUIRED, language="en")
    assert check.ok is False
    assert "unchecked" in check.violations
    assert check.unchecked_labels == ("ten",)


def test_check_issue_body_reports_missing_raw_data_without_flagging_it() -> None:
    """Record a missing attachment, but never treat it as a form violation on its own."""
    check = checker.check_issue_body(_body(_REQUIRED, attachment=False), required_labels=_REQUIRED, language="en")
    assert check.raw_data_missing is True
    assert check.ok is True
    assert check.violations == ()


def test_check_issue_body_adds_raw_data_to_an_existing_violation() -> None:
    """List the missing raw data alongside a form violation, where it belongs to the same comment."""
    check = checker.check_issue_body(_body(_REQUIRED[:3], attachment=False), required_labels=_REQUIRED, language="en")
    assert check.violations == ("bypassed", "no-raw-data")


def test_check_issue_body_empty_body_is_bypassed() -> None:
    """Treat an empty body as a bypassed form."""
    check = checker.check_issue_body("", required_labels=_REQUIRED, language="en")
    assert "bypassed" in check.violations


# ---------------------------------------------------------------------------
# Comment formatting
# ---------------------------------------------------------------------------


def test_format_comment_lists_every_violation() -> None:
    """Render one bullet per violation plus the marker used for duplicate detection."""
    check = checker.check_issue_body(_body(_REQUIRED[:3], attachment=False), required_labels=_REQUIRED, language="en")
    comment = checker.format_comment(check, auto_closed=False)
    assert checker.COMMENT_MARKER in comment
    assert "AI_POLICY.md" in comment
    assert comment.count("- ❌") == len(check.violations)
    assert "stays open" in comment


def test_format_comment_german() -> None:
    """Render the German wording for an issue filed with the German template."""
    check = checker.check_issue_body(_body(_REQUIRED[:3]), required_labels=_REQUIRED, language="de")
    comment = checker.format_comment(check, auto_closed=True)
    assert "Issue-Formular nicht verwendet" in comment
    assert "automatisch geschlossen" in comment
    assert "öffnet es nicht wieder" in comment
    assert "bleibt bis dahin offen" not in comment


def test_format_comment_auto_closed_asks_for_a_new_issue() -> None:
    """Tell the reporter the issue is closed and that only a new issue through the form helps."""
    check = checker.check_issue_body(_body(_REQUIRED[:3], attachment=False), required_labels=_REQUIRED, language="en")
    comment = checker.format_comment(check, auto_closed=True)
    assert comment.startswith(f"{checker.COMMENT_MARKER}\n## 🔒 Closed")
    assert "closed automatically" in comment
    assert "does not reopen" in comment
    assert checker.NEW_ISSUE_URL in comment
    assert checker.DISCUSSIONS_URL in comment
    assert "AI_POLICY.md" in comment
    assert comment.count("- ❌") == len(check.violations)
    assert "stays open" not in comment


def test_format_comment_names_unchecked_labels() -> None:
    """Name the checklist items the reporter left unticked."""
    body = _body(_REQUIRED[:-1]) + "\n- [ ] ten\n"
    check = checker.check_issue_body(body, required_labels=_REQUIRED, language="en")
    assert "`ten`" in checker.format_comment(check, auto_closed=False)


# ---------------------------------------------------------------------------
# Exemptions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("association", ["OWNER", "MEMBER", "COLLABORATOR"])
def test_is_exempt_for_maintainers(association: str) -> None:
    """Never check issues filed by maintainers - they legitimately use the API."""
    assert checker.is_exempt(author_association=association, labels=()) is True


def test_is_exempt_via_skip_label() -> None:
    """Allow a maintainer to silence the check on a specific issue."""
    assert checker.is_exempt(author_association="NONE", labels=(checker.SKIP_LABEL,)) is True


def test_is_not_exempt_for_external_reporter() -> None:
    """Check issues filed by everyone else."""
    assert checker.is_exempt(author_association="NONE", labels=("bug",)) is False


# ---------------------------------------------------------------------------
# Regression: the report shape that motivated the check
# ---------------------------------------------------------------------------


def test_freely_composed_report_is_flagged() -> None:
    """
    Flag the body shape that motivated this check: a composed report without attachments.

    It reworded the checklist labels and replaced the mandatory diagnostics item with a
    prose note, which the issue form's required-field validation would have rejected -
    the issue was created through the API instead.
    """
    body = (
        "> **AI disclosure (per AI_POLICY.md):** This report was written by Claude (Anthropic).\n\n"
        "### I agree to the following\n"
        "- [x] I have read the documentation\n"
        "- [x] I have read the troubleshooting documentation and tried to identify/solve the issue by myself\n"
        "- [x] I am aware of the latest release notes\n"
        "- [ ] Diagnostics file: **intentionally not attached** - see below\n\n"
        "### The problem\n"
        "Commands are dropped while the cover is moving.\n"
    )
    required = checker.load_required_checkbox_labels(_TEMPLATE_DIR / "bug_report.yml")
    check = checker.check_issue_body(body, required_labels=required, language="en")
    assert check.ok is False
    assert "bypassed" in check.violations
    assert "no-raw-data" in check.violations
