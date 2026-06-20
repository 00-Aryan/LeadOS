# Manual Actions

## Required Now

Provision the local backend validation tools and rerun TASK-0207 validation.

As of TASK-0207 start, PR #1 Backend CI is verified passing at commit `1db856783a2620fc963c12b79a1d5adba76dde88`. Local HEAD matched that commit before TASK-0207 edits. TASK-0207 has uncommitted local changes because required local validation is blocked.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `1db856783a2620fc963c12b79a1d5adba76dde88`, Backend CI passed.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Next Implementation

Complete TASK-0207 and verify:

```bash
cd backend && make check
cd .. && git diff --check
```

Then commit and push TASK-0207, and verify Backend CI for that pushed commit.

Current local blocker:

- `make format-check` and `make lint` cannot run because `ruff` is not installed.
- `make test` cannot run because pyenv Python `3.12` is not installed for `backend/.python-version`.
- `PYTHONPATH=. python3 -m pytest` cannot run because the system Python 3.12.3 does not have `pytest` installed.
- `git diff --check` passed locally for TASK-0207.

Before TASK-0206 starts, verify Backend CI is green for the TASK-0207 commit.

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
