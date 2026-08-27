# ADR 008: Compute Audience-Appropriateness at Query Time Instead of Storing relationship_context

## Status
Accepted

## Context
The original schema (see 001_init_schema.sql) modeled `relationship_context`
(friends/family/partner/strangers) as its own table, with a join table
connecting questions to one or more valid contexts. This was designed
alongside `categories` (topic) as two independent tagging dimensions.

While building topic and intimacy classification (see ADR 004,
severity-classification-model.md), a design question surfaced: for
certain topics (e.g. "sexual"), audience-appropriateness is clearly
constrained regardless of the intimacy score — a sexual-topic question
should likely never be shown in a "family" context, independent of how
intimate the specific wording scores. This meant relationship_context
wasn't fully independent of topic and intimacy — it was a function of
them.

An earlier draft schema attempted to model question, category, and
relationship_context as a single ternary (three-way) relationship. This
was recognized as a spurious ternary relationship: topic and
audience-appropriateness don't need to vary jointly and independently
of each other in a way that requires a three-way join — the underlying
relationship is that relationship_context is *derived from* topic and
intimacy, not a third independent fact about a question.

## Decision
Do not store relationship_context as data at all. Instead, compute
audience-appropriate contexts at query/serving time, as a function of
a question's already-stored `topic` and `intimacy_score`:

```python
def get_valid_contexts(topic: str, intimacy: float) -> list[str]:
    if topic == "sexual":
        return ["partner", "friends"]
    if intimacy > 0.3:
        return ["partner"]
    if intimacy > 0.0:
        return ["partner", "friends"]
    return ["partner", "friends", "family"]
```

The `relationship_context` table and its join table are dropped from
the schema.

## Reasoning
- **Store facts, compute policy.** Topic and intimacy are measured
  properties of a question (produced by ML models, relatively
  objective as far as such models go). Audience-appropriateness is a
  judgment/policy layered on top of those facts, not an independent
  fact itself.
- **Avoids reclassification for rule changes.** If the mapping logic
  changes (e.g. deciding controversial-debate questions should also be
  family-excluded), this is a one-line code change applied instantly to
  the entire existing dataset — not a data migration or re-run of any
  classification model.
- **Enables features not possible with stored fixed tags**, identified
  during this discussion:
  - A continuous "closeness slider" (filter by intimacy_score range)
    is only meaningful against a stored continuous value, not discrete
    pre-assigned context buckets.
  - A "family-friendly toggle" is a simple query-time filter, with no
    dependency on how questions were tagged at classification time.
  - Per-user customization of what counts as appropriate for which
    audience becomes a parameter to a function call, not a change to
    stored data — directly supports optional-account personalization
    (see project notes on accounts being optional, not required).
- **Computational cost is negligible.** The mapping function is a
  handful of conditional checks against two already-computed values —
  not a repeat of expensive ML inference. This is meaningfully
  different in cost from re-running the zero-shot or intimacy models,
  which only ever run once per question at classification time.

## Consequences
**Positive:**
- Simpler schema — two stored classification signals (topic, intimacy)
  instead of three, no ternary-relationship risk
- Rule changes and personalization features require no data migration
- Natural fit for planned future features (sliders, toggles, per-user
  preferences)

**Trade-offs accepted:**
- Audience-appropriateness logic now lives in application code (API
  layer) rather than being queryable directly via SQL joins alone —
  acceptable since the logic is cheap and the API layer is the natural
  place for serving-time policy anyway
- The mapping function itself is not yet validated against real user
  expectations — since it wasn't classified/reviewed the way topic and
  intimacy were, its correctness will need to be assessed once the API
  and frontend exist to actually exercise it





  