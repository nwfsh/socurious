## step 2: blind-label the test pool in the terminal, no ai help
## nothing from llama or the old rules is shown, seeing it would nudge ur answer (anchoring bias)
## saves after every answer so u can quit and come back whenever
##
## --relabel: later on (a week+ after ur last test label), label 50 test questions AGAIN without seeing
## ur first answer. agreement.py compares the two for kappa
##
## usage: python3 -m src.ml.directed.label [--relabel]

import argparse
from datetime import datetime
from src.ml.directed.common import (
    TEST_POOL_PATH, TEST_PATH, RELABEL_PATH, LABELS, UNSURE, DEFINITIONS,
    relabel_pool, days_until_relabel, read_jsonl, write_jsonl, append_jsonl,
)

KEYS = {"1": LABELS[0], "2": LABELS[1], "3": LABELS[2], "4": UNSURE}

HELP = DEFINITIONS + "\n\n" + "\n".join(f"  {k}  {v}" for k, v in KEYS.items()) + """
  s  skip for now
  u  undo last label
  ?  show this again
  q  quit"""


def relabel_todo(test_labels):
    if not test_labels:
        print("no test labels yet, label the test pool first")
        return None
    days = days_until_relabel(test_labels)
    if days:
        print(f"heads up: wait ~{days} more day(s) since ur last test label or ull just remember ur answers")
        if input("relabel anyway? [y/N] ").strip().lower() != "y":
            return None
    return relabel_pool(test_labels)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--relabel", action="store_true")
    args = parser.parse_args()

    out_path = RELABEL_PATH if args.relabel else TEST_PATH
    if args.relabel:
        pool = relabel_todo(read_jsonl(TEST_PATH))
        if pool is None:
            return
    else:
        pool = read_jsonl(TEST_POOL_PATH)
        if not pool:
            print("no test pool found, run python3 -m src.ml.directed.sample first")
            return

    labels = read_jsonl(out_path)
    done = {row["id"] for row in labels} & {q["id"] for q in pool}
    todo = [q for q in pool if q["id"] not in done]
    skipped = []

    print(HELP)
    i = 0
    while i < len(todo):
        q = todo[i]
        print(f"\n[{len(done) + 1}/{len(pool)}]  {q['text']}")
        key = input("> ").strip().lower()

        if key == "q":
            break
        if key == "?":
            print(HELP)
            continue
        if key == "s":
            skipped.append(q)
            i += 1
            continue
        if key == "u":
            if not labels:
                print("nothing to undo")
                continue
            last = labels.pop()
            write_jsonl(out_path, labels)
            done.discard(last["id"])
            ## put the undone question back in front of the current one
            todo.insert(i, next(p for p in pool if p["id"] == last["id"]))
            print(f"undid: {last['text']}")
            continue
        if key not in KEYS:
            print("? for keys")
            continue

        row = {"id": q["id"], "text": q["text"], "label": KEYS[key], "labeled_at": datetime.now().isoformat()}
        if "pool" in q:
            row["pool"] = q["pool"]
        append_jsonl(out_path, row)
        labels.append(row)
        done.add(q["id"])
        print(f"  -> {row['label']}")
        i += 1

    left = len(pool) - len(done)
    print(f"\nlabeled {len(done)}/{len(pool)}" + (f", {left} left" if left else ", all done !!"))
    if skipped:
        print(f"skipped {len(skipped)} this session, theyll show up again next time")


if __name__ == "__main__":
    main()
