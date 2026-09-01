# Embedding Model Choice — Deduplication

## What this is for
Semantic deduplication of cleaned questions (`questions` table), catching
near-duplicate/paraphrased questions that exact-match and fuzzy string
matching cannot reliably detect. See ADR 006 for the full decision
process and comparison against fuzzy matching.

## Model chosen
`sentence-transformers/all-MiniLM-L6-v2`

## Why this model

### 1. Task fit
This is a **prediction-based (transformer) embedding model**, not a
frequency-based method like TF-IDF or bag-of-words. It captures learned
semantic meaning rather than word overlap — this distinction was the
actual reason it outperformed fuzzy string matching in this project's
own testing (see ADR 006): it correctly separated "What's your favorite
movie?" from "What's your favorite food?" (different meaning, near-
identical structure) while fuzzy matching falsely flagged that pair as
a duplicate.

### 2. Task-appropriate scale
Considered against much larger, higher-benchmark-ranking embedding
models (e.g. Qwen3-Embedding-8B, an 8-billion-parameter model topping
current MTEB leaderboards). Rejected in favor of the smaller
`all-MiniLM-L6-v2` (~22M parameters) because:
- No demonstrated task failure justifying the extra weight/cost
- This project's dedup task (short-sentence semantic similarity) is
  not the kind of workload (large-scale multilingual retrieval, long-
  document RAG) that benchmark leaders are specifically optimized for
- Lighter weight matters given the project's plan to eventually run
  classification/dedup steps inside GitHub Actions' resource-
  constrained CI environment
- Consistent with this project's established pattern of choosing
  right-sized tools over leaderboard-chasing (see also: choice of
  `deberta-v3-large-zeroshot` over larger zero-shot alternatives,
  rejection of Airflow/AWS in favor of simpler tooling)

### 3. Domain relevance — Reddit-sourced training data
`all-MiniLM-L6-v2` originates from the Hugging Face "Train the Best
Sentence Embedding Model Ever with 1B Training Pairs" community project
(2021 JAX/Flax sprint). The project's own public roadmap explicitly
named Reddit as a planned data source:

> "Mine Conversational Datasets from Reddit: PolyAI has the script
> ready" — project roadmap

This refers to PolyAI's `conversational-datasets` repository, which
provides **3.7 billion Reddit comments structured as threaded
conversations**, purpose-built for training conversational response
models.

Separately, Nils Reimers (the project's lead and the model's creator)
independently published a "Reddit (title, body) pairs" dataset
(`sentence-transformers/reddit-title-body`, 2021), cited in later
academic work (KaLM-Embedding-V2, 2025) as part of the broader
Sentence-Transformers training ecosystem.

**Honest caveat on sourcing:** the model's own official Hugging Face
card does not itself enumerate the exact final training dataset mixture
in prose — that level of detail lives in a `data_config.json` file in
the model's repository, which was not directly inspected for this
writeup. The claims above are based on the project's own public
roadmap (a primary source describing planned data collection) and a
separately published, creator-authored Reddit dataset — strong,
converging evidence, though not a line-by-line confirmation of the
final training mix.

**Why this matters for this project specifically:** to whatever extent
Reddit conversational data informed this model's training, that is a
genuine, non-coincidental reason to expect reasonable performance on
this project's own Reddit-sourced question data — the model's training
distribution plausibly overlaps with this project's actual data
distribution, rather than being trained on an unrelated domain
(e.g. formal news text or academic writing) and applied here regardless.

## Known limitations
- **Monolingual English.** Quality drops sharply on non-English input.
  This project's data occasionally includes non-English questions
  (e.g. Spanish-language posts observed in raw data); these will
  receive lower-quality embeddings and dedup checks on them are less
  reliable.
- **Text-only.** No multimodal capability, not needed for this
  project's use case.
- **256 word-piece max sequence length.** Not a practical constraint
  given this project's short-question data.
- **Not the highest-scoring model on general benchmarks** (MTEB) as of
  2026 — several newer, larger models outperform it by 8-16 average
  points on general tasks. Accepted trade-off given this project's
  scale and resource constraints (see above).

## Validation
Tested against both real project data (525 questions) and curated
adversarial test cases (see ADR 006) before adoption. Found 6 real
duplicate pairs with zero false positives on real data; correctly
handled a same-structure/different-meaning adversarial pair that fuzzy
matching failed on. One known unresolved risk: scored a "different
meaning, high vocabulary overlap" adversarial pair (bananas/oranges
preference framing) ambiguously high (0.884) — not yet observed in
real data, documented as an open risk to monitor as data volume grows.

## Sources
- Project roadmap ("Train the Best Sentence Embedding Model Ever with
  1B Training Pairs"), Hugging Face JAX/Flax community sprint, 2021
- PolyAI `conversational-datasets` repository —
  github.com/PolyAI-LDN/conversational-datasets
- `sentence-transformers/reddit-title-body` dataset, Nils Reimers, 2021
  — huggingface.co/datasets/sentence-transformers/reddit-title-body
- Model card: huggingface.co/sentence-transformers/all-MiniLM-L6-v2