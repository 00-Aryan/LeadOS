# Audit Rubric

## Objective

The audit service identifies visible digital-presence gaps in a business website. The first version must be deterministic and evidence-backed.

## Result values

Each check returns one of:

```text
true
false
unknown
```

Unknown is valid when the system cannot safely determine the answer.

## Audit categories

### Access

- website_loads
- https_enabled
- redirect_resolved
- fetch_error_recorded

### Trust

- title_exists
- meta_description_exists
- phone_detected
- address_detected
- social_link_detected

### Conversion

- contact_page_detected
- contact_form_detected
- whatsapp_detected
- booking_link_detected
- call_link_detected

### Local SEO

- schema_markup_detected
- city_or_location_detected
- category_keywords_detected

## Evidence rule

Every true or false finding should include evidence when possible. Evidence may be a matched URL, HTML tag, detected text snippet, or error type.

## Guardrails

- Do not infer facts from weak signals.
- Do not mark a feature missing if the fetch failed.
- Do not use AI for the first audit version.
- Broken websites should produce structured failures, not crashes.
