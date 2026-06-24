# Active Tasks

## Status

This is the canonical active task index for current LeadOS work.

Historical files such as `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, `docs/FIX_LOG.md`, `docs/SPRINT_1_REVIEW.md`, and `docs/SPRINT_2_REVIEW.md` are references only. Do not execute tasks from those files without checking this file first.

## Current Validation State

- PR: #1
- Branch: phase-0-product-foundation
- Latest verified CI: User-provided task handoff records Backend CI passed at
  commit `7012d052e37e12b458420e38e03f80e011faf1b2` in run #108.
- Local validation caveat: local tests may fail to run on machines without Python 3.12 and backend dependencies; GitHub Actions is current PR validation source of truth.
- Latest local HEAD before TASK-PHASE0-CLOSEOUT edits:
  `7012d052e37e12b458420e38e03f80e011faf1b2`.
- Current-head CI status: Current local HEAD matched the user-provided latest
  verified CI commit and GitHub PR head before closeout edits. Any pushed
  closeout commit must receive fresh Backend CI verification.

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
| TASK-0206 | Add SQL extraction/reporting foundation | Backend implementation | Complete | GitHub issue #24 | Backend CI verified at commit `1cb9f66a1437ee1fa442cea340aeaf59626559af`. |
| TASK-0208 | Add BI export dataset layer | Backend implementation | Complete | User-assigned Day 7 task | Backend CI verified at commit `9b7fce3c03a1644cbbf79264d96901f2a10962ec`. |
| TASK-0701 | Add Power BI dashboard specification and sample export fixtures | Documentation/test fixtures | Complete | User-assigned Day 8 task | Backend CI verified at commit `ca7df13b1d46fcc58a841e8a2ed69d34b7cb00d0`. Adds a manual Power BI dashboard specification, deterministic BI export CSV fixtures, and tests without `.pbix`, Power BI automation, frontend, API route, external storage, pandas, dependencies, AI analytics, integrations, or outbound sending. |
| TASK-0702 | Add Tableau dashboard specification using BI export fixtures | Documentation/test fixtures | Complete | User-assigned Day 9 task | User-provided task handoff records Backend CI verified at commit `362fd8018dce531fe8fdd0d8b8fb8f40d28a4b0b` in run #100. Adds a manual Tableau dashboard specification and documentation tests without Tableau workbook binaries or new dependencies. |
| TASK-0502 | Add outreach draft foundation | Backend implementation | Complete | User-assigned Day 10 task | Backend CI verified at commit `e96bc4cdb5bd32f75de9c138d20c52af2bc4041f` in run #102. Adds deterministic email and WhatsApp drafts with mandatory human review and no sending or external services. |
| TASK-0602 | Build deterministic outreach evaluator template | Backend implementation | Complete | User-assigned Day 11 task | Backend CI verified at commit `4bfb6300bc68c7babc750f74d9142690225454f9` in run #104. Evaluates structured outreach drafts without sending, rewriting, persistence, routes, LLM integration, or new dependencies. |
| TASK-0603 | Create expert outreach review checklist | Documentation/documentation test | Complete | User-assigned task | Backend CI verified at commit `0fd9c69581865a864bf6a657f683bd5083b39888` in run #106. Adds a mandatory manual decision gate after deterministic evaluation and before human sending. |
| TASK-0503 | Generate the first validated sample outreach set | Sample data/test/documentation | Complete | User-assigned task | Backend CI verified at commit `7012d052e37e12b458420e38e03f80e011faf1b2` in run #108. Adds six deterministic fictional cases covering both channels and approve, revise, and reject decisions. |
| TASK-PHASE0-CLOSEOUT | Verify Phase 0 completion and prepare PR #1 for merge | Documentation/validation/state reconciliation | In progress | User-assigned task | Creates an evidence-based completion report, reconciles PR/task state, updates the PR description, and preserves deferred scope. No product feature or automatic merge. |

## Blocked / Waiting

| ID | Task | Blocker | Required Action | Notes |
|---|---|---|---|---|
| WAIT-0001 | Full local backend test validation | Local Python 3.12 / pytest environment not fully provisioned | Use GitHub Actions as PR validation source or provision local Python 3.12 dependencies | Do not claim local tests pass unless they are actually run. |
| WAIT-0012 | Phase 0 closeout commit, push, fresh CI, and final PR review | Closeout documents are newer than the verified baseline until committed, pushed, checked, and reviewed | After user authorization, commit and push closeout changes, verify fresh Backend CI, then perform final human PR review | Do not mark Phase 0 complete or merge PR #1 until these actions pass. |

## Next Up

No next implementation task should start until WAIT-0012 is cleared.

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
