# Documentation Inventory

## Audit Metadata

- Branch: `phase-0-product-foundation`
- Date: 2026-06-15
- Reviewer: Codex
- Scope: Repository documentation, agent operating instructions, GitHub issue templates, backend CI workflow, and backend validation tooling. Backend source code was not audited for behavior in this pass.

## TASK-0005 Label Update

Historical/status labels were added to the highest-risk stale docs: `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, `docs/TOOLING_NOTES.md`, `docs/AUTOMATION_NOTE.md`, `docs/FIX_LOG.md`, `docs/SPRINT_1_REVIEW.md`, and `docs/SPRINT_2_REVIEW.md`.

## TASK-0006 Active Task Index Update

`docs/ACTIVE_TASKS.md` now exists as the canonical active task source. Historical task, sprint, and fix-log docs are references only.

## TASK-0006A CI State Reconciliation Attempt

GitHub Actions could not be inspected from this environment after the TASK-0006 push. This was later superseded by verified Backend CI run #60 at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`.

## TASK-0007 Local Environment Setup Update

`docs/LOCAL_ENVIRONMENT.md` now exists as the local backend setup guide. The latest verified PR state is Backend CI run #60 at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`.

## Executive Summary

LeadOS has a strong documentation base for product boundaries, rubrics, backend validation, and AI-agent execution. The new agent operating layer is useful and should be treated as the primary control layer for future Codex sessions.

The main risk is not missing documentation, but document drift. Several older sprint, tooling, and backlog files describe earlier states: CI is now present, SQL persistence exists, scoring/audit code exists, and local validation can still be blocked by environment setup. Current verified PR validation is Backend CI run #60 at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`. Future agents should read the agent-control docs first, then treat sprint reviews and older notes as historical context unless confirmed against source code and current CI.

## Documentation Map

| Path | Purpose | Current Status | Read Priority | Notes |
|---|---|---|---|---|
| `AGENTS.md` | Main operating instructions for AI coding agents. | Current, canonical. | P0 | Controls task workflow, hard constraints, validation, and final report format. |
| `README.md` | Top-level project identity and initial build principle. | Current, useful. | P1 | Good product boundary summary. |
| `docs/CONTEXT_INDEX.md` | Map of important files and when to read them. | Current, canonical. | P0 | Should be read immediately after `AGENTS.md`. |
| `docs/ACTIVE_TASKS.md` | Canonical active task index. | Current, canonical. | P0 | Use this as the active source for executable work before reading historical task/backlog files. |
| `docs/WORKFLOW.md` | Standard agent planning, implementation, validation, failure, and reporting loop. | Current, canonical. | P0 | Reinforces CI/test failures blocking feature work. |
| `docs/DONE_CRITERIA.md` | Definition of done for tasks. | Current, canonical. | P0 | Prevents false completion when validation fails. |
| `docs/VALIDATION_COMMANDS.md` | Backend and docs validation commands. | Current, canonical. | P0 | Needs local environment caveat from `docs/MANUAL_ACTIONS.md`. |
| `docs/LOCAL_ENVIRONMENT.md` | Local Python and backend validation setup guide. | Current, canonical. | P0 | Use when local validation cannot run or before provisioning backend dependencies. |
| `docs/MANUAL_ACTIONS.md` | Manual work and environment/CI verification requirements. | Current, operational. | P0 | Tracks verified CI state and local environment caveats. |
| `docs/CHANGELOG_AGENT.md` | Latest known agent state and blockers. | Current, operational. | P0 | Records PR #1 Backend CI pass at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`, run #60. |
| `docs/DECISIONS.md` | ADR-style project decisions. | Current, canonical. | P1 | Controls standalone scope, no scraping, no sending, deterministic-first approach. |
| `docs/RISK_REGISTER.md` | Risk table for product and workflow risks. | Current, useful. | P1 | Important before network fetch, outreach, scoring, migrations, or CI work. |
| `docs/FILE_OWNERSHIP.md` | Directory responsibility map. | Current, useful. | P1 | Helps agents limit edits to owned paths. |
| `docs/PRODUCT_SPEC.md` | Product thesis, user, workflow, modules, non-goals. | Current, canonical. | P1 | Product source of truth. |
| `docs/MVP_SCOPE.md` | MVP objective, in/out of scope, workflow, success criteria. | Current, canonical. | P1 | Overlaps with product spec but is more scope-focused. |
| `docs/ARCHITECTURE.md` | Service boundaries and dependency rules. | Current, canonical. | P1 | Required before touching service boundaries. |
| `docs/DATA_MODEL.md` | Table plan and current database strategy. | Mostly current, incomplete. | P1 | Audit/score tables are described as reserved; source code should confirm current persistence. |
| `docs/DATA_TRANSFORMATION_PLAN.md` | CSV transformation and future extraction query plan. | Current, useful. | P1 | Important for import, dedupe, and reporting work. |
| `docs/ENGINEERING_RULES.md` | Engineering constraints and task design rule. | Useful, partly superseded. | P2 | Overlaps with `AGENTS.md`, `WORKFLOW.md`, and `DONE_CRITERIA.md`. |
| `docs/DRIFT_CONTROL.md` | Product drift checks. | Useful, lightweight. | P2 | Keep as quick scope guard; overlaps with `AGENTS.md` and `DECISIONS.md`. |
| `docs/EXPERT_COUNCIL.md` | Role-based review mechanism and task design rule. | Useful, broad. | P2 | Good for planning complex tasks; too broad for every small fix. |
| `docs/AUDIT_RUBRIC.md` | Deterministic website audit rubric. | Current, useful. | P1 | Required before audit changes. |
| `docs/SCORING_RUBRIC.md` | Deterministic scoring rubric. | Current, useful. | P1 | Required before scoring changes. |
| `docs/OUTREACH_RUBRIC.md` | Draft-only outreach rules and forbidden behavior. | Current, useful. | P1 | Required before outreach work. |
| `docs/EVALUATION_RUBRIC.md` | Outreach evaluation scoring and review triggers. | Current, useful. | P1 | Required before evaluator work. |
| `docs/API_REVIEW_001.md` | Review of stateless scoring preview API. | Useful, historical. | P2 | Good for scoring API context; not a complete API contract. |
| `docs/SECURITY_REVIEW_001.md` | Website audit fetcher security review. | Useful, important. | P1 | Required before fetch/network/audit expansion. |
| `docs/SCORING_REVIEW_001.md` | First scoring function review. | Useful, historical. | P2 | Good for risks and future hardening; source should confirm implementation state. |
| `docs/COUNCIL_REVIEW_001.md` | Early council review summary. | Historical, partly stale. | P3 | Says next task is CI workflow; CI now exists. |
| `docs/SPRINT_1_REVIEW.md` | Sprint 1 backend skeleton review. | Historical label added. | P3 | Historical reference; CI note now points to PR #1 run #54. |
| `docs/SPRINT_2_REVIEW.md` | Sprint 2 SQL/data-layer review. | Historical label added. | P3 | Historical reference; validation count and status still need reconfirmation before planning. |
| `docs/FIX_LOG.md` | Summary of Sprint 1 and Sprint 2 fixes. | Historical label added. | P3 | Historical reference; recorded `10 passed` is not current validation. |
| `docs/TASKS.md` | Backlog and phase/task status. | Historical/backlog label added. | P1 | Do not execute tasks from it without checking current state first. |
| `docs/GITHUB_ISSUES_TO_CREATE.md` | Issue backlog candidates. | Historical/backlog label added. | P2 | CI note added; still needs backlog reconciliation. |
| `docs/STACK.md` | Tooling stack and deferred work. | Useful, partly stale. | P2 | Mentions `uv`; Makefile uses pip. Validate before relying on tool choice. |
| `docs/TOOLING_NOTES.md` | Tooling rationale and known limitation. | Historical label added. | P3 | CI note added; current tooling truth remains Makefile, validation docs, and workflow. |
| `docs/AUTOMATION_NOTE.md` | Short note to add automated backend checks. | Historical label added. | P3 | CI note added; retained for traceability only. |
| `docs/REFERENCES.md` | Sources considered for tooling decisions. | Useful but thin. | P3 | Lists reference categories without links or versions. |
| `docs/NOTE.md` | Minimal focus reminder. | Redundant. | P3 | Covered by README, product spec, drift control, and AGENTS. |
| `.github/workflows/backend-ci.yml` | Backend CI workflow. | Current, operational. | P1 | Runs install, format, lint, and tests on Python 3.12. |
| `.github/ISSUE_TEMPLATE/task.md` | Task issue template. | Current, useful. | P1 | Aligns task intake with validation/manual-work requirements. |
| `.github/ISSUE_TEMPLATE/bug.md` | Bug issue template. | Current, useful. | P1 | Captures logs, reproduction, constraints, and validation commands. |
| `backend/Makefile` | Backend validation command interface. | Current, operational. | P1 | Local `python` and `ruff` availability still depend on environment. |
| `backend/ruff.toml` | Ruff format/lint settings. | Current, operational. | P1 | Defines Python 3.12 target and selected lint families. |

## Agent-Critical Docs

### `AGENTS.md`

- Why it matters: It is the main control surface for AI-agent behavior.
- When to read it: First in every Codex or AI-agent session.
- What decision it controls: Scope boundaries, hard constraints, validation expectations, and final report format.

### `docs/CONTEXT_INDEX.md`

- Why it matters: It tells agents which project, architecture, data, test, CI, and review files to read for a task.
- When to read it: Immediately after `AGENTS.md`, before planning edits.
- What decision it controls: Which context is mandatory for the task area.

### `docs/WORKFLOW.md`

- Why it matters: It defines planning, implementation, validation, failure, and reporting modes.
- When to read it: Before any task that may edit files or make validation claims.
- What decision it controls: Whether to proceed with feature work or stop for validation repair.

### `docs/DONE_CRITERIA.md`

- Why it matters: It prevents agents from marking tasks done when tests, lint, docs, risks, or manual work are incomplete.
- When to read it: During planning and before final reporting.
- What decision it controls: Task completion status.

### `docs/VALIDATION_COMMANDS.md`

- Why it matters: It records exact backend and docs validation commands.
- When to read it: Before validation or when deciding whether a local check is sufficient.
- What decision it controls: Which commands must be run before completion.

### `docs/MANUAL_ACTIONS.md`

- Why it matters: It records current manual gates, including CI/manual test verification.
- When to read it: Before final reporting and before claiming the repo is merge-ready.
- What decision it controls: What must be done outside the current environment.

### `docs/CHANGELOG_AGENT.md`

- Why it matters: It records latest known branch, PR, CI state, and next blockers.
- When to read it: Early in every session, after the static operating rules.
- What decision it controls: Whether current validation state is known, pending, or blocked.

### `docs/DECISIONS.md`

- Why it matters: It captures architectural decisions that constrain implementation.
- When to read it: Before any feature, integration, persistence, outreach, scoring, audit, or CI work.
- What decision it controls: Whether a proposed change violates standalone, deterministic-first, no-sending, or CI-blocking rules.

### `docs/RISK_REGISTER.md`

- Why it matters: It lists known product and workflow risks.
- When to read it: Before network, scoring, outreach, persistence, reporting, or agent-workflow changes.
- What decision it controls: What mitigation or manual warning must accompany work.

## Product Docs

- `README.md` gives the top-level LeadOS identity and deferred areas.
- `docs/PRODUCT_SPEC.md` is the best product source of truth for target user, product thesis, MVP modules, and non-goals.
- `docs/MVP_SCOPE.md` is the best scope source of truth for what is in and out of the MVP.
- `docs/DRIFT_CONTROL.md` is a concise product-drift checklist.
- `docs/ENGINEERING_RULES.md` connects product focus to engineering constraints.
- `docs/EXPERT_COUNCIL.md` defines role-based review perspectives and task design expectations.
- `docs/AUDIT_RUBRIC.md`, `docs/SCORING_RUBRIC.md`, `docs/OUTREACH_RUBRIC.md`, and `docs/EVALUATION_RUBRIC.md` define domain-specific behavior expectations.
- `docs/STACK.md` defines intended stack, but should be checked against `backend/Makefile`, `requirements.txt`, and CI because it mentions `uv` while current commands use pip.
- `docs/REFERENCES.md` records reference categories for tooling choices but lacks exact links or versions.

## Engineering Docs

- `docs/ARCHITECTURE.md` defines independent service loops and dependency rules.
- `docs/DATA_MODEL.md` defines table shapes and database strategy, but should be reviewed against current ORM models before schema work.
- `docs/DATA_TRANSFORMATION_PLAN.md` documents CSV normalization, validation, dedupe, and future reporting queries.
- `docs/DECISIONS.md` is the ADR layer and should control architecture-sensitive changes.
- `docs/DONE_CRITERIA.md`, `docs/VALIDATION_COMMANDS.md`, and `docs/WORKFLOW.md` are the core engineering workflow docs.
- `docs/RISK_REGISTER.md` is the main engineering/product risk tracker.
- `docs/FILE_OWNERSHIP.md` maps directories to responsibilities.
- `.github/workflows/backend-ci.yml`, `backend/Makefile`, and `backend/ruff.toml` are operational validation files and should be treated as source of truth for CI behavior.

## Sprint / Task Docs

- `docs/TASKS.md` is the backlog, but its statuses appear stale and should not be used blindly for planning.
- `docs/FIX_LOG.md` summarizes Sprint 1 and Sprint 2 fixes, but the recorded `10 passed` validation result is historical.
- `docs/SPRINT_1_REVIEW.md` and `docs/SPRINT_2_REVIEW.md` are useful history, but both include validation and remaining-work statements that need reconfirmation.
- `docs/API_REVIEW_001.md`, `docs/SCORING_REVIEW_001.md`, and `docs/SECURITY_REVIEW_001.md` are focused review artifacts and remain useful for their domains.
- `docs/COUNCIL_REVIEW_001.md` is historical and partly stale because CI now exists.
- `docs/GITHUB_ISSUES_TO_CREATE.md` contains useful issue seeds, but it still lists CI workflow work that appears completed.
- `docs/AUTOMATION_NOTE.md` and `docs/TOOLING_NOTES.md` are older workflow notes and are now partly superseded by the CI workflow and validation docs.

## Potential Duplicates or Overlaps

- `AGENTS.md`, `docs/WORKFLOW.md`, `docs/DONE_CRITERIA.md`, `docs/VALIDATION_COMMANDS.md`, and `docs/ENGINEERING_RULES.md` overlap on agent workflow and validation. Keep them separate for now: `AGENTS.md` is the entrypoint, while the docs files provide deeper operating detail.
- `README.md`, `docs/PRODUCT_SPEC.md`, `docs/MVP_SCOPE.md`, and `docs/DRIFT_CONTROL.md` overlap on project identity and deferred work. Keep them separate, but make `PRODUCT_SPEC` and `MVP_SCOPE` the canonical product/scope pair.
- `docs/ENGINEERING_RULES.md`, `docs/EXPERT_COUNCIL.md`, and `docs/WORKFLOW.md` overlap on task planning. Keep `EXPERT_COUNCIL` for complex design review and use `WORKFLOW` for routine execution.
- `docs/FIX_LOG.md`, `docs/SPRINT_1_REVIEW.md`, `docs/SPRINT_2_REVIEW.md`, and `docs/CHANGELOG_AGENT.md` overlap on state. Keep sprint/fix docs as historical records; use `CHANGELOG_AGENT.md` for current agent state.
- `docs/STACK.md`, `docs/TOOLING_NOTES.md`, `docs/VALIDATION_COMMANDS.md`, `backend/Makefile`, and `.github/workflows/backend-ci.yml` overlap on tooling. Treat Makefile and CI workflow as operational truth, with validation docs as the human-readable guide.
- `docs/AUDIT_RUBRIC.md`, `docs/SECURITY_REVIEW_001.md`, and `docs/RISK_REGISTER.md` overlap on audit/network safety. Keep all three: rubric defines behavior, security review defines controls, risk register tracks unresolved risk.

## Stale or Risky Docs

- `docs/TASKS.md`: Several task statuses look stale relative to implemented backend code and CI. Risk: agents may rebuild completed work or ignore current blockers.
- `docs/GITHUB_ISSUES_TO_CREATE.md`: Lists "Add CI workflow" as remaining even though `.github/workflows/backend-ci.yml` exists. Risk: duplicate or unnecessary CI work.
- `docs/TOOLING_NOTES.md`: Says workflow file creation was not completed. Risk: agents may assume CI is absent.
- `docs/AUTOMATION_NOTE.md`: Says automated backend checks should be added. Risk: agents may duplicate existing CI instead of verifying it.
- `docs/FIX_LOG.md`: States `10 passed` without date/environment. Risk: agents may treat historical local validation as current.
- `docs/SPRINT_1_REVIEW.md` and `docs/SPRINT_2_REVIEW.md`: Historical validation and remaining-work notes may be outdated. Risk: stale completion assumptions.
- `docs/COUNCIL_REVIEW_001.md`: Says next task is adding automated backend checks. Risk: conflicts with current CI state.
- `docs/STACK.md`: Mentions `uv` as stack while current backend Makefile uses pip. Risk: toolchain confusion.
- `docs/REFERENCES.md`: Does not include exact links, dates, or versions. Risk: weak provenance for tooling decisions.
- `docs/DATA_MODEL.md`: May lag behind ORM implementation details. Risk: schema drift if used without checking models.

## Missing Docs

- `docs/DOCS_INVENTORY.md`: Added by this audit.
- `docs/API_CONTRACT.md`: A canonical endpoint contract is missing; `docs/API_REVIEW_001.md` is only a focused review.
- `docs/LOCAL_ENVIRONMENT.md`: Added as the local Python 3.12, dependency install, Ruff, pytest, and validation setup guide.
- `docs/CI_TROUBLESHOOTING.md`: Missing a focused guide for format/lint/test failures and GitHub Actions inspection.
- `docs/MIGRATIONS_PLAN.md`: Missing migration strategy for moving beyond local SQLite.
- `docs/REPORTING_PLAN.md`: Missing canonical plan for SQL extraction/reporting work listed as a blocker.
- `docs/SCORING_PERSISTENCE_PLAN.md`: Missing plan for score persistence and versioning.
- `docs/PR_CHECKLIST.md` or `.github/pull_request_template.md`: Missing PR-level checklist for validation, manual work, and scope boundaries.
- `docs/DOCS_MAINTENANCE.md`: Missing ownership and update rules for keeping docs current.

## Recommended Reading Order for Future Codex Sessions

1. `AGENTS.md`
2. `docs/CONTEXT_INDEX.md`
3. `docs/ACTIVE_TASKS.md`
4. `docs/CHANGELOG_AGENT.md`
5. `docs/MANUAL_ACTIONS.md`
6. `docs/WORKFLOW.md`
7. `docs/DONE_CRITERIA.md`
8. Assigned issue/task
9. `docs/DECISIONS.md`
10. Relevant product/scope docs: `README.md`, `docs/PRODUCT_SPEC.md`, `docs/MVP_SCOPE.md`
11. Relevant domain docs: audit, scoring, outreach, evaluation, data, architecture, or security docs as applicable
12. Relevant source files and tests
13. `docs/RISK_REGISTER.md` before final planning for risky areas
14. `docs/VALIDATION_COMMANDS.md` before running checks

## Manual Work Required

### Required now

- None unless a newer commit invalidates the verified CI state.
- Update stale validation/state docs before using them as planning sources.

### Required before merge

- GitHub Actions Backend CI must be green for the latest PR head commit. As of PR #1 commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`, Backend CI passed in run #60 / `27554650321`.
- Reconcile `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, `docs/TOOLING_NOTES.md`, and `docs/AUTOMATION_NOTE.md` with the current CI and implementation state.

### Can be deferred

- Create dedicated local environment, CI troubleshooting, migration, reporting, scoring persistence, API contract, PR checklist, and docs maintenance docs.
- Merge or archive redundant historical notes after the current PR is stable.

## Recommendations Before Next Implementation Task

1. Add `docs/CI_TROUBLESHOOTING.md`.
2. Update stale task and tooling docs so agents do not plan from outdated state.
3. Treat `AGENTS.md`, `docs/CONTEXT_INDEX.md`, `docs/ACTIVE_TASKS.md`, `docs/WORKFLOW.md`, `docs/DONE_CRITERIA.md`, `docs/VALIDATION_COMMANDS.md`, `docs/MANUAL_ACTIONS.md`, and `docs/CHANGELOG_AGENT.md` as the agent operating layer.
4. Before feature work, choose one assigned task and read only the relevant domain docs plus affected source files.
