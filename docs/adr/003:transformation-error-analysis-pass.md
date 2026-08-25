# ADR 003: Error Analysis Pass Before Promoting Filter Rules

## Status
Accepted


EXTRA :
True positive — rule rejects it, and it should be rejected (correct)
False positive — rule rejects it, but it was actually a good question (rule is too aggressive)
True negative — rule keeps it, and it should be kept (correct)
False negative — rule keeps it, but it was actually bad (rule missed it)

calculate precision and recall

case for me, im looking for 


## Context
After writing the rules-based filter pipeline (`should_reject` in `filters.py`), the rules existed but had never been validated against real data. The filters were written by intuition — "questions with 'I' are probably personal experience posts, not curiosity-driven questions" — but intuition is not evidence. Rule-based classifiers fail in two directions: over-rejection (filtering out good questions) and under-rejection (letting noise through). Neither failure is visible without looking at what the rules actually do on real posts.

The naive path is to just ship the filters and iterate in production. The problem is that without a baseline measurement, you have no way to tell whether changes make things better or worse, and no sense of which rules are doing the most work vs. which might be wrong.

## Decision
Before promoting the filter rules into the main load pipeline, run a deliberate error analysis pass: feed all rows from `raw_questions` through `should_reject`, collect rejection reasons using a `Counter`, and print a frequency breakdown ordered by most common reason.

Additionally, wrote a `review_rule(reason_to_check)` function that lets you drill into a specific rejection category and print every title that got rejected by that rule. This makes it easy to eyeball whether a rule is firing correctly or being too aggressive.

The analysis script lives in `src/transform/review.py` and is meant to be run manually as a diagnostic — it is not part of the load pipeline.

**Ordering the filters cheap-to-expensive:**
Inside `should_reject`, filters are ordered by cost and kill probability. `is_too_short` runs first (a string split, no regex), then `extract_question` (partition on `?`, very fast), then pronoun checks (regex, still cheap), then `is_english` (calls `langdetect`, the only one with real overhead). This ordering means the slow filter rarely runs because most bad posts are already caught before reaching it.

## What the Pass Revealed
Running `reasons.most_common()` on the raw dataset shows which filter is the dominant rejection signal. This matters because:
- A rule firing >50% of rejections is load-bearing — if it's wrong, it's catastrophic
- A rule firing <1% of rejections might be correct but might also be dead weight
- The distribution tells you where to look when you review individual titles with `review_rule`

After eyeballing rejections per category, you can confirm the rule is working as intended or tighten/relax the pattern before it affects the final dataset.

## Consequences

**Positive:**
- Catches rule errors before they silently corrupt the classified dataset
- Gives a sense of how much of the raw data survives filtering (the pass rate), which is a signal for whether the sourced subreddits are well-targeted
- `review_rule` is a reusable diagnostic — if a rule gets changed later, re-running it on the same raw data shows the delta
- Documents the empirical basis for the rule ordering in `should_reject`, which would otherwise look like an arbitrary choice

**Trade-offs / limitations accepted:**
- The analysis is manual and point-in-time — it's not a continuous quality gate, just a pre-promotion check
- `review.py` has top-level code outside the `if __name__ == "__main__"` block, which means importing it has side effects (DB connection, print output); acceptable for a throwaway diagnostic, but would need restructuring if it ever became part of a real pipeline
- `langdetect` is non-deterministic on short strings — the `is_english` check is intentionally skipped for titles under 4 words, which is a deliberate approximation accepted here
