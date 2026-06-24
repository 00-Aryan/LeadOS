# PR Checklist

## Purpose

This file defines the required checks before marking a LeadOS PR ready for merge. Use it to keep PR review focused on verified validation, assigned scope, documented manual work, and the project boundaries that protect the MVP.

## Scope

This checklist applies to PR #1 and future LeadOS PRs unless a task explicitly defines a stricter checklist.

## Current PR State

- PR: #1
- Branch: `phase-0-product-foundation`
- Latest verified head commit: `7012d052e37e12b458420e38e03f80e011faf1b2`
- Latest verified CI run: Backend CI success, run #108
- Current merge posture: The verified baseline matches the local and GitHub PR
  head. Phase 0 implementation criteria pass, but the closeout commit still
  requires push, fresh Backend CI, and final human review before merge.

## Phase 0 Closeout Checklist

- [x] Verified baseline commit matches the local and GitHub PR head.
- [x] Backend CI run #108 passed for the verified baseline.
- [x] Phase 0 implementation criteria are mapped to concrete source and tests.
- [x] Deferred production and integration work is explicit.
- [ ] `docs/PHASE_0_COMPLETION_REPORT.md` is committed and pushed.
- [ ] Completion documentation tests pass in fresh Backend CI.
- [x] PR #1 title/body reflects the complete Phase 0 scope.
- [ ] Final PR diff has been manually reviewed.
- [ ] Branch protection and required checks are satisfied.
- [x] No automatic merge was performed by this closeout task.

## Required Before Marking Ready

- [ ] Latest PR head has passing GitHub Actions Backend CI.
- [ ] `git diff --check` passes.
- [ ] No unintended backend/test/CI/dependency files changed.
- [ ] Scope matches the assigned task.
- [ ] No feature work bundled into docs-only tasks.
- [ ] No docs-only task claims backend tests passed unless they actually ran.
- [ ] Manual actions are documented in `docs/MANUAL_ACTIONS.md`.
- [ ] Active task status is updated in `docs/ACTIVE_TASKS.md`.
- [ ] Relevant context docs are updated.
- [ ] Stale/historical docs are not used as active task sources.
- [ ] PR description is updated if PR scope changed materially.

## Sprint 1 and Sprint 2 Gate Checklist

- [ ] `docs/SPRINT_1_2_COMPLETION_GATE.md` reflects final Sprint 1 and Sprint 2 status.
- [ ] `cd backend && make check` passes locally or the exact local blocker is recorded.
- [ ] `git diff --check` passes.
- [ ] Backend CI is re-verified after any new pushed commit.
- [ ] Sprint 3 remains deferred until TASK-0105 passes.

## Required Before Merge

- [ ] Latest PR head Backend CI is green.
- [ ] PR branch is up to date enough with base branch for safe merge.
- [ ] No unresolved critical documentation drift remains.
- [ ] No known failing validation is hidden.
- [ ] Deferred items are explicitly listed and not implied complete.
- [ ] Security-sensitive changes are reviewed if applicable.
- [ ] No secrets, tokens, credentials, or local-only paths are committed.
- [ ] Current scope is still aligned with `docs/MVP_SCOPE.md`.
- [ ] Product boundaries in `docs/ARCHITECTURE.md` are preserved.
- [ ] Outbound sending, scraping, CRM integration, auth, billing, and external integrations remain deferred unless explicitly assigned.

## Docs-Only PR/Commit Checklist

- [ ] Only documentation files changed.
- [ ] `git diff --check` passed.
- [ ] Backend tests were not claimed unless actually run.
- [ ] CI state is recorded conservatively.
- [ ] Any new docs are added to `docs/CONTEXT_INDEX.md`.
- [ ] `docs/CHANGELOG_AGENT.md` records the task.
- [ ] `docs/ACTIVE_TASKS.md` is updated if task status changed.

## Backend Change Checklist

- [ ] Format check passes.
- [ ] Lint passes.
- [ ] Tests pass locally or local blocker is recorded.
- [ ] GitHub Actions Backend CI passes.
- [ ] Error handling is explicit.
- [ ] Edge cases are covered.
- [ ] Tests cover expected and invalid inputs.
- [ ] No broad refactor is bundled unless assigned.

## Dependency / Tooling Change Checklist

- [ ] Dependency change is explicitly assigned.
- [ ] Reason for dependency change is documented.
- [ ] CI still installs dependencies cleanly.
- [ ] Lock/version implications are understood.
- [ ] No unused dependency added.

## Manual Verification Checklist

- [ ] Manual action is listed in `docs/MANUAL_ACTIONS.md`.
- [ ] Owner/user action is clear.
- [ ] Verification command or UI step is explicit.
- [ ] Blocking vs deferred status is clear.

## Agent Safety Rules

- Do not merge or recommend merge if latest PR head CI is unknown, pending, or failed.
- Do not treat historical docs as active instructions.
- Do not update PR status based on local assumptions.
- Do not hide local environment failures.
- Do not modify unrelated files to satisfy a checklist.
- Do not downgrade tests or CI to make a PR pass.
- Do not claim production readiness unless explicitly validated.

## Current Deferred Items

- local environment provisioning
- backlog reconciliation
- migrations
- reporting service
- scoring persistence
- audit persistence
- deployment
- authentication
- billing
- outbound sending
- CRM integration
- ProjectOS integration
- Content Creation Automation integration

## Related Files

- [`docs/ACTIVE_TASKS.md`](ACTIVE_TASKS.md)
- [`docs/MANUAL_ACTIONS.md`](MANUAL_ACTIONS.md)
- [`docs/VALIDATION_COMMANDS.md`](VALIDATION_COMMANDS.md)
- [`docs/LOCAL_ENVIRONMENT.md`](LOCAL_ENVIRONMENT.md)
- [`docs/CI_TROUBLESHOOTING.md`](CI_TROUBLESHOOTING.md)
- [`docs/DONE_CRITERIA.md`](DONE_CRITERIA.md)
- [`.github/workflows/backend-ci.yml`](../.github/workflows/backend-ci.yml)
- [`docs/MVP_SCOPE.md`](MVP_SCOPE.md)
- [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)
