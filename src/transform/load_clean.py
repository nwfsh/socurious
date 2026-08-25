import psycopg
from collections import Counter
from src.transform.filters import should_reject

def load_clean_questions():
    conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
    rows = conn.execute(
        "SELECT id, raw_title FROM raw_questions WHERE question_id IS NULL"
    ).fetchall()

    kept = 0
    rejected_reasons = Counter()

    for raw_id, title in rows:
        rejected, reason = should_reject(title)
        if rejected:
            rejected_reasons[reason] += 1
            continue

        result = conn.execute(
            """INSERT INTO questions (raw_question_id, text, severity)
               VALUES (%s, %s, %s) RETURNING id""",
            (raw_id, title, 1)
        )
        question_id = result.fetchone()[0]

        conn.execute(
            "UPDATE raw_questions SET question_id = %s WHERE id = %s",
            (question_id, raw_id)
        )
        kept += 1

    conn.commit()
    conn.close()

    print(f"Processed: {len(rows)}")
    print(f"Kept: {kept}")
    print(f"Rejected: {sum(rejected_reasons.values())}")
    for reason, count in rejected_reasons.most_common():
        print(f"  {reason}: {count}")


if __name__ == "__main__":
    load_clean_questions()