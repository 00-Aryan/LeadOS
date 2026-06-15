# File Ownership

| Path | Responsibility |
|---|---|
| `backend/app/schemas` | API request/response contracts and typed service payloads. |
| `backend/app/models` | SQLAlchemy ORM models and persisted table shape. |
| `backend/app/repositories` | Database access patterns and persistence operations. |
| `backend/app/services` | Business logic for import, audit, scoring, outreach, and evaluation. |
| `backend/app/routers` | FastAPI route boundaries and dependency wiring. |
| `backend/tests` | Backend regression tests, service tests, repository tests, and route tests. |
| `docs` | Product, architecture, workflow, risk, and operating documentation. |
| `.github/workflows` | GitHub Actions CI configuration. |
| `data` | Sample input data and future local fixtures. |
