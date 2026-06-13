# Tooling Notes

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
