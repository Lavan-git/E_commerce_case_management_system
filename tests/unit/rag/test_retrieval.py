import numpy as np
import pytest

from src.app.rag.documents.models import DocumentChunk
from src.app.rag.embeddings import SentenceTransformerEmbeddingProvider
from src.app.rag.retrieval import Retriever
from src.app.rag.vectorstore import FaissVectorIndex


class FakeSentenceTransformer:
    def get_sentence_embedding_dimension(self) -> int:
        return 3

    def encode(
        self,
        texts: list[str],
        *,
        convert_to_numpy: bool,
        normalize_embeddings: bool,
        show_progress_bar: bool,
    ) -> np.ndarray:
        mapping = {
            "payment issue": [1.0, 0.0, 0.0],
            "refund issue": [0.0, 1.0, 0.0],
            "delivery issue": [0.0, 0.0, 1.0],
            "customer was charged but order not created": [0.95, 0.05, 0.0],
        }

        return np.asarray(
            [mapping[text] for text in texts],
            dtype=np.float32,
        )


def make_chunk(
    chunk_id: str,
    text: str,
    source: str,
    section: str,
) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        document_id=source.removesuffix(".md"),
        source=source,
        section=section,
        text=text,
        metadata={
            "document_type": "Policy",
            "version": "1.0",
        },
    )


def build_retriever() -> Retriever:
    provider = SentenceTransformerEmbeddingProvider(
        model=FakeSentenceTransformer(),
    )

    chunks = [
        make_chunk(
            "payment_01",
            "payment issue",
            "payment_policy.md",
            "Payment dispute",
        ),
        make_chunk(
            "refund_01",
            "refund issue",
            "refund_policy.md",
            "Refund initiation",
        ),
        make_chunk(
            "delivery_01",
            "delivery issue",
            "delivery_policy.md",
            "Delivery dispute",
        ),
    ]

    embeddings = provider.embed_documents(
        [chunk.text for chunk in chunks]
    )

    index = FaissVectorIndex(provider.dimension)
    index.add(chunks, embeddings)

    return Retriever(provider, index)


def test_retriever_returns_ranked_results() -> None:
    retriever = build_retriever()

    results = retriever.search(
        "customer was charged but order not created",
        top_k=2,
    )

    assert len(results) == 2
    assert results[0].rank == 1
    assert results[0].chunk_id == "payment_01"
    assert results[0].source == "payment_policy.md"
    assert results[0].score > results[1].score


def test_retriever_rejects_empty_query() -> None:
    retriever = build_retriever()

    with pytest.raises(ValueError, match="Query cannot be empty"):
        retriever.search("   ")


def test_retriever_rejects_invalid_top_k() -> None:
    retriever = build_retriever()

    with pytest.raises(ValueError, match="top_k must be positive"):
        retriever.search("payment issue", top_k=0)