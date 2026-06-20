# Manual Actions

## Required Now

Commit and push TASK-0701, then verify GitHub Actions Backend CI for the pushed commit.

As of TASK-0701 start, PR #1 Backend CI is verified passing at commit `9b7fce3c03a1644cbbf79264d96901f2a10962ec`. Local HEAD matched that commit before TASK-0701 edits.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Later

Manually build the `.pbix` file in Power BI Desktop from the CSV fixtures in `data/bi_exports/*.csv`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `9b7fce3c03a1644cbbf79264d96901f2a10962ec`, Backend CI passed.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Next Implementation

Complete TASK-0701 and verify:

```bash
cd backend && make check
cd .. && git diff --check
```

Then commit and push TASK-0701, and verify Backend CI for that pushed commit before starting TASK-0702 or TASK-0502.

Current local blocker:

- `make format-check` and `make lint` cannot run because `ruff` is not installed in the active environment.
- `make test` cannot run because pyenv Python `3.12` is not installed for `backend/.python-version`.
- Exact supplemental commands using the default pyenv shims are blocked because `python` and `pytest` are unavailable in the active shim selection.
- Supplemental TASK-0701 tests should be run with `PYENV_VERSION=backend-3.11.9 PYTHONPATH=backend pytest backend/tests/test_power_bi_dashboard_docs.py` if the full local gate is blocked.
- `git diff --check` should pass locally for TASK-0701 before commit.

## Required Before Production

- Configure production DB URL.
- Add migrations.
- Review security and compliance.
- Configure secrets if deployment is added.

## Deferred

- Deployment.
- Auth.
- Billing.
- Screenshot capture and portfolio case-study update.
- Outbound sending.
- CRM integration.
