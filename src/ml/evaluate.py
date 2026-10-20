## step 5: score a model against ur hand labels
## --model deberta  -> the current pipeline (uses the label it already stored in the db, no need to rerun it)
## --model <path>   -> a model u trained with train_topic.py
##
## defaults to train.jsonl so u dont burn the test set while experimenting
## only use --split test for the final "which model wins" comparison
##
## usage: python3 -m src.ml.evaluate --model deberta [--split test]

import argparse
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from src.ml.common import SAMPLE_PATH, TRAIN_PATH, TEST_PATH, LABELS, read_jsonl

## short names so the confusion matrix fits in a terminal
SHORT = {
    "relationships": "rel", "family and childhood": "fam", "career": "car",
    "fears and insecurities": "fear", "random everyday questions": "rand",
    "hypothetical scenarios": "hypo", "sexual": "sex", "controversial debate": "cont",
    "advice": "adv", "none": "none",
}


def predict_deberta(rows):
    stored = {q["id"]: q["deberta"] for q in read_jsonl(SAMPLE_PATH)}
    return [stored[r["id"]] for r in rows]


def predict_saved(path, rows):
    from sentence_transformers import SentenceTransformer
    bundle = joblib.load(path)
    X = SentenceTransformer(bundle["embed_model"]).encode([r["text"] for r in rows])
    return list(bundle["clf"].predict(X))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="'deberta' or a path to a .joblib")
    parser.add_argument("--split", choices=["train", "test"], default="train")
    parser.add_argument("--show-errors", type=int, default=10, help="how many wrong predictions to print")
    args = parser.parse_args()

    rows = read_jsonl(TEST_PATH if args.split == "test" else TRAIN_PATH)
    if not rows:
        print("no split found, run python3 -m src.ml.split first")
        return
    if args.split == "train" and args.model != "deberta":
        print("(heads up: this model was trained on train.jsonl so this score is inflated, check train_topic's cross val instead)\n")

    y = [r["topic"] for r in rows]
    preds = predict_deberta(rows) if args.model == "deberta" else predict_saved(args.model, rows)

    print(f"{args.model} on {args.split} ({len(rows)} questions)  accuracy: {accuracy_score(y, preds):.2f}\n")
    print(classification_report(y, preds, labels=LABELS, zero_division=0))

    ## rows = what u labeled, columns = what the model said
    present = [l for l in LABELS if l in y or l in preds]
    cm = confusion_matrix(y, preds, labels=present)
    print("confusion matrix (row = truth, col = predicted)")
    print("      " + "".join(f"{SHORT[l]:>5}" for l in present))
    for label, row in zip(present, cm):
        print(f"{SHORT[label]:>5} " + "".join(f"{n:5}" for n in row))

    errors = [(r["text"], t, p) for r, t, p in zip(rows, y, preds) if t != p]
    if errors and args.show_errors:
        print(f"\nsome mistakes ({len(errors)} total):")
        for text, truth, pred in errors[: args.show_errors]:
            print(f"  [{SHORT[truth]} -> {SHORT[pred]}] {text}")


if __name__ == "__main__":
    main()
