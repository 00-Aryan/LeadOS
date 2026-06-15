# Manual Actions

## Required Now

None, unless a newer commit is pushed and CI has not completed.

As of TASK-0010, PR #1 Backend CI is verified passing at commit `8e5f2a5c1a48884c110ccf8ed53027d72f183416`, run #67 / `27564758959`. If a newer commit is pushed, manually verify Backend CI for the pushed PR head.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `8e5f2a5c1a48884c110ccf8ed53027d72f183416`, Backend CI passed in run #67 / `27564758959`.

Local backend tests may still fail to run on machines without Python 3.12 and backend dependencies installed; GitHub Actions is the current source of truth for PR validation.

## Required Before Implementation

Manually verify current GitHub issues and PR body before starting TASK-0203. GitHub CLI could not connect to `api.github.com` during TASK-0010, so issue state was not inspected from this environment.

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
