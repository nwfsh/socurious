## streamlit ui for the offline ml work: label questions + see how the categories hold up
## same files as label.py / evaluate.py, so u can mix terminal and browser freely
##
## label tab:    blind labeling, deberta's guess stays hidden (anchoring bias, same as label.py)
## evaluate tab: ur labels vs deberta (or a trained .joblib), per category + confusion matrix + mistakes
##
## usage: streamlit run src/ml/app.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # streamlit only puts src/ml on the path

import altair as alt
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from src.ml.common import (
    SAMPLE_PATH, LABELS_PATH, TRAIN_PATH, TEST_PATH, MODELS_DIR,
    LABELS, read_jsonl, write_jsonl, append_jsonl,
)

st.set_page_config(page_title="socurious categories", layout="wide")


## ---------- label ----------

def label_tab():
    sample = read_jsonl(SAMPLE_PATH)
    if not sample:
        st.warning("no sample found, run `python3 -m src.ml.sample` first")
        return

    labels = read_jsonl(LABELS_PATH)
    done = {r["id"] for r in labels}
    skipped = st.session_state.setdefault("skipped", set())
    todo = [q for q in sample if q["id"] not in done and q["id"] not in skipped]

    st.progress(len(done) / len(sample), text=f"labeled {len(done)}/{len(sample)}")

    if not todo:
        if skipped:
            st.info(f"only skipped questions left ({len(skipped)})")
            if st.button("bring skipped back"):
                skipped.clear()
                st.rerun()
        else:
            st.success("all done !!")
        undo_button(labels)
        return

    q = todo[0]
    st.markdown(f"### {q['text']}")

    def save(topic):
        append_jsonl(LABELS_PATH, {"id": q["id"], "text": q["text"], "topic": topic, "good": topic is not None})

    cols = st.columns(5)
    for i, label in enumerate(LABELS):
        if cols[i % 5].button(label, key=f"lbl_{label}", width="stretch"):
            save(label)
            st.rerun()

    st.write("")
    a, b, c = st.columns(3)
    if a.button("bad question (shouldnt be in the app)", width="stretch"):
        save(None)
        st.rerun()
    if b.button("skip for now", width="stretch"):
        skipped.add(q["id"])
        st.rerun()
    with c:
        undo_button(labels)

    if labels:
        last = labels[-1]
        st.caption(f"last: {last['topic'] or 'bad question'} ← {last['text']}")


def undo_button(labels):
    if st.button("undo last label", width="stretch", disabled=not labels):
        labels.pop()
        write_jsonl(LABELS_PATH, labels)
        st.rerun()


## ---------- evaluate ----------

@st.cache_resource
def load_saved(path):
    import joblib
    from sentence_transformers import SentenceTransformer
    bundle = joblib.load(path)
    return bundle["clf"], SentenceTransformer(bundle["embed_model"])


def predict(model, rows):
    if model == "deberta":
        stored = {q["id"]: q["deberta"] for q in read_jsonl(SAMPLE_PATH)}
        return [stored.get(r["id"], "none") for r in rows]
    clf, embedder = load_saved(model)
    return list(clf.predict(embedder.encode([r["text"] for r in rows])))


def evaluate_tab():
    labels = read_jsonl(LABELS_PATH)
    if not labels:
        st.warning("no labels yet, go label some first")
        return

    splits = {"all labels": labels}
    if TRAIN_PATH.exists():
        splits["train"] = read_jsonl(TRAIN_PATH)
    if TEST_PATH.exists():
        splits["test (final comparisons only)"] = read_jsonl(TEST_PATH)
    models = ["deberta"] + sorted(str(p) for p in MODELS_DIR.glob("*.joblib"))

    a, b = st.columns(2)
    split = a.selectbox("split", list(splits), index=1 if "train" in splits else 0)
    model = b.selectbox("model", models, format_func=lambda m: Path(m).name)

    if split.startswith("test"):
        st.warning("this is the locked test set, dont tune categories or models against what u see here")
    if model != "deberta" and split != "test (final comparisons only)":
        st.info("this model was trained on train.jsonl so these scores are inflated, check train_topic's cross val instead")

    rows = splits[split]
    good = [r for r in rows if r["good"]]
    bad = [r for r in rows if not r["good"]]
    if not good:
        st.warning("no good questions labeled in this split yet")
        return

    y = [r["topic"] for r in good]
    preds = predict(model, good)

    m1, m2, m3 = st.columns(3)
    m1.metric("accuracy", f"{accuracy_score(y, preds):.2f}")
    m2.metric("questions", len(good))
    m3.metric("bad questions", len(bad), help="labeled 'x', not scored")

    st.subheader("per category")
    report = classification_report(y, preds, labels=LABELS, zero_division=0, output_dict=True)
    per_cat = pd.DataFrame({l: report[l] for l in LABELS}).T
    per_cat["support"] = per_cat["support"].astype(int)
    per_cat["predicted"] = [preds.count(l) for l in LABELS]
    st.dataframe(
        per_cat[["precision", "recall", "f1-score", "support", "predicted"]].style.format(
            {"precision": "{:.2f}", "recall": "{:.2f}", "f1-score": "{:.2f}"}
        ),
        width="stretch",
    )
    st.caption("low precision = category is a catch-all eating other stuff. low recall = category is leaking into others")

    st.subheader("confusion matrix")
    present = [l for l in LABELS if l in y or l in preds]
    cm = confusion_matrix(y, preds, labels=present)
    cells = pd.DataFrame(
        [{"truth": t, "predicted": p, "n": int(cm[i][j])}
         for i, t in enumerate(present) for j, p in enumerate(present)]
    )
    base = alt.Chart(cells).encode(
        x=alt.X("predicted:N", sort=present, title="predicted"),
        y=alt.Y("truth:N", sort=present, title="ur label"),
    )
    heat = base.mark_rect().encode(
        color=alt.Color("n:Q", scale=alt.Scale(scheme="blues"), legend=None),
        tooltip=["truth", "predicted", "n"],
    )
    text = base.mark_text().encode(
        text=alt.condition(alt.datum.n > 0, "n:Q", alt.value("")),
        color=alt.condition(alt.datum.n > cm.max() / 2, alt.value("white"), alt.value("black")),
    )
    st.altair_chart((heat + text).properties(height=420), width="stretch")

    st.subheader("mistakes")
    errors = pd.DataFrame(
        [{"ur label": t, "predicted": p, "text": r["text"]} for r, t, p in zip(good, y, preds) if t != p]
    )
    if errors.empty:
        st.success("no mistakes !!")
    else:
        f1, f2 = st.columns(2)
        truth_f = f1.multiselect("ur label", present)
        pred_f = f2.multiselect("predicted", present)
        if truth_f:
            errors = errors[errors["ur label"].isin(truth_f)]
        if pred_f:
            errors = errors[errors["predicted"].isin(pred_f)]
        st.dataframe(errors, width="stretch", hide_index=True)

    if bad and model == "deberta":
        st.subheader("where deberta put the bad questions")
        bad_preds = pd.Series(predict(model, bad)).value_counts().rename_axis("category").reset_index(name="n")
        st.dataframe(bad_preds, width="stretch", hide_index=True)


label, evaluate = st.tabs(["label", "evaluate"])
with label:
    label_tab()
with evaluate:
    evaluate_tab()
