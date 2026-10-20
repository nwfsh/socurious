## shared bits for the offline ml work (sampling, labeling, training, eval)
## NOT part of the daily pipeline, everything in src/ml is run by hand

import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

## override with SOCURIOUS_DATA_DIR if u wanna test on a throwaway copy
DATA_DIR = Path(os.getenv("SOCURIOUS_DATA_DIR", ROOT / "data" / "topic"))
MODELS_DIR = ROOT / "models"

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


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def append_jsonl(path: Path, row: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(row) + "\n")
