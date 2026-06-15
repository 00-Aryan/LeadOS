# LeadOS Agent Operating Instructions

## Project Identity

LeadOS is a standalone lead intelligence platform for importing local-business leads, auditing visible digital-presence gaps, scoring outreach opportunity, preparing outreach drafts, and evaluating those drafts before human use.

LeadOS is intentionally separate from ProjectOS and the existing content-creation automation tool. Future integrations may be designed through clean APIs and structured outputs, but they are not part of the MVP unless explicitly assigned.

## MVP Loop

```text
CSV import -> deterministic website audit -> explainable scoring -> outreach draft -> evaluator
```

## Current Execution Rule

Do not start new feature work if CI is failing. Fix formatting, lint, tests, or broken CI configuration first, then proceed only after the repository is back to a verifiable state.

## Required Agent Workflow

For every assigned task:

1. Read `AGENTS.md`.
2. Read `docs/CONTEXT_INDEX.md`.
3. Read the assigned issue or task.
4. Inspect affected files before editing.
5. Produce a short implementation plan.
6. Make the smallest safe change that satisfies scope.
7. Run validation.
8. Report files changed, commands run, result, risks, and manual work.

## Hard Constraints

- Do not add scraping or crawling.
- Do not add outbound sending.
- Do not add CRM integration.
- Do not add ProjectOS integration.
- Do not add Content Creation Automation integration.
- Do not add AI calls unless explicitly assigned.
- Do not modify unrelated files.
- Do not mark a task done if validation fails.
- Do not hide manual work from the user.

## Backend Validation Commands

Run these from a clean working tree when backend behavior or shared Python code is touched:

```bash
cd backend
make format-check
make lint
make test
```

If formatting fails:

```bash
cd backend
ruff format .
make format-check
```

For a full backend gate:

```bash
cd backend
make check
```

## Required Final Report Format

Every agent task must end with this structure:

```text
TASK-XXXX REPORT

Files created:
- ...

Files updated:
- ...

Commands run:
- ...

Validation result:
- ...

Manual work required:
- Required now: ...
- Can be deferred: ...

Risks remaining:
- ...

Next recommended task:
- ...
```

If validation could not be run, explain the exact blocker and do not claim the task is complete.
