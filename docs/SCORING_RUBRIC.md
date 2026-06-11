# Scoring Rubric

## Objective

The scoring engine ranks leads by outreach opportunity. It must be deterministic, explainable, and safe under missing data.

## Total score

The total score is out of 100.

```text
business_strength: 0-25
digital_gap: 0-30
contactability: 0-20
commercial_fit: 0-15
outreach_priority: 0-10
```

## Business strength

Signals include rating, review count, category relevance, and evidence that the business is active.

## Digital gap

Signals include missing website, weak website basics, missing contact path, missing booking path, missing social links, and weak SEO basics.

A strong business with a weak digital presence is a strong opportunity.

## Contactability

Signals include phone number, website contact page, email, WhatsApp link, booking link, and clear address.

## Commercial fit

Signals include whether the niche can realistically pay for digital improvement and whether the service gap is commercially meaningful.

## Outreach priority

Signals include urgency, simplicity of the pitch, and confidence that the user can offer a relevant improvement.

## Output format

Every score must return:

```text
total_score
category_scores
priority_label
confidence_level
reason_summary
risk_flags
missing_data
```

## Priority labels

```text
high
medium
low
review_needed
```

## Guardrails

- Missing data must reduce confidence.
- A score without explanation is invalid.
- AI judgment must not silently change deterministic scoring.
- Risk flags must be visible.
