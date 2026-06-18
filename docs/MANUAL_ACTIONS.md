# Manual Actions

## Required Now

Verify Backend CI after the TASK-0303 commit is pushed.

As of TASK-0303 start, PR #1 Backend CI is verified passing at commit `daccb2cc9f75a268f2d394557a609435fa96bfba`, run #78 / `27631431957`. Local HEAD matched that commit before TASK-0303 edits. Any pushed TASK-0303 commit must receive fresh Backend CI verification before TASK-0304 starts.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `daccb2cc9f75a268f2d394557a609435fa96bfba`, Backend CI passed in run #78 / `27631431957`.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Next Implementation

Complete TASK-0303 and verify:

```bash
cd backend && make check
cd .. && git diff --check
```

Then verify Backend CI after the TASK-0303 commit is pushed.

Current local blocker:

- `make format-check` and `make lint` cannot run because `ruff` is not installed.
- `make test` cannot run because pyenv Python `3.12` is not installed for `backend/.python-version`.
- Supplemental Python 3.11.9 cannot run pytest because `pytest` is not installed there.
- `gh issue list --limit 50` cannot verify remaining GitHub issue coverage because this environment cannot connect to `api.github.com`.
- `git diff --check` passed locally.

Before TASK-0304 starts, verify Backend CI is green for the TASK-0303 commit. The existing stash `wip-task-0303-audit-files-after-task-0105` was inspected and must not be dropped until TASK-0303 is committed, pushed, and CI is green.

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
