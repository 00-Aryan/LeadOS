# LeadOS

LeadOS is a standalone lead intelligence product for finding local business prospects, auditing their digital presence, scoring outreach opportunity, and preparing reviewed outreach drafts.

This repository is intentionally separate from ProjectOS and the existing content-creation tool. Future integrations should remain possible through clean APIs and structured outputs, but they are not part of the initial build.

## Initial build principle

Each loop must be independently testable:

1. Lead import
2. Website audit
3. Lead scoring
4. Outreach drafting
5. Outreach evaluation

The first implementation path is:

```text
CSV import -> deterministic audit -> explainable score -> outreach draft -> evaluator
```

Scraping, CRM integration, ProjectOS integration, content-tool integration, authentication, payment, and automated sending are deferred.
