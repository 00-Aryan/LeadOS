# GitHub Issues To Create Later

> **Status:** Historical/backlog reference, not the active task source of truth.
> Do not execute tasks from this document without checking `docs/CHANGELOG_AGENT.md`, GitHub issues, and the current PR state.
> For current agent workflow, read `AGENTS.md` and `docs/WORKFLOW.md`.
>
> **CI note:** PR #1 Backend CI was externally verified as passing at commit `eda102a7286e00acb6d874411e238245c1a1c65c`, run #54 (`27545766287`). If newer commits exist, verify CI again before merging.

## Completed/fixed issues

### Fix Sprint 1 missing backend skeleton

Labels:

```text
sprint-1, backend, tests, fixed
```

Summary:

```text
Added missing FastAPI app, health endpoint, lead import route, list route, tests, dependencies, pytest config and Makefile.
```

### Fix Sprint 2 broken SQL data layer

Labels:

```text
sprint-2, database, data-quality, fixed
```

Summary:

```text
Fixed Pydantic v2 settings issue, added SQLAlchemy models, repository layer, import run tracking, rejected-row persistence and deterministic transformations.
```

## Remaining issues

### Add Alembic migrations

Labels:

```text
enhancement, database, migration, sprint-2
```

### Add SQL extraction/reporting service

Labels:

```text
enhancement, sql, analytics, sprint-2
```

### Add CI workflow

Labels:

```text
enhancement, ci, backend, tests
```
