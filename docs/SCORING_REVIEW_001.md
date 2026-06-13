# Scoring Review 001

## Scope

This review covers the first deterministic LeadOS scoring function.

The scoring function converts lead data and website audit output into an explainable opportunity score.

## Primary risks

### False confidence

A score can look more precise than it really is. LeadOS must show missing data, confidence level, and risk flags with every score.

### Hidden bias

Category-based commercial fit can unfairly over-prioritize some niches. The first version uses explicit category rules instead of hidden model behavior.

### Misuse as conversion prediction

The score is an outreach opportunity score. It is not a conversion probability, revenue estimate, or business quality guarantee.

### Overfitting to the first niche

The first target niche is clinics and dentists, but the service must remain configurable later.

## Controls added

- Deterministic scoring only.
- No AI judgment used in scoring.
- Category scores are returned separately.
- Missing data is returned explicitly.
- Risk flags are returned explicitly.
- Confidence level is separate from score.
- Priority is downgraded to review_needed when confidence is low.
- Reason summary explains why the score was assigned.

## Current limitations

- Weights are heuristic and need calibration with real outcomes.
- Category commercial value is hardcoded.
- No tenant-specific scoring configuration exists yet.
- No reviewer feedback loop exists yet.
- No historical conversion data exists yet.

## Required future hardening

- Store score runs with versioned scoring rules.
- Add reviewer feedback fields.
- Add calibration against real outreach outcomes.
- Add configuration per niche.
- Add score distribution monitoring.

## Product boundary

No scraping, crawling, outbound automation, CRM sync, ProjectOS sync, content-tool sync, or AI-based scoring was added.
