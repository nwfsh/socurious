Found 4 near-duplicate pairs out of 525 questions
# ADR 006: Fuzzy Dedup at High Threshold — Chosen Over Embedding Similarity, Pending Validation

## Status
Proposed (pending empirical validation against real data — see Open Question below)

## Context
The original project doc specified fuzzy string matching (`rapidfuzz`)
for deduplication, to catch rephrased duplicates that exact-match
dedup (already enforced via `UNIQUE (source_id, post_id)` at the raw
ingestion stage) cannot.

Before implementing, two real concerns were raised and worked through:

1. **Computational cost of comparing new questions against the full
   existing dataset.** Naive full pairwise comparison is O(n²), which
   could become a real cost at large scale.

2. **A deeper concern about correctness, not just cost:** whether
   fuzzy string matching (lexical similarity) can actually distinguish
   between questions with meaningfully different intent/structure but
   overlapping vocabulary. Concretely: "Do you like bananas and
   oranges?" and "Do you prefer oranges or bananas?" share very high
   word overlap but represent structurally different questions (a
   yes/no check vs. a forced choice) — a case where naive word-overlap
   or moderate-threshold fuzzy matching could wrongly flag them as
   duplicates.

## Options considered

**A. Fuzzy string matching (rapidfuzz) at a high similarity threshold
(~90%+).** Catches near-identical text (typos, punctuation, minor
phrasing differences) while a high threshold naturally avoids the
banana/orange failure mode, since such pairs typically do not reach
90%+ character/sequence similarity despite sharing vocabulary.

**B. Sentence embedding similarity (e.g. sentence-transformers,
cosine similarity).** Captures semantic meaning rather than lexical
overlap, so it can catch true paraphrases with little word overlap
("What's your biggest fear?" / "What scares you most?"). However,
embeddings are not guaranteed to separate tone/register differences
that a human might consider meaningfully distinct even when the
denotative meaning is the same (discussed further below) — this is a
real limitation of embeddings too, not just fuzzy matching.

**C. No dedup at all; rely solely on exact-match dedup already in
place at ingestion.** Considered given the observation that: (a) the
cost of a near-duplicate slipping through is low — more data
continuously arrives, unlike a fixed/historical dataset — and (b) the
actual rate of near-duplication in this project's data is unknown and
may be low enough not to justify the engineering effort.

## Decision
Proceed with Option A (fuzzy matching, high threshold ~90%) as the
primary approach, but **only after running a diagnostic pass against
the existing real dataset** to measure actual near-duplicate
prevalence before committing further engineering time. If the
diagnostic shows negligible duplication, Option C (skip dedup, revisit
later if evidence changes) becomes the more honest choice, following
the same reasoning already applied elsewhere in this project (e.g.
dropping the `is_english` filter after measuring its real-world
impact was below the threshold worth automating).

## Reasoning for high threshold over embeddings, for now
- A high fuzzy-match threshold is simple, fast (rapidfuzz is
  implemented in C, near-instant at this project's current scale),
  and empirically avoids the banana/orange failure mode without
  needing a new model dependency.
- Embeddings would catch more true paraphrase-duplicates, but add a
  new model/dependency for a problem not yet confirmed to exist at
  meaningful scale in this dataset, and would not fully solve the
  tone/register distinction problem either — a genuinely open, harder
  problem (e.g. "what's your biggest fear" reads as more reflective,
  "what scares you most" reads as more casual, despite near-identical
  denotative meaning) that may not be solvable by either lexical or
  embedding similarity alone.
- Consistent with this project's established pattern: test the
  simpler approach against real data first; only reach for a heavier
  tool (embeddings, or eventually an LLM-based semantic check) if the
  simpler approach demonstrably fails on real examples.

## Open question / next step
Run a diagnostic script comparing all pairs in the current `questions`
table at the 90% threshold, and manually review any matches found, to
determine:
1. Whether meaningful near-duplication actually exists in this dataset
2. Whether the 90% threshold correctly avoids false-positive merges
   like the banana/orange case, using real data rather than a single
   hypothetical example

This ADR should be updated to "Accepted" or revised once that
diagnostic has been run and reviewed.

## Consequences (anticipated, pending validation)
- If duplication is confirmed present and the threshold behaves well:
  proceed to wire fuzzy dedup into the load pipeline, likely scoped by
  topic category to reduce comparison volume as data grows.
- If duplication is negligible: skip dedup as a built pipeline stage
  for now, documented as a deliberate decision based on evidence
  rather than an oversight, revisited if data volume/duplication
  patterns change materially (e.g. after adding a second source).
  
  
  [94.5945945945946] Why indian developers leaked gta 6?
   <-> Why indian developers leaked the gta 6?

[100.0] Whats a secret or opinion you purposefully keeping from your significant other, regardless if it’s a small or big thing?
   <-> Whats a secret or opinion you purposefully keeping from your significant other, regardless if it’s a small or big thing?

[100.0] What is your favourite genre of music?
   <-> What is your favourite genre of music?

[100.0] What's something from your childhood that would confuse kids today?
   <-> What's something from your childhood that would confuse kids today?

   