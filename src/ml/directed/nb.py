## step 4 model 1: naive bayes (ADR 012)
## 5-fold stratified cv on train ONLY. test.jsonl stays locked for the final comparison

import joblib
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from src.ml.directed.common import TRAIN_PATH, LABELS, MODELS_DIR, read_jsonl
from src.ml.directed.features import make_vectorizer

MODEL_PATH = MODELS_DIR / "directed_nb.joblib"
CV = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


def load_train(path=TRAIN_PATH):
    rows = [r for r in read_jsonl(path) if r["label"] in LABELS]  # unsure left out, same as scoring
    return [r["text"] for r in rows], [r["label"] for r in rows]


def build():
    return make_pipeline(make_vectorizer(), MultinomialNB(alpha=1.0))


def cv_predict(model, texts, labels):
    return cross_val_predict(model, texts, labels, cv=CV)


def to_binary(labels):
    """directed vs general, so it lines up with the rules baseline"""
    return ["general" if l == "general" else "directed" for l in labels]


if __name__ == "__main__":
    texts, labels = load_train()

    for name, model in [("dummy", DummyClassifier(strategy="most_frequent")), ("naive bayes", build())]:
        pred = cv_predict(model, texts, labels)
        print(f"== {name}, 3 labels (5-fold cv on train) ==")
        print(classification_report(labels, pred, labels=LABELS, zero_division=0))
        print(f"== {name}, directed vs general ==")
        print(classification_report(to_binary(labels), to_binary(pred), zero_division=0))

    ## refit on all of train and save, test set gets scored once later
    model = build().fit(texts, labels)
    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"saved {MODEL_PATH}")
