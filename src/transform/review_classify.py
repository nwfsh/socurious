import psycopg
import os
from dotenv import load_dotenv
from src.transform.classify import classify_topic, classify_intimacy

load_dotenv()


def get_conn():
    return psycopg.connect(
        os.getenv("DATABASE_URL")
    )

def review_classifications(limit: int = 20):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT text FROM questions ORDER BY random() LIMIT %s", (limit,)
        ).fetchall()

    results = []
    for (text,) in rows:
        topic, topic_score = classify_topic(text)
        intimacy = classify_intimacy(text)
        results.append((text, topic, topic_score, intimacy))

    results.sort(key=lambda r: r[3])

    for text, topic, topic_score, intimacy in results:
        print(f"[{intimacy:.2f}] [{topic} {topic_score:.2f}] {text}")

if __name__ == "__main__":
    review_classifications()
    
