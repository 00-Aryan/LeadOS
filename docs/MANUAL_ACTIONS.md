# Manual Actions

## Required Now

Verify Backend CI after any new TASK-0105 commit is pushed.

As of TASK-0105 start, PR #1 Backend CI is verified passing at commit `64f116cc77758de2e3e51792fe4b898cda2dd9e1`, run #76 / `27574177028`. Local HEAD matches that commit, but the worktree has uncommitted changes. Any pushed commit must receive fresh Backend CI verification before Sprint 3 starts.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `64f116cc77758de2e3e51792fe4b898cda2dd9e1`, Backend CI passed in run #76 / `27574177028`.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Next Implementation

Complete TASK-0105 and verify:

```bash
cd backend && make check
cd .. && git diff --check
```

Then verify Backend CI after the TASK-0105 commit is pushed.

Current local blocker:

- `make format-check` and `make lint` cannot run because `ruff` is not installed.
- `make test` cannot run because pyenv Python `3.12` is not installed for `backend/.python-version`.
- `gh issue list --limit 50` cannot verify remaining GitHub issue coverage because this environment cannot connect to `api.github.com`.
- `git diff --check` passed locally.

Before Sprint 3 starts, verify that deferred gaps from `docs/SPRINT_1_2_COMPLETION_GATE.md` are tracked as GitHub issues, or create issues for any missing gaps.

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
