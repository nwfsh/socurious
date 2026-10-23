## step 1: pull questions from raw_questions and split them into test + train pools, ONCE
## pulls from raw_questions (not questions) so the stuff the old group rules rejected is still in there to score
## two pools (ADR 012):
##   random   = unbiased slice, so precision/recall numbers reflect the real mix
##   enriched = has group words, so fixable/unsalvageable dont end up with like 5 examples
## the test/train split happens HERE, before labeling, so u know which ones to label blind
##
## usage: python3 -m src.ml.directed.sample [--random 150] [--enriched 250] [--test-size 100]

import os
import argparse
import random
import psycopg
from dotenv import load_dotenv
from src.ml.directed.common import (
    ROOT, TEST_POOL_PATH, TRAIN_POOL_PATH, TEST_PATH,
    passes_format_rules, is_enriched, write_jsonl,
)

load_dotenv(ROOT / ".env")

SEED = 42


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--random", type=int, default=150)
    parser.add_argument("--enriched", type=int, default=250)
    parser.add_argument("--test-size", type=int, default=100)
    parser.add_argument("--force", action="store_true", help="resample even though pools exist (u almost never want this)")
    args = parser.parse_args()

    if TEST_POOL_PATH.exists() and not args.force:
        print(f"{TEST_POOL_PATH} already exists, the pools are fixed. pass --force if u really mean it")
        if TEST_PATH.exists():
            print("(heads up: u already have blind test labels, resampling makes them point at a different test set)")
        return

    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        rows = conn.execute(
            """SELECT r.id, r.raw_title, s.name
               FROM raw_questions r
               JOIN sources s ON s.id = r.source_id"""
        ).fetchall()

    ## only questions the format rules (the ones that stay) let through
    eligible = []
    for raw_id, title, source in rows:
        q = passes_format_rules(title)
        if q is not None:
            eligible.append({"id": raw_id, "text": q, "raw_title": title, "source": source})
    print(f"{len(eligible)} of {len(rows)} raw questions pass the format rules")

    rng = random.Random(SEED)
    rng.shuffle(eligible)

    random_pool = eligible[: args.random]
    taken = {q["id"] for q in random_pool}
    enriched_candidates = [q for q in eligible if q["id"] not in taken and is_enriched(q["text"])]
    enriched_pool = enriched_candidates[: args.enriched]
    print(f"  random   {len(random_pool)}")
    print(f"  enriched {len(enriched_pool)} (of {len(enriched_candidates)} with group words)")

    for q in random_pool:
        q["pool"] = "random"
    for q in enriched_pool:
        q["pool"] = "enriched"

    ## test gets the same random/enriched mix as the whole sample
    total = len(random_pool) + len(enriched_pool)
    n_test_random = round(args.test_size * len(random_pool) / total)
    n_test_enriched = args.test_size - n_test_random
    test = random_pool[:n_test_random] + enriched_pool[:n_test_enriched]
    train = random_pool[n_test_random:] + enriched_pool[n_test_enriched:]

    ## shuffle so ur not labeling 60 "men who..." in a row (that biases u too)
    rng.shuffle(test)
    rng.shuffle(train)
    write_jsonl(TEST_POOL_PATH, test)
    write_jsonl(TRAIN_POOL_PATH, train)
    print(f"wrote {len(test)} test ({n_test_random} random, {n_test_enriched} enriched), {len(train)} train")


if __name__ == "__main__":
    main()
