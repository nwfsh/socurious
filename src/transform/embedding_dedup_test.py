from sentence_transformers import SentenceTransformer, util
from src.transform.classify import get_conn


model = SentenceTransformer('all-MiniLM-L6-v2')

def run_embedding_diagnostic(threshold: float):
    conn = get_conn()
    rows = conn.execute("SELECT id, text FROM questions").fetchall()
    texts = [r[1] for r in rows]
    embeddings = model.encode(texts)

    near_dupes = []
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            score = util.cos_sim(embeddings[i], embeddings[j]).item()
            if score >= threshold:
                near_dupes.append((texts[i], texts[j], score))

    print(f"Found {len(near_dupes)} near-duplicate pairs")
    for a, b, score in near_dupes:
        print(f"[{score:.3f}] {a}\n    <-> {b}\n")

def test_embedding_cases():
    test_pairs = [
        ("What's your biggest fear?", "whats ur biggest fear", True),
        ("Why indian developers leaked gta 6?", "Why indian developers leaked the gta 6?", True),
        ("Do you like bananas and oranges?", "Do you prefer oranges or bananas?", False),
        ("What's your favorite movie?", "What's your favorite food?", False),
        ("How do you deal with heartbreak?", "How do you cope with heartbreak?", True),
    ]

    for text_a, text_b, expected in test_pairs:
        emb_a = model.encode(text_a)
        emb_b = model.encode(text_b)
        score = util.cos_sim(emb_a, emb_b).item()
        print(f"[{score:.3f}] expected_dup={expected}")
        print(f"    {text_a}\n    {text_b}\n")


if __name__ == "__main__":
    run_embedding_diagnostic(0.90)
    test_embedding_cases()