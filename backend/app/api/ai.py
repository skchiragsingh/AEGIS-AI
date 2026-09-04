from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.rag import ask_aegis


router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)


class AIRequest(BaseModel):
    query: str


@router.post("/ask")
def ask_ai(request: AIRequest):
    answer = ask_aegis(request.query)

    return {
        "status": "success",
        "query": request.query,
        "answer": answer
    }