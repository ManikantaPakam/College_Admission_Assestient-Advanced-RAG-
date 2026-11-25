from pydantic import BaseModel, Field
from typing import Optional


# Request Schema
class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=3,
        description="User question for the RAG application"
    )


# Source Schema
class SourceResponse(BaseModel):

    file: Optional[str] = None
    page: Optional[int] = None
    category: Optional[str] = None


# Response Schema
class ChatResponse(BaseModel):

    question: str
    rewritten_query: str
    answer: str
    sources: list[SourceResponse]