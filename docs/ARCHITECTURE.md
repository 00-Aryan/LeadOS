# Architecture

## Architecture principle

LeadOS must be built as independent loops, not as one tangled pipeline.

```text
Input -> Processing -> Output -> Evaluation -> Review -> Improvement
```

Each service should accept structured input and return structured output. Future integrations can consume these outputs without rewriting core logic.

## Service boundaries

### Lead import service

Responsible for parsing, validating, and normalizing incoming lead rows.

### Audit service

Responsible for deterministic digital-presence checks. It should not score the lead and should not generate outreach.

### Scoring service

Responsible for converting lead and audit data into an explainable score.

### Outreach service

Responsible for preparing draft messages from known lead facts and audit findings.

### Evaluation service

Responsible for scoring outreach quality, risk, truthfulness, clarity, and personalization.

## Initial backend shape

```text
backend/app/main.py
backend/app/config.py
backend/app/database.py
backend/app/models/
backend/app/schemas/
backend/app/services/
backend/app/routers/
backend/app/tests/
```

## Future-compatible fields

The data model may include optional future fields such as tenant_id, source_run_id, confidence_score, and review_status. These fields should not force full multi-tenancy or enterprise workflow in the MVP.

## Dependency rule

- Import must not depend on audit.
- Audit must not depend on scoring.
- Scoring must not depend on outreach.
- Outreach must not bypass evaluation.
- Evaluation must be able to run on any draft.
