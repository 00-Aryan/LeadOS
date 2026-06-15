# Active Tasks

## Status

This is the canonical active task index for current LeadOS work.

Historical files such as `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, `docs/FIX_LOG.md`, `docs/SPRINT_1_REVIEW.md`, and `docs/SPRINT_2_REVIEW.md` are references only. Do not execute tasks from those files without checking this file first.

## Current Validation State

- PR: #1
- Branch: phase-0-product-foundation
- Latest verified CI: Backend CI passed at commit `ed6050567c33c50557b994ca263e82a555fe4dd8`, run #69 / 27565986172
- Local validation caveat: local tests may fail to run on machines without Python 3.12 and backend dependencies; GitHub Actions is current PR validation source of truth.
- Latest local HEAD: `ed6050567c33c50557b994ca263e82a555fe4dd8`
- Current-head CI status: Current local HEAD matches the latest verified CI commit. TASK-0203 worktree changes are not yet verified by CI.

## Current Operating Rule

No feature work should begin unless the latest PR head has passing Backend CI or the task is explicitly limited to docs/cleanup.

## Active Now

| ID | Task | Type | Status | Source | Notes |
|---|---|---|---|---|---|
| TASK-0006 | Create canonical active task index | Documentation/workflow | Complete pending review | User-assigned task | Created this file and updated allowed operating docs only. |
| TASK-0006A | Reconcile active task index after TASK-0006 push | Documentation/state reconciliation | Complete | User-assigned task | Later superseded by verified PR #1 Backend CI run #67 at commit `8e5f2a5c1a48884c110ccf8ed53027d72f183416`. |
| TASK-0007 | Add local environment setup doc | Documentation/workflow | Complete pending review | User-assigned task | Created `docs/LOCAL_ENVIRONMENT.md` and updated allowed operating docs only. |
| TASK-0008 | Add CI troubleshooting doc | Documentation/workflow | Complete pending review | User-assigned task | Created `docs/CI_TROUBLESHOOTING.md`; Backend CI later verified at commit `8e5f2a5c1a48884c110ccf8ed53027d72f183416`. |
| TASK-0009 | Add PR checklist | Documentation/workflow | Complete pending review | User-assigned task | Created `docs/PR_CHECKLIST.md`; Backend CI later verified at commit `8e5f2a5c1a48884c110ccf8ed53027d72f183416`. |
| TASK-0010 | Reconcile active implementation backlog against GitHub issues | Documentation/workflow | Complete pending review and manual GitHub issue verification | User-assigned task | Created `docs/BACKLOG_RECONCILIATION.md`; GitHub CLI could not inspect issue state from this environment. |
| TASK-0203 | Build CSV lead import validator | Backend implementation | Implemented pending validation | GitHub issue #2 | Added deterministic CSV import validation, structured result, multipart upload route, and tests. Local validation is blocked because `ruff` is missing and Python 3.12 is not installed. |

## Blocked / Waiting

| ID | Task | Blocker | Required Action | Notes |
|---|---|---|---|---|
| WAIT-0001 | Full local backend test validation | Local Python 3.12 / pytest environment not fully provisioned | Use GitHub Actions as PR validation source or provision local Python 3.12 dependencies | Do not claim local tests pass unless they are actually run. |
| WAIT-0003 | TASK-0203 local validation | `ruff` is not installed and pyenv Python 3.12 is missing locally | Provision local backend tooling or verify Backend CI after push | `git diff --check` and Python 3.11 syntax compile passed; format, lint, and tests did not run to completion. |

## Next Up

| ID | Task | Type | Why Next | Acceptance Criteria |
|---|---|---|---|---|
| TASK-0203-VALIDATE | Validate TASK-0203 implementation | Backend validation | TASK-0203 code and tests are implemented, but local format/lint/test commands are blocked by missing tooling. | `make format-check`, `make lint`, and `make test` pass locally or latest pushed head Backend CI is verified green. |

## Deferred

| ID | Task | Reason Deferred | Resume When |
|---|---|---|---|
| DEF-0001 | Alembic migrations | Requires dedicated database migration planning. | Local/CI validation and data model reconciliation are complete. |
| DEF-0002 | SQL reporting service | Reporting scope should follow task/backlog reconciliation. | Active implementation backlog is reconciled. |
| DEF-0003 | Scoring persistence repository | Needs persistence/versioning plan and migration strategy. | Scoring persistence plan and migrations are defined. |
| DEF-0004 | Audit persistence repository | Needs persistence plan and migration strategy. | Audit persistence plan and migrations are defined. |
| DEF-0005 | Sprint 3 implementation | Documentation cleanup and active task reconciliation are not complete. | Active task index and implementation backlog are current. |
| DEF-0006 | Deployment | Out of MVP cleanup scope. | Production readiness planning begins. |
| DEF-0007 | Auth | Deferred by product scope. | Product scope explicitly prioritizes auth. |
| DEF-0008 | Billing | Deferred by product scope. | Product scope explicitly prioritizes billing. |
| DEF-0009 | Outbound sending | Deferred by safety/product constraints. | Explicitly assigned and guarded by evaluation/manual review policy. |
| DEF-0010 | CRM integration | Deferred integration. | Explicitly assigned after core loop stabilizes. |
| DEF-0011 | ProjectOS integration | Deferred integration. | Explicitly assigned after standalone boundaries are preserved. |
| DEF-0012 | Content Creation Automation integration | Deferred integration. | Explicitly assigned after standalone boundaries are preserved. |

## Do Not Start Yet

- Scraping/crawling
- Automatic outbound sending
- CRM sync
- AI-powered audit inference
- ProjectOS integration
- Content Creation Automation integration
- Deployment/billing/auth
- New product features before active task reconciliation

## How To Update This File

Future agents should update this file when:

- A task starts, completes, becomes blocked, or is deferred.
- A new PR head commit changes the verified CI state.
- Manual work becomes required or is resolved.
- Historical backlog items are promoted into active work.
- GitHub issues become the source for a task.

Keep this file concise. Do not copy historical backlog content here unless it is being promoted into current active work.
