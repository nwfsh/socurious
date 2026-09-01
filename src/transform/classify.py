from transformers import pipeline
from question_intimacy.predict_intimacy import IntimacyEstimator
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

## to decide on topic, zero shot classification 
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
topic_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")

## intamacy score model ( researched backed YAY win for avery)
intimacy_scorer = IntimacyEstimator(cuda=False)

## very simple maybe not the best for now
categories = [
    "relationships",
    "family and childhood",
    "career",
    "fears and insecurities",
    "random everyday questions",
    "hypothetical scenarios",
    "sexual",
    "controversial debate",
    "advice",
]

# helper function 
def classify_topic(title: str) -> tuple[str,float]:
    result = topic_classifier(title, categories)
    return result["labels"][0], result["scores"][0]

# helper function 
def classify_intimacy(title: str) -> float:
    result = intimacy_scorer.predict([title], type='list')
    return float(result[0])

def get_conn():
    return psycopg.connect(
        os.getenv("DATABASE_URL")
    )

def classify_and_store(conn, threshold: float = 0.4):
    rows = conn.execute(
        "SELECT id, text FROM questions WHERE intimacy_score IS NULL"
    ).fetchall()

    for question_id, text in rows:
        ## eg (relationships, 0.40)
        label, score = classify_topic(text)
        if score >= threshold:
            category_row = conn.execute(
                "SELECT id FROM categories WHERE name = %s", (label,)
            ).fetchone()
            ## making sure that the category name even exist in the database 
            if category_row:
                category_id = category_row[0] ## psycog returns selection as multiple tuples even if its just one number, so u just gotta grab that 
                ## turning (4,) into 4, an int 
                conn.execute(
                    """INSERT INTO question_category (question_id, category_id)
                       VALUES (%s, %s) ON CONFLICT DO NOTHING""",
                    (question_id, category_id)
                )

    conn.commit()
    print(f"Classified {len(rows)} questions")


if __name__ == "__main__":
    conn = get_conn()
    classify_and_store(conn)
    conn.close()

## so far with abt 500 questions we have..
# ORDER BY COUNT(*) DESC;
#            name            | count 
# ---------------------------+-------
#  random everyday questions |   126
#  relationships             |    94
#  hypothetical scenarios    |    80
#  advice                    |    37
#  controversial debate      |    27
#  sexual                    |    23
#  family and childhood      |    22
#  career                    |    12
#  fears and insecurities    |     2
# (9 rows)

## if you ever decided to remove one of teh categories,
## remove the categories and re run classify on orphaned tuples 
