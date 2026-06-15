# Manual Actions

## Required Now

None, unless a newer commit is pushed and CI has not completed.

During TASK-0008, GitHub CLI could not connect to inspect latest-head CI. If local HEAD `abfddf741f1f7c8765afd718b43e1f511377e94d` or any newer commit is pushed, manually verify Backend CI for the pushed PR head.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`, Backend CI passed in run #60 / `27554650321`.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

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
