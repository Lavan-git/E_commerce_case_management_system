from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np

from src.app.rag.documents.models import DocumentChunk


@dataclass(frozen=True)
class RetrievedChunk:
    """A chunk returned by vector similarity search."""

    chunk: DocumentChunk
    score: float


class FaissVectorIndex:
    """FAISS inner-product index over normalized document embeddings.

    Because embeddings are normalized before insertion, inner product is
    equivalent to cosine similarity for this retrieval use case.
    """

    def __init__(self, dimension: int) -> None:
        if dimension <= 0:
            raise ValueError("Vector dimension must be positive.")

        self.dimension = dimension
        self._index = faiss.IndexFlatIP(dimension)
        self._chunks: list[DocumentChunk] = []

    @property
    def size(self) -> int:
        return int(self._index.ntotal)

    def add(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have exactly one embedding.")

        if not chunks:
            return

        matrix = np.asarray(embeddings, dtype=np.float32)

        if matrix.ndim != 2:
            raise ValueError(f"Embeddings must be a 2D matrix, got {matrix.shape}.")

        if matrix.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension {matrix.shape[1]} does not match "
                f"index dimension {self.dimension}."
            )

        self._index.add(matrix)
        self._chunks.extend(chunks)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        metadata_filter: dict[str, str] | None = None,
        min_score: float | None = None,
    ) -> list[RetrievedChunk]:
        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        if self.size == 0:
            return []

        query = np.asarray([query_embedding], dtype=np.float32)

        if query.ndim != 2 or query.shape[1] != self.dimension:
            raise ValueError(
                f"Query dimension "
                f"{query.shape[1] if query.ndim == 2 else 'invalid'} "
                f"does not match index dimension {self.dimension}."
            )

        # Without metadata filtering, use the normal efficient top-k search.
        search_k = min(top_k, self.size)

        # With metadata filtering, retrieve all candidates first because FAISS
        # itself does not know about our chunk metadata.
        if metadata_filter:
            search_k = self.size

        scores, indices = self._index.search(
            query,
            search_k,
        )

        results: list[RetrievedChunk] = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue

            chunk = self._chunks[int(index)]

            if metadata_filter:
                matches = all(
                    chunk.metadata.get(key) == value
                    for key, value in metadata_filter.items()
                )

                if not matches:
                    continue
            if min_score is not None and float(score) < min_score:
                continue

            results.append(
                RetrievedChunk(
                    chunk=chunk,
                    score=float(score),
                )
            )

            if len(results) >= top_k:
                break

        return results

    def save(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self._index,
            str(directory / "index.faiss"),
        )

        metadata = {
            "dimension": self.dimension,
            "chunks": [chunk.model_dump() for chunk in self._chunks],
        }

        (directory / "chunks.json").write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, directory: Path) -> "FaissVectorIndex":
        index_path = directory / "index.faiss"
        chunks_path = directory / "chunks.json"

        if not index_path.is_file() or not chunks_path.is_file():
            raise FileNotFoundError(f"FAISS index files not found in {directory}")

        raw = json.loads(chunks_path.read_text(encoding="utf-8"))

        instance = cls(dimension=int(raw["dimension"]))
        instance._index = faiss.read_index(str(index_path))
        instance._chunks = [
            DocumentChunk.model_validate(item)
            for item in raw["chunks"]
        ]

        if instance._index.ntotal != len(instance._chunks):
            raise ValueError(
                "FAISS vector count does not match stored chunk metadata."
            )

        return instance
