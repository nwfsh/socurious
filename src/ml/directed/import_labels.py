## step 4: pull ur corrected train labels out of a label studio JSON export
## export from label studio: project -> export -> JSON, then point this at the file
## keeps llama's original label next to urs so agreement.py can count overrides
##
## usage: python3 -m src.ml.directed.import_labels path/to/export.json

import argparse
import json
from collections import Counter
from src.ml.directed.common import LLAMA_TRAIN_PATH, TRAIN_PATH, read_jsonl, write_jsonl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("export", help="label studio JSON export")
    args = parser.parse_args()

    llama = {r["id"]: r["llama"] for r in read_jsonl(LLAMA_TRAIN_PATH)}
    with open(args.export) as f:
        tasks = json.load(f)

    rows, unlabeled = [], 0
    for task in tasks:
        ## last non-cancelled annotation = ur final answer
        annotations = [a for a in task.get("annotations", []) if not a.get("was_cancelled")]
        choices = [r["value"]["choices"][0] for a in annotations[-1:] for r in a["result"] if r.get("type") == "choices"]
        if not choices:
            unlabeled += 1
            continue
        qid = task["data"]["id"]
        rows.append({
            "id": qid,
            "text": task["data"]["text"],
            "pool": task["data"].get("pool"),
            "label": choices[0],
            "llama": llama.get(qid),
            "overridden": choices[0] != llama.get(qid),
            "labeled_at": annotations[-1].get("updated_at") or annotations[-1].get("created_at"),
        })

    write_jsonl(TRAIN_PATH, rows)
    counts = Counter(r["label"] for r in rows)
    print(f"wrote {len(rows)} train labels to {TRAIN_PATH}" + (f", {unlabeled} tasks still unlabeled" if unlabeled else ""))
    for label, n in counts.most_common():
        print(f"  {label:14} {n}")


if __name__ == "__main__":
    main()
