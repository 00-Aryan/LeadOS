# Outreach Expert Review Checklist

## 1. Purpose and boundary

This checklist is a mandatory manual human-review gate. Use it after the
deterministic evaluator has produced its result and before a human considers
sending an outreach message.

The checklist does not replace or override evaluator output. It adds evidence,
safety, quality, and channel review so a human can decide `approve`, `revise`,
or `reject`.

This review does not send, schedule, persist, route, or automatically rewrite
a message. Approval means only that the draft is safe for a human to consider
sending. No automatic sending is permitted.

## 2. Required review inputs

Do not begin review until all of these inputs are available:

- [ ] Original structured outreach draft, including subject line when present
  and message body.
- [ ] Evaluator score breakdown.
- [ ] Evaluator total score.
- [ ] Evaluator risk rating.
- [ ] Evaluator pass-or-review result.
- [ ] Evaluator failure reasons.
- [ ] Evaluator bad lines.
- [ ] Evaluator suggested revision guidance (`suggested_revision`).
- [ ] Supported facts or evidence used for the draft.
- [ ] Draft channel.
- [ ] Assumptions used.
- [ ] Personalization notes.

If a required input is missing, stop and escalate or reject the draft.

## 3. Evidence verification checklist

- [ ] The business name is correct.
- [ ] The business category is correct.
- [ ] The business location is correct.
- [ ] Each audit claim is supported by accessible evidence.
- [ ] No private or inaccessible data is referenced.
- [ ] Scoring context is not presented as an objective business fact.
- [ ] Unsupported revenue, ranking, conversion, or customer-loss claims are
  absent.
- [ ] No fabricated relationship or previous conversation is implied.
- [ ] Every assumption has been reviewed.
- [ ] Unverifiable claims have been removed.

Evidence verification fails if any material statement cannot be traced to the
supplied supported facts or accessible public evidence.

## 4. Evaluator-result review

Review the evaluator output directly:

- [ ] Total score is at least **45 out of 60**.
- [ ] Truthfulness score is at least **8 out of 10**.
- [ ] CTA quality score is at least **7 out of 10**.
- [ ] Risk rating is `low` or `medium`; `high` cannot be approved.
- [ ] Every failure reason has been resolved or has a documented disposition.
- [ ] Every bad line has been removed, corrected, or rejected.
- [ ] Message length is suitable for the selected channel.
- [ ] The `pass_or_review` result is consistent with the draft and score
  breakdown.

Passing numeric thresholds does not override evidence or safety failures. A
threshold-passing draft must still be revised or rejected when it contains an
unsupported claim, unsafe wording, unresolved failure reason, or channel
violation.

## 5. Content quality review

### Relevance

- [ ] The message addresses the recipient's actual business context and a
  supported, useful opportunity. Generic sales copy is not acceptable.

### Personalization

- [ ] Personalization uses verified business, category, location, or audit
  facts. It is specific without being intrusive or irrelevant.

### Clarity

- [ ] The message is easy to understand on one reading, states the legitimate
  offer plainly, and avoids unnecessary detail or competing asks.

### Tone

- [ ] Wording is respectful, professional, low-pressure, and appropriate for a
  first contact.

### Truthfulness

- [ ] Every factual or outcome-related statement is supported, qualified where
  necessary, and free from exaggeration or deceptive implication.

### CTA quality

- [ ] The draft ends with one clear, low-friction next step that the recipient
  can accept or decline without pressure.

## 6. Forbidden-content review

Reject the draft when a prohibited claim or tactic is central to the message
and cannot be removed while preserving a legitimate offer. Otherwise require
revision and re-evaluation.

- [ ] No unsupported claims.
- [ ] No guaranteed outcomes.
- [ ] No invented revenue numbers.
- [ ] No claim that the business is losing customers without evidence.
- [ ] No claim involving private-data access.
- [ ] No fake familiarity or invented prior conversation.
- [ ] No fear-based urgency.
- [ ] No manipulative pressure.
- [ ] No irrelevant personalization.
- [ ] No confusing or multi-part CTA.
- [ ] No excessive channel length.
- [ ] No insulting, patronizing, or coercive wording.

Any unchecked item blocks approval.

## 7. Channel-specific checks

Review only the channel declared on the structured draft. LeadOS supports
`short_email` and `whatsapp_message`; do not substitute or invent another
channel.

### `short_email`

- [ ] Subject is relevant and non-deceptive.
- [ ] Greeting is appropriate.
- [ ] Body is concise.
- [ ] There is only one clear CTA.
- [ ] Sign-off is suitable.

### `whatsapp_message`

- [ ] There is no subject line.
- [ ] Wording is concise and conversational.
- [ ] The message is not a multi-paragraph sales pitch.
- [ ] There are no pressure tactics.
- [ ] There is only one low-friction CTA.

## 8. Decision matrix

Apply the first matching decision below. Record only one decision.

### `approve`

Approve only when all of these conditions are true:

- Evidence is verified.
- No forbidden content exists.
- Risk is `low` or `medium`.
- Total, truthfulness, and CTA-quality thresholds pass.
- No unresolved failure reason remains.
- The CTA is clear and low-friction.
- Wording and length suit the selected channel.

A `medium` risk draft cannot be approved while the cause of that rating is
unresolved. Approval means **safe for a human to consider sending**. It never
means automatic sending.

### `revise`

Choose revise when a legitimate evidence-based message can be preserved but
one or more of these conditions applies:

- Facts are valid but presentation is weak.
- Evaluator thresholds fail.
- Risk is `medium` because of remediable wording or channel issues.
- Wording is too long, unclear, generic, or pressuring.
- The CTA needs correction.
- Unsupported lines can be removed without changing the legitimate offer.

Document each required change. A revised draft must be evaluated again before
another manual review. Re-evaluation after revision is mandatory.

### `reject`

Reject when any of these conditions applies:

- Evidence cannot be verified.
- The draft depends on fabricated facts.
- Private-data claims appear.
- Guaranteed or deceptive claims are central to the message.
- The draft is abusive, discriminatory, coercive, or spam-like.
- Revision cannot preserve a legitimate evidence-based message.

Do not attempt to approve a rejected draft by merely deleting evaluator
failure reasons. A materially new draft must start the evaluation and manual
review workflow again.

## 9. Required reviewer record

Maintain a manual review record with these fields. This is documentation only;
it does not define a database schema or persistence layer.

| Field | Required entry |
|---|---|
| Reviewer | Name or reviewer identifier |
| Review date | Date of manual review |
| Draft channel | `short_email` or `whatsapp_message` |
| Evaluator total score | Score out of 60 |
| Evaluator risk rating | `low`, `medium`, or `high` |
| Decision | `approve`, `revise`, or `reject` |
| Evidence checked | Evidence sources and verified facts |
| Unresolved concerns | Remaining issues, or `none` |
| Required revisions | Specific changes, or `none` |
| Re-evaluation required | `yes` for revised or materially changed drafts |
| Final human approval status | `pending`, `approved`, or `not approved` |

## 10. Reusable review form

```markdown
# Outreach manual review record

- Reviewer:
- Review date:
- Draft channel: [ ] short_email  [ ] whatsapp_message
- Evaluator total score: ___ / 60
- Evaluator risk rating: [ ] low  [ ] medium  [ ] high
- Evaluator result: [ ] pass  [ ] review

## Inputs and evidence

- [ ] Original structured draft reviewed
- [ ] Score breakdown reviewed
- [ ] Failure reasons reviewed
- [ ] Bad lines reviewed
- [ ] Suggested revision reviewed
- [ ] Supported facts and evidence checked
- [ ] Assumptions used reviewed
- [ ] Personalization notes reviewed

Evidence checked:

Unresolved concerns:

Required revisions:

## Decision

- [ ] approve
- [ ] revise
- [ ] reject

Decision reason:

Re-evaluation required: [ ] yes  [ ] no
Final human approval status: [ ] pending  [ ] approved  [ ] not approved

- [ ] No automatic sending is permitted.
- [ ] A revised draft must be evaluated again.
- [ ] Human approval does not guarantee campaign or business results.
```

## 11. Failure and escalation rules

Stop review and reject or escalate when:

- Facts conflict.
- Evidence is missing.
- Evaluator output appears inconsistent with the draft.
- High-risk language is detected.
- A legal, privacy, discrimination, or compliance concern exists.
- The intended recipient or contact authority is uncertain.

Escalation does not authorize sending. Record the concern, preserve the draft
and evaluator output for human inspection, and leave final approval as
`pending` or `not approved`.

## 12. Review decision examples

These examples illustrate review decisions only. They are not production
outreach templates.

### Approvable review

A `short_email` has verified business and public audit facts, a total score of
52, truthfulness of 10, CTA quality of 10, low risk, no failure reasons, one
clear question, and suitable length. The reviewer records `approve`, meaning
the draft is safe for a human to consider sending.

### Revision-required review

A `whatsapp_message` uses verified facts but is overlong, has a multi-part CTA,
and receives medium risk with channel-length and CTA failure reasons. The
reviewer records `revise`, requires a shorter message with one low-friction
question, and marks re-evaluation as required.

### Rejected review

A draft claims private-data access and guaranteed revenue, while the supplied
evidence supports neither statement. The message depends on deceptive claims,
so the reviewer records `reject` and final human approval as `not approved`.
