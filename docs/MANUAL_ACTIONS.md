# Manual Actions

## Required Now

Complete TASK-0502, then commit and push the scoped outreach foundation changes.
Verify GitHub Actions Backend CI for the pushed commit.

As of TASK-0502 start, the user-provided task handoff records PR #1 Backend CI
passing at commit `362fd8018dce531fe8fdd0d8b8fb8f40d28a4b0b` in run #100.
This environment could not re-query GitHub Actions.

For current task sequencing and blockers, use `docs/ACTIVE_TASKS.md`.

## Required Later

- Manually review every generated outreach draft before use.
- Run the future evaluator before a human sends any draft.
- Build the Power BI and Tableau workbooks manually outside this repository.
- Capture dashboard screenshots for the portfolio case study.

No automatic outbound sending is permitted.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

Local backend validation may remain blocked on machines without Python 3.12 and
backend dependencies. GitHub Actions is the final validation source.

## Required Before Next Implementation

Complete TASK-0502 and run:

```bash
cd backend
make format-check
make lint
make test
cd ..
git diff --check
```

If Python 3.12 is unavailable, use the documented Python 3.11 fallback and
state clearly that the full local gate was not verified.

Then commit and push TASK-0502 and verify Backend CI for that pushed commit.

## Required Before Production

- Configure the production database URL.
- Add migrations.
- Review security and compliance.
- Configure secrets if deployment is added.

## Deferred

- Deployment.
- Authentication.
- Billing.
- Outreach evaluator implementation.
- Automatic outbound sending.
- CRM integration.
- ProjectOS integration.
- Content Creation Automation integration.
