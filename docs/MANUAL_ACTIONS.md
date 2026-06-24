# Manual Actions

## Required Now

Complete TASK-0602, then commit and push the scoped deterministic evaluator
changes. Verify GitHub Actions Backend CI for the pushed commit.

As of TASK-0602 start, Backend CI is verified passing at commit
`e96bc4cdb5bd32f75de9c138d20c52af2bc4041f` in run #102.

For current task sequencing and blockers, use `docs/ACTIVE_TASKS.md`.

## Required Later

- Supply verified lead and audit facts when evaluating a draft.
- Manually review every draft before human use.
- Revise drafts marked `review` before sending.
- Build the Power BI and Tableau workbooks manually outside this repository.
- Capture dashboard screenshots for the portfolio case study.

No automatic outbound sending is permitted.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

Local backend validation may remain blocked on machines without Python 3.12
and backend dependencies. GitHub Actions is the final validation source.

## Required Before Next Implementation

Complete TASK-0602 and run the backend validation commands documented in
`AGENTS.md`. If Python 3.12 is unavailable, use the documented Python 3.11
fallback and state that the full local gate was not verified.

Then commit and push TASK-0602 and verify Backend CI for that pushed commit.

## Required Before Production

- Configure the production database URL.
- Add migrations.
- Review security and compliance.
- Configure secrets if deployment is added.

## Deferred

- Deployment.
- Authentication.
- Billing.
- Automatic draft rewriting.
- Automatic outbound sending.
- CRM integration.
- ProjectOS integration.
- Content Creation Automation integration.
