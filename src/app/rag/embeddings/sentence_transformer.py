from __future__ import annotations

from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbeddingProvider:
    """Embedding provider backed by Sentence Transformers."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        model: Any | None = None,
    ) -> None:
        self.model_name = model_name
        self._model = model or SentenceTransformer(model_name)

    @property
    def dimension(self) -> int:
        dimension = self._model.get_sentence_embedding_dimension()
        if dimension is None:
            raise RuntimeError("Embedding model did not report a vector dimension.")
        return int(dimension)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        vectors = self._encode(texts)
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Query text cannot be empty.")

        vectors = self._encode([text])
        return vectors[0].tolist()

    def _encode(self, texts: list[str]) -> np.ndarray:
        vectors = self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        array = np.asarray(vectors, dtype=np.float32)
        if array.ndim != 2:
            raise RuntimeError(
                f"Embedding model returned unexpected shape: {array.shape}"
            )
        return array
