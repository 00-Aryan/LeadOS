# Context Index

Use this file to decide what to read before editing. Read narrowly, but always read enough context to understand product boundaries, service ownership, and validation expectations.

## Product Context

- `README.md`: Project identity, standalone boundary, initial build principle, and deferred areas.
- `docs/PRODUCT_SPEC.md`: Product thesis, target user, MVP modules, non-goals, and quality bar.
- `docs/MVP_SCOPE.md`: In-scope and out-of-scope MVP capabilities.
- `docs/TASKS.md`: Backlog, task IDs, phase structure, and current task language.

## Architecture Context

- `docs/ARCHITECTURE.md`: Service boundaries, dependency rules, and backend shape.
- `docs/WORKFLOW.md`: Standard planning, implementation, validation, failure, and reporting loop.
- `docs/DONE_CRITERIA.md`: Completion gate for any task.
- `docs/DECISIONS.md`: Architecture decision records that constrain future changes.

## Data Context

- `docs/DATA_MODEL.md`: Current and reserved tables, key columns, uniqueness rule, and database strategy.
- `docs/DATA_TRANSFORMATION_PLAN.md`: CSV normalization, validation, dedupe, and future reporting queries.
- `data/sample_leads.csv`: Sample input data for import-related checks.

## Backend Code

- `backend/app/main.py`: FastAPI application entrypoint and router registration.
- `backend/app/config.py`: Runtime settings.
- `backend/app/database.py`: SQLAlchemy engine, session, and database helpers.
- `backend/app/schemas/`: Request and response contracts.
- `backend/app/models/`: SQLAlchemy ORM models.
- `backend/app/repositories/`: Persistence access patterns.
- `backend/app/services/`: Business logic for import, audit, scoring, outreach, and evaluation.
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

## CI/Tooling

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
