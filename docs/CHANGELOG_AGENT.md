# Agent Changelog

## Latest Agent State

- Current branch: `phase-0-product-foundation`
- Current PR: `#1`
- Latest known CI state: user-provided task handoff records Backend CI passed on PR #1 at commit `362fd8018dce531fe8fdd0d8b8fb8f40d28a4b0b` in run #100; this environment could not re-query GitHub Actions.
- Sprint 1 status: complete for TASK-0105 gate.
- Sprint 2 status: complete for TASK-0105 gate; migrations/reporting remain deferred.
- Next blockers: TASK-0502 commit/push and fresh Backend CI, migrations, deferred evaluator implementation
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

## TASK-0402/TASK-0403 Explainable Scoring

Strengthened deterministic scoring so it normalizes both legacy audit check names and newer presence-audit keys before scoring digital gaps and contactability. Expanded scoring tests for strong and weak digital presence, missing/blocked/failed audits, contactability gaps, commercial category fit, category caps, priority transitions, reason summaries, and Pydantic serialization.

## TASK-0207 Scoring Persistence Repository

Added a dedicated score repository for persisting deterministic `LeadScore` results linked to existing leads. The repository stores scoring version, total score, category JSON, priority, confidence, reason summary, positive signals, risk flags, and missing data without committing transactions, running scoring, fetching audit data, reporting, adding dependencies, or adding migrations.

## TASK-AGENTS-DEDUP Agent Operating Instructions Repair

Deduplicated `AGENTS.md` into one clean operating instruction file while preserving repository state checks, scoped commit rules, hallucination prevention, local validation fallback, hard constraints, backend validation commands, and final reporting requirements.

## TASK-0206 SQL Reporting Foundation

Added a read-only SQL-backed reporting foundation with explicit Pydantic row schemas, a report repository, and repository tests for leads by city/category, missing websites, high-review weak presence, manual review, score distribution, import quality, and missing-data reports. The reporting repository reads persisted `Lead`, `LeadAudit`, `LeadScore`, `LeadImportRun`, and `LeadImportError` rows without dashboards, BI export, external API calls, AI analytics, outreach logic, migrations, scoring rule changes, audit rule changes, dependency changes, or CI changes.

## TASK-0208 BI Export Dataset Layer

Added a BI export dataset layer that converts SQL-backed reporting outputs into stable, flat, dashboard-ready tables and CSV strings. The layer adds explicit BI export schemas, a service that calls `ReportRepository`, tests for dataset/table/CSV behavior and side effects, and BI export documentation without dashboards, API routes, file download endpoints, scheduled jobs, external storage, pandas, new dependencies, AI analytics, or integrations.

## TASK-0701 Power BI Dashboard Specification

Added a manual Power BI dashboard specification, deterministic sample BI export CSV fixtures, and docs/fixture tests. The dashboard spec maps all seven BI export tables to pages, visuals, slicers, measures, modeling guidance, and manual build steps while keeping `.pbix` creation deferred and excluding Power BI automation, frontend work, API routes, external storage, pandas, new dependencies, AI analytics, integrations, and outbound sending.

## TASK-0702 Tableau Dashboard Specification

Added a manual Tableau dashboard specification and documentation tests using the existing BI export CSV fixtures. The Tableau spec maps all seven BI export tables to manual dashboard pages, worksheets, filters, calculated fields, tooltip guidance, and portfolio screenshot planning while keeping `.twb`, `.twbx`, and `.hyper` workbook creation deferred and excluding Tableau automation, frontend work, API routes, external storage, pandas, new dependencies, AI analytics, integrations, and outbound sending.

## TASK-0502 Outreach Draft Foundation

Added structured outreach drafting schemas and deterministic templates for `short_email` and `whatsapp_message`. Drafts use only supplied business, location, audit, scoring, and offer context; keep scoring context in internal personalization notes; expose assumptions; and always require human review. The task does not add sending, evaluation, routes, persistence, migrations, LLM calls, integrations, or new dependencies.

## TASK-0602 Deterministic Outreach Evaluator

Added structured evaluation schemas and a deterministic evaluator for outreach
relevance, personalization, clarity, tone, truthfulness, CTA quality, risk,
failure reasons, bad lines, and pass-or-review decisions. Evaluation uses
explicit supported facts and does not rewrite, persist, route, or send drafts.
No LLM integration, external API, migration, route, frontend, integration, or
new dependency was added.
