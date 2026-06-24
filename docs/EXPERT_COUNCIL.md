# LeadOS Expert Council

## Purpose

The expert council is a design and review mechanism for keeping LeadOS scalable, testable, and commercially useful. It prevents feature stacking by requiring every task to declare owner perspective, constraints, acceptance criteria, and review gates before implementation.

## Council roles

### Product Strategist

Owns market fit, MVP boundaries, and user value. Rejects features that make the product larger without strengthening the core loop.

### Backend Architect

Owns API boundaries, service isolation, error handling, maintainability, and future integration readiness.

### Data Quality Engineer

Owns input validation, normalization, missing-data behavior, duplicate handling, confidence flags, and explainability of data transformations.

### Audit Specialist

Owns website audit rubric, evidence capture, true/false/unknown decisions, and prevention of unsupported inference.

### Scoring Specialist

Owns scoring logic, deterministic rules, weight explainability, confidence handling, and risk flags.

### AI Safety and Outreach Reviewer

Owns outreach truthfulness, brand safety, tone, unsupported-claim detection, and manual-review triggers.

### QA Engineer

Owns unit tests, edge cases, regression tests, API behavior tests, and acceptance criteria verification.

### Security and Compliance Reviewer

Owns data handling, safe outbound constraints, privacy boundaries, rate-limit awareness, and prevention of spam-like automation.

## Task design rule

Every task must define:

```text
goal
owner roles
constraints
inputs
outputs
acceptance criteria
failure cases
tests
review gate
```

## Architecture rule

No service should silently perform another service's job.

- Import validates and normalizes data.
- Audit checks evidence.
- Scoring ranks opportunity.
- Outreach drafts messages.
- Evaluation reviews drafts.

## Scalability rule

Phase 1 may use in-memory or stateless processing, but interfaces must not block later persistence, async jobs, tenant fields, or integration consumers.

## Coding standard

- Prefer typed functions.
- Prefer small deterministic services.
- Return structured errors.
- Do not hide partial failures.
- Do not crash on bad user data.
- Keep AI-dependent behavior behind explicit service boundaries.
- Test edge cases before expanding features.
