# Sprint 2 Review: SQL Data Layer and Data Transformation

> **Status:** Historical reference.
> This document may describe earlier implementation state, task planning, or validation status.
> For current agent instructions and repository state, read `AGENTS.md`, `docs/CONTEXT_INDEX.md`, and `docs/CHANGELOG_AGENT.md` first.
>
> **Completion gate:** See `docs/SPRINT_1_2_COMPLETION_GATE.md` for TASK-0105 final Sprint 1 and Sprint 2 gate evidence.

## Status

Sprint 2 is complete for the SQL data layer and CSV transformation gate.

## Goal

Move LeadOS from stateless CSV processing toward a real SQL-backed lead intelligence data layer.

## Completed files

```text
backend/app/config.py
backend/app/database.py
backend/app/models/lead.py
backend/app/models/lead_import.py
backend/app/models/lead_audit.py
backend/app/models/lead_score.py
backend/app/repositories/lead_repository.py
backend/app/services/lead_transform_service.py
backend/app/services/lead_import_service.py
backend/tests/test_lead_transform_service.py
backend/tests/test_lead_repository.py
backend/tests/test_lead_import_service.py
```

## Fixed issues

- Replaced invalid Pydantic v2 settings import with `pydantic-settings`.
- Added missing dependencies.
- Added SQLAlchemy 2.0 ORM models.
- Added import run tracking.
- Added rejected-row persistence.
- Added repository layer.
- Added deterministic transform service.
- Added duplicate detection using normalized business name and city.
- Removed per-row commits from import service.
- Added tests for transform, repository, import service, and API route.
- Added automatic local SQLite directory creation.

## Data transformation coverage

```text
trim repeated whitespace
normalize duplicate keys with casefolding
normalize phone separators
parse rating with explicit validation
parse review_count with explicit validation
validate website scheme
track invalid rows with reasons
track duplicate rows
```

## Validation

```text
Use the current backend gate:

cd backend && make check

The latest verified CI baseline for this review is PR #1 Backend CI success at commit `64f116cc77758de2e3e51792fe4b898cda2dd9e1`, run #76 / `27574177028`.
```

## Remaining non-blocking improvements

- Add Alembic migrations before production deployment.
- Add richer dedupe using phone and website.
- Add extraction/reporting query services.
- Add PostgreSQL-specific CI job later.
