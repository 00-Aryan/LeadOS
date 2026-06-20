# Manual Actions

## Required Now

Complete TASK-0702, then commit and push the scoped Tableau dashboard specification changes. Verify GitHub Actions Backend CI for the pushed commit.

As of TASK-0702 start, PR #1 Backend CI is verified passing at commit `ca7df13b1d46fcc58a841e8a2ed69d34b7cb00d0`.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Later

Manually build the `.pbix` file in Power BI Desktop from the CSV fixtures in `data/bi_exports/*.csv`.

Manually build the Tableau workbook outside this repository from the CSV fixtures in `data/bi_exports/*.csv`.

Do not commit `.pbix`, `.twb`, `.twbx`, or `.hyper` files unless a future task explicitly allows it.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `ca7df13b1d46fcc58a841e8a2ed69d34b7cb00d0`, Backend CI passed.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Next Implementation

Complete TASK-0702 and verify:

```bash
cd backend && make check
cd .. && git diff --check
```

Then commit and push TASK-0702, and verify Backend CI for that pushed commit before starting TASK-0502 or any other feature task.

Current local blocker history:

- `make format-check` and `make lint` may fail if `ruff` is not installed in the active environment.
- `make test` may fail if pyenv Python `3.12` is not installed for `backend/.python-version`.
- Supplemental TASK-0702 tests should be run with `PYENV_VERSION=backend-3.11.9 PYTHONPATH=backend pytest backend/tests/test_tableau_dashboard_docs.py` if the full local gate is blocked.
- `git diff --check` should pass locally for TASK-0702 before commit.

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
