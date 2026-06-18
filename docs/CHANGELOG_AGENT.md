# Agent Changelog

## Latest Agent State

- Current branch: `phase-0-product-foundation`
- Current PR: `#1`
- Latest known CI state: Backend CI passed on PR #1 at commit `244b050ed6fdd29cc00c0d597ec2de746ddd3091`.
- Sprint 1 status: complete for TASK-0105 gate.
- Sprint 2 status: complete for TASK-0105 gate; migrations/reporting remain deferred.
- Next blockers: TASK-0304 local validation tooling, fresh Backend CI after the TASK-0304 push, migrations, scoring persistence, SQL reporting
- Local backend tests may still fail to run on machines without Python 3.12/dependencies, but GitHub Actions is the current source of truth for PR validation.

Do not claim CI passes unless the relevant GitHub Actions run has been verified.

## TASK-0005 Documentation Safety Labels

Added historical/status labels to highest-risk stale docs so future agents do not treat old backlog, tooling, sprint, or fix-log notes as current instructions.

## TASK-0006 Canonical Active Task Index

Created `docs/ACTIVE_TASKS.md` as the canonical active task source. Historical backlog, sprint review, and fix-log docs remain references only.

## TASK-0006A CI State Reconciliation Attempt

GitHub Actions could not be inspected from this environment after the TASK-0006 push. This was later superseded by verified Backend CI run #60 at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`.

## TASK-0007 Local Environment Setup

Added local environment setup guidance so humans and agents can reproduce backend validation more reliably. Latest verified Backend CI is PR #1 run #60 at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`.

## TASK-0008 CI Troubleshooting

Added CI troubleshooting guidance so future agents diagnose GitHub Actions failures by failing step and avoid unrelated changes.

## TASK-0009 PR Checklist

Added PR checklist guidance for merge readiness, docs-only commits, backend changes, dependency/tooling changes, and agent safety rules.

## TASK-0010 Backlog Reconciliation

Added backlog reconciliation guidance to identify the next safe implementation task after Phase 0 hardening and PR-readiness controls.

## TASK-0203 CSV Lead Import Validator

Implemented deterministic CSV lead import validation with explicit schema, row-level invalid reasons, partial import support, API route, and tests. Local backend validation is pending because `ruff` is not installed and pyenv Python 3.12 is missing in this environment.

## TASK-0105 Sprint 1 and Sprint 2 Completion Gate

Created `docs/SPRINT_1_2_COMPLETION_GATE.md` to map each Sprint 1 and Sprint 2 acceptance check to concrete backend tests and validation commands. Local backend validation is blocked by missing `ruff` and missing pyenv Python `3.12`; GitHub issue verification is blocked by lack of `api.github.com` connectivity; `git diff --check` passed. Sprint 3 remains deferred until the gate passes in a provisioned environment or Backend CI is re-verified after the TASK-0105 changes are pushed.

## TASK-0303 Deterministic Audit Checks

Implemented deterministic provided-HTML audit checks for title, meta description, phone link, WhatsApp link, booking signal, contact signal, social link, schema markup, and HTTPS. The new check surface uses `true`, `false`, and `unknown` statuses with concise evidence. Local `make format-check` and `make lint` are blocked because `ruff` is not installed; local `make test` is blocked because pyenv Python `3.12` is not installed. `git diff --check` passed, and fresh Backend CI is required after push.

## TASK-0304 Audit Persistence Repository

Added an audit repository for persisting deterministic audit results linked to existing leads. The repository stores `lead_id`, `requested_url`, `fetch_status`, and JSON-serializable audit output, and supports listing by lead plus latest-audit lookup without committing transactions, fetching websites, scoring, or adding migrations.
