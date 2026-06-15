# Validation Commands

Run commands from the repository root unless the command changes directories.

## Backend Setup

```bash
cd backend
make install
```

## Backend Checks

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
