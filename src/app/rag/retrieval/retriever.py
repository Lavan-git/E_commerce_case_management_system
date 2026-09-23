from __future__ import annotations

from dataclasses import dataclass

from src.app.rag.embeddings import EmbeddingProvider
from src.app.rag.vectorstore import FaissVectorIndex, RetrievedChunk


@dataclass(frozen=True)
class RetrievalResult:
    """A ranked retrieval result exposed to the application layer."""

    rank: int
    chunk_id: str
    score: float
    text: str
    source: str
    section: str
    metadata: dict[str, str]


class Retriever:
    """Application-level semantic retriever over the FAISS index."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_index: FaissVectorIndex,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.vector_index = vector_index

    def search(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: dict[str, str] | None = None,
        min_score: float | None = None,
    ) -> list[RetrievalResult]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        if min_score is not None and not 0.0 <= min_score <= 1.0:
            raise ValueError("min_score must be between 0 and 1.")

        query_embedding = self.embedding_provider.embed_query(query)

        matches: list[RetrievedChunk] = self.vector_index.search(
            query_embedding,
            top_k=top_k,
            metadata_filter=metadata_filter,
            min_score=min_score,
        )

        return [
            RetrievalResult(
                rank=rank,
                chunk_id=result.chunk.chunk_id,
                score=result.score,
                text=result.chunk.text,
                source=result.chunk.source,
                section=result.chunk.section,
                metadata=result.chunk.metadata,
            )
            for rank, result in enumerate(matches, start=1)
        ]