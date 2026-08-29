from src.api.repository.question_repo import fetch_random_question, fetch_random_questions
from fastapi import HTTPException

def get_random_question(topic: str | None = None, min_intimacy: float | None = None, max_intimacy: float | None = None):
    result = fetch_random_question(topic=topic, min_intimacy=min_intimacy, max_intimacy=max_intimacy)
    if result is None:
        raise HTTPException(status_code=404, detail="No question found matching the given filters")
    return result

def get_random_questions(topic: str | None = None, min_intimacy: float | None = None, max_intimacy: float | None = None, limit: int = 12):
    questions = fetch_random_questions(topic=topic, min_intimacy=min_intimacy, max_intimacy=max_intimacy, limit=limit)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found matching the given filters")
    return questions
## adde