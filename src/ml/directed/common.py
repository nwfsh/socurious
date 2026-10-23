## directed-question model bits (ADR 012): paths, labels, which filter rules still apply
## shared helpers (jsonl, ROOT, MODELS_DIR) live in src/ml/common.py

import os
import re
from pathlib import Path

from src.ml.common import ROOT, MODELS_DIR, read_jsonl, write_jsonl, append_jsonl
from src.transform.filters import (
    extract_question, is_too_short, is_ama_format,
    contains_i_pronoun, contains_me_pronoun, contains_my_pronoun, contains_im_pronoun,
)

DATA_DIR = Path(os.getenv("SOCURIOUS_DIRECTED_DIR", ROOT / "data" / "directed"))

## sample.py splits the sample into these two BEFORE anything gets labeled
TEST_POOL_PATH = DATA_DIR / "test_pool.jsonl"     # ~100, u label these blind
TRAIN_POOL_PATH = DATA_DIR / "train_pool.jsonl"   # ~300, llama pre-labels, u correct in label studio

TEST_PATH = DATA_DIR / "test.jsonl"               # ur blind labels, locked, final comparisons only
RELABEL_PATH = DATA_DIR / "relabel.jsonl"         # 50 test questions labeled again later, for kappa
TRAIN_PATH = DATA_DIR / "train.jsonl"             # ur corrected labels, pulled out of label studio

LLAMA_TRAIN_PATH = DATA_DIR / "llama_train.jsonl"  # what llama said on train, to measure overrides
LLAMA_TEST_PATH = DATA_DIR / "llama_test.jsonl"    # what llama said on test, DONT look at this while labeling
LABEL_STUDIO_IMPORT_PATH = DATA_DIR / "label_studio_import.json"

LABELS = ["general", "fixable", "unsalvageable"]
UNSURE = "unsure"  # left out of scoring, counted separately

## the test from ADR 012, shown in the labeler + sent to llama so we're both using the same rules
DEFINITIONS = """\
the test: take out who it's addressed to. can a typical partner still answer it from their own life?

  general        anyone can answer it as written. can mention men/women, as long as its ABOUT them not AIMED at them
                 "Why do men fake tender moments?"
  fixable        aimed at a group, but anyone can answer once u strip the address
                 "Ladies, what makes you buy clothes for your partner?"
  unsalvageable  only the addressed group can really answer it
                 "Men who are still virgins over the age of 30, why?\""""

## enriched pool: questions with any of these get oversampled, since directed ones are only ~5% of raw
## only used to PICK questions, never to label them
GROUP_WORDS = re.compile(
    r"\b(men|women|ladies|gents|guys|girls|boys|males?|females?|dudes|man|woman|"
    r"parents|redditors|of reddit|as an?|people who|those who|anyone who)\b",
    re.IGNORECASE,
)
LEADING_ADDRESS = re.compile(r"^[^,:?]{2,40}[,:]\s")  # "Ladies, ..." / "Nurses of reddit: ..."


def passes_format_rules(title: str) -> str | None:
    """the should_reject rules that STAY (ADR 012, 'which rules stay').
    returns the cleaned question, or None if a format rule rejects it.
    rerun here instead of trusting rejection_reason, since should_reject stops at the first rule that fires"""
    q = extract_question(title)
    if q is None or is_too_short(q):
        return None
    if contains_i_pronoun(q) or contains_me_pronoun(q) or contains_my_pronoun(q) or contains_im_pronoun(q):
        return None
    if is_ama_format(q):
        return None
    return q


def is_enriched(text: str) -> bool:
    return bool(GROUP_WORDS.search(text) or LEADING_ADDRESS.search(text))
