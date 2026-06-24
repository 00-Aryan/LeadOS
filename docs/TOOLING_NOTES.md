# Tooling Notes

> **Status:** Historical reference.
> This document may describe earlier implementation state, task planning, or validation status.
> For current agent instructions and repository state, read `AGENTS.md`, `docs/CONTEXT_INDEX.md`, and `docs/CHANGELOG_AGENT.md` first.
>
> **CI note:** PR #1 Backend CI was externally verified as passing at commit `eda102a7286e00acb6d874411e238245c1a1c65c`, run #54 (`27545766287`). If newer commits exist, verify CI again before merging.

## Selected baseline

- Python 3.12
- FastAPI
- Pydantic v2
- pytest
- Ruff
- GitHub Actions later

## Why this order

The project should first protect the backend feedback loop. The next implementation work should remain close to the LeadOS idea and should not expand into integrations.

## Known limitation

Workflow file creation was not completed from this environment. The backend now has local command support through the Makefile and test configuration.
