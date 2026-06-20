# Active Tasks

## Status

This is the canonical active task index for current LeadOS work.

Historical files such as `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, `docs/FIX_LOG.md`, `docs/SPRINT_1_REVIEW.md`, and `docs/SPRINT_2_REVIEW.md` are references only. Do not execute tasks from those files without checking this file first.

## Current Validation State

- PR: #1
- Branch: phase-0-product-foundation
- Latest verified CI: Backend CI passed at commit `6fd06479e370e21e3583b557536564ab1fce6bc4`
- Local validation caveat: local tests may fail to run on machines without Python 3.12 and backend dependencies; GitHub Actions is current PR validation source of truth.
- Latest local HEAD before TASK-0206 edits: `6fd06479e370e21e3583b557536564ab1fce6bc4`
- Current-head CI status: Current local HEAD matched the latest verified CI commit before TASK-0206 edits. Any pushed TASK-0206 commit must receive fresh Backend CI verification.

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
| TASK-0105 | Verify Sprint 1 and Sprint 2 completion gate | Documentation/QA gate | Complete pending review | GitHub issue #25 | Created Sprint 1 and Sprint 2 completion gate. Backend CI later verified at commit `daccb2cc9f75a268f2d394557a609435fa96bfba`. |
| TASK-0303 | Build deterministic audit checks | Backend implementation | Complete pending review | GitHub issue #4 | Adds provided-HTML audit checks with `true` / `false` / `unknown` status. Backend CI later verified at commit `244b050ed6fdd29cc00c0d597ec2de746ddd3091`. |
| TASK-0304 | Add audit persistence repository | Backend implementation | Complete pending review | GitHub issue #27 | Added repository methods for persisting and retrieving deterministic audit results. Backend CI later verified at commit `8ac976d30da41181328c64884835f6ac4461c81a`. |
| TASK-0402/TASK-0403 | Strengthen explainable scoring function and scoring test cases | Backend implementation | Complete | User-assigned task | Backend CI verified at commit `1db856783a2620fc963c12b79a1d5adba76dde88`. |
| TASK-0207 | Add scoring persistence repository | Backend implementation | Complete | GitHub issue #26 | Backend CI verified at commit `90a674aae2ad13a68d5aaf2f7e374ffbf66fd568`. |
| TASK-AGENTS-DEDUP | Deduplicate agent operating instructions | Documentation/repair | Complete | User-assigned task | AGENTS.md repair completed at commit `6fd06479e370e21e3583b557536564ab1fce6bc4`. |
| TASK-0206 | Add SQL extraction/reporting foundation | Backend implementation | In progress | GitHub issue #24 | Adds read-only SQL-backed reporting schemas, repository queries, and tests without dashboards, BI export, migrations, scoring rule changes, audit rule changes, or dependencies. |

## Blocked / Waiting

| ID | Task | Blocker | Required Action | Notes |
|---|---|---|---|---|
| WAIT-0001 | Full local backend test validation | Local Python 3.12 / pytest environment not fully provisioned | Use GitHub Actions as PR validation source or provision local Python 3.12 dependencies | Do not claim local tests pass unless they are actually run. |
| WAIT-0005 | Fresh CI after TASK-0206 push | TASK-0206 changes are newer than the verified baseline until pushed and checked | Verify Backend CI after any new pushed commit | Do not start BI export or dashboard preparation from unverified TASK-0206 code. |

## Next Up

| ID | Task | Type | Why Next | Acceptance Criteria |
|---|---|---|---|---|
| BI export or dashboard preparation | Reporting surface planning | Backend implementation | Only after TASK-0206 is committed, pushed, and Backend CI is green | Any surface should consume read-only report outputs | Do not start until TASK-0206 verification is complete. |

## Deferred

| ID | Task | Reason Deferred | Resume When |
|---|---|---|---|
| DEF-0001 | Alembic migrations | Requires dedicated database migration planning. | Local/CI validation and data model reconciliation are complete. |
| DEF-0002 | SQL reporting service | Reporting scope should follow task/backlog reconciliation. | Active implementation backlog is reconciled. |
| DEF-0003 | Scoring persistence migrations | Migrations are excluded from TASK-0207 scope. | A dedicated migration task is assigned. |
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
