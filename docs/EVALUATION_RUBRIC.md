# Evaluation Rubric

## Objective

The evaluation layer scores outreach drafts before human use. It is a guardrail, not a cosmetic review step.

## Score dimensions

Each dimension is scored from 0 to 10.

```text
relevance
personalization
clarity
tone
truthfulness
cta_quality
```

The total score is out of 60.

## Risk rating

Risk is separate from score.

```text
low
medium
high
```

A high-risk draft requires manual revision even if the numeric score is high.

## Required output

```text
score_breakdown
total_score
risk_rating
pass_or_review
failure_reasons
bad_lines
suggested_revision
```

## Automatic review triggers

A draft must be marked review_required when it includes:

- Unsupported claims
- Overpromising
- Manipulative pressure
- Fake familiarity
- Irrelevant personalization
- Confusing CTA
- Too much length for the channel

## Pass condition

A draft passes only if:

- Total score is at least 45 out of 60
- Risk rating is low or medium
- Truthfulness is at least 8
- CTA quality is at least 7
