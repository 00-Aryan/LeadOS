# Validation Commands

Run commands from the repository root unless the command changes directories.

For local Python setup, dependency installation, and common environment failures, read `docs/LOCAL_ENVIRONMENT.md`.

For GitHub Actions Backend CI failure diagnosis, read `docs/CI_TROUBLESHOOTING.md`.

For PR readiness and merge gate checks, read `docs/PR_CHECKLIST.md`.

## Backend Setup

```bash
cd backend
make install
```

## Backend Checks

One-command backend gate:

```bash
cd backend && make check
```

Individual backend gate steps:

```bash
cd backend
make format-check
make lint
make test
make check
```

## Common Fix Commands

```bash
cd backend
ruff format .
ruff check . --fix
make check
```

## Docs-Only Check

```bash
git diff --check
```

## Merge Gate

GitHub Actions must pass before merging. Do not claim CI passes unless the relevant workflow run has been verified.
