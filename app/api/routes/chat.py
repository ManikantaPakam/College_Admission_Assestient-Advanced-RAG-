from fastapi import APIRouter, Request
from app.core.rate_limiter import limiter
from app.api.schemas.chat import ChatRequest, ChatResponse
from app.rag.pipeline import run_rag_pipeline
import logging

logger = logging.getLogger(__name__)

# Create API Router
router = APIRouter(
    prefix="/api/v1",
    tags=["RAG Chat"]
)


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
def chat(
    request: Request,
    chat_request: ChatRequest
):

    logger.info("Chat request received")

    question = chat_request.question

    result = run_rag_pipeline(question)

    logger.info("RAG pipeline completed successfully")

    return ChatResponse(
        question=result["original_question"],
        rewritten_query=result["rewritten_query"],
        answer=result["answer"],
        sources=result["sources"]
    )