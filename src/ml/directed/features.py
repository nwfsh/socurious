## step 4 shared features (ADR 012), same for every model so the bake-off is fair
## word 1-3 grams + position (START_men) + shape (early comma, group word then "who")

import re

from sklearn.feature_extraction.text import CountVectorizer

from src.ml.directed.common import GROUP_WORDS

WORD = re.compile(r"[a-z0-9']+")
GROUP_THEN_WHO = re.compile(GROUP_WORDS.pattern + r"\s+who\b", re.IGNORECASE)


def extra_tokens(text):
    """position + shape signals, as fake words so any count-based model can use them"""
    words = WORD.findall(text.lower())
    extras = []
    if words:
        extras.append(f"START_{words[0]}")
    comma = text.find(",")
    if 0 <= comma <= 40:
        extras.append("SHAPE_early_comma")
    if GROUP_THEN_WHO.search(text):
        extras.append("SHAPE_group_who")
    return extras


def analyze(text):
    """what the vectorizer sees: 1-3 grams + the extras. module level so it pickles"""
    words = WORD.findall(text.lower())
    grams = [" ".join(words[i:i + n]) for n in (1, 2, 3) for i in range(len(words) - n + 1)]
    return grams + extra_tokens(text)


def make_vectorizer():
    return CountVectorizer(analyzer=analyze, min_df=2)  # min_df=2: drop grams seen once, theyre just noise at 300 rows
