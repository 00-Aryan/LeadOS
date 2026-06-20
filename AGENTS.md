# LeadOS Agent Operating Instructions

## Project Identity

LeadOS is a standalone lead intelligence platform for importing local-business leads, auditing visible digital-presence gaps, scoring outreach opportunity, preparing outreach drafts, and evaluating those drafts before human use.

LeadOS is intentionally separate from ProjectOS and the existing content-creation automation tool. Future integrations may be designed through clean APIs and structured outputs, but they are not part of the MVP unless explicitly assigned.

## MVP Loop

```text
CSV import -> deterministic website audit -> explainable scoring -> outreach draft -> evaluator
```

## Current Execution Rule

Do not start new feature work if CI is failing. Fix formatting, lint, tests, or broken CI configuration first, then proceed only after the repository is back to a verifiable state.

Docs-only cleanup and explicit repair tasks may proceed from a dirty or unverified baseline only when the task scope permits that repair.

## Required Repository State Check

Before editing, the agent must run:

```bash
git status --short
git branch --show-current
git log --oneline -5
```

When the task depends on current PR validation, the agent must verify:

- current PR head commit
- current Backend CI status
- whether local HEAD matches the verified PR head

The agent must not start feature work from an unverified or dirty baseline unless the task is explicitly a repair task.

## Scoped Commit Rule

The agent must stage only files allowed by the assigned task.

Before committing, run:

```bash
git status --short
git diff --check
```

The final commit must not include unrelated files, environment files, caches, local test artifacts, or generated files unless explicitly assigned.

If unexpected files appear, the agent must stop and ask before staging them.

## Required Agent Workflow

For every assigned task:

1. Read `AGENTS.md`.
2. Read `docs/CONTEXT_INDEX.md`.
3. Read the assigned issue or task.
4. Run the required repository state check.
5. Inspect affected files before editing.
6. Produce a short implementation plan.
7. Make the smallest safe change that satisfies scope.
8. Run validation.
9. Report files changed, commands run, result, risks, and manual work.

## Context Discipline and Drift Prevention

Before editing code, the agent must establish the task boundary using evidence from files, not assumptions.

For every assigned task, the agent must identify:

1. The active task source:
   - GitHub issue, user-assigned task, or `docs/ACTIVE_TASKS.md`.
2. The authoritative state source:
   - `docs/ACTIVE_TASKS.md`
   - `docs/BACKLOG_RECONCILIATION.md`
   - Current PR head and CI status when PR validation is relevant.
3. The affected backend layer:
   - schema
   - service
   - repository
   - model
   - router
   - tests
   - documentation
4. The allowed files for the task.
5. The explicitly forbidden files or scopes.
6. The validation gate required before completion.

The agent must not rely on historical docs as active work unless the task is promoted in `docs/ACTIVE_TASKS.md` or assigned by the user.

Historical/reference-only docs include:

- `docs/TASKS.md`
- `docs/GITHUB_ISSUES_TO_CREATE.md`
- `docs/FIX_LOG.md`
- `docs/SPRINT_1_REVIEW.md`
- `docs/SPRINT_2_REVIEW.md`

## Backend Context Map

Use this map to decide which files must be inspected before backend implementation.

### Lead import tasks

Inspect:

- `backend/app/schemas/lead.py`
- `backend/app/models/lead.py`
- `backend/app/models/lead_import.py`
- `backend/app/repositories/lead_repository.py`
- `backend/app/services/lead_import_service.py`
- `backend/app/services/lead_transform_service.py`
- `backend/app/routers/leads.py`
- `backend/tests/test_lead_import_service.py`
- `backend/tests/test_lead_repository.py`
- `backend/tests/test_leads_router.py`

### Audit tasks

Inspect:

- `backend/app/schemas/audit.py`
- `backend/app/models/lead_audit.py`
- `backend/app/repositories/audit_repository.py`
- `backend/app/services/audit_service.py`
- `backend/tests/test_audit_service.py`
- `backend/tests/test_audit_repository.py`
- `docs/AUDIT_RUBRIC.md`

### Scoring tasks

Inspect:

- `backend/app/schemas/score.py`
- `backend/app/models/lead_score.py`
- `backend/app/repositories/score_repository.py`
- `backend/app/services/scoring_service.py`
- `backend/app/routers/scoring.py`
- `backend/tests/test_scoring_service.py`
- `backend/tests/test_score_repository.py`
- `backend/tests/test_scoring_router.py`
- `docs/SCORING_RUBRIC.md`

### Outreach tasks

Inspect:

- `backend/app/services/outreach_service.py`
- `docs/OUTREACH_RUBRIC.md`
- `docs/EVALUATION_RUBRIC.md`
- Existing outreach/evaluation tests, if present.

### Evaluation tasks

Inspect:

- `backend/app/services/evaluation_service.py`
- `docs/EVALUATION_RUBRIC.md`
- `docs/EXPERT_COUNCIL.md`
- Existing evaluation tests, if present.

### Cross-cutting backend tasks

Inspect:

- `backend/app/main.py`
- `backend/app/database.py`
- `backend/app/config.py`
- `backend/Makefile`
- `backend/pytest.ini`
- `backend/ruff.toml`
- `.github/workflows/backend-ci.yml`
- `docs/ARCHITECTURE.md`
- `docs/DATA_MODEL.md`
- `docs/ENGINEERING_RULES.md`
- `docs/DRIFT_CONTROL.md`
- `docs/DONE_CRITERIA.md`
- `docs/VALIDATION_COMMANDS.md`

## Pre-Edit Report Requirement

Before modifying files, the agent must produce a short pre-edit report:

```text
PRE-EDIT CONTEXT CHECK

Active task:
- ...

Authoritative sources read:
- ...

Affected layers:
- ...

Files inspected:
- ...

Allowed files:
- ...

Forbidden scope:
- ...

Assumptions:
- ...

Validation gate:
- ...
```

If this report cannot be produced, the agent must stop and ask for clarification.

## Hallucination Prevention Rule

The agent must not claim:

- A file exists unless it has inspected the file tree or file content.
- A test passed unless the command output confirms it.
- CI is green unless GitHub Actions confirms it.
- A task is complete unless code is committed, pushed, and CI passes.
- A behavior exists unless it is shown in code or tests.

Every final report must distinguish:

```text
Verified:
- ...

Not verified:
- ...

Blocked:
- ...
```

## Local Validation Fallback

Local validation failures caused by missing local tools do not mean the implementation passed.

When local validation is blocked by missing Python, Ruff, pytest, or dependencies:

- Report the exact blocker.
- Run any safe supplemental checks available, such as:
  - `git diff --check`
  - `python -m py_compile` where possible.
- Commit and push only if the scoped changes are intentional.
- Treat GitHub Backend CI as the completion source of truth.
- Do not mark the task complete until GitHub Backend CI passes for the pushed commit.

## Hard Constraints

- Do not add scraping or crawling.
- Do not add outbound sending.
- Do not add CRM integration.
- Do not add ProjectOS integration.
- Do not add Content Creation Automation integration.
- Do not add AI calls unless explicitly assigned.
- Do not modify unrelated files.
- Do not mark a task done if required validation is failing or unverified.
- Do not hide manual work from the user.

## Backend Validation Commands

Run these from a clean working tree when backend behavior or shared Python code is touched:

```bash
cd backend
make format-check
make lint
make test
```

If formatting fails:

```bash
cd backend
ruff format .
make format-check
```

For a full backend gate:

```bash
cd backend
make check
```

## Required Final Report Format

Every agent task must end with this structure:

```text
TASK-XXXX REPORT

Files created:
- ...

Files updated:
- ...

Commands run:
- ...

Validation result:
- ...

Verified:
- ...

Not verified:
- ...

Blocked:
- ...

Manual work required:
- Required now: ...
- Can be deferred: ...

Risks remaining:
- ...

Next recommended task:
- ...
```

If validation could not be run, explain the exact blocker and do not claim the task is complete.
