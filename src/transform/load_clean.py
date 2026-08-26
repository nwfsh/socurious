import os
import psycopg
from collections import Counter
from dotenv import load_dotenv
from src.transform.filters import should_reject

load_dotenv()

def load_clean_questions():
    with psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    ) as conn:
        rows = conn.execute(
            "SELECT id, raw_title FROM raw_questions WHERE question_id IS NULL AND rejection_reason is NULL"
            ## wont proccess raw questions where they already have a question id 
        ).fetchall()

        kept = 0
        rejected_reasons = Counter()

        for raw_id, title in rows:
            rejected, reason, cleaned_question = should_reject(title)
            if rejected:
                rejected_reasons[reason] += 1
                conn.execute("UPDATE raw_questions SET rejection_reason = %s WHERE id = %s",
                (reason, raw_id))
                continue

            result = conn.execute(
                """INSERT INTO questions (raw_question_id, text, severity)
                   VALUES (%s, %s, %s) RETURNING id""",
                (raw_id, cleaned_question, 1)  # severity=1 placeholder until classification is added
            )
            question_id = result.fetchone()[0]

            conn.execute(
                "UPDATE raw_questions SET question_id = %s WHERE id = %s",
                (question_id, raw_id) ## now raw_question will not reproccess as they use this as indicator 
            )
            kept += 1

        conn.commit()

    print(f"Processed: {len(rows)}")
    print(f"Kept: {kept}")
    print(f"Rejected: {sum(rejected_reasons.values())}")
    for reason, count in rejected_reasons.most_common():
        print(f"  {reason}: {count}")


if __name__ == "__main__":
    load_clean_questions()