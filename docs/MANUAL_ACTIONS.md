# Manual Actions

## Required Now

None, unless a newer commit is pushed and CI has not completed.

As of TASK-0009, PR #1 Backend CI is verified passing at commit `bd79762147ac0732bc5185cad50110ad9984be7e`, run #65 / `27563984088`. If a newer commit is pushed, manually verify Backend CI for the pushed PR head.

For current task sequencing and manual-work blockers, use `docs/ACTIVE_TASKS.md`.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

As of PR #1 commit `bd79762147ac0732bc5185cad50110ad9984be7e`, Backend CI passed in run #65 / `27563984088`.

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
