from pathlib import Path

import numpy as np
import pytest

from src.app.rag.documents.models import DocumentChunk
from src.app.rag.embeddings import SentenceTransformerEmbeddingProvider
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
            "payment deducted": [0.95, 0.05, 0.0],
        }
        return np.asarray([mapping[text] for text in texts], dtype=np.float32)


def make_chunk(chunk_id: str, text: str) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        document_id="payment_policy",
        source="payment_policy.md",
        section="Payment dispute",
        text=text,
        metadata={"version": "1.0"},
    )


def test_embedding_provider_returns_expected_dimensions() -> None:
    provider = SentenceTransformerEmbeddingProvider(
        model=FakeSentenceTransformer(),
    )

    vectors = provider.embed_documents(["payment issue", "refund issue"])

    assert provider.dimension == 3
    assert len(vectors) == 2
    assert all(len(vector) == 3 for vector in vectors)


def test_query_embedding_rejects_empty_text() -> None:
    provider = SentenceTransformerEmbeddingProvider(
        model=FakeSentenceTransformer(),
    )

    with pytest.raises(ValueError, match="cannot be empty"):
        provider.embed_query("   ")


def test_faiss_returns_most_similar_chunk_first() -> None:
    provider = SentenceTransformerEmbeddingProvider(
        model=FakeSentenceTransformer(),
    )
    chunks = [
        make_chunk("payment", "payment issue"),
        make_chunk("refund", "refund issue"),
        make_chunk("delivery", "delivery issue"),
    ]
    vectors = provider.embed_documents([chunk.text for chunk in chunks])

    index = FaissVectorIndex(provider.dimension)
    index.add(chunks, vectors)

    query = provider.embed_query("payment deducted")
    results = index.search(query, top_k=2)

    assert len(results) == 2
    assert results[0].chunk.chunk_id == "payment"
    assert results[0].score > results[1].score


def test_faiss_save_and_load(tmp_path: Path) -> None:
    provider = SentenceTransformerEmbeddingProvider(
        model=FakeSentenceTransformer(),
    )
    chunks = [
        make_chunk("payment", "payment issue"),
        make_chunk("refund", "refund issue"),
    ]
    vectors = provider.embed_documents([chunk.text for chunk in chunks])

    index = FaissVectorIndex(provider.dimension)
    index.add(chunks, vectors)
    index.save(tmp_path)

    loaded = FaissVectorIndex.load(tmp_path)
    assert loaded.size == 2

    results = loaded.search(provider.embed_query("payment deducted"), top_k=1)
    assert results[0].chunk.chunk_id == "payment"


def test_faiss_rejects_dimension_mismatch() -> None:
    index = FaissVectorIndex(3)
    chunk = make_chunk("payment", "payment issue")

    with pytest.raises(ValueError, match="dimension"):
        index.add([chunk], [[1.0, 0.0]])


def test_faiss_filters_by_metadata() -> None:
    provider = SentenceTransformerEmbeddingProvider(
        model=FakeSentenceTransformer(),
    )

    payment_chunk = DocumentChunk(
        chunk_id="payment",
        document_id="payment_policy",
        source="payment_policy.md",
        section="Payment dispute",
        text="payment issue",
        metadata={
            "domain": "Payment disputes",
            "version": "1.0",
        },
    )

    refund_chunk = DocumentChunk(
        chunk_id="refund",
        document_id="refund_policy",
        source="refund_policy.md",
        section="Refund",
        text="refund issue",
        metadata={
            "domain": "Refunds",
            "version": "1.0",
        },
    )

    chunks = [payment_chunk, refund_chunk]
    vectors = provider.embed_documents(
        [chunk.text for chunk in chunks]
    )

    index = FaissVectorIndex(provider.dimension)
    index.add(chunks, vectors)

    results = index.search(
        provider.embed_query("payment issue"),
        top_k=5,
        metadata_filter={"domain": "Payment disputes"},
    )

    assert len(results) == 1
    assert results[0].chunk.chunk_id == "payment"