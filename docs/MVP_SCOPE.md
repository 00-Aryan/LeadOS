# MVP Scope

## MVP objective

Build the smallest useful version of LeadOS that can convert a raw local-business lead into a reviewed outreach opportunity.

## In scope

- CSV-based lead import
- Lead validation
- Basic persistence model
- Deterministic website audit checks
- Explainable lead scoring
- Outreach draft structure
- Evaluation rubric for outreach quality and risk
- Backend skeleton with clear service boundaries

## Out of scope

- Scraping and crawling at scale
- CRM integration
- Project management integration
- Content platform integration
- Automatic outbound sending
- Authentication and billing
- Advanced machine learning
- Multi-user enterprise features

## First usable workflow

```text
Upload or load CSV
Validate rows
Store valid leads
Run audit per lead
Score lead opportunity
Generate outreach draft
Evaluate draft
Return reviewed output
```

## First target niche

The first recommended niche is local clinics and dentists. This niche usually has visible digital-presence signals, appointment intent, review data, and clear commercial value.

## MVP success criteria

- A sample CSV can be imported.
- Invalid lead rows return clear errors.
- Audit checks return true, false, or unknown.
- Lead score is reproducible and explainable.
- Outreach drafts never include unsupported claims.
- Evaluation flags risky or low-quality outreach.
