from pydantic import BaseModel

from typing import List, Optional


class ChatRequest(BaseModel):

    query: str

    top_k: int = 5


class SourceResponse(BaseModel):

    content: str

    source: Optional[str] = None

    score: Optional[float] = None


class ChatResponse(BaseModel):

    answer: str

    sources: List[SourceResponse]