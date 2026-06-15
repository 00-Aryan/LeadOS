# Risk Register

| Risk | Impact | Current control | Future mitigation | Status |
|---|---|---|---|---|
| SSRF risk | Website audit could be abused to access internal or unsafe URLs. | No scraping/crawling in MVP; deterministic audit scope is constrained. | Add URL allow/deny rules, network egress controls, timeouts, and SSRF tests before network fetching expands. | Open |
| Unsupported outreach claims | Drafts may make claims not supported by lead or audit evidence. | Outreach is draft-only and evaluation must flag risk. | Enforce evidence-linked claims and add evaluator tests for unsupported claims. | Open |
| Score false authority | Users may over-trust numeric scores. | Scoring is explainable and should include confidence and missing data. | Add calibration notes, score disclaimers, and review workflows. | Open |
| Weak dedupe | Duplicate leads may pass through when names or cities vary. | Normalized business name plus normalized city uniqueness rule. | Add richer dedupe keys, review queues, and source-level reconciliation. | Open |
| Missing migrations | Schema changes may be hard to apply consistently. | SQLite local development and documented data model. | Add Alembic or equivalent migration tooling before production. | Open |
| CI instability | Formatting, lint, or test drift can block PRs. | Backend CI runs install, format, lint, and tests. | Keep validation commands documented and fix CI before feature work. | Open |
| Schema drift | Docs, schemas, ORM models, and tests may diverge. | Data model and context index identify ownership. | Add migration tests and schema review checklist. | Open |
| Manual work invisibility | Agents may omit deployment, CI, or review steps from reports. | Required final report includes manual work. | Add PR checklist and issue template enforcement. | Open |
| Scope drift | Agents may add deferred integrations or features too early. | `AGENTS.md`, MVP scope, and ADRs forbid deferred areas unless assigned. | Add review gate for any scope expansion. | Open |
