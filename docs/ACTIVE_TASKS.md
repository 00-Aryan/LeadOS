# Active Tasks

## Status

This is the canonical active task index for current LeadOS work.

Historical files such as `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, `docs/FIX_LOG.md`, `docs/SPRINT_1_REVIEW.md`, and `docs/SPRINT_2_REVIEW.md` are references only. Do not execute tasks from those files without checking this file first.

## Current Validation State

- PR: #1
- Branch: phase-0-product-foundation
- Latest verified CI: Backend CI passed at commit `64f116cc77758de2e3e51792fe4b898cda2dd9e1`, run #76 / 27574177028
- Local validation caveat: local tests may fail to run on machines without Python 3.12 and backend dependencies; GitHub Actions is current PR validation source of truth.
- Latest local HEAD: `64f116cc77758de2e3e51792fe4b898cda2dd9e1`
- Current-head CI status: Current local HEAD matches the latest verified CI commit. The worktree has uncommitted changes, so any pushed commit must receive fresh Backend CI verification.

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
| TASK-0203 | Build CSV lead import validator | Backend implementation | Complete pending review | GitHub issue #2 | Added deterministic CSV import validation, structured result, multipart upload route, and tests. Backend CI later verified at commit `64f116cc77758de2e3e51792fe4b898cda2dd9e1`. |
| TASK-0105 | Verify Sprint 1 and Sprint 2 completion gate | Documentation/QA gate | In progress | GitHub issue #25 | Create final Sprint 1 and Sprint 2 completion gate before Sprint 3 starts. No product feature work. |

## Blocked / Waiting

| ID | Task | Blocker | Required Action | Notes |
|---|---|---|---|---|
| WAIT-0001 | Full local backend test validation | Local Python 3.12 / pytest environment not fully provisioned | Use GitHub Actions as PR validation source or provision local Python 3.12 dependencies | Do not claim local tests pass unless they are actually run. |
| WAIT-0004 | Fresh CI after next push | Local HEAD currently matches verified CI, but uncommitted changes exist | Verify Backend CI after any new pushed commit | Do not start Sprint 3 from unverified pushed code. |

## Next Up

| ID | Task | Type | Why Next | Acceptance Criteria |
|---|---|---|---|---|
| TASK-0105-COMPLETE | Complete Sprint 1 and Sprint 2 gate | Documentation/QA gate | Sprint 3 must not begin until this gate is documented and validation is green. | Sprint review docs and completion gate are updated; `cd backend && make check` and `git diff --check` pass or exact blockers are recorded. |

## Deferred

| ID | Task | Reason Deferred | Resume When |
|---|---|---|---|
| DEF-0001 | Alembic migrations | Requires dedicated database migration planning. | Local/CI validation and data model reconciliation are complete. |
| DEF-0002 | SQL reporting service | Reporting scope should follow task/backlog reconciliation. | Active implementation backlog is reconciled. |
| DEF-0003 | Scoring persistence repository | Needs persistence/versioning plan and migration strategy. | Scoring persistence plan and migrations are defined. |
| DEF-0004 | Audit persistence repository | Needs persistence plan and migration strategy. | Audit persistence plan and migrations are defined. |
| DEF-0005 | Sprint 3 implementation | TASK-0105 completion gate must pass first. | Sprint 1 and Sprint 2 gate is complete and latest Backend CI is verified green after any new push. |
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
- New product features before TASK-0105 completion gate passes

## How To Update This File

Future agents should update this file when:

- A task starts, completes, becomes blocked, or is deferred.
- A new PR head commit changes the verified CI state.
- Manual work becomes required or is resolved.
- Historical backlog items are promoted into active work.
- GitHub issues become the source for a task.

Keep this file concise. Do not copy historical backlog content here unless it is being promoted into current active work.
