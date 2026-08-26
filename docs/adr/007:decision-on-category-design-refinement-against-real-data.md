# ADR 007: Topic Category Design — Iterative Refinement Against Real Data

## Status
Accepted

## Context
The original project doc proposed a fixed topic category list, chosen
before any real data had been reviewed: relationships, family/childhood,
career, fears/insecurities, values, hypotheticals, funny/random.

Given prior findings in this project (rules-based niche-group detection
proved unreliable — see filters.py `targets_specific_group`, ~50-60%
precision), the same risk was suspected for an unvalidated category
list: categories chosen from intuition rather than real data are likely
to misrepresent the actual distribution of content.

## Process
Rather than accepting the original list, each candidate category set
was run against real batches of cleaned questions (20-60 rows per
round) using zero-shot classification, with manual review of every
result — same error-analysis discipline used throughout this project's
filter development.

### Round 1 — Original 7-category list
Result: "hypotheticals" acted as a de facto catch-all, absorbing
questions with no real relation to hypothetical scenarios (e.g. "How do
mutated people pee or poop?", "What are you doing awake at this hour?")
simply because no other category fit better. ~13/20 questions in one
batch landed in "hypotheticals" — a clear signal the category was too
broad, not that the model was underperforming.

### Round 2 — Split "hypotheticals" into two
Added "curiosity and how things work" alongside "hypothetical
scenarios" to separate genuine what-if questions from general
curiosity/trivia questions. This measurably reduced (but did not
eliminate) the catch-all effect.

### Round 3 — Model swap
Initial model (`facebook/bart-large-mnli`) repeatedly failed with a
library-level `<eos>` token count error, reproducible regardless of
category wording — confirmed via research as a known BART-architecture
compatibility issue with the installed transformers/torch versions, not
a data or config problem. Switched to `MoritzLaurer/deberta-v3-base-
zeroshot-v1`, which resolved the error entirely and is a more modern,
purpose-built zero-shot model per the author's own benchmarking notes
(DeBERTa-v3 recommended over BART/RoBERTa for accuracy-priority use
cases).

### Round 4 — Category list expansion and pruning
Based on repeated manual review across multiple batches:
- Added "sexual" and "advice" as their own categories — both were
  previously being absorbed awkwardly into other buckets despite
  representing a large, distinct share of the real data.
- Added "controversial debate" (renamed from a plainer "debate") to
  more precisely target contested/opinion-inviting content, separate
  from ordinary preference questions.
- Introduced, tested, then removed "values" and "finding relatability"
  — neither ever won a classification with meaningful confidence across
  several batches, indicating they weren't distinguishable from other
  categories in practice. Cut as dead weight rather than kept on
  intuition.
- Merged "questions about everyday" into "funny and random" once it
  became clear both were serving the same "light, no clear topic"
  role and were competing rather than complementing each other.

### Round 5 — Confidence threshold
Rather than forcing every question into a best-fit category, adopted a
confidence threshold (~0.4) below which a question receives no topic
tag at all. This reflects that some questions genuinely don't belong to
any defined topic, and forcing a low-confidence label is worse than
leaving it untagged. The threshold value itself was set by manually
reviewing where the model's own scores stopped correlating with
independent judgment of "is this label actually correct" — not chosen
arbitrarily.

## Final category list
```python
categories = [
    "relationships",
    "family and childhood",
    "career",
    "fears and insecurities",
    "random everyday questions",
    "hypothetical scenarios",
    "sexual",
    "controversial debate",
    "advice",
]
```

## Validation
Final list tested across a 20-question batch with all classifications
above the 0.4 threshold manually reviewed: 14/14 judged correct or
defensible, a marked improvement over early rounds where catch-all
categories dominated with much lower real precision.

## Consequences
- Category list reflects actual data distribution rather than an
  assumption made before seeing any real questions — directly avoided
  a repeat of the false-precision problem seen in early rules-based
  filters.
- Questions may end up with no topic tag if no category scores above
  threshold; this is treated as a valid, meaningful state, not a defect
  to fix.
- Category list may need further revision as more/different data is
  ingested (e.g. from a future second source) — this is expected, not
  a one-time fixed decision.

  testing something 