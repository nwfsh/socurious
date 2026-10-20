## step 1: pull a stratified sample of questions from the db to label
## stratified = equal-ish amount per deberta label, so rare topics (fears, career) dont end up with like 3 examples
## also pulls questions deberta left uncategorized (below the 0.4 threshold) since thats where it struggles
##
## usage: python3 -m src.ml.sample [--per-bucket 32]

import os
import argparse
import random
import psycopg
from dotenv import load_dotenv
from src.ml.common import ROOT, SAMPLE_PATH, LABELS_PATH, NONE_LABEL, read_jsonl, write_jsonl

load_dotenv(ROOT / ".env")

SEED = 42


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-bucket", type=int, default=32)
    parser.add_argument("--force", action="store_true", help="overwrite an existing sample")
    args = parser.parse_args()

    if SAMPLE_PATH.exists() and not args.force:
        print(f"{SAMPLE_PATH} already exists, pass --force to resample")
        if read_jsonl(LABELS_PATH):
            print("(heads up: u already have labels, resampling only adds new questions to label, old labels stay)")
        return

    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        ## questions only ever get one category (top-1 from deberta), so left join gives one row each
        rows = conn.execute(
            """SELECT q.id, q.text, c.name
               FROM questions q
               LEFT JOIN question_category qc ON qc.question_id = q.id
               LEFT JOIN categories c ON c.id = qc.category_id"""
        ).fetchall()

    buckets: dict[str, list] = {}
    for qid, text, cat in rows:
        buckets.setdefault(cat or NONE_LABEL, []).append((qid, text))

    rng = random.Random(SEED)
    sample = []
    for cat, items in sorted(buckets.items()):
        picked = rng.sample(items, min(args.per_bucket, len(items)))
        sample += [{"id": qid, "text": text, "deberta": cat} for qid, text in picked]
        print(f"  {cat:28} {len(picked):3} of {len(items)}")

    ## shuffle so ur not labeling 32 sexual questions in a row (that biases u too)
    rng.shuffle(sample)
    write_jsonl(SAMPLE_PATH, sample)
    print(f"wrote {len(sample)} questions to {SAMPLE_PATH}")


if __name__ == "__main__":
    main()
