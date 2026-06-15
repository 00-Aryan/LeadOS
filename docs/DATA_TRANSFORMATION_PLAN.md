# Data Transformation Plan

## Current transformations

LeadOS currently transforms raw CSV rows before persistence.

## Transform rules

| Field | Transformation | Failure behavior |
|---|---|---|
| business_name | trim and collapse whitespace | required |
| category | trim and collapse whitespace | required |
| city | trim and collapse whitespace | required |
| normalized fields | casefolded normalized text | derived |
| phone | remove spaces and separators, preserve leading plus | optional |
| rating | parse float | reject if non-numeric or outside 0-5 |
| review_count | parse integer | reject if non-integer or negative |
| website | trim | reject if not http/https |

## Why this matters

This makes the project a data product rather than a simple API. It demonstrates:

```text
input validation
data cleaning
normalization
deduplication
import quality tracking
SQL persistence
```

## Next extraction queries

Implement these in a query/report service later:

```text
leads by city/category
leads missing website
high review count + weak digital presence
leads needing manual review
score distribution by category
import quality summary
missing-data report
```
