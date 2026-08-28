from fastapi import FastAPI
from src.api.routers import questions

app = FastAPI(title="Socurious API")

app.include_router(questions.router, prefix="/questions", tags=["questions"])
