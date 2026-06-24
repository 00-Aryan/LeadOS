# Security Review 001: Website Audit Fetcher

## Scope

This review covers the first LeadOS website audit fetcher.

The fetcher accepts one provided website URL and returns structured fetch and audit information. It is not a crawler.

## Primary risk

The main risk is server-side request forgery. A user-supplied URL could try to make the backend request internal services, localhost, cloud metadata endpoints, or non-web protocols.

## Controls added

- Only http and https schemes are allowed.
- Direct requests to private IPs are blocked.
- Direct requests to loopback IPs are blocked.
- Direct requests to link-local IPs are blocked.
- Direct requests to multicast and reserved IPs are blocked.
- Redirect following is disabled.
- Timeout is explicit.
- Response HTML is capped before audit checks.
- Network failures return structured errors.
- Tests use mock transport instead of live network calls.

## Current limitations

- Domain names are not resolved and checked against private IP ranges yet.
- DNS rebinding protection is not implemented yet.
- Network-layer egress controls are not implemented yet.
- Robots.txt and rate-limit policy are not relevant yet because this is not crawling.

## Product boundary

No scraping, crawling, ProjectOS integration, content-tool integration, billing, deployment, or outbound automation was added.

## Required future hardening

Before production use, add DNS resolution checks, egress restrictions, response size streaming limits, audit rate limits, and tenant-level quotas.
