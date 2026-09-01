import os
import psycopg
import numpy as np
from collections import Counter
from dotenv import load_dotenv
from src.transform.filters import should_reject
from src.transform.classify import classify_intimacy
from sentence_transformers import SentenceTransformer, util

load_dotenv()

# loading in embedding model 
_model = SentenceTransformer('all-MiniLM-L6-v2')
SIMILARITY_THRESHOLD = 0.90

INTIMACY_FLOOR = -0.25

def load_clean_questions():
    with psycopg.connect(
        os.getenv("DATABASE_URL")
    ) as conn:
        rows = conn.execute(
            "SELECT id, raw_title FROM raw_questions WHERE question_id IS NULL AND rejection_reason is NULL"
            ## wont proccess raw questions where they already have a question id 
        ).fetchall()

        ## collect list of tuples ( your existing words ) -> turn into plan string -> then converting into embedded words ( vectors )
        existing_texts = conn.execute("SELECT text FROM questions").fetchall()
        existing_texts = [r[0] for r in existing_texts]
        existing_embeddings = _model.encode(existing_texts) if existing_texts else [] # incase tuple is empty, then it might behave weirdly

        kept = 0
        rejected_reasons = Counter()

        for raw_id, title in rows:
            rejected, reason, cleaned_question = should_reject(title)
            if rejected:
                rejected_reasons[reason] += 1
                conn.execute("UPDATE raw_questions SET rejection_reason = %s WHERE id = %s",
                (reason, raw_id))
                continue

            intimacy = classify_intimacy(cleaned_question)
            if intimacy < INTIMACY_FLOOR:
                rejected_reasons["too_impersonal"] += 1
                conn.execute("UPDATE raw_questions SET rejection_reason = %s WHERE id = %s",
                             ("too_impersonal", raw_id))
                continue

            ## converts incoming question into its embedded vector 
            candidate_embedding = _model.encode(cleaned_question)
            if len(existing_embeddings) > 0:

                ## check the similarity of incoming sentence + all the vector sentences that were in the database 
                scores = util.cos_sim(candidate_embedding, existing_embeddings)[0]

                ## check if they are similiar enough if so, then reject them 
                if float(scores.max()) >= SIMILARITY_THRESHOLD:
                    rejected_reasons["near_duplicate"] += 1
                    conn.execute("UPDATE raw_questions SET rejection_reason = %s WHERE id = %s",
                                 ("near_duplicate", raw_id))
                    continue

            ## if not similiar, now u can insert !
            result = conn.execute(
                """INSERT INTO questions (raw_question_id, text, intimacy_score)
                   VALUES (%s, %s, %s) RETURNING id""",
                (raw_id, cleaned_question, intimacy)
            )
            question_id = result.fetchone()[0]

            conn.execute(
                "UPDATE raw_questions SET question_id = %s WHERE id = %s",
                (question_id, raw_id) ## now raw_question will not reproccess as they use this as indicator 
            )
            existing_texts.append(cleaned_question)
            if len(existing_embeddings) == 0:
                existing_embeddings = candidate_embedding.reshape(1, -1)
            else:
                existing_embeddings = np.vstack([existing_embeddings, candidate_embedding.reshape(1, -1)])
            kept += 1

        conn.commit()

    print(f"Processed: {len(rows)}")
    print(f"Kept: {kept}")
    print(f"Rejected: {sum(rejected_reasons.values())}")
    for reason, count in rejected_reasons.most_common():
        print(f"  {reason}: {count}")


if __name__ == "__main__":
    load_clean_questions()

# NOTE: current approach re-stacks the full existing_embeddings array on every
# accepted insert (O(n) per insert). Fine at current scale (~500s of rows).
# If this becomes slow: split into a small `new_embeddings` list (O(1) append)
# for within-batch duplicates, keep existing_embeddings as the untouched
# pre-built array, and only vstack the small new_embeddings list per check.
# Do NOT defer vstack to end-of-loop naively — that silently breaks
# within-batch dedup, since later rows in the same batch wouldn't be
# compared against earlier-accepted rows from the same run.