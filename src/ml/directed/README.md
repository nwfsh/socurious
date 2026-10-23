# directed-question labeling (ADR 012)

Labels each question `general` / `fixable` / `unsalvageable` (+ `unsure`).
The test: take out who it's addressed to. Can a typical partner still answer it from their own life?

This folder only builds and checks the labels. The models (naive bayes, L1 logreg, boosting) aren't here yet.

## order matters

| # | command | what it does |
|---|---|---|
| 1 | `python3 -m src.ml.directed.sample` | pulls from `raw_questions`, keeps what passes the format rules, picks a random + enriched pool, splits into ~100 test / ~300 train. run once |
| 2 | `python3 -m src.ml.directed.label` | blind-label the 100 test questions in the terminal. no llama, no rules shown |
| 3 | `python3 -m src.ml.directed.prelabel` | llama labels both pools through ollama. refuses to run until step 2 is done |
| 4 | label studio | import `data/directed/label_studio_import.json`, paste `label_studio.xml` into the labeling interface, correct llama's labels, export as JSON |
| 5 | `python3 -m src.ml.directed.import_labels export.json` | turns the export into `train.jsonl`, keeping llama's label next to urs |
| 6 | `python3 -m src.ml.directed.label --relabel` | a week+ after step 2, label 50 test questions again without seeing ur first answer |
| 7 | `python3 -m src.ml.directed.agreement` | kappa, llama's blind accuracy, override rate, and the anchoring gap |

Label Studio isn't in `requirements.txt`, it's heavy. Install it in its own env: `pip install label-studio && label-studio start`.
Ollama: `ollama serve` + `ollama pull llama3.1:8b`.

## files in data/directed

- `test_pool.jsonl` / `train_pool.jsonl`: the questions, split once by `sample.py`
- `test.jsonl`: ur blind labels. locked, final comparisons only
- `relabel.jsonl`: the 50 relabels, for kappa
- `train.jsonl`: ur corrected labels from label studio
- `llama_test.jsonl`: llama's test labels. **dont open this**, the anchoring check depends on u never seeing it
- `llama_train.jsonl`: llama's train labels, for counting overrides
