# Manual Actions

## Required Now

- Verify PR #1 Backend CI manually for latest head commit `2b1645c70674c530f8af462c2a180bc32baa2ac5`; GitHub Actions could not be inspected from this environment.
- Do not start TASK-0007 or feature work until latest-head Backend CI is verified passing.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `eda102a7286e00acb6d874411e238245c1a1c65c`, Backend CI passed in run #54.

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
