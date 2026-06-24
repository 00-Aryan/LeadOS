# Sample Outreach Set

## Purpose and safety boundary

This sample set demonstrates the complete deterministic LeadOS outreach safety
workflow:

```text
fictional lead facts
-> outreach draft
-> deterministic evaluation
-> expert review decision
```

All six businesses, locations, and facts are fictional. They are not real
prospects and include no real contact information. No message was sent.
The fixtures exist only for validation and portfolio demonstration.

The outreach service produced each base draft from the committed structured
input. Passing cases retain that output unchanged. Review and rejection cases
apply a small, documented deterministic mutation so the evaluator guardrails
and manual review decisions can be demonstrated.

The evaluator scored the resulting draft for relevance, personalization,
clarity, tone, truthfulness, CTA quality, and risk. The expert checklist then
mapped the evidence and evaluator output to `approve`, `revise`, or `reject`.

Evaluator `pass` does not authorize automatic sending. An `approve` decision
means only that a human may consider sending the draft. No automatic sending
is permitted. Revised drafts must be evaluated again before another expert
review. Rejected drafts must not be used.

## Case summary

| Case ID | Channel | Scenario | Total score | Risk rating | Evaluator result | Expert decision | Lesson |
|---|---|---|---:|---|---|---|---|
| `sample-01-email-approve` | `short_email` | Supported email draft | 60 | low | pass | approve | Verified facts and one clear CTA can pass all gates. |
| `sample-02-whatsapp-approve` | `whatsapp_message` | Supported WhatsApp draft | 60 | low | pass | approve | Concise, evidence-based personalization can be approvable. |
| `sample-03-email-revise` | `short_email` | Unclear CTA | 53 | low | review | revise | A truthful draft still needs revision when its next step is unclear. |
| `sample-04-whatsapp-revise` | `whatsapp_message` | Length and pressure failures | 44 | medium | review | revise | Excessive length, urgency, and fake familiarity require revision. |
| `sample-05-email-reject` | `short_email` | Guaranteed revenue claim | 52 | high | review | reject | Guaranteed results and unsupported revenue claims require rejection. |
| `sample-06-whatsapp-reject` | `whatsapp_message` | Unsupported customer-loss claim | 38 | high | review | reject | Missing evidence and customer-loss claims make the draft unusable. |

## What each case demonstrates

### `sample-01-email-approve`

The service-generated email uses well-supported personalization, suitable
length, respectful wording, and one clear CTA. The evaluator passes it with
low risk. Expert approval still does not send the message.

### `sample-02-whatsapp-approve`

The service-generated WhatsApp message uses verified fictional facts and
stays concise and conversational. It passes evaluation and is safe only for a
human to consider sending.

### `sample-03-email-revise`

An exact mutation replaces the service CTA with a statement that has no clear
question or next step. Facts remain supported, but CTA quality fails. The
required correction is followed by re-evaluation.

### `sample-04-whatsapp-revise`

Documented mutations add excessive channel length, manipulative urgency, and
fake familiarity. These are remediable presentation failures, so the reviewer
requires revision and re-evaluation.

### `sample-05-email-reject`

A documented mutation adds guaranteed results and an unsupported revenue
claim. The evaluator marks the draft high risk, and the expert checklist
rejects it because deceptive outcome claims are central to the added wording.

### `sample-06-whatsapp-reject`

The evaluator receives missing supported facts, and a documented mutation
adds an unsupported customer-loss and business-loss claim. The evidence gate
fails and the evaluator marks the draft high risk, so the draft is rejected
and must not be used.

## Reproduction

`backend/tests/test_sample_outreach_set.py` loads each input, calls
`create_outreach_draft`, applies any recorded mutation, calls
`evaluate_outreach_draft`, and compares the resulting draft and evaluation
with `data/outreach_samples/sample_outreach_cases.json`.

The test uses no database, TestClient, network, external service, current
time, random value, or LLM call.
