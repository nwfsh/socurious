## step 4: train a topic classifier on train.jsonl
## first model: minilm embeddings (same model as dedup) + logistic regression
## minilm turns each question into 384 numbers, logreg learns which direction in that space = which topic
##
## uses 5-fold cross validation on the TRAIN set to score itself, so u can try ideas without touching test
##
## usage: python3 -m src.ml.train_topic [--C 1.0]

import argparse
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import classification_report
from src.ml.common import TRAIN_PATH, MODELS_DIR, read_jsonl

EMBED_MODEL = "all-MiniLM-L6-v2"
SEED = 42


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--C", type=float, default=1.0, help="lower = simpler model (more regularization)")
    parser.add_argument("--out", default=str(MODELS_DIR / "topic_logreg.joblib"))
    args = parser.parse_args()

    train = read_jsonl(TRAIN_PATH)
    if not train:
        print("no train.jsonl, run python3 -m src.ml.split first")
        return

    texts = [r["text"] for r in train]
    y = [r["topic"] for r in train]

    embedder = SentenceTransformer(EMBED_MODEL)
    X = embedder.encode(texts, show_progress_bar=True)

    ## class_weight balanced = rare topics count more, otherwise it just learns to guess the big ones
    clf = LogisticRegression(C=args.C, class_weight="balanced", max_iter=2000)

    ## cross validation: train on 4/5, predict the other 1/5, rotate 5 times -> every train row gets a fair prediction
    n_folds = min(5, min(y.count(t) for t in set(y)))
    if n_folds >= 2:
        cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=SEED)
        preds = cross_val_predict(clf, X, y, cv=cv)
        print(f"\n{n_folds}-fold cross validation on train (C={args.C}):")
        print(classification_report(y, preds, zero_division=0))
    else:
        print("some topic has < 2 train examples, skipping cross validation")

    ## then fit on all of train and save
    clf.fit(X, y)
    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump({"embed_model": EMBED_MODEL, "clf": clf}, args.out)
    print(f"saved model to {args.out}")


if __name__ == "__main__":
    main()
