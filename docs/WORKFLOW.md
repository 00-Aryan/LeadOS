# Agent Workflow

This workflow applies to future Codex and AI-agent execution in this repository.

## Planning Mode

Before editing:

- Read `AGENTS.md`.
- Read `docs/CONTEXT_INDEX.md`.
- Read the assigned issue or task.
- Inspect files likely to be affected.
- Check current git status.
- Identify whether CI, formatting, lint, or tests are already failing.
- Produce a short implementation plan.

If CI or local validation is failing, fix that failure before adding more feature scope.

## Implementation Mode

During edits:

- Make the smallest safe change.
- Stay inside the assigned scope.
- Preserve existing product boundaries.
- Prefer established patterns in `backend/app`.
- Do not implement unrelated features.
- Do not add scraping, crawling, outbound sending, CRM integration, ProjectOS integration, Content Creation Automation integration, deployment, auth, billing, or AI calls unless explicitly assigned.
- Update docs only when behavior, workflow, or operating rules change.

## Validation Mode

Run the narrowest useful checks first, then the full gate when practical.

Backend gate:

```bash
cd backend
make format-check
make lint
make test
```

Full backend gate:

```bash
cd backend
make check
```

For docs-only changes, run at least:

```bash
git diff --check
```

GitHub Actions must pass before merge.

## Failure Mode

If formatting fails, fix formatting before continuing:

```bash
cd backend
ruff format .
make format-check
```

If lint fails, fix lint before adding features.

If tests fail, stop feature work and fix or report the failure with logs and affected tests.

If validation cannot run because of environment limits, report the exact command, error, and what must be run manually. Do not mark the task done unless the remaining validation gap is explicitly called out.

## Reporting Mode

Every final report must include:

- Files created.
- Files updated.
- Commands run.
- Validation result.
- Manual work required.
- Risks remaining.
- Next recommended task.

Do not hide manual work or deferred validation. Do not claim CI passes unless it was verified.
