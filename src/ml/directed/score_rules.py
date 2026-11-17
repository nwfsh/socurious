## step 2: score the old hand-written rules (ADR 012)
## rules only say yes/no, so: rule fires = "directed", no rule = "general"

from src.ml.directed.common import TEST_PATH, LABELS, read_jsonl
from src.transform.filters import format_reject, directed_reject


def rules_predict(text):
    """what the old rules say about one question"""
    _, _, question = format_reject(text)
    if question is None:
        return "general"
    rejected, _ = directed_reject(question)
    return "directed" if rejected else "general"


def score_rules(path=TEST_PATH):
    """ur labels vs the rules, both collapsed to directed / general"""
    rows = [r for r in read_jsonl(path) if r["label"] in LABELS]
    truth = ["general" if r["label"] == "general" else "directed" for r in rows]
    pred = [rules_predict(r["text"]) for r in rows]
    return rows, truth, pred
