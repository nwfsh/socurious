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
        """, (topic,)).fetchone() # fill in the %s with topic
    else:
        ## or just grab any random question 
        row = conn.execute("""
            SELECT id, text, intimacy_score
            FROM questions
            ORDER BY random()
            LIMIT 1
        """).fetchone()

    return row

# question_repo.py
def fetch_random_questions(topic: str | None = None, limit: int = 12):
    conn = get_conn()

    if topic:
        rows = conn.execute("""
            SELECT q.id, q.text, q.intimacy_score
            FROM questions q
            JOIN question_category qc ON q.id = qc.question_id
            JOIN categories c ON qc.category_id = c.id
            WHERE c.name = %s
            ORDER BY random()
            LIMIT %s 
        """, (topic, limit)).fetchall()  # fill in the %s and %s string with topic & limit 
    else:
        rows = conn.execute("""
            SELECT id, text, intimacy_score
            FROM questions
            ORDER BY random()
            LIMIT %s
        """, (limit,)).fetchall() 

    conn.close()
    return [{"id": r[0], "text": r[1], "intimacy_score": float(r[2])} for r in rows]
    ## this is list comprehension, for every r in row, build a dictionary of the id, text + intimacy score 