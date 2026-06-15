# Active Tasks

## Status

This is the canonical active task index for current LeadOS work.

Historical files such as `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, `docs/FIX_LOG.md`, `docs/SPRINT_1_REVIEW.md`, and `docs/SPRINT_2_REVIEW.md` are references only. Do not execute tasks from those files without checking this file first.

## Current Validation State

- PR: #1
- Branch: phase-0-product-foundation
- Latest verified CI: Backend CI passed at commit `bd79762147ac0732bc5185cad50110ad9984be7e`, run #65 / 27563984088
- Local validation caveat: local tests may fail to run on machines without Python 3.12 and backend dependencies; GitHub Actions is current PR validation source of truth.
- Latest local HEAD: `bd79762147ac0732bc5185cad50110ad9984be7e`
- Current-head CI status: Current local HEAD matches the latest verified CI commit.

## Current Operating Rule

No feature work should begin unless the latest PR head has passing Backend CI or the task is explicitly limited to docs/cleanup.

## Active Now

| ID | Task | Type | Status | Source | Notes |
|---|---|---|---|---|---|
| TASK-0006 | Create canonical active task index | Documentation/workflow | Complete pending review | User-assigned task | Created this file and updated allowed operating docs only. |
| TASK-0006A | Reconcile active task index after TASK-0006 push | Documentation/state reconciliation | Complete | User-assigned task | Later superseded by verified PR #1 Backend CI run #65 at commit `bd79762147ac0732bc5185cad50110ad9984be7e`. |
| TASK-0007 | Add local environment setup doc | Documentation/workflow | Complete pending review | User-assigned task | Created `docs/LOCAL_ENVIRONMENT.md` and updated allowed operating docs only. |
| TASK-0008 | Add CI troubleshooting doc | Documentation/workflow | Complete pending review | User-assigned task | Created `docs/CI_TROUBLESHOOTING.md`; Backend CI later verified at commit `bd79762147ac0732bc5185cad50110ad9984be7e`. |
| TASK-0009 | Add PR checklist | Documentation/workflow | Complete pending review | User-assigned task | Created `docs/PR_CHECKLIST.md` and updated allowed operating docs only. |

## Blocked / Waiting

| ID | Task | Blocker | Required Action | Notes |
|---|---|---|---|---|
| WAIT-0001 | Full local backend test validation | Local Python 3.12 / pytest environment not fully provisioned | Use GitHub Actions as PR validation source or provision local Python 3.12 dependencies | Do not claim local tests pass unless they are actually run. |

## Next Up

| ID | Task | Type | Why Next | Acceptance Criteria |
|---|---|---|---|---|
| TASK-0010 | Reconcile active implementation backlog against GitHub issues | Documentation/workflow | Historical backlog files are labeled but not reconciled into an executable implementation queue. | Active implementation tasks are aligned with GitHub issues/current PR state; historical docs remain references only. |

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
