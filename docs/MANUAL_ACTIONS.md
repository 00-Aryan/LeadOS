# Manual Actions

## Required Now

Use `docs/OUTREACH_EXPERT_REVIEW_CHECKLIST.md` as a mandatory manual gate after
deterministic evaluation and before any human considers sending a draft.

Every revised draft must be evaluated again before another manual review.
Automatic outbound sending remains prohibited.

As of TASK-0603 start, the user-provided task handoff records Backend CI
passing at commit `4bfb6300bc68c7babc750f74d9142690225454f9`
in run #104.

For current task sequencing and blockers, use `docs/ACTIVE_TASKS.md`.

## Required Later

- Supply verified lead and audit facts when evaluating a draft.
- Manually review every evaluated draft with the expert checklist.
- Re-evaluate every revised draft before it returns to manual review.
- Build the Power BI and Tableau workbooks manually outside this repository.
- Capture dashboard screenshots for the portfolio case study.

No automatic outbound sending is permitted.

## Required Before Merge

GitHub Actions Backend CI must be green for the latest PR head commit.

Local backend validation may remain blocked on machines without Python 3.12
and backend dependencies. GitHub Actions is the final validation source.

## Required Before Next Implementation

Complete TASK-0603 local validation using the commands documented in
`AGENTS.md` and the task instructions. If Python 3.12 is unavailable, use the
documented Python 3.11 fallback and state that clearly.

After explicit user authorization, commit and push TASK-0603. Fresh Backend CI
must pass for that pushed commit before TASK-0603 can be marked complete.

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
