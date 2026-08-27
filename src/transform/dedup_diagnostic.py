from rapidfuzz import fuzz, process
from src.transform.classify import get_conn

def run_dedup_diagnostic(threshold: int):
    conn = get_conn()
    rows = conn.execute("SELECT id, text FROM questions").fetchall()
    texts = [r[1] for r in rows]

    ## using their optimized batch function becus i dont wanna be writing n^2 for loops 
    near_dupes = []
    for i, text in enumerate(texts):
        # compare this text against everything after it, using rapidfuzz's optimized batch function
        matches = process.extract(
            text, texts[i+1:], scorer=fuzz.ratio, score_cutoff=threshold, limit=None
        )
        for match_text, score, _ in matches:
            near_dupes.append((text, match_text, score))

    print(f"Found {len(near_dupes)} near-duplicate pairs out of {len(rows)} questions")
    for a, b, score in near_dupes:
        print(f"[{score}] {a}\n   <-> {b}\n")


def test_threshold_cases(threshold: int):
    """Manually curated test cases to check threshold behavior against
    known true-duplicate and known false-duplicate pairs."""
    
    test_pairs = [
        # (text_a, text_b, expected_duplicate)
        ("What's your biggest fear?", "whats ur biggest fear", True),
        ("Why indian developers leaked gta 6?", "Why indian developers leaked the gta 6?", True),
        ("Do you like bananas and oranges?", "Do you prefer oranges or bananas?", False),
        ("What's your favorite movie?", "What's your favorite food?", False),
        ("How do you deal with heartbreak?", "How do you cope with heartbreak?", True),
    ]

    for text_a, text_b, expected in test_pairs:
        score = fuzz.ratio(text_a, text_b)
        predicted = score >= threshold
        status = "✅" if predicted == expected else "❌"
        print(f"{status} [{score:.1f}] expected_dup={expected} predicted_dup={predicted}")
        print(f"    {text_a}\n    {text_b}\n")


if __name__ == "__main__":
    run_dedup_diagnostic(90)
    test_threshold_cases(90)

