# Severity Classification — Using a Research-Backed Intimacy Model

## Why this exists
Original plan (project doc, step 6) was keyword-based rules for severity
(1 = light, 2 = personal/reflective, 3 = heavy/sensitive). Topic keyword
rules already proved unreliable for a related problem (`contains_certain_group`
couldn't distinguish "people who just started the gym" from "people who
survived extreme poverty" — same phrasing, very different meaning).
Given severity/intimacy is arguably an even harder judgment call than
topic, a pretrained, research-validated model was sought instead of
hand-written rules.

## The source
**Paper**: Pei, J. & Jurgens, D. (2020). *Quantifying Intimacy in Language*.
EMNLP 2020.
https://aclanthology.org/2020.emnlp-main.428.pdf

**Key finding directly relevant to this project**: the paper explicitly
tests topic alone as a predictor of intimacy and finds it insufficient
("many topics span the range of intimacies... topic alone is often
insufficient") — independent confirmation that severity and topic should
be modeled as separate dimensions, not derived from one another. This
matches the project's own schema decision (severity + topic +
relationship_context as separate axes).

The paper trained a model on 2,247 human-annotated Reddit/Twitter/book/
movie questions using Best-Worst-Scaling, then fine-tuned RoBERTa to
predict a continuous intimacy score, achieving Pearson's r=0.87 against
human judgment — notably higher than topic-based or bag-of-words
baselines (r=0.62 and r=0.51 respectively).

## The model
Authors released their trained model publicly:
- Hugging Face: `pedropei/question-intimacy`
- GitHub: https://github.com/Jiaxin-Pei/question-intimacy
- Verified as the authors' own official release (linked directly from
  their paper's repo, matching author identity)

**Output**: a single continuous score from -1 (least intimate) to 1
(most intimate) — not a fixed category. Matches the paper's own
argument that intimacy is better modeled as continuous than as discrete
buckets, since "people naturally perceive intimacy along a continuum."

## Usage
```python
from question_intimacy.predict_intimacy import IntimacyEstimator

inti = IntimacyEstimator(cuda=False)
score = inti.predict("What's your biggest fear?", type='list')
```

## Validation plan (in progress)
Before trusting this model's output as a hard classification signal,
running it against a real, deliberately varied sample of this project's
own `questions` data and manually checking whether the resulting
ranking (not necessarily the exact score) matches independent human
judgment of relative intimacy — same error-analysis process used for
every other rule in this pipeline (see `docs/transform-best-practices.md`).

## Bug found during validation: `type='list'` requires a list input
Initial integration passed a bare string to `predict(title, type='list')`.
This silently produced one score per token/word in the sentence rather
than one score for the sentence as a whole (e.g. a 5-word question
returned ~19 scores). Because the code took `result[0]`, every stored
"intimacy score" was actually the score of roughly the first token,
not the sentence — producing tightly clustered, near-meaningless
values (e.g. explicit/vulnerable content scoring the same as mundane
questions).

Root cause: the package expects a list of sentences even for a single
input — `predict([title], type='list')`, not `predict(title, type='list')`.

Caught by comparing pipeline output against the paper's own documented
reference example ("What is this movie?" ≈ -0.27) in isolation, outside
the pipeline — the isolated call matched the paper closely (-0.29),
while the in-pipeline output did not, pointing to a usage bug rather
than a model or data issue.

After the fix, a 20-question batch spanned intimacy scores from -0.44
to 0.50 (vs. -0.37 to 0.09 before the fix), with ordering matching
independent human judgment: abstract/impersonal questions scored
lowest, emotionally vulnerable/explicit content scored highest — in
line with the paper's own reported range (-0.58 to 0.48).

## Why this is notable for this project
This is the second time in this project that a rules-based approach was
tried first, found to hit a real ceiling on ambiguous/context-dependent
judgments, and a stronger approach was found only after directly
attempting and documenting the failure (see also: `contains_certain_group`
in filters.py). In this case, rather than reaching for a generic
zero-shot model, a domain-specific, peer-reviewed, purpose-built model
was found and verified — a stronger fit than either hand-written rules
or an off-the-shelf general classifier.

AVERY'S NEXT STEP

Testing a model against your own data before trusting it — this is called validation on your own distribution, and it's a real, named concern in ML: a model trained on one dataset (Reddit questions from 2018, in this case) doesn't automatically transfer perfectly to yours (2026, different subreddits, already pre-filtered by your rules). Checking this before trusting the model is exactly what a careful practitioner does, and plenty of people skip it — you're not.
Deciding rules aren't good enough, then reaching for ML — but only after proving the rules failed — this is precisely the standard "rules-based baseline, then ML upgrade" pattern that shows up across real production systems (spam filters, content moderation, fraud detection all follow this same arc). Your own project doc predicted this exact structure before you'd even hit it.
Keeping severity and topic as separate axes — turns out this matches actual academic literature (the paper's own finding). You didn't know that when you made the schema decision — you reasoned it out independently, and it happened to align with published research. That's a good sign about your instincts, not a coincidence to downplay.