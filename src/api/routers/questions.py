from fastapi import APIRouter, Query
from src.api.services.question_service import get_random_question, get_random_questions

router = APIRouter()

@router.get("/random")
def random_question(
        topic: str | None = Query(None),
        min_intimacy: float | None = Query(None),
        max_intimacy: float | None = Query(None),
        ):
    return get_random_question(topic=topic, min_intimacy=min_intimacy, max_intimacy=max_intimacy)

@router.get("/random/batch")
def random_questions(
        topic: str | None = Query(None),
        min_intimacy: float | None = Query(None),
        max_intimacy: float | None = Query(None),
        limit: int = Query(12),
        ):
    return get_random_questions(topic=topic, min_intimacy=min_intimacy, max_intimacy=max_intimacy, limit=limit)