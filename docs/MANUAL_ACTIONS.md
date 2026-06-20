# Manual Actions

## Required Now

Verify GitHub Actions Backend CI after the TASK-0206 commit is pushed.

As of TASK-0206 start, PR #1 Backend CI is verified passing at commit `6fd06479e370e21e3583b557536564ab1fce6bc4`. Local HEAD matched that commit before TASK-0206 edits.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `6fd06479e370e21e3583b557536564ab1fce6bc4`, Backend CI passed.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Next Implementation

Complete TASK-0206 and verify:

```bash
cd backend && make check
cd .. && git diff --check
```

Then commit and push TASK-0206, and verify Backend CI for that pushed commit before starting BI export or dashboard preparation.

Current local blocker:

- `make format-check` and `make lint` cannot run because `ruff` is not installed in the active environment.
- `make test` cannot run because pyenv Python `3.12` is not installed for `backend/.python-version`.
- Supplemental TASK-0206 tests pass with `PYENV_VERSION=backend-3.11.9 PYTHONPATH=. pytest tests/test_report_repository.py`.
- `git diff --check` passes locally for TASK-0206.

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
