# Sprint 2 Review: SQL Data Layer and Data Transformation

## Status

Sprint 2 is now complete enough for MVP continuation.

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
10 tests passed locally in the fixed package.
```

## Remaining non-blocking improvements

- Add Alembic migrations before production deployment.
- Add richer dedupe using phone and website.
- Add extraction/reporting query services.
- Add PostgreSQL-specific CI job later.
