from src.transform.classify import get_conn

## only file that touches the database and queries it

def fetch_random_question(topic: str | None = None):
    conn = get_conn()

    ## for python psycopg, u need to write """ when u wanna do multiple sql lines
    if topic:
        row = conn.execute("""
            SELECT q.id, q.text, q.intimacy_score
            FROM questions q
            JOIN question_category qc ON q.id = qc.question_id
            JOIN categories c ON qc.category_id = c.id
            WHERE c.name = %s
            ORDER BY random()
            LIMIT 1
        """, (topic,)).fetchone() # (topic) returns only the topic (topic,) returns the actual tuple 
    else:
        ## or just grab any random question 
        row = conn.execute("""
            SELECT id, text, intimacy_score
            FROM questions
            ORDER BY random()
            LIMIT 1
        """).fetchone()

    return row
