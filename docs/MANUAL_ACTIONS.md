# Manual Actions

## Required Now

Review the Phase 0 closeout diff and completion report. After explicit user
authorization, commit and push the closeout changes, then verify fresh Backend
CI and perform final human review of PR #1.

The verified baseline is commit
`7012d052e37e12b458420e38e03f80e011faf1b2`; user-provided Backend CI run
#108 passed, and GitHub PR inspection confirmed that commit as the PR head.

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

- Review the final PR diff.
- Confirm branch protection and required checks.
- Confirm no secrets or local artifacts are present.
- Confirm the updated PR title/body still reflects the final committed scope.
- Confirm fresh Backend CI is green for the closeout commit.
- Merge manually only after final human review.
- Delete or retain the branch according to repository policy.

No automatic merge is permitted.

## Required Before Next Implementation

Complete TASK-PHASE0-CLOSEOUT validation using the commands documented in
`AGENTS.md` and the task instructions. If the existing Python 3.11 TestClient
timeout occurs, record it, run the complete non-TestClient suite, and use
fresh GitHub Actions as the final gate.

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
