## streamlit version of label.py, same files, so u can mix terminal and browser freely
##
## test mode:    blind-label the test pool. nothing from llama or the old rules is shown (anchoring bias)
## relabel mode: a week+ later, label 50 test questions again without seeing ur first answer, for kappa
##
## usage: streamlit run src/ml/directed/app.py

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # streamlit only puts src/ml/directed on the path

import streamlit as st

from src.ml.directed.common import (
    TEST_POOL_PATH, TEST_PATH, RELABEL_PATH, LABELS, UNSURE, DEFINITIONS,
    relabel_pool, days_until_relabel, read_jsonl, write_jsonl, append_jsonl,
)

st.set_page_config(page_title="socurious directed labels", layout="centered")

BUTTONS = [(LABELS[0], "general"), (LABELS[1], "fixable"), (LABELS[2], "unsalvageable"), (UNSURE, "unsure")]


def get_pool(mode):
    """the questions to label in this mode, or None if theres nothing to do yet"""
    if mode == "test":
        pool = read_jsonl(TEST_POOL_PATH)
        if not pool:
            st.warning("no test pool found, run `python3 -m src.ml.directed.sample` first")
            return None
        return pool

    test_labels = read_jsonl(TEST_PATH)
    if not test_labels:
        st.warning("no test labels yet, label the test pool first")
        return None
    days = days_until_relabel(test_labels)
    if days and not st.checkbox(f"its only been a bit, wait ~{days} more day(s) or ull just remember ur answers. relabel anyway?"):
        return None
    return relabel_pool(test_labels)


def label_view(mode):
    out_path = TEST_PATH if mode == "test" else RELABEL_PATH
    pool = get_pool(mode)
    if pool is None:
        return

    labels = read_jsonl(out_path)
    pool_ids = {q["id"] for q in pool}
    done = {r["id"] for r in labels} & pool_ids
    skipped = st.session_state.setdefault(f"skipped_{mode}", set())
    todo = [q for q in pool if q["id"] not in done and q["id"] not in skipped]

    st.progress(len(done) / len(pool), text=f"labeled {len(done)}/{len(pool)}")

    if not todo:
        if skipped:
            st.info(f"only skipped questions left ({len(skipped)})")
            if st.button("bring skipped back"):
                skipped.clear()
                st.rerun()
        else:
            st.success("all done !!")
        undo_button(labels, out_path)
        return

    q = todo[0]
    st.markdown(f"### {q['text']}")

    def save(label):
        row = {"id": q["id"], "text": q["text"], "label": label, "labeled_at": datetime.now().isoformat()}
        if "pool" in q:
            row["pool"] = q["pool"]
        append_jsonl(out_path, row)

    cols = st.columns(len(BUTTONS))
    for col, (label, text) in zip(cols, BUTTONS):
        if col.button(text, key=f"{mode}_{label}", width="stretch", type="primary" if label != UNSURE else "secondary"):
            save(label)
            st.rerun()

    st.write("")
    a, b = st.columns(2)
    if a.button("skip for now", width="stretch"):
        skipped.add(q["id"])
        st.rerun()
    with b:
        undo_button(labels, out_path)

    ## only ever shows the label u JUST gave in this mode, never ur first answer while relabeling
    if labels:
        st.caption(f"last: {labels[-1]['label']} ← {labels[-1]['text']}")


def undo_button(labels, out_path):
    if st.button("undo last label", width="stretch", disabled=not labels):
        labels.pop()
        write_jsonl(out_path, labels)
        st.rerun()


mode = st.sidebar.radio(
    "mode", ["test", "relabel"],
    format_func=lambda m: {"test": "test (blind)", "relabel": "relabel (for kappa)"}[m],
)
with st.sidebar.expander("label definitions", expanded=True):
    st.code(DEFINITIONS, language=None, wrap_lines=True)

label_view(mode)
