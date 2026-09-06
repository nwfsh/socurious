from fastapi import APIRouter, Query, Request 
from src.api.services.question_service import get_random_question, get_random_questions
from src.api.limiter import limiter

router = APIRouter()

@router.get("/random")
@limiter.limit("60/minute")
def random_question(
        request: Request,
        topic: str | None = Query(None, max_length=20),
        min_intimacy: float | None = Query(None, ge=-0.25, le=1.0),
        max_intimacy: float | None = Query(None, ge=-0.25, le=1.0),
        ):
    return get_random_question(topic=topic, min_intimacy=min_intimacy, max_intimacy=max_intimacy)

@router.get("/random/batch")
@limiter.limit("60/minute")
def random_questions(
        request: Request,
        topic: str | None = Query(None, max_length=20),
        min_intimacy: float | None = Query(None, ge=-0.25, le=1.0),
        max_intimacy: float | None = Query(None, ge=-0.25, le=1.0),
        limit: int = Query(12, ge=1, le=50),
        ):
    return get_random_questions(topic=topic, min_intimacy=min_intimacy, max_intimacy=max_intimacy, limit=limit)