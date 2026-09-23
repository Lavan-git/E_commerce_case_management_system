from fastapi import APIRouter, Depends

from src.app.rag.factory import get_rag_service
from src.app.rag.service import RAGService
from src.app.schemas.rag import (
    RAGQueryRequest,
    RAGQueryResponse,
    RAGSource,
)


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/query",
    response_model=RAGQueryResponse,
)
def query_rag(
    request: RAGQueryRequest,
    service: RAGService = Depends(get_rag_service),
) -> RAGQueryResponse:
    result = service.ask(
        request.question,
    )

    return RAGQueryResponse(
        answer=result.answer,
        sources=[
            RAGSource(
                source=source.split(" — ", 1)[0],
                section=(
                    source.split(" — ", 1)[1]
                    if " — " in source
                    else ""
                ),
                score=0.0,
            )
            for source in result.sources
        ],
        retrieved_chunks=len(result.retrieved_chunks),
        grounding_blocked=result.grounding_blocked,
        grounding_violations=result.grounding_violations or [],
    )