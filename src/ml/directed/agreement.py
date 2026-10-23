## step 5: how good are the labels? (ADR 012, "two measures of label quality")
##   kappa         ur test labels vs ur relabel of the same 50. the ceiling on the whole project
##   llama blind   llama's hidden test labels vs ur blind ones. how good llama ACTUALLY is
##   override rate how often u changed llama's label on train. how good llama LOOKS when u can see it
## gap between the last two = how much seeing llama's answer pulled u toward it
##
## this only scores the labels, not any model
##
## usage: python3 -m src.ml.directed.agreement

from collections import Counter
from sklearn.metrics import cohen_kappa_score, confusion_matrix
from src.ml.directed.common import (
    TEST_PATH, RELABEL_PATH, TRAIN_PATH, LLAMA_TEST_PATH, LABELS, UNSURE, read_jsonl,
)


def kappa():
    first = {r["id"]: r["label"] for r in read_jsonl(TEST_PATH)}
    again = {r["id"]: r["label"] for r in read_jsonl(RELABEL_PATH)}
    ids = [i for i in again if i in first]
    print("\n== self-agreement (kappa) ==")
    if len(ids) < 10:
        print(f"only {len(ids)} relabeled so far, run python3 -m src.ml.directed.label --relabel")
        return
    a, b = [first[i] for i in ids], [again[i] for i in ids]
    k = cohen_kappa_score(a, b)
    same = sum(x == y for x, y in zip(a, b))
    print(f"kappa {k:.2f} on {len(ids)} questions ({same} identical)")
    print("  below ~0.7 = tighten the label definitions before training anything")
    changed = Counter((x, y) for x, y in zip(a, b) if x != y)
    for (x, y), n in changed.most_common():
        print(f"  {x} -> {y}: {n}")


def llama_blind():
    mine = {r["id"]: r["label"] for r in read_jsonl(TEST_PATH)}
    llama = {r["id"]: r["llama"] for r in read_jsonl(LLAMA_TEST_PATH)}
    print("\n== llama on the blind test set ==")
    if not llama:
        print("no llama_test.jsonl yet, run python3 -m src.ml.directed.prelabel")
        return None
    ## unsure isnt a real answer, so it cant be right or wrong
    ids = [i for i in llama if mine.get(i) in LABELS]
    agree = sum(mine[i] == llama[i] for i in ids)
    rate = agree / len(ids)
    print(f"llama matches u on {agree}/{len(ids)} = {rate:.0%} (left out {sum(1 for i in llama if mine.get(i) == UNSURE)} unsure)")

    cols = LABELS + ["invalid"]
    cm = confusion_matrix([mine[i] for i in ids], [llama[i] for i in ids], labels=cols)
    corner = "u \\ llama"
    print(f"  {corner:14}" + "".join(f"{c[:6]:>8}" for c in cols))
    for label, row in zip(LABELS, cm):
        print(f"  {label:14}" + "".join(f"{n:8}" for n in row))
    return rate


def override_rate():
    rows = [r for r in read_jsonl(TRAIN_PATH) if r["label"] != UNSURE]
    print("\n== overrides on train (llama visible) ==")
    if not rows:
        print("no train labels yet, run python3 -m src.ml.directed.import_labels <export.json>")
        return None
    overridden = sum(r["overridden"] for r in rows)
    print(f"u changed llama's label on {overridden}/{len(rows)} = {overridden / len(rows):.0%}")
    flips = Counter((r["llama"], r["label"]) for r in rows if r["overridden"])
    for (was, now), n in flips.most_common():
        print(f"  llama {was} -> u {now}: {n}")
    return 1 - overridden / len(rows)


def main():
    kappa()
    blind = llama_blind()
    visible = override_rate()
    if blind is not None and visible is not None:
        print("\n== anchoring ==")
        print(f"llama looks {visible:.0%} right when u can see it, {blind:.0%} right when u cant")
        print(f"gap: {visible - blind:+.0%} (positive = seeing llama's answer pulled u toward it)")


if __name__ == "__main__":
    main()
