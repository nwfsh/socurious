# ADR 012: Replace hand-written directed-question rules with a learned classifier

**Status:** Proposed
**Date:** 2026-10-22

## Context

A large share of the question bank is written *at* a specific group rather than *to* a person. These questions read like Reddit threads, not something you'd ask a friend or partner:

- "Ladies, what's a physical preference you have in a partner that's considered shallow?"
- "Men who have dated assertive women, what was your experience?"
- "Men from Arabic countries, what's the logic behind…"

Counting only gendered questions so far:

- 1,074 of 8,577 raw questions mention men or women, and 910 of those are live in the app as written.
- ~243 open by addressing a group ("Men,", "Ladies,", "Women of Reddit:").
- ~216 use the "Women who X, …" filter shape.
- 45 otherwise-decent questions are rejected only by the `of reddit` rule.

Directed questions by profession, age and life experience haven't been counted yet.

I first tried a regex rule that stripped leading addresses like "Men, …". It handled ~226 questions, but every edge case needed its own hand-written guard. For example, "Why do men…" must not be stripped, but "Men, why do you…" should be. The rule set was growing faster than the coverage, so I reverted it.

The real problem: **hand-written rules encode exceptions one at a time.** A learned model encodes them as weights learned from labeled examples. Adding coverage then means adding labels, not code.

## Decision

Replace the hand-written directed-question rules with a trained classifier that routes each question three ways:

| Label | Meaning | Route |
|---|---|---|
| `general` | Already askable to anyone | Keep |
| `fixable` | Directed, but the underlying question is answerable by a typical partner | Send to rewriter |
| `unsalvageable` | Only answerable by the addressed group | Reject (optionally store for an opt-in group bank later) |

**The label is defined by answerability, not address.** The test: after removing the addressee, can a typical partner answer it from their own life? "Ladies, what's a preference…" passes, so it's `fixable`. "Men from Arabic countries…" fails, so it's `unsalvageable`. Who a question is addressed to is a surface feature for the model to learn; answerability is the decision being made.

### Which rules stay

Not every rule in `should_reject` is about directedness. Rules that check a question's *format* are cheap, accurate and still make sense. Only the rules that guess who a question is aimed at get replaced.

| Rule | Reason code | Fate |
|---|---|---|
| `is_too_short` | `too_short` | Stays |
| `extract_question` | `not_a_question` | Stays |
| `contains_i/me/my/im_pronoun` | `contains_i`, `contains_me`, `contains_my`, `contains_im` | Stays (about the asker, not aimed at a group) |
| `is_ama_format` | `is_ask_me_anything` | Stays (a post format, not a group address) |
| `targets_specific_group` | `contains_certain_group` | Replaced by the classifier |
| `targets_reddit_audience` | `contains_reddit_audience` | Replaced by the classifier |

New pipeline order: format rules → directedness classifier (+ rewriter) → intimacy floor → near-dup check. The classifier runs before intimacy and dedup because a rewritten question can change both scores.

`should_reject` in `src/transform/filters.py` is split into these two layers: `format_reject` (layer 1, the rules that stay) runs first, then `directed_reject` (layer 2). Layer 2 still holds the two regex rules for now, since they're the baseline being scored in Step 2. When the classifier ships, it replaces the inside of `directed_reject` and nothing else in the pipeline changes.

### Step 1: Build the labeled data

**Where questions come from.** Sample from `raw_questions`, keeping only the questions that pass the rules that stay. Re-run those rules in Python at sampling time rather than trusting the stored `rejection_reason`. Rows filtered before the two-layer split were checked in the old order, where `is_ama_format` ran after the group rules, so a stored `contains_certain_group` was never checked against it. Questions the two replaced rules rejected must be included, or those rules can't be scored. Draw from two pools and record which pool each question came from:

- **Random pool:** an unbiased slice of the raw data, so precision and recall estimates reflect the real mix.
- **Enriched pool:** questions containing group words (men, women, ladies, guys, "who", "as a"). Directed questions are only ~5% of the raw data, so without this the rare labels get too few examples. It also brings in hard negatives like "Why do men…" and "What do women wish…", so the labels (and later the models) separate structure from "mentions men".

**Labels:** `general`, `fixable`, `unsalvageable`, plus `unsure` for genuine toss-ups. `unsure` questions are left out of scoring and counted separately. They preview what the review queue will look like. Edge-case calls live in `docs/guidelines/directed-labelling.md`, which changes as labelling goes on; this ADR doesn't.

**Three sets, labeled in this order:**

| Set | Size | Labeled by | Used for |
|---|---|---|---|
| Test | ~100 | Me, blind, no AI help | Final comparison only. Locked. |
| Train | ~300 | Llama pre-labels, I correct in Label Studio | Training and cross-validation |
| Relabel | 50, drawn from the test set | Me, blind, again, at least a week later | Self-agreement (Cohen's kappa) |

**The test set is labeled first, by hand.** It's the ground truth that the rules, every model and Llama are all scored against, so no model output is visible while labeling it.

**The training set is Llama-assisted.** Llama 3.1 8B (the same local setup as the rewriter) pre-labels ~300 questions, and I accept or correct each one in Label Studio. This is much faster than labeling from scratch. For every question, log Llama's label, my final label, and whether I overrode it.

**Two measures of label quality:**

- **Override rate:** how often I changed Llama's label on the training set. It shows how good the LLM is as a labeler before any model comparison runs.
- **Kappa:** relabel 50 test questions without seeing the first label, and compute Cohen's kappa against the originals. This is the ceiling on the whole project: no model can be reliably scored as more accurate than my own consistency. Below ~0.7 means the label definitions need tightening before training.

**Anchoring caveat.** Seeing Llama's suggestion pulls me toward agreeing with it (the same reason DeBERTa's guess is hidden in the topic labeler). So the override rate *understates* how often Llama is wrong. To measure that honestly, Llama also labels the test set, and I never see those labels. Its accuracy against my blind labels, compared with the override rate, shows how big the anchoring effect is. If the same prompt is used, that blind score also serves as the zero-shot LLM's result in the follow-up comparison.

### Step 2: Score the current rules

Before training anything, measure how well the hand-written rules already running do. The rules aren't tuned on anything, so scoring them on the test set leaks nothing.

The two rules being replaced (`targets_specific_group` and `targets_reddit_audience` in `src/transform/filters.py`) only say yes or no. They can't tell `fixable` from `unsalvageable`. So score them as a binary classifier: a rule fires = "directed" (either label), no rule fires = `general`. Report:

- **Precision:** of the questions the rules reject, how many really are directed? Each miss is a good question thrown away.
- **Recall:** of the directed questions, how many do the rules catch? This is likely low, since no rule targets "Men," or "Ladies," openings at all.
- **Per-rule breakdown:** which rule causes the false positives (` as a ` is the likely suspect).

### Step 3: Two baselines

| Baseline | Question it answers |
|---|---|
| Dummy classifier (always predicts the most common label) | Is a model learning anything at all? |
| Current hand-written rules | Is a model better than what's already running? |

The dummy matters because `general` will be the large majority. Always guessing `general` scores high accuracy with zero recall on the classes that matter, which is why every result is reported as per-class precision and recall, not accuracy. A model has to beat the dummy to show it's learning, and beat the rules to be worth replacing them.

### Step 4: Model bake-off

Three classic models, built by hand:

- **Naive Bayes.** The fastest classic text model. If it scores close to the others, the problem is simple.
- **L1 logistic regression.** Usually the strongest classic model on text. L1 zeroes out most weights, leaving a readable list of the phrases that drive each decision.
- **Gradient boosting (LightGBM-style).** The only contender that learns feature *combinations*. Tests whether signals like `START_men` + `who` carry meaning together that neither carries alone.

**Shared setup, so the comparison is fair:**

- Same labeled data from Step 1.
- Same features: word 1–3 grams; position features (`START_men`); shape features (an early comma, "who" directly after a group word).
- Models are compared to each other on all three labels. They're compared to the rules on the same binary collapse (directed vs `general`), since the rules can't do better than binary.
- Same 5-fold stratified cross-validation on the training split.
- A held-out test set is locked away and not used for model selection.

**Primary metric:** precision on `unsalvageable`. Wrongly rejecting a good question is the costly error (same reasoning as ADR 004). The decision threshold for that class is tuned upward from the default 0.5 using a precision–recall curve. Low-confidence predictions go to a review queue, not the reject pile.

**What happens next:** the best of the three advances as the "classic" contender in a follow-up comparison against a fine-tuned encoder and a zero-shot LLM, scored on the locked test set. That comparison gets its own ADR.

### Rewriter (fixable route only)

- **Simple addresses** ("Ladies, …"): delete the address tokens.
- **Group-filter questions** ("Men who have dated…"): an LLM restructures them (Llama 3.1 8B via Ollama, run locally).
- **Originals are never overwritten.** The rewrite is stored alongside the original.
- Every rewrite is validated before entering the bank:
  - it's still a question
  - no group words remain
  - its embedding stays close to the original's, so the meaning is preserved
  - it passes dedup against the existing bank (stripping an address often produces a question already in the bank)

## Alternatives considered

**Keep extending the regex.** Rejected. This is what already failed: each edge case needed its own guard, and the rule set grew faster than coverage.

**Bake off all seven classic models** (adding linear SVM, a shallow decision tree, and a RIPPER rule learner). Rejected for now. With a few hundred labels, models reading the same features will land within noise of each other. Each extra model also duplicates one already in the set: SVM behaves like logistic regression, the shallow tree is a weaker boosting, and L1 already provides the readable-rules benefit of RIPPER. Revisit only if a classic model ends up close to the encoder and LLM in the follow-up comparison.

**Hand-label everything without Llama.** Rejected. Labeling ~400 questions from scratch is slow, and the blind test set already provides clean ground truth. Llama assistance only touches training data, where small label noise costs less.

**Let Llama label everything, including the test set.** Rejected. Llama would then be grading the models against its own opinions, and the zero-shot LLM contender would be scored against itself.

**Go straight to a fine-tuned encoder or LLM.** Rejected as a *first* step. Without a classic baseline, there's no way to tell whether the heavier model's accuracy is worth its cost.

## Consequences

**Positive:**
- Coverage grows by labeling, not by writing exception code.
- L1 weights double as documentation of which phrasings signal directedness.
- The boosting result answers a real question: do directedness signals interact, or does each one work on its own?
- Rewriting recovers ~460 questions that would otherwise be rejected or served as-is.

**Negative:**
- Labeling ~400 questions is real upfront cost, and label consistency caps accuracy more than model choice does.
- Training labels start as Llama's, so its systematic mistakes can survive my corrections. The blind test set and the anchoring check are what catch this.
- `unsalvageable` will be the smallest class, and the ~100-question test set may hold only a handful of them. Its precision will be noisy, so report the raw counts alongside the percentage.
- The rewriter adds an LLM dependency and a validation step to the pipeline.

## Open questions

- How large are non-gendered directed questions (profession, age, life experience)? Count before finalizing the labeling sample.
- Should `unsalvageable` questions be deleted, or stored for an opt-in group bank? Store the label either way; defer the product decision.