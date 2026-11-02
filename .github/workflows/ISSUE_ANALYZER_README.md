# Issue Analyzer Workflow

This GitHub Actions workflow automatically **triages** newly created issues. It deliberately
does **not** diagnose root causes: an audit of 181 bot-commented issues (2026-07) showed that
LLM root-cause analyses were fully correct in only 18% of cases and outright wrong in 24%,
while the data-collection parts (missing diagnostics/log requests) were the reliably useful
ones. The bot therefore focuses on deterministic checks; do not re-add diagnosis sections.

## What the bot does

1. **Checks required raw data (deterministic)**
   - Detects the integration diagnostics (.json) and the log file, both as **uploaded files**.
     A log excerpt pasted into a fenced code block does not count: it is a selection made by
     the reporter and usually drops the context the analysis needs (see `AI_POLICY.md`).
   - Requests missing data and maintains the `needs-raw-data` triage label. The label keys on
     the raw data alone — detected AI content does not earn it, because an AI-assisted report
     with both files attached is allowed.

2. **Validates the reported version (deterministic)**
   - Parses the version from the issue-form field, tolerating context the reporter added to it
     ("2.11.0 (aiohomematic 2026.9.1)")
   - Compares it against the actually published releases of
     [homematicip_local](https://github.com/sukramj/homematicip_local/releases)
   - Posts a *neutral* notice when the version is outdated or matches no published release —
     never a "critical" banner

3. **Detects AI-authored reports (deterministic)**
   - Three signals, in descending reliability: the template's AI-tool field answered with
     anything but a denial; an authorship disclosure or model self-identification in the body;
     at least two stylistic markers
   - Redirects the reporter to attach the underlying files — but stays silent when both files
     are already attached, since AI-assisted writing is allowed in that case

4. **Searches for similar issues (GitHub search API)**
   - Uses the device model (extracted deterministically) plus LLM-suggested search terms
   - Queries the real GitHub search API (the previous implementation listed the most
     recently updated issues regardless of relevance)

5. **Uses Claude only for triage, not diagnosis**
   - A short summary (max. 2 sentences), 0-2 documentation links, search terms, and
     routing flags (device-related, feature request)
   - The prompt contains the current date and forbids root-cause claims
   - If the Claude call fails, the deterministic triage comment is still posted

6. **Multilingual support**
   - Detects the template language (German/English) and responds in it

## Companion workflow: Close Issue - Insufficient Information

`close-insufficient-info.yml` closes an issue that lacks the required data. It is triggered
manually (`workflow_dispatch`) and protects against premature closes with guardrails:

- refuses to close when the issue contains uploaded files or screenshots (a pasted log
  excerpt deliberately does not block the close — it does not satisfy the raw-data
  requirement either)
- refuses to close issues labeled as feature requests (`enhancement`/`feature`)
- enforces a minimum waiting period of **72 hours** after the `needs-raw-data` label was
  applied (or after issue creation), giving reporters time to supply the data
- `force: true` input overrides all guardrails

## Companion workflow: Validate Issue Template

`validate-issue-template.yml` verifies that a new issue actually went through the issue form.
The forms mark every checklist item as `required: true`, but GitHub enforces that only in the
browser — an issue created through the API can carry an arbitrary body.

`check_issue_template.py` reads the required checkbox labels from `.github/ISSUE_TEMPLATE/*.yml`
at run time, so the check cannot drift away from the templates, and reports:

- `bypassed` — the body keeps less than half of the required checklist (freely composed)
- `rewritten` — more required labels are missing than template drift explains
  (`MAX_DRIFT_MISSING`, measured against the 25 most recent externally filed issues)
- `unchecked` — a required item is present but not ticked
- `no-raw-data` — no uploaded file; reported only alongside a form violation, since the
  analyzer already covers it on its own

On a violation the issue gets the `invalid-template` label, one explanatory comment, and is
**closed as not planned right away**. Editing the issue later does not reopen it; the comment
asks for a new issue through the form. To only label and comment, set the repository variable
`AUTO_CLOSE_INVALID_TEMPLATE` to `false`, or untick the `auto_close` input of a manual run.
Maintainers (`OWNER`/`MEMBER`/
`COLLABORATOR`) and issues labeled `skip-template-check` are exempt.

## Setup

### Prerequisites

To activate the workflow, you need an Anthropic API key:

1. Create an account at [Anthropic](https://console.anthropic.com/)
2. Generate an API key

### Configuration

1. **Add GitHub Secret**
   - Go to: Repository Settings → Secrets and variables → Actions
   - Click on "New repository secret"
   - Name: `ANTHROPIC_API_KEY`
   - Value: Your Anthropic API key

2. **Optional: pin the Claude model**
   - Repository variable `ANALYZER_MODEL` overrides the default model used for the
     triage summary (no code change needed when a model is renamed)

3. **Activate workflow**
   - The workflow is automatically active after adding the secret
   - It runs on every newly created or edited issue (a comment is only posted once)

### Permissions

The workflow requires the following permissions (already configured):

- `issues: write` - To post comments and maintain labels
- `contents: read` - To read the repository

## Comment structure

A posted comment can contain (only sections with content are rendered):

- Summary (LLM, descriptive only)
- Version notice (deterministic: outdated / unknown version)
- Missing required information (diagnostics / log / version field)
- Raw-data redirect when a pasted AI analysis was detected
- Feature-request routing hint (pointing to the discussions)
- Screenshot hint for device-related issues
- Helpful documentation (max. 2 links)
- Similar issues (search-API results)

If none of the sections has content, no comment is posted.

## Customization

- **Documentation links**: `DOCS_LINKS` in `.github/scripts/analyze_issue.py`
- **Triage prompt**: `CLAUDE_TRIAGE_PROMPT` in `analyze_issue.py` (keep the no-diagnosis rules!)
- **Version-field markers**: `VERSION_FIELD_MARKERS` (update when the issue-template labels change)

## Costs

- One Claude call per issue with a small output budget (max. 600 tokens)
- Estimated costs: well below $0.01-0.03 per issue

## Troubleshooting

### Workflow is not running

- Check if the `ANTHROPIC_API_KEY` secret is set
- Review the workflow logs under Actions → Issue Analyzer

### Comment is not posted

- The workflow only posts when at least one section has content
- Check the logs for error messages

### API errors

- Make sure the API key is valid
- Check your Anthropic account for sufficient credits
- The deterministic checks still run and post when the Claude call fails

## Deactivation

To deactivate the workflow:

1. Delete or rename the file `.github/workflows/issue-analyzer.yml`
2. Or add at the beginning:
   ```yaml
   on:
     workflow_dispatch: # Only manually executable
   ```
