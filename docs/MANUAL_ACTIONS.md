# Manual Actions

## Required Now

Verify GitHub Actions Backend CI after the TASK-0208 commit is pushed.

As of TASK-0208 start, PR #1 Backend CI is verified passing at commit `1cb9f66a1437ee1fa442cea340aeaf59626559af`. Local HEAD matched that commit before TASK-0208 edits.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `1cb9f66a1437ee1fa442cea340aeaf59626559af`, Backend CI passed.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Next Implementation

Complete TASK-0208 and verify:

```bash
cd backend && make check
cd .. && git diff --check
```

Then commit and push TASK-0208, and verify Backend CI for that pushed commit before starting TASK-0701.

Current local blocker:

- `make format-check` and `make lint` cannot run because `ruff` is not installed in the active environment.
- `make test` cannot run because pyenv Python `3.12` is not installed for `backend/.python-version`.
- Exact supplemental commands using the default pyenv shims are blocked because `python` and `pytest` are unavailable in the active shim selection.
- Supplemental TASK-0208 tests pass with `PYENV_VERSION=backend-3.11.9 PYTHONPATH=backend pytest backend/tests/test_bi_export_service.py`.
- Supplemental compile passes with `PYENV_VERSION=backend-3.11.9 python -m py_compile backend/app/schemas/bi_export.py backend/app/services/bi_export_service.py`.
- `git diff --check` passes locally for TASK-0208.

## Required Before Production

- Configure production DB URL.
- Add migrations.
- Review security and compliance.
- Configure secrets if deployment is added.

## Deferred

- Deployment.
- Auth.
- Billing.
- Outbound sending.
- CRM integration.
