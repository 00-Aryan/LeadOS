# Decisions

## ADR-001 LeadOS Remains Standalone

LeadOS is a standalone lead intelligence platform. It must remain separate from ProjectOS and the Content Creation Automation tool during the MVP.

## ADR-002 No Scraping/Crawling in MVP

The MVP must not include scraping or crawling. CSV import and deterministic checks are the initial data path.

## ADR-003 SQLite for Local Development, PostgreSQL Later

SQLite remains the local development database. PostgreSQL is the expected production target after migrations are introduced.

## ADR-004 SQLAlchemy Is the Persistence Layer

SQLAlchemy is the persistence layer for ORM models, sessions, and repository-backed storage behavior.

## ADR-005 Deterministic Audit/Scoring Before AI

Deterministic audit and explainable scoring must exist before any AI-assisted workflow is added.

## ADR-006 Outreach Is Draft-Only; No Sending

Outreach output is draft-only in the MVP. LeadOS must not send emails, messages, or automated outbound communication.

## ADR-007 CI Failure Blocks Feature Work

Formatting, lint, test, or CI failures block new feature work. Fix the validation failure first.
