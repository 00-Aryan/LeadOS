# Sprint 1 and Sprint 2 Completion Gate

## Status

- Task: TASK-0105
- GitHub issue: #25
- Gate date: 2026-06-16
- Branch: `phase-0-product-foundation`
- Verified CI baseline: PR #1 Backend CI passed at commit `64f116cc77758de2e3e51792fe4b898cda2dd9e1`, run #76 / `27574177028`
- Local HEAD at review start: `64f116cc77758de2e3e51792fe4b898cda2dd9e1`
- Current gate result: Local validation blocked by missing local backend tooling. `git diff --check` passed.
- GitHub issue verification: Blocked locally because `gh issue list --limit 50` could not connect to `api.github.com`.

If a commit newer than `64f116cc77758de2e3e51792fe4b898cda2dd9e1` is pushed, Backend CI must be re-verified before Sprint 3 starts.

## Local Validation Result

Attempted on 2026-06-16:

```text
cd backend && make format-check
```

Result: blocked because `ruff` is not installed.

```text
cd backend && make lint
```

Result: blocked because `ruff` is not installed.

```text
cd backend && make test
```

Result: blocked because pyenv Python `3.12` is not installed for `backend/.python-version`.

```text
git diff --check
```

Result: passed.

Do not treat TASK-0105 as fully complete until backend validation runs locally in a provisioned environment or Backend CI is verified green after the TASK-0105 changes are pushed.

Remaining deferred gaps are listed below, but live GitHub issue tracking could not be verified from this environment. Before Sprint 3 starts, verify that the deferred gaps are already tracked as GitHub issues or create issues for any missing items.

## One-Command Backend Validation

Run from the repository root:

```bash
cd backend && make check
```

This is equivalent to:

```bash
cd backend
make format-check
make lint
make test
```

GitHub Actions runs the same backend gate as separate steps in `.github/workflows/backend-ci.yml`.

## Sprint 1 Completion

Sprint 1 is complete for the backend foundation gate.

Evidence:

- FastAPI app and health route exist in `backend/app/main.py`.
- Lead import route is covered by `backend/tests/test_leads_router.py`.
- Lead import service is covered by `backend/tests/test_lead_import_service.py`.
- Backend dependency and validation commands exist in `backend/requirements.txt`, `backend/pytest.ini`, and `backend/Makefile`.
- Backend CI has passed for the verified baseline commit listed above.

## Sprint 2 Completion

Sprint 2 is complete for the SQL data layer and CSV transformation gate.

Evidence:

- SQLAlchemy models exist for leads, import runs, import errors, audits, and scores.
- SQLAlchemy tables initialize in the shared test fixture through `Base.metadata.create_all(bind=engine)`.
- Repository persistence behavior is covered by `backend/tests/test_lead_repository.py`.
- CSV transformation behavior is covered by `backend/tests/test_lead_transform_service.py`.
- CSV import persistence, invalid-row persistence, and duplicate detection are covered by `backend/tests/test_lead_import_service.py`.

## Required Check Mapping

| Requirement | Evidence |
|---|---|
| Backend tests run locally and in CI | Local command is `cd backend && make check`; CI workflow runs install, format, lint, and test in `.github/workflows/backend-ci.yml`. |
| CSV import persists valid leads | `test_import_csv_persists_valid_rows_and_run_summary` in `backend/tests/test_lead_import_service.py`. |
| Invalid rows are persisted as import errors | `test_import_csv_rejects_invalid_rows_and_persists_errors` in `backend/tests/test_lead_import_service.py`. |
| Duplicate rows are detected through normalized keys | `test_import_csv_detects_duplicates_with_normalized_keys` in `backend/tests/test_lead_import_service.py` and `test_repository_adds_and_finds_duplicate` in `backend/tests/test_lead_repository.py`. |
| SQLAlchemy tables initialize successfully | `db_session` fixture in `backend/tests/conftest.py` imports models and runs `Base.metadata.create_all(bind=engine)`; route tests use this fixture through `client`. |
| Existing audit and scoring services remain import-compatible after lead schema changes | `backend/tests/test_audit_service.py`, `backend/tests/test_scoring_service.py`, and `backend/tests/test_scoring_router.py` import and exercise the services and schemas under the current package layout. |

## Deferred Work

The following items remain deferred and are not blockers for Sprint 1 or Sprint 2 completion:

- Alembic migrations before production deployment.
- Richer duplicate detection using phone and website.
- Reporting/query services.
- Audit persistence repository.
- Scoring persistence repository.
- Deployment, auth, billing, outbound sending, CRM integration, ProjectOS integration, and content-tool integration.

## Sprint 3 Gate

Do not start Sprint 3 until:

- `cd backend && make check` passes locally or Backend CI is verified green after the TASK-0105 changes are pushed.
- `git diff --check` passes.
- Backend CI is re-verified after any pushed commit newer than `64f116cc77758de2e3e51792fe4b898cda2dd9e1`.
- Any remaining gaps are tracked in active docs or GitHub issues.
