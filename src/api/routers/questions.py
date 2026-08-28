from fastapi import APIRouter
from src.api.services import question_service

router = APIRouter()


@router.get("/random")
def get_random_question():
    """Return a single random question."""
    pass
