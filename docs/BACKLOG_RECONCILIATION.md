# Backlog Reconciliation

## Purpose

This document reconciles historical backlog docs, current active task docs, PR state, and GitHub issue state into one implementation sequence. Future humans and AI agents should use it to choose the next implementation task without treating stale sprint notes or draft issue lists as current instructions.

## Current Verified State

- PR: #1
- Branch: `phase-0-product-foundation`
- Latest verified head commit: `8e5f2a5c1a48884c110ccf8ed53027d72f183416`
- Latest verified CI run: Backend CI success, run #67 / `27564758959`
- Current sprint/task position: Phase 0 hardening and PR-readiness controls are complete through TASK-0009; TASK-0010 is the backlog reconciliation gate before product implementation work.
- Whether GitHub issues were inspected: No. GitHub CLI could not connect to `api.github.com`, so issue state was not accessible from this environment.

## Source Priority

Future agents must use this source priority:

1. `docs/ACTIVE_TASKS.md`
2. GitHub issues, if accessible and current
3. Current PR body and checks
4. Product scope docs: `docs/MVP_SCOPE.md`, `docs/PRODUCT_SPEC.md`, `docs/ARCHITECTURE.md`
5. Historical backlog docs as references only

## Historical Sources Reviewed

| Source | Role | Useful For | Risk | Current Use |
|---|---|---|---|---|
| `docs/TASKS.md` | Historical phase backlog | Original phase IDs and MVP sequence | Statuses are stale relative to implemented SQL import, audit, scoring, CI, and docs work | Reference for candidate task IDs only |
| `docs/GITHUB_ISSUES_TO_CREATE.md` | Historical draft issue list | Deferred migrations/reporting and earlier fixed issue summaries | Still lists CI workflow as remaining even though Backend CI exists | Reference for deferred items only |
| `docs/FIX_LOG.md` | Historical fix summary | Sprint 1 and Sprint 2 implementation context | Historical local `10 passed` result can be mistaken for current validation | Reference only |
| `docs/SPRINT_1_REVIEW.md` | Historical Sprint 1 review | Backend skeleton and early lead import context | Mentions old CI state and early remaining work | Reference only |
| `docs/SPRINT_2_REVIEW.md` | Historical Sprint 2 review | SQL data layer, transformation, import run, duplicate, and rejected-row context | Historical validation and remaining work may not reflect current head | Reference only |
| `docs/DATA_TRANSFORMATION_PLAN.md` | Current data transformation guide | CSV normalization, validation, dedupe, import quality tracking, and future reporting ideas | Should be checked against source before implementation | Current planning input for TASK-0203 |
| PR body note provided in TASK-0010 | Current PR planning hint | Names `TASK-0203` as the next product task | Could be stale if GitHub issues disagree; issues were inaccessible | Supports TASK-0203 pending manual issue verification |

## GitHub Issue Reconciliation

```text
GitHub issues were not accessible from this environment. This reconciliation is based on repository documentation and PR state only.
```

## Candidate Implementation Tasks

| Candidate ID | Task | Source | Relevance | Risk | Recommendation |
| ------------ | ---- | ------ | --------- | ---- | -------------- |
| TASK-0203 | CSV lead import validator with clear invalid-row reporting and import summary | PR body note, `docs/TASKS.md`, `docs/DATA_TRANSFORMATION_PLAN.md`, MVP workflow | Highest; CSV import and validation are the first MVP loop dependency | Existing import code may already cover part of the task, so implementation must inspect source/tests before editing | Start next after manual GitHub issue verification |
| TASK-0303 | Deterministic website audit checks | `docs/TASKS.md`, `docs/MVP_SCOPE.md`, `docs/ARCHITECTURE.md` | Next after reliable imported lead data exists | Must not add scraping/crawling or AI inference | Defer until TASK-0203 is complete |
| TASK-0402 / TASK-0403 | Explainable scoring function and scoring test cases | `docs/TASKS.md`, `docs/PRODUCT_SPEC.md`, `docs/MVP_SCOPE.md` | Depends on lead and audit outputs | Historical docs may understate existing scoring code; inspect source before implementation | Defer until audit data path is stable |
| TASK-0502 / TASK-0503 | Outreach draft generation and sample outreach set | `docs/TASKS.md`, `docs/PRODUCT_SPEC.md` | Later MVP loop step | Must remain draft-only with no sending and no unsupported claims | Defer until scoring output is stable |
| TASK-0602 / TASK-0603 | Evaluator template and expert review checklist | `docs/TASKS.md`, `docs/PRODUCT_SPEC.md` | Required final safety loop | Should evaluate drafts, not send or automate outreach | Defer until outreach draft structure exists |
| DEF-0001 | Migrations | `docs/ACTIVE_TASKS.md`, `docs/DATA_MODEL.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, Sprint 2 review | Important before production persistence hardening | Can distract from MVP loop if started early | Defer unless directly required by next task |
| DEF-0002 | Reporting service | `docs/ACTIVE_TASKS.md`, `docs/DATA_TRANSFORMATION_PLAN.md`, `docs/GITHUB_ISSUES_TO_CREATE.md` | Useful for analytics after import quality stabilizes | Not required for first implementation task | Defer unless directly required by next task |
| DEF-0003 / DEF-0004 | Scoring and audit persistence | `docs/ACTIVE_TASKS.md`, `docs/DATA_MODEL.md` | Needed for durable later workflows | Requires persistence/versioning decisions | Defer until audit/scoring implementation scope is explicit |
| Deferred integrations | Deployment, authentication, billing, outbound sending, CRM integration, ProjectOS integration, Content Creation Automation integration | `docs/ACTIVE_TASKS.md`, `README.md`, `docs/MVP_SCOPE.md`, `docs/PRODUCT_SPEC.md` | Not part of MVP implementation sequence | Violates current scope if started casually | Do not start |

## Recommended Active Implementation Sequence

| Order | Task ID | Task | Why This Order | Acceptance Criteria | Allowed Scope |
| ----: | ------- | ---- | -------------- | ------------------- | ------------- |
| 1 | TASK-0203 | CSV lead import validator with clear invalid-row reporting and import summary | The MVP starts with CSV import, and every later audit/scoring/outreach step depends on trusted lead rows and import quality reporting | Source/tests are inspected first; invalid rows return clear reasons; import summary reports total, valid, invalid, and duplicate rows; behavior is covered by focused backend tests; Backend CI passes for latest PR head | Backend import validation, schemas, services, repositories, and tests directly required for CSV import quality |
| 2 | TASK-0303 | Deterministic website audit checks | Audit is the next MVP step after valid leads exist | Deterministic checks return true, false, or unknown; no scraping/crawling is added; tests cover missing and malformed inputs | Audit service and tests only |
| 3 | TASK-0402 / TASK-0403 | Explainable scoring function and scoring test cases | Scoring depends on lead facts and audit outputs | Score is reproducible and explainable; tests cover expected signals, missing data, and risk flags | Scoring service, schemas, API/tests directly related to scoring |
| 4 | TASK-0502 | Outreach draft generation | Drafts depend on scored lead context | Drafts use only known facts, avoid unsupported claims, and do not send messages | Draft generation service/templates/tests only |
| 5 | TASK-0602 | Evaluator template | Evaluation is the final review gate before human use | Evaluation flags truthfulness, clarity, personalization, and risk issues | Evaluator service/templates/tests only |

## Deferred / Do Not Start Yet

```text
Scraping/crawling
automatic outbound sending
CRM sync/integration
ProjectOS integration
Content Creation Automation integration
AI-powered audit inference
deployment
authentication
billing
migrations unless directly required by next task
reporting service unless directly required by next task
```

## Risks and Ambiguities

- Historical backlog docs contain stale statuses and should not be used as active instructions.
- GitHub issues were not accessible from this environment, so issue state must be manually verified before implementation starts.
- The PR body points to TASK-0203, and local docs support that order, but live GitHub issues could still contain newer prioritization.
- CSV import quality is a prerequisite for later audit, scoring, outreach, and evaluator work.
- Validation risk remains if local Python 3.12 and backend dependencies are not provisioned; agents must not claim local backend tests passed unless they actually ran.
- If a commit newer than `8e5f2a5c1a48884c110ccf8ed53027d72f183416` is pushed, Backend CI must be re-verified before implementation proceeds.

## Decision

```text
The next implementation task is: TASK-0203: CSV lead import validator with clear invalid-row reporting and import summary
```

## Manual Work Required

### Required now

None, unless a newer commit is pushed and CI has not completed.

### Required before implementation

- Manually verify current GitHub issues and PR body because GitHub CLI could not connect from this environment.
- Confirm that TASK-0203 is still the intended next product task after checking GitHub issue state.
- Verify Backend CI remains green for the latest PR head if any newer commit is pushed.

### Can be deferred

- GitHub-native PR template creation.
- Local environment provisioning beyond current docs.
- Migrations, reporting service, scoring persistence, audit persistence, deployment, authentication, billing, outbound sending, CRM integration, ProjectOS integration, and Content Creation Automation integration.

## How Future Agents Should Use This File

Check this file before historical backlog docs. Update it after every backlog-affecting task, including task completion, GitHub issue reconciliation, PR body changes, or scope changes. Do not start deferred work unless it is explicitly promoted in `docs/ACTIVE_TASKS.md` and the assigned task allows it.
