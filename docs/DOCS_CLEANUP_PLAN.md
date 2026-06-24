# Documentation Cleanup Plan

## Purpose

Documentation cleanup is needed because LeadOS now has a useful agent operating layer, verified PR CI state, and a broader set of historical planning notes that no longer all describe the current repository accurately. The cleanup should make future human and AI-agent work safer by separating current instructions from historical context, reducing duplicate task sources, and preventing agents from following stale CI, tooling, or sprint-state notes.

This plan does not perform cleanup. It defines what should be updated, labeled, merged later, or left alone.

## TASK-0005 Progress

Historical/status labels were added to the highest-risk stale docs. This reduces agent confusion, but it does not fully reconcile backlog statuses, merge duplicate docs, or archive historical material.

## TASK-0006 Progress

`docs/ACTIVE_TASKS.md` was created as the canonical active task source. Historical backlog, sprint review, and fix-log docs should remain references unless a task is promoted into the active index.

## TASK-0006A Progress

CI state reconciliation was attempted after the TASK-0006 push, but GitHub Actions could not be inspected from this environment. This was later superseded by verified Backend CI run #60 at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`.

## TASK-0007 Progress

`docs/LOCAL_ENVIRONMENT.md` was added as the local backend environment setup guide. It documents Python 3.12, virtual environments, dependency installation, validation commands, common setup failures, and the current verified PR CI state.

## TASK-0008 Progress

`docs/CI_TROUBLESHOOTING.md` was added as the Backend CI troubleshooting guide. It documents failing-step diagnosis, local command equivalents, common CI failure categories, and agent safety rules for CI repair.

## TASK-0009 Progress

`docs/PR_CHECKLIST.md` was added as the canonical PR readiness checklist. It documents merge readiness, docs-only checks, backend-change checks, dependency/tooling checks, manual verification, deferred items, and agent safety rules.

## TASK-0010 Progress

`docs/BACKLOG_RECONCILIATION.md` was added as the canonical implementation backlog reconciliation. It records source priority, historical backlog risks, GitHub issue access status, candidate tasks, the recommended implementation sequence, and the next task decision.

## Current Documentation Risk Summary

- Stale implementation state: older backlog and sprint docs still describe pending work that appears partially or fully implemented.
- Stale CI state: older tooling notes still say automated checks or workflow creation are missing even though Backend CI exists and PR #1 passed run #67.
- Duplicate task sources: `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, sprint reviews, fix logs, and agent changelog all describe work state from different moments.
- Historical notes mistaken as current instructions: sprint reviews, council review, automation note, and tooling note can be read as active guidance unless clearly labeled.
- Broad planning docs conflicting with current sprint reality: role-based and drift-control guidance is useful, but should not override the current agent operating layer or verified CI state.

## Cleanup Classification

| File | Current Role | Risk Level | Problem | Recommended Action | Timing |
|---|---|---:|---|---|---|
| `docs/TASKS.md` | Backlog and phase task list. | High | Multiple statuses appear stale relative to implemented backend, CI, audit, and scoring work. | Reference through `docs/BACKLOG_RECONCILIATION.md` before update | Now |
| `docs/GITHUB_ISSUES_TO_CREATE.md` | Draft issue backlog. | High | Still lists "Add CI workflow" as remaining even though Backend CI exists and passed PR #1 run #67. | Reference through `docs/BACKLOG_RECONCILIATION.md` before update | Now |
| `docs/TOOLING_NOTES.md` | Early tooling rationale. | High | Says workflow file creation was not completed; this conflicts with current CI. | Mark historical | Now |
| `docs/AUTOMATION_NOTE.md` | Short note to add backend checks. | High | Says automated backend checks should be added; Backend CI already exists. | Mark historical | Now |
| `docs/FIX_LOG.md` | Sprint fix summary. | Medium | Historical label added; `10 passed` remains a historical local result, not current validation. | Mark historical | Before merge |
| `docs/SPRINT_1_REVIEW.md` | Sprint 1 historical review. | Medium | Historical label and CI note added; remaining CI text is preserved for traceability. | Mark historical | Before merge |
| `docs/SPRINT_2_REVIEW.md` | Sprint 2 historical review. | Medium | Historical label added; validation and remaining-work notes remain historical. | Mark historical | Before merge |
| `docs/COUNCIL_REVIEW_001.md` | Early council review. | Medium | Says next task is adding automated backend checks when CI now exists. | Mark historical | Before merge |
| `docs/STACK.md` | Stack and tooling summary. | Medium | Mentions `uv` as stack while Makefile and CI use pip; can confuse local setup. | Update | Before merge |
| `docs/DATA_MODEL.md` | Data model reference. | Medium | May lag ORM implementation; audit/score persistence wording should be verified against source before schema work. | Update | Before merge |
| `docs/REFERENCES.md` | Tooling reference note. | Low | Lists reference categories without links, dates, or versions. | Update | Deferred |
| `docs/NOTE.md` | Minimal focus reminder. | Low | Redundant with README, product spec, drift control, and AGENTS. | Merge later | Deferred |
| `docs/ENGINEERING_RULES.md` | Early engineering rules and task design guidance. | Medium | Overlaps with AGENTS, WORKFLOW, DONE_CRITERIA, and DECISIONS. | Merge later | Deferred |
| `docs/DRIFT_CONTROL.md` | Product drift checklist. | Low | Overlaps with AGENTS and DECISIONS but remains useful as a quick product guard. | Keep current | Deferred |
| `docs/EXPERT_COUNCIL.md` | Role-based review model. | Low | Broad planning document could be overused for small fixes. | Keep current | Deferred |
| `docs/API_REVIEW_001.md` | Focused scoring API review. | Low | Historical review, not a canonical API contract. | Mark historical | Deferred |
| `docs/SCORING_REVIEW_001.md` | Focused scoring review. | Low | Useful risk review, but historical and should not be treated as live implementation status. | Mark historical | Deferred |
| `docs/SECURITY_REVIEW_001.md` | Focused audit fetcher security review. | Medium | Useful security review, but implementation state should be checked before relying on "controls added." | Mark historical | Deferred |
| `docs/DOCS_INVENTORY.md` | Documentation audit and reading-order guide. | Low | Should be updated after cleanup so it reflects new labels and canonical sources. | Update | After merge |
| `docs/CHANGELOG_AGENT.md` | Current agent state. | Low | Current after CI reconciliation; must remain small and operational. | Keep current | Now |
| `docs/MANUAL_ACTIONS.md` | Manual gates and deferred work. | Low | Current after CI reconciliation; update only when manual gates change. | Keep current | Now |
| `docs/CONTEXT_INDEX.md` | Context map for agents. | Low | Should eventually point agents away from stale files once cleanup happens. | Update | After merge |

## Canonical Sources Going Forward

| Topic | Canonical File | Notes |
| ----- | -------------- | ----- |
| Agent instructions | `AGENTS.md` | Primary entrypoint for AI coding agents. |
| Current state | `docs/CHANGELOG_AGENT.md` | Keep concise; update when branch, PR, CI, blockers, or completion state changes. |
| Manual actions | `docs/MANUAL_ACTIONS.md` | Source of truth for current required-now, before-merge, before-production, and deferred manual work. |
| Validation commands | `docs/VALIDATION_COMMANDS.md` | Human-readable validation guide; `backend/Makefile` and `.github/workflows/backend-ci.yml` remain operational truth. |
| Product scope | `docs/PRODUCT_SPEC.md` and `docs/MVP_SCOPE.md` | Product thesis and MVP boundary should remain separate but aligned. |
| Architecture | `docs/ARCHITECTURE.md` | Source of truth for service boundaries and dependency direction. |
| Data model | `docs/DATA_MODEL.md` | Must be kept aligned with `backend/app/models/` and future migrations. |
| Task execution | `docs/WORKFLOW.md` and `docs/DONE_CRITERIA.md` | Controls how agents plan, implement, validate, and report work. |
| Risks | `docs/RISK_REGISTER.md` | Source of truth for known risks and future mitigations. |
| Sprint state | `docs/ACTIVE_TASKS.md` and `docs/CHANGELOG_AGENT.md` | Active work belongs in `docs/ACTIVE_TASKS.md`; current validation/state belongs in `docs/CHANGELOG_AGENT.md`; sprint reviews and fix logs are historical references. |

## Files Recommended for Immediate Update

### `docs/TASKS.md`

- Why it needs update: It is a likely planning source and contains statuses that appear stale relative to current backend and CI state.
- Exact section to update: Phase/task statuses across Phase 0 through Phase 6, especially tasks for schema, service boundaries, lead import, audit, scoring, and CI-adjacent work.
- Safe change type: Add a "Status note" at the top stating that this file is stale pending reconciliation, or update statuses after checking source and CI.
- What not to change: Do not delete backlog items or redefine product scope in this pass.

### `docs/GITHUB_ISSUES_TO_CREATE.md`

- Why it needs update: It lists "Add CI workflow" as remaining even though Backend CI exists and passed PR #1 run #67.
- Exact section to update: `Remaining issues`.
- Safe change type: Move "Add CI workflow" to completed or replace it with a narrower "document CI troubleshooting/local environment" issue.
- What not to change: Do not create, close, or renumber GitHub issues from this document.

### `docs/TOOLING_NOTES.md`

- Why it needs update: It states workflow creation was not completed and references GitHub Actions as later.
- Exact section to update: `Selected baseline` and `Known limitation`.
- Safe change type: Mark the document historical at the top and point to `docs/VALIDATION_COMMANDS.md`, `.github/workflows/backend-ci.yml`, and `backend/Makefile` as current.
- What not to change: Do not change CI behavior or backend tooling from this note.

### `docs/AUTOMATION_NOTE.md`

- Why it needs update: It says automated backend checks should be added before the next feature module; that is stale after Backend CI was added and verified.
- Exact section to update: Entire file or top-level note.
- Safe change type: Mark historical and point to Backend CI and validation docs.
- What not to change: Do not expand this into a CI design document.

### `docs/STACK.md`

- Why it needs update: It lists `uv` as stack while current Makefile and CI use pip, which can confuse environment setup.
- Exact section to update: `Backend` and `CI checks`.
- Safe change type: Clarify current operational tooling versus acceptable future tooling.
- What not to change: Do not add dependencies or change the Makefile.

### `docs/DATA_MODEL.md`

- Why it needs update: The data model should be checked against ORM models before future persistence, migration, reporting, or scoring persistence work.
- Exact section to update: Table descriptions for `lead_audits` and `lead_scores`, plus any current/reserved wording that differs from source.
- Safe change type: Reconcile wording after inspecting `backend/app/models/` only.
- What not to change: Do not design migrations or alter schema from this cleanup task.

## Files Recommended for Archive or Historical Label

### `docs/FIX_LOG.md`

- Why it is risky: It contains a historical `10 passed` validation result that can be mistaken for current validation.
- Whether it still has useful information: Yes, it summarizes important Sprint 1 and Sprint 2 fixes.
- Proposed archive path if applicable: `docs/archive/FIX_LOG.md`.

### `docs/SPRINT_1_REVIEW.md`

- Why it is risky: It says GitHub Actions CI remains to be added.
- Whether it still has useful information: Yes, it records Sprint 1 scope, files, and constraints.
- Proposed archive path if applicable: `docs/archive/SPRINT_1_REVIEW.md`.

### `docs/SPRINT_2_REVIEW.md`

- Why it is risky: It contains historical validation and completion claims that need current context.
- Whether it still has useful information: Yes, it records SQL/data-layer changes and remaining non-blocking improvements.
- Proposed archive path if applicable: `docs/archive/SPRINT_2_REVIEW.md`.

### `docs/COUNCIL_REVIEW_001.md`

- Why it is risky: It says the next task is adding automated backend checks.
- Whether it still has useful information: Yes, it records early constraint checks.
- Proposed archive path if applicable: `docs/archive/COUNCIL_REVIEW_001.md`.

### `docs/API_REVIEW_001.md`

- Why it is risky: It is a focused review and not a canonical API contract.
- Whether it still has useful information: Yes, especially around scoring preview risks and boundaries.
- Proposed archive path if applicable: `docs/archive/API_REVIEW_001.md`.

### `docs/SCORING_REVIEW_001.md`

- Why it is risky: It can be mistaken for current scoring implementation status.
- Whether it still has useful information: Yes, especially scoring risks and future hardening.
- Proposed archive path if applicable: `docs/archive/SCORING_REVIEW_001.md`.

### `docs/SECURITY_REVIEW_001.md`

- Why it is risky: It states controls added; future agents should verify source/tests before relying on those controls.
- Whether it still has useful information: Yes, it remains important audit-fetcher security context.
- Proposed archive path if applicable: `docs/archive/SECURITY_REVIEW_001.md`.

### `docs/AUTOMATION_NOTE.md`

- Why it is risky: It now conflicts with verified Backend CI.
- Whether it still has useful information: Minimal; it is mostly historical.
- Proposed archive path if applicable: `docs/archive/AUTOMATION_NOTE.md`.

### `docs/TOOLING_NOTES.md`

- Why it is risky: It conflicts with current CI state and can confuse agents about workflow availability.
- Whether it still has useful information: Some, especially rationale for keeping checks small.
- Proposed archive path if applicable: `docs/archive/TOOLING_NOTES.md`.

## Files That Should Not Be Touched Yet

- `AGENTS.md`: Current agent instruction layer; only update if workflow rules change.
- `docs/CHANGELOG_AGENT.md`: Current after CI reconciliation; keep concise.
- `docs/MANUAL_ACTIONS.md`: Current after CI reconciliation; update only when gates change.
- `docs/WORKFLOW.md`: Current execution loop.
- `docs/DONE_CRITERIA.md`: Current done criteria.
- `docs/VALIDATION_COMMANDS.md`: Current validation command guide.
- `docs/DECISIONS.md`: Current ADR layer.
- `docs/RISK_REGISTER.md`: Current risk register.
- `docs/PRODUCT_SPEC.md`: Canonical product thesis and non-goals.
- `docs/MVP_SCOPE.md`: Canonical MVP scope.
- `docs/ARCHITECTURE.md`: Canonical service-boundary guidance.
- Domain rubrics: `docs/AUDIT_RUBRIC.md`, `docs/SCORING_RUBRIC.md`, `docs/OUTREACH_RUBRIC.md`, `docs/EVALUATION_RUBRIC.md`.
- `.github/workflows/backend-ci.yml`: CI behavior should not change during docs cleanup.
- Backend files and tests: not part of documentation cleanup.

## Proposed Cleanup Order

1. Manually verify GitHub issue state before starting TASK-0203.
2. Reconcile `docs/TASKS.md` against current source, tests, verified PR #1 Backend CI, and `docs/ACTIVE_TASKS.md`.
3. Clarify current tooling in `docs/STACK.md` without changing CI or dependencies.
4. Reconcile `docs/DATA_MODEL.md` against ORM models before migration/reporting/scoring persistence work.
5. Mark remaining review artifacts as historical where needed, including `docs/COUNCIL_REVIEW_001.md`.
6. Update `docs/CONTEXT_INDEX.md` to identify historical files and point future agents to canonical active sources.
7. Update `docs/DOCS_INVENTORY.md` after cleanup so it reflects new labels and any archive decisions.
8. Archive obsolete notes under `docs/archive/` after PR merge if the team wants a cleaner top-level docs folder.

## Manual Work Required

### Required now

- Manually verify current GitHub issue state before starting TASK-0203 because GitHub CLI could not connect during TASK-0010.
- Keep PR #1 Backend CI green for the latest head commit if any new commit is pushed.

### Required before merge

- Update or label the highest-risk stale docs so future agents do not plan from obsolete CI/task state.
- Confirm whether `docs/TASKS.md` should remain the canonical backlog or be replaced by a smaller active task index.

### Can be deferred

- Move historical docs to `docs/archive/`.
- Add `docs/API_CONTRACT.md`, `docs/MIGRATIONS_PLAN.md`, `docs/REPORTING_PLAN.md`, and `docs/SCORING_PERSISTENCE_PLAN.md`.
- Merge redundant lightweight docs such as `docs/NOTE.md` into canonical product or drift-control docs.

## Risks If Cleanup Is Skipped

Stale docs could cause future Codex or AI-agent sessions to duplicate completed CI work, rebuild already implemented backend modules, trust historical local test results as current validation, or follow broad planning notes instead of the current agent operating layer. Conflicting task sources could also lead agents to start feature work before documentation drift, local environment gaps, migrations, or reporting plans are addressed.

The largest operational risk is that an agent reads `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, or old sprint reviews as current truth and ignores `docs/CHANGELOG_AGENT.md`, `docs/MANUAL_ACTIONS.md`, and verified Backend CI state.

## Next Recommended Task

TASK-0203: CSV lead import validator with clear invalid-row reporting and import summary.
