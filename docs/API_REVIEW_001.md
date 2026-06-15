# API Review 001: Scoring Preview

## Scope

This review covers the stateless scoring preview API.

Endpoint:

```text
POST /scoring/preview
```

## Purpose

Expose the deterministic scoring loop through an API boundary without adding persistence, external integrations, or background jobs.

## Security and misuse risks

### False authority

A score can appear more objective than it is. The response must include confidence, risk flags, missing data, and reason summary.

### Data persistence assumptions

This endpoint does not save data. It should not be described as a CRM or lead database operation.

### Overposting

The request accepts only the typed lead and audit schemas. Unknown fields are handled by Pydantic behavior and should be reviewed before production hardening.

### Abuse through large payloads

Large request payload limits are not implemented yet. API gateway or application-level body limits should be added before public deployment.

## Controls added

- Stateless route.
- Typed request model.
- Typed response model.
- No external network access.
- No AI call.
- No persistence side effect.
- Invalid payloads return validation errors.

## Current limitations

- No auth.
- No rate limiting.
- No payload size limit.
- No request logging policy.
- No versioned scoring rule identifier in the response yet.

## Product boundary

This endpoint exists only to expose the current LeadOS core loop:

```text
lead + audit -> explainable score
```

It does not add scraping, outreach automation, CRM sync, ProjectOS sync, or content-tool integration.
