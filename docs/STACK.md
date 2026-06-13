# LeadOS Stack

## Rule

Use current and reliable tools that support the core LeadOS loop.

## Backend

- Python 3.12
- FastAPI
- Pydantic v2
- pytest
- Ruff
- uv

## Why

LeadOS needs typed API contracts, strict validation, fast tests, and simple CI.

## CI checks

Run these checks for backend changes:

```text
ruff format --check
ruff check
pytest
```

## Keep deferred

- Scraping
- CRM sync
- ProjectOS sync
- Content tool sync
- Billing
- Deployment

## Current product loop

```text
CSV import -> audit -> scoring -> outreach draft -> evaluation
```
