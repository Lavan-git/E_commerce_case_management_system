from pydantic import BaseModel, Field


class RAGQueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class RAGSource(BaseModel):
    source: str
    section: str
    score: float


class RAGQueryResponse(BaseModel):
    answer: str
    sources: list[RAGSource]
    retrieved_chunks: int
    grounding_blocked: bool
    grounding_violations: list[str]