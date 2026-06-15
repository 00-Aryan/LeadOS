# Local Environment Setup

## Purpose

This file exists to make local backend validation reproducible for humans and AI agents. Future sessions should use it to provision Python, install backend dependencies, and run the same validation commands that GitHub Actions runs for PR checks.

## Current Reference Environment

- Python version: `3.12`, from `backend/.python-version` and GitHub Actions `actions/setup-python`.
- Dependency source: `backend/requirements.txt`.
- Validation commands: `make format-check`, `make lint`, `make test`, or `make check` from `backend`.
- CI workflow reference: `.github/workflows/backend-ci.yml`.

## Quick Start

```bash
cd /path/to/LeadOS
cd backend
python --version
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
make format-check
make lint
make test
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Recommended Python Setup

The backend expects Python `3.12`. This comes from `backend/.python-version`, and CI uses Python `3.12` in `.github/workflows/backend-ci.yml`.

For pyenv users:

```bash
pyenv install 3.12
cd backend
pyenv local 3.12
python --version
```

For system Python users:

```bash
python3.12 --version
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

For venv users:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Do not assume one setup method is required everywhere. The important requirement is that `python --version` inside the active backend environment reports Python 3.12 and dependencies from `backend/requirements.txt` are installed.

## Dependency Installation

Dependencies are installed from:

```text
backend/requirements.txt
```

Use:

```bash
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Validation Commands

Canonical local commands:

```bash
cd backend
make format-check
make lint
make test
```

Full check:

```bash
cd backend
make check
```

## Common Local Failures and Fixes

| Symptom | Likely Cause | Fix |
| ------- | ------------ | --- |
| `pyenv: version '3.12' is not installed` | `backend/.python-version` selects Python 3.12, but pyenv does not have it installed. | Run `pyenv install 3.12`, or use a system `python3.12` to create and activate `.venv`. |
| `No module named pytest` | Backend dependencies were not installed in the active Python environment. | Activate the intended virtual environment and run `python -m pip install -r requirements.txt` from `backend`. |
| `ruff: No such file or directory` | Ruff is not installed or the virtual environment is not active. | Activate `.venv`, install `backend/requirements.txt`, then rerun `make format-check` or `make lint`. |
| `ModuleNotFoundError: app` | Tests are being run outside the backend context or without `PYTHONPATH=.`. | Run tests with `cd backend && make test`, which sets `PYTHONPATH=.`. |
| SQLite/data directory errors | Local database path or parent directory may not exist or may not be writable. | Confirm the configured SQLite path and parent directory are writable; rerun tests through the backend test fixtures. |
| `make` not available on some systems | The OS does not include GNU Make by default. | Install `make`, or run equivalent commands manually: `ruff format --check .`, `ruff check .`, and `PYTHONPATH=. pytest` from `backend`. |

## GitHub Actions as Source of Truth

GitHub Actions is the required PR validation gate. Local validation is preferred because it catches problems before push, but local environments are not always equivalent to CI.

If local tests cannot run, the agent must not claim local tests passed. Record the exact local environment failure and rely on GitHub Actions only when the relevant workflow run has been verified.

Current verified PR state: Backend CI succeeded at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`, run #60 / `27554650321`.

If a newer commit exists, CI must be re-verified before merging or starting non-cleanup feature work.

## Agent Rules for Local Validation

- Do not mark tests as passed if they did not run.
- Record exact environment failures.
- Use `docs/MANUAL_ACTIONS.md` when user action is required.
- Prefer fixing environment docs before changing code if the failure is local setup only.
- Do not modify dependencies unless explicitly assigned.

## Manual Work

### Required now

None, unless a newer commit is pushed and CI has not completed.

### Required before merge

GitHub Actions Backend CI must be green for the latest PR head commit.

### Can be deferred

- Local setup automation beyond this documentation.
- CI troubleshooting guide.
- PR checklist.
- Production deployment environment setup.

## Related Files

- `backend/.python-version`
- `backend/requirements.txt`
- `backend/Makefile`
- `backend/ruff.toml`
- `backend/pytest.ini`
- `.github/workflows/backend-ci.yml`
- `docs/VALIDATION_COMMANDS.md`
- `docs/MANUAL_ACTIONS.md`
