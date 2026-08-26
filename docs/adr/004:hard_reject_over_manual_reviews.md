# ADR 004: hard_reject_over_manual_reviews

## Status
Accepted

## Context
Several structural/format filters (`contains_my`, `contains_certain_group`)
showed weaker precision on manual error-analysis review (~50-70%) than
others (`contains_i`, `too_short`, both >90%). Two options were considered
for handling these lower-confidence rules:

1. Keep them as hard rejects in `should_reject`, accepting the false-positive
   cost.
2. Route their rejections to a separate `pending_review` state, to be
   manually approved/rejected later rather than auto-excluded.

## Decision
Keep all filter rules as hard rejects. No manual review tier was built.

## Reasoning
The data source (Reddit, polled on an ongoing basis) is continuously
refreshing, not a fixed/finite pool. A question wrongly rejected today by
an imperfect rule is not a permanent loss — semantically similar questions,
phrased differently, reliably reappear from new posts over time. This
differs from a one-time/historical dataset, where a false positive would
represent genuine, unrecoverable data loss.

A manual review tier was evaluated as overhead disproportionate to its
benefit: it would require building a review UI/query, remembering to
process the queue, and manually approving/rejecting borderline content —
effectively re-implementing manual question review, a task already
happening informally during rule-tuning error-analysis passes against
live Reddit data.

## Scope of this decision
This reasoning applies specifically to *style/quality* filters, where
losing an individual instance is low-cost given ongoing supply. It does
NOT apply to content severity/appropriateness classification (e.g.
explicit content, sensitive topics), where the goal is correct routing
to the right audience context for every instance, not eventual averaging
out over time. That remains a tag-and-gate problem (severity +
relationship_context), handled separately from this reject/keep decision.

## Consequences
**Positive:**
- Simpler system — one filter function, one clear keep/reject outcome,
  no additional state or maintenance queue
- Matches the actual scale and workflow (solo maintainer, already reading
  real data during rule development)

**Trade-offs accepted:**
- Some real false positives (per-rule, roughly 30-50% for the weakest
  rules) are permanently discarded rather than recoverable
- If a future rule shows very poor precision on a topic that does NOT
  reliably recur (unlike general conversation questions), this decision
  should be revisited for that specific case
  
  
That's a real, legitimate argument, and it changes the calculus — worth taking seriously rather than defaulting back to "build the review tier anyway."
Your reasoning: this is a continuously-refreshing data source, not a fixed finite pool. A false positive today isn't a permanent loss — the same underlying question, phrased more generically, will likely show up again from a different post. That's actually a meaningful property of your data source that a lot of filtering systems don't have (e.g. a one-time historical dataset, where every false positive is genuinely gone forever). You have ongoing supply.
Given that, the manual review tier is solving a problem you don't actually have. It exists to prevent losing content permanently — but if losing content doesn't matter because more is always coming, the review queue is pure overhead: something you'd have to actually look at and maintain, for a benefit you've just correctly argued you don't need.
So — skip it. Keep should_reject as a single hard-reject function, as it already is. Don't build the review tier, don't add review_status, don't split into soft/hard. Simpler system, and your reasoning for why it's fine is sound, not lazy.
Where this reasoning has a limit, worth naming so you don't over-apply it: it works for quality/style false positives (contains_my, contains_certain_group) — losing a decent question to an imperfect rule, when equivalent questions will resurface. It does not apply to the content/severity tagging question from earlier (CSA, explicit-for-partner content) — that's not a "will more show up later" problem, that's "does this get correctly routed to the right audience," which needs to happen for every instance, not just eventually average out. Keep those as separate problems: reject-and-move-on for style rules, tag-and-gate for content/severity.