from __future__ import annotations

from typing import Protocol


class EmbeddingProvider(Protocol):
    """Interface for converting text into vector embeddings."""

    @property
    def dimension(self) -> int:
        """Return the embedding vector dimension."""
        ...

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a collection of documents/chunks."""
        ...

    def embed_query(self, text: str) -> list[float]:
        """Embed a single user query."""
        ...
