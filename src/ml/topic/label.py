## step 2: label questions in the terminal, one at a time
## saves after every answer so u can quit and come back whenever
## deberta's guess is hidden on purpose, seeing it would nudge ur answer (anchoring bias)
##
## usage: python3 -m src.ml.topic.label

from src.ml.topic.common import SAMPLE_PATH, LABELS_PATH, LABELS, read_jsonl, write_jsonl, append_jsonl

KEYS = {str(i + 1): label for i, label in enumerate(LABELS[:9])}
KEYS["0"] = LABELS[9]  # none

HELP = "\n".join(f"  {k}  {v}" for k, v in KEYS.items()) + """
  x  bad question (shouldnt be in the app at all)
  s  skip for now
  u  undo last label
  q  quit"""


def main():
    sample = read_jsonl(SAMPLE_PATH)
    if not sample:
        print(f"no sample found, run python3 -m src.ml.topic.sample first")
        return

    labels = read_jsonl(LABELS_PATH)
    done = {row["id"] for row in labels}
    todo = [q for q in sample if q["id"] not in done]
    skipped = []

    print(HELP)
    i = 0
    while i < len(todo):
        q = todo[i]
        print(f"\n[{len(done) + 1}/{len(sample)}]  {q['text']}")
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
            write_jsonl(LABELS_PATH, labels)
            done.discard(last["id"])
            ## put the undone question back in front of the current one
            todo.insert(i, next(s for s in sample if s["id"] == last["id"]))
            print(f"undid: {last['text']}")
            continue
        if key == "x":
            row = {"id": q["id"], "text": q["text"], "topic": None, "good": False}
        elif key in KEYS:
            row = {"id": q["id"], "text": q["text"], "topic": KEYS[key], "good": True}
        else:
            print("? for keys")
            continue

        append_jsonl(LABELS_PATH, row)
        labels.append(row)
        done.add(q["id"])
        print(f"  -> {row['topic'] or 'bad question'}")
        i += 1

    left = len(sample) - len(done)
    print(f"\nlabeled {len(done)}/{len(sample)}" + (f", {left} left" if left else ", all done !!"))
    if skipped:
        print(f"skipped {len(skipped)} this session, theyll show up again next time")


if __name__ == "__main__":
    main()
