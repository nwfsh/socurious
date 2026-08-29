from fastapi import APIRouter, HTTPException, Query
from src.api.services.question_service import get_random_question, get_random_questions

router = APIRouter()

@router.get("/random")
def random_question(topic: str | None = Query(None)):
    """Return a single random question."""
    return get_random_question(topic = topic)

@router.get("/random/batch")
def random_questions(topic: str | None = Query(None)):
    """Return multiple random questions."""
    return get_random_questions(topic = topic)