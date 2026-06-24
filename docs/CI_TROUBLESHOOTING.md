# CI Troubleshooting

## Purpose

This document helps humans and AI agents diagnose GitHub Actions Backend CI failures without broad, unrelated changes. Use it to identify the failing step, reproduce only that failure category locally when possible, and avoid bundling feature work into CI repair.

## Backend CI Overview

Backend CI is defined in `.github/workflows/backend-ci.yml`.

- Trigger conditions: runs on pushes to `main` and `phase-0-product-foundation`, and on pull requests targeting `main`.
- Python version: `3.12`, configured through `actions/setup-python@v5` and aligned with `backend/.python-version`.
- Dependency installation: `make install`, which upgrades pip and installs `backend/requirements.txt`.
- Working directory: all run steps execute from `backend`.
- Validation steps: `make format-check`, `make lint`, and `make test`.
- Expected success path: checkout succeeds, Python 3.12 is installed, dependencies install from `requirements.txt`, Ruff formatting passes, Ruff lint passes, and pytest passes with `PYTHONPATH=.`.

## Canonical CI Steps

| Step | What It Checks | Local Equivalent | Common Failure Type |
|---|---|---|---|
| Checkout | Repository contents can be fetched for the workflow run. | `git status --short` and `git rev-parse HEAD` | GitHub permissions, missing branch, stale or unexpected commit |
| Python setup | Python 3.12 is available and pip cache can be prepared. | `cd backend && python --version` | Python version mismatch or unavailable interpreter |
| Dependency install | Backend dependencies install from `backend/requirements.txt`. | `cd backend && make install` | Missing package, resolver failure, network/package index issue |
| Format check | Ruff formatting matches repository rules. | `cd backend && make format-check` | Unformatted Python files |
| Lint | Ruff lint rules pass. | `cd backend && make lint` | Import ordering, unused code, bugbear, pyupgrade, simplification, or syntax issues |
| Tests | Pytest collection and test execution pass. | `cd backend && make test` | Assertion failure, fixture failure, import path failure, collection error |

## Failure Diagnosis Flow

1. Identify failing CI step.
2. Read only the logs for the failing step.
3. Map failure to local equivalent command.
4. Reproduce locally if environment is available.
5. Fix only the failure category.
6. Re-run validation.
7. Do not start unrelated feature work.

## Common CI Failures

| CI Symptom | Likely Cause | Correct Fix | Do Not Do |
|---|---|---|---|
| `make format-check` fails | Python files are not Ruff-formatted. | Run `cd backend && ruff format .`, inspect the diff, and keep only intended formatting changes. | Do not change logic to make formatting pass. |
| `make lint` fails | Ruff found a rule violation. | Read the exact rule, fix the smallest affected scope, then rerun `make lint`. | Do not suppress or disable rules unless explicitly assigned. |
| `make test` fails | A test assertion, fixture, import, or runtime behavior failed. | Identify the failing test and fix the product bug or justified test issue. | Do not weaken tests just to make CI green. |
| `ModuleNotFoundError` | Dependencies are missing or tests are not running with the backend import path. | Install `backend/requirements.txt` and run tests through `cd backend && make test`. | Do not add imports hacks or change package layout without scope. |
| Missing dependency | Dependency install did not run, used wrong environment, or a truly required package is absent. | Confirm `make install` ran against the intended Python environment; only update requirements if the task explicitly requires it. | Do not casually add dependencies. |
| Python version mismatch | Local or CI Python is not 3.12. | Use Python 3.12 as specified by `backend/.python-version` and CI. | Do not change CI Python version to match a local machine. |
| Import path failure | Command ran outside `backend` or without `PYTHONPATH=.`. | Use `cd backend && make test`, which sets `PYTHONPATH=.`. | Do not rewrite imports before checking command context. |
| Pytest collection failure | Syntax error, missing import, fixture error, or incompatible test setup. | Read the first collection error and fix that root cause. | Do not skip whole test modules without explicit justification. |
| Backend working directory mismatch | Command was run from repository root while CI runs backend commands from `backend`. | Run the Makefile command from `backend`. | Do not change CI working directory unless the workflow itself is wrong. |
| Local passes but CI fails | CI has a cleaner environment, Python 3.12, different OS, or missing local-only state. | Compare the failing CI step with the exact local command and inspect environment assumptions. | Do not assume CI is flaky without evidence. |
| CI passes but local fails | Local Python, dependencies, Make, path, or OS setup differs from CI. | Use `docs/LOCAL_ENVIRONMENT.md` to fix local setup or record the exact local blocker. | Do not claim local validation passed if it did not run. |

## Formatting Failures

Use:

```bash
cd backend
make format-check
```

If formatting fails, the safe local fix command available from the Makefile context is:

```bash
cd backend
ruff format .
make format-check
```

Only keep formatting changes for intended files. Do not reformat unrelated files just because they are nearby. Do not change logic to fix formatting.

## Lint Failures

Use:

```bash
cd backend
make lint
```

Read the exact Ruff rule and the file/line reported in the CI log. Fix the smallest scope that satisfies the rule, then rerun lint. Do not suppress rules, change `backend/ruff.toml`, or add ignores unless the assigned task explicitly asks for that.

## Test Failures

Use:

```bash
cd backend
make test
```

Identify the failing test, read the assertion and fixture context, and inspect the code under test before editing. Distinguish a product bug from a test bug. Do not weaken tests without justification. If local environment setup blocks testing, record the exact command and error, then update `docs/MANUAL_ACTIONS.md` when human verification is required.

## Dependency Failures

Backend dependencies come from:

```text
backend/requirements.txt
```

Do not add dependencies unless the task explicitly requires it. If a missing dependency is already listed in `requirements.txt`, fix install/setup first. If a new dependency is truly necessary, document why before modifying requirements and keep that change in a task that allows dependency edits.

## GitHub Actions vs Local Validation

GitHub Actions is the PR validation source of truth. Local validation should mirror CI, but it may fail due to local machine setup, missing Python 3.12, missing Make, inactive virtual environments, or dependency installation gaps.

If local validation cannot run, agents must record the exact blocker. Do not claim local tests passed unless they ran. Do not claim latest CI passed unless the relevant GitHub Actions workflow run has been verified.

## Agent Safety Rules

- Fix only the failing CI category.
- Do not bundle feature work into CI repair.
- Do not change CI workflow unless CI config itself is the failing artifact.
- Do not update dependencies casually.
- Do not mark PR ready if latest head CI is not green.
- Update `docs/MANUAL_ACTIONS.md` if human verification is required.
- Update `docs/ACTIVE_TASKS.md` when CI blocks task execution.

## Current CI State

- PR: #1
- Branch: `phase-0-product-foundation`
- Latest verified CI: Backend CI passed at commit `59e999b4135e393a1bb3768a11fe8ba79c18791e`, run #60 / `27554650321`.
- Current local HEAD: `abfddf741f1f7c8765afd718b43e1f511377e94d`
- GitHub CLI check during TASK-0008: `gh pr checks 1` and `gh run list --branch phase-0-product-foundation --workflow "Backend CI" --limit 5` could not connect to `api.github.com`.

```text
Current local HEAD is newer than the last verified CI commit. CI must be re-verified after push.
```

## Related Files

- [`.github/workflows/backend-ci.yml`](../.github/workflows/backend-ci.yml)
- [`backend/Makefile`](../backend/Makefile)
- [`backend/.python-version`](../backend/.python-version)
- [`backend/requirements.txt`](../backend/requirements.txt)
- [`backend/ruff.toml`](../backend/ruff.toml)
- [`backend/pytest.ini`](../backend/pytest.ini)
- [`docs/LOCAL_ENVIRONMENT.md`](LOCAL_ENVIRONMENT.md)
- [`docs/VALIDATION_COMMANDS.md`](VALIDATION_COMMANDS.md)
- [`docs/MANUAL_ACTIONS.md`](MANUAL_ACTIONS.md)
- [`docs/ACTIVE_TASKS.md`](ACTIVE_TASKS.md)
