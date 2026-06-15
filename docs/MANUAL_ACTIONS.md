# Manual Actions

## Required Now

None, unless a newer commit is pushed and CI has not completed.

As of TASK-0203 start, PR #1 Backend CI is verified passing at commit `ed6050567c33c50557b994ca263e82a555fe4dd8`, run #69 / `27565986172`. If TASK-0203 changes or any newer commit are pushed, manually verify Backend CI for the pushed PR head.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `ed6050567c33c50557b994ca263e82a555fe4dd8`, Backend CI passed in run #69 / `27565986172`.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Implementation

Provision local backend validation tooling or verify Backend CI after pushing TASK-0203. In this environment, `make format-check` and `make lint` failed because `ruff` is not installed, and `make test` failed because pyenv Python 3.12 is missing.

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
