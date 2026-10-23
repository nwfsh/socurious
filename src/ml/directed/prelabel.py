## step 3: llama pre-labels BOTH pools, locally through ollama
##   train -> llama_train.jsonl + label_studio_import.json (u see these, then correct them)
##   test  -> llama_test.jsonl (u NEVER see these, its how we measure llama honestly, see agreement.py)
## run this AFTER ur done blind-labeling the test pool, so theres no way to peek
##
## needs ollama running: `ollama serve` + `ollama pull llama3.1:8b`
##
## usage: python3 -m src.ml.directed.prelabel [--model llama3.1:8b]

import argparse
import json
import requests
from src.ml.directed.common import (
    TEST_POOL_PATH, TRAIN_POOL_PATH, TEST_PATH,
    LLAMA_TRAIN_PATH, LLAMA_TEST_PATH, LABEL_STUDIO_IMPORT_PATH,
    LABELS, DEFINITIONS, read_jsonl, write_jsonl, append_jsonl,
)

OLLAMA_URL = "http://localhost:11434/api/chat"

PROMPT = f"""You label questions for a question bank that partners ask each other.
Each question came from Reddit. Decide if it's aimed at a specific group of people.

{DEFINITIONS}

Answer with JSON only: {{"label": "general" | "fixable" | "unsalvageable"}}"""


def ask_llama(model: str, text: str) -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [{"role": "system", "content": PROMPT}, {"role": "user", "content": text}],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0, "seed": 42},  # same answer every run
        },
        timeout=120,
    )
    resp.raise_for_status()
    try:
        label = json.loads(resp.json()["message"]["content"]).get("label")
    except json.JSONDecodeError:
        label = None
    ## anything weird counts as llama not knowing, not as a guess
    return label if label in LABELS else "invalid"


def prelabel(model, pool, out_path):
    done = {r["id"] for r in read_jsonl(out_path)}  # resume if it crashed halfway
    todo = [q for q in pool if q["id"] not in done]
    for n, q in enumerate(todo, 1):
        label = ask_llama(model, q["text"])
        append_jsonl(out_path, {"id": q["id"], "text": q["text"], "llama": label, "model": model})
        print(f"  [{n}/{len(todo)}] {label:14} {q['text'][:80]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="llama3.1:8b")
    args = parser.parse_args()

    test_pool, train_pool = read_jsonl(TEST_POOL_PATH), read_jsonl(TRAIN_POOL_PATH)
    if not train_pool:
        print("no pools found, run python3 -m src.ml.directed.sample first")
        return
    if len(read_jsonl(TEST_PATH)) < len(test_pool):
        print("finish blind-labeling the test pool first (python3 -m src.ml.directed.label)")
        print("otherwise llama_test.jsonl is sitting right there while u label")
        return

    print("test pool (hidden):")
    prelabel(args.model, test_pool, LLAMA_TEST_PATH)
    print("train pool:")
    prelabel(args.model, train_pool, LLAMA_TRAIN_PATH)

    ## label studio import: one task per question, llama's label as a pre-filled prediction
    llama = {r["id"]: r["llama"] for r in read_jsonl(LLAMA_TRAIN_PATH)}
    tasks = []
    for q in train_pool:
        task = {"data": {"id": q["id"], "text": q["text"], "pool": q["pool"]}}
        if llama.get(q["id"]) in LABELS:
            task["predictions"] = [{
                "model_version": args.model,
                "result": [{
                    "from_name": "label", "to_name": "text", "type": "choices",
                    "value": {"choices": [llama[q["id"]]]},
                }],
            }]
        tasks.append(task)
    LABEL_STUDIO_IMPORT_PATH.write_text(json.dumps(tasks, indent=2))

    invalid = sum(1 for v in llama.values() if v == "invalid")
    print(f"wrote {len(tasks)} tasks to {LABEL_STUDIO_IMPORT_PATH}" + (f" ({invalid} with no valid llama label)" if invalid else ""))


if __name__ == "__main__":
    main()
