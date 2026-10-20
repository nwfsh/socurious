## step 3: split labels into train + test, ONCE
## stratified so both halves have the same topic mix, fixed seed so its reproducible
## test.jsonl is locked after this, dont tune anything against it or ur scores lie to u
##
## usage: python3 -m src.ml.split [--test-size 100]

import argparse
from collections import Counter
from sklearn.model_selection import train_test_split
from src.ml.common import LABELS_PATH, TRAIN_PATH, TEST_PATH, read_jsonl, write_jsonl

SEED = 42
MIN_PER_TOPIC = 2  # stratify needs at least 2 of each topic


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-size", type=int, default=100)
    parser.add_argument("--force", action="store_true", help="re-split even though a test set exists (u almost never want this)")
    args = parser.parse_args()

    if TEST_PATH.exists() and not args.force:
        print(f"{TEST_PATH} already exists, the test set is locked. pass --force if u really mean it")
        return

    ## bad questions have no topic, so they cant train a topic model
    rows = [r for r in read_jsonl(LABELS_PATH) if r["good"]]
    counts = Counter(r["topic"] for r in rows)
    too_few = [t for t, n in counts.items() if n < MIN_PER_TOPIC]
    if too_few:
        print(f"label more first, these topics have < {MIN_PER_TOPIC} examples: {too_few}")
        return

    train, test = train_test_split(
        rows,
        test_size=args.test_size,
        stratify=[r["topic"] for r in rows],
        random_state=SEED,
    )
    write_jsonl(TRAIN_PATH, train)
    write_jsonl(TEST_PATH, test)

    train_counts, test_counts = Counter(r["topic"] for r in train), Counter(r["topic"] for r in test)
    print(f"{'topic':28} train  test")
    for topic, _ in counts.most_common():
        print(f"  {topic:26} {train_counts[topic]:5} {test_counts[topic]:5}")
    print(f"wrote {len(train)} train, {len(test)} test")


if __name__ == "__main__":
    main()
