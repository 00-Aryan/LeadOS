# Context Index

Use this file to decide what to read before editing. Read narrowly, but always read enough context to understand product boundaries, service ownership, and validation expectations.

## Historical or Stale Docs Warning

Some documents are retained for traceability and may not represent current implementation state. Future agents must treat files marked historical as references only and must check `docs/CHANGELOG_AGENT.md` before acting on them.

## Active Task Source

- `docs/ACTIVE_TASKS.md`: Canonical active task index for current executable work.
- `docs/BACKLOG_RECONCILIATION.md`: Canonical implementation backlog reconciliation and next-task decision after Phase 0 hardening.
- Historical task and backlog files such as `docs/TASKS.md`, `docs/GITHUB_ISSUES_TO_CREATE.md`, `docs/FIX_LOG.md`, `docs/SPRINT_1_REVIEW.md`, and `docs/SPRINT_2_REVIEW.md` are references only. Do not execute tasks from them without checking `docs/ACTIVE_TASKS.md` first.

## Product Context

- `README.md`: Project identity, standalone boundary, initial build principle, and deferred areas.
- `docs/PRODUCT_SPEC.md`: Product thesis, target user, MVP modules, non-goals, and quality bar.
- `docs/MVP_SCOPE.md`: In-scope and out-of-scope MVP capabilities.
- `docs/ACTIVE_TASKS.md`: Canonical active task index.
- `docs/BACKLOG_RECONCILIATION.md`: Current reconciled implementation sequence and deferred-work guardrails.
- `docs/TASKS.md`: Historical backlog, task IDs, and phase structure.

## Architecture Context

- `docs/ARCHITECTURE.md`: Service boundaries, dependency rules, and backend shape.
- `docs/WORKFLOW.md`: Standard planning, implementation, validation, failure, and reporting loop.
- `docs/DONE_CRITERIA.md`: Completion gate for any task.
- `docs/DECISIONS.md`: Architecture decision records that constrain future changes.

## Data Context

- `docs/DATA_MODEL.md`: Current and reserved tables, key columns, uniqueness rule, and database strategy.
- `docs/DATA_TRANSFORMATION_PLAN.md`: CSV normalization, validation, dedupe, and future reporting queries.
- `docs/BI_EXPORT.md`: BI export dataset layer, table names, CSV behavior, and deferred dashboard boundaries.
- `docs/POWER_BI_DASHBOARD.md`: Power BI dashboard specification that maps BI export tables to manual dashboard pages and visuals.
- `docs/TABLEAU_DASHBOARD.md`: Tableau dashboard specification that maps BI export fixtures to manual workbook dashboards, worksheets, filters, calculated fields, and portfolio screenshots.
- `data/sample_leads.csv`: Sample input data for import-related checks.
- `data/bi_exports/*.csv`: Deterministic sample BI export fixtures for manual dashboard builds.

## Backend Code

- `backend/app/main.py`: FastAPI application entrypoint and router registration.
- `backend/app/config.py`: Runtime settings.
- `backend/app/database.py`: SQLAlchemy engine, session, and database helpers.
- `backend/app/schemas/`: Request and response contracts.
- `backend/app/schemas/bi_export.py`: BI export dataset, table, column, and cell schemas.
- `backend/app/models/`: SQLAlchemy ORM models.
- `backend/app/repositories/`: Persistence access patterns.
- `backend/app/services/`: Business logic for import, audit, scoring, BI export, outreach, and evaluation.
- `backend/app/services/bi_export_service.py`: Builds dashboard-ready datasets and CSV strings from SQL-backed reporting outputs.
- `backend/app/routers/`: API route boundaries.

## Tests

- `backend/tests/conftest.py`: Test fixtures and database setup.
- `backend/tests/test_health.py`: Health endpoint coverage.
- `backend/tests/test_leads_router.py`: Lead API coverage.
- `backend/tests/test_lead_import_service.py`: Import validation and persistence behavior.
- `backend/tests/test_lead_repository.py`: Repository behavior.
- `backend/tests/test_lead_transform_service.py`: CSV transformation and validation behavior.
- `backend/tests/test_audit_service.py`: Deterministic audit behavior.
- `backend/tests/test_scoring_service.py`: Scoring behavior.
- `backend/tests/test_scoring_router.py`: Scoring API behavior.
- `backend/tests/test_report_repository.py`: SQL-backed reporting query behavior.
- `backend/tests/test_bi_export_service.py`: BI export dataset and CSV behavior.
- `backend/tests/test_power_bi_dashboard_docs.py`: Power BI dashboard documentation and sample fixture coverage.
- `backend/tests/test_tableau_dashboard_docs.py`: Tableau dashboard documentation, fixture, workbook-deferral, and context-index coverage.

## Release / Review / Validation Context

- `docs/PR_CHECKLIST.md`: Release readiness, merge gates, docs-only checks, backend-change checks, dependency/tooling checks, and agent PR safety rules.
- `docs/VALIDATION_COMMANDS.md`: Backend and docs validation commands.
- `docs/DONE_CRITERIA.md`: Completion gate for any task.
- `docs/MANUAL_ACTIONS.md`: Manual verification and external action requirements.

## CI/Tooling

- `docs/CI_TROUBLESHOOTING.md`: GitHub Actions Backend CI failure diagnosis, failing-step mapping, and agent safety rules for CI repair.
- `docs/LOCAL_ENVIRONMENT.md`: Local Python 3.12, virtual environment, dependency install, and backend validation setup.
- `.github/workflows/backend-ci.yml`: GitHub Actions backend CI gate.
- `backend/Makefile`: Install, format, lint, test, and check commands.
- `backend/ruff.toml`: Ruff format and lint configuration.
- `backend/requirements.txt`: Backend dependency list.
- `backend/pytest.ini`: Pytest configuration.

## Sprint/Review Docs

- `docs/FIX_LOG.md`: Historical fixes and last recorded test result.
- `docs/SPRINT_1_REVIEW.md`: Sprint 1 review context.
- `docs/SPRINT_2_REVIEW.md`: Sprint 2 review context.
- `docs/API_REVIEW_001.md`: API review notes.
- `docs/COUNCIL_REVIEW_001.md`: Expert council review notes.
- `docs/SECURITY_REVIEW_001.md`: Security review notes.
- `docs/SCORING_REVIEW_001.md`: Scoring review notes.
- `docs/GITHUB_ISSUES_TO_CREATE.md`: Planned GitHub issue backlog.
