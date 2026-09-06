from src.transform.classify import get_conn

def fetch_random_question(
        topic: list[str] | None = None,
        min_intimacy: float | None = None,
        max_intimacy: float | None = None,
        ):
    conn = get_conn()

    conditions = []
    params = []

    if topic:
        # join %s by the number of topics written, eg: placeholders = '%s,%s'
        placeholders = ','.join(['%s'] * len(topic))
        conditions.append(f"c.name IN ({placeholders})")
        # extend lets u write WHERE c.name IN (%s,%s)
        # -    with params ['relationships', 'career']
        params.extend(topic)

    if min_intimacy is not None:
        conditions.append("q.intimacy_score >= %s")
        params.append(min_intimacy)

    if max_intimacy is not None:
        conditions.append("q.intimacy_score <= %s")
        params.append(max_intimacy)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    if conditions:
        row = conn.execute(f"""
            SELECT q.id, q.text, q.intimacy_score
            FROM questions q
            JOIN question_category qc ON q.id = qc.question_id
            JOIN categories c ON qc.category_id = c.id
            {where_clause}
            ORDER BY random()
            LIMIT 1
        """, params).fetchone()
    else:
        row = conn.execute("""
            SELECT id, text, intimacy_score
            FROM questions
            ORDER BY random()
            LIMIT 1
        """).fetchone()

    conn.close()
    return {"id": row[0], "text": row[1], "intimacy_score": float(row[2])} if row else None

def fetch_random_questions(
        topic: list[str] | None = None,
        min_intimacy: float | None = None,
        max_intimacy: float | None = None,
        limit: int = 12):
    conn = get_conn()

    conditions = []
    params = []

    if topic:
        placeholders = ','.join(['%s'] * len(topic))
        conditions.append(f"c.name IN ({placeholders})")
        params.extend(topic)

    if min_intimacy is not None:
        conditions.append("q.intimacy_score >= %s")
        params.append(min_intimacy)

    if max_intimacy is not None:
        conditions.append("q.intimacy_score <= %s")
        params.append(max_intimacy)

    if conditions:
        topic_join = "JOIN question_category qc ON q.id = qc.question_id JOIN categories c ON qc.category_id = c.id" if topic else ""
        where_clause = f"WHERE {' AND '.join(conditions)}"
        rows = conn.execute(f"""
            WITH matching AS (
                SELECT DISTINCT q.id, q.text, q.intimacy_score
                FROM questions q
                {topic_join}
                {where_clause}
            )
            SELECT id, text, intimacy_score
            FROM matching
            ORDER BY random()
            LIMIT %s
        """, params + [limit]).fetchall()
    else:
        rows = conn.execute("""
            SELECT id, text, intimacy_score
            FROM questions
            ORDER BY random()
            LIMIT %s
        """, (limit,)).fetchall()

    conn.close()
    return [{"id": r[0], "text": r[1], "intimacy_score": float(r[2])} for r in rows]
