# LeadOS Task Backlog

## Phase 0: Product Foundation

### TASK-0001: Define product boundary

Status: Done

Deliverables:

- Product thesis
- MVP scope
- Non-goals
- Future integration constraints

Acceptance criteria:

- LeadOS is clearly separate from ProjectOS and other tools.
- Future integrations are named but not implemented.
- MVP can be explained in one workflow.

### TASK-0002: Define target customer segment

Status: Pending

Deliverables:

- Primary niche
- Backup niche
- Pain point
- Data availability notes

Recommended first niche: local clinics and dentists.

### TASK-0003: Define MVP workflow

Status: In progress

Workflow:

```text
CSV import -> validation -> audit -> score -> draft -> evaluate -> manual review
```

### TASK-0004: Define expert review gates

Status: In progress

Review gates:

- Lead quality review
- Audit accuracy review
- Scoring logic review
- Outreach quality review
- Product scope review

## Phase 1: Data Model and Architecture

### TASK-0101: Design database schema

Status: Pending

Tables:

- leads
- lead_audits
- lead_scores
- outreach_drafts
- draft_evaluations
- source_runs

### TASK-0102: Define API contract

Status: Pending

Initial endpoints:

```text
GET /health
POST /leads/import
GET /leads
GET /leads/{lead_id}
POST /leads/{lead_id}/audit
POST /leads/{lead_id}/score
POST /leads/{lead_id}/outreach
POST /outreach/{draft_id}/evaluate
```

### TASK-0103: Define internal service boundaries

Status: Pending

Services:

- lead_import_service
- audit_service
- scoring_service
- outreach_service
- evaluation_service

## Phase 2: Lead Import MVP

### TASK-0201: Define CSV source strategy

Status: Pending

Start with CSV input before scraping.

### TASK-0202: Define lead CSV format

Status: Pending

Columns:

```text
business_name,category,city,state,phone,website,rating,review_count,address,source_url
```

### TASK-0203: Build lead import validator

Status: Pending

Validation must reject invalid rows with clear reasons.

## Phase 3: Website Audit MVP

### TASK-0301: Define audit rubric

Status: Done

### TASK-0302: Build website fetcher

Status: Pending

### TASK-0303: Build deterministic audit checks

Status: Pending

## Phase 4: Scoring MVP

### TASK-0401: Define scoring rubric v1

Status: Done

### TASK-0402: Build scoring function

Status: Pending

### TASK-0403: Create scoring test cases

Status: Pending

## Phase 5: Outreach MVP

### TASK-0501: Define outreach structure

Status: Done

### TASK-0502: Build outreach prompt/template

Status: Pending

### TASK-0503: Generate first sample outreach set

Status: Pending

## Phase 6: Evaluation and Guardrails

### TASK-0601: Define evaluation rubric

Status: Done

### TASK-0602: Build evaluator template

Status: Pending

### TASK-0603: Create expert review checklist

Status: Pending
