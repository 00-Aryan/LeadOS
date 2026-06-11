# LeadOS Product Specification

## Product thesis

LeadOS is a standalone lead intelligence product for local-business prospecting. It helps a user import business leads, audit visible digital gaps, score outreach opportunity, prepare personalized outreach drafts, and evaluate those drafts before human use.

The product is not a scraper-first tool. The core value is the intelligence loop: evidence-backed lead qualification, transparent scoring, and safe outreach preparation.

## Target user

The initial user is a solo operator, freelancer, agency founder, or small SaaS builder who wants to identify local businesses that likely need digital improvement services.

## Primary problem

Raw lead lists are noisy. Business names, phone numbers, ratings, and websites are not enough to decide who to contact. LeadOS should turn raw leads into explainable outreach opportunities.

## MVP workflow

```text
CSV import -> validation -> website audit -> scoring -> outreach draft -> evaluation -> manual review
```

## MVP modules

1. Lead import
2. Lead storage
3. Deterministic website audit
4. Explainable scoring
5. Outreach draft generation
6. Outreach evaluation

## Non-goals

The MVP must not include external product integrations, CRM replacement features, payment systems, marketplace features, automatic message sending, or complex model training.

## Future integration constraints

LeadOS should remain future-compatible with project-management, content-creation, CRM, and email systems through clean module boundaries and structured outputs.

## Product quality bar

Every product loop must have typed input, explainable processing, structured output, evaluation criteria, a human review path, and clear failure handling.
