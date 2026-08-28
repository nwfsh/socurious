from fastapi import APIRouter, HTTPException, Query
from src.api.services.question_service import get_random_question

router = APIRouter

router = APIRouter()


@router.get("/random")
def random_question(topic: str | None = Query(None)):
    """Return a single random question."""
    return get_random_question(topic = topic)
