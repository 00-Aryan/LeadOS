# Manual Actions

## Required Now

The TASK-0503 sample cases are entirely fictional and exist only for
validation and portfolio demonstration. They are not real prospects and must
not be treated as an outreach queue.

No automatic sending is permitted. `approve` means only that a human may
consider sending a separately verified draft. `revise` cases require
re-evaluation before another manual review. `reject` cases must not be used.

As of TASK-0503 start, the user-provided task handoff records Backend CI
passing at commit `0fd9c69581865a864bf6a657f683bd5083b39888`
in run #106.

For current task sequencing and blockers, use `docs/ACTIVE_TASKS.md`.

## Required Later

- Supply verified lead and audit facts when evaluating a draft.
- Manually review every evaluated draft with the expert checklist.
- Re-evaluate every revised draft before it returns to manual review.
- Never use rejected sample drafts as outreach.
- Build the Power BI and Tableau workbooks manually outside this repository.
- Capture dashboard screenshots for the portfolio case study.

No automatic outbound sending is permitted.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

Local backend validation may remain blocked on machines without Python 3.12
and backend dependencies. GitHub Actions is the final validation source.

## Required Before Next Implementation

Complete TASK-0503 local validation using the commands documented in
`AGENTS.md` and the task instructions. If Python 3.12 is unavailable, use the
documented Python 3.11 fallback and state that clearly.

After explicit user authorization, commit and push TASK-0503. Fresh Backend CI
must pass for that pushed commit before TASK-0503 can be marked complete.

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
