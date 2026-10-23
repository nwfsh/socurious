## topic model bits: paths + category list
## shared helpers (jsonl, ROOT, MODELS_DIR) live in src/ml/common.py

import os
from pathlib import Path

from src.ml.common import ROOT, MODELS_DIR, read_jsonl, write_jsonl, append_jsonl

## override with SOCURIOUS_DATA_DIR if u wanna test on a throwaway copy
DATA_DIR = Path(os.getenv("SOCURIOUS_DATA_DIR", ROOT / "data" / "topic"))

SAMPLE_PATH = DATA_DIR / "sample.jsonl"   # questions picked for labeling
LABELS_PATH = DATA_DIR / "labels.jsonl"   # ur hand labels
TRAIN_PATH = DATA_DIR / "train.jsonl"
TEST_PATH = DATA_DIR / "test.jsonl"       # locked, only for final comparisons

## same list as src/transform/classify.py (copied so we dont load deberta just to import it)
CATEGORIES = [
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
NONE_LABEL = "none"  # question doesnt fit any category
LABELS = CATEGORIES + [NONE_LABEL]
