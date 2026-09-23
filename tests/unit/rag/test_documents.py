from pathlib import Path

import pytest

from src.app.rag.documents import MarkdownChunker, MarkdownDocumentLoader


KNOWLEDGE_BASE = Path("data/knowledge_base")


def test_loader_loads_all_knowledge_base_documents() -> None:
    loader = MarkdownDocumentLoader(KNOWLEDGE_BASE)

    documents = loader.load_all()

    assert len(documents) == 5
    assert {document.document_id for document in documents} == {
        "payment_policy",
        "refund_policy",
        "return_policy",
        "delivery_policy",
        "vendor_payout_policy",
    }


def test_loader_extracts_title_and_metadata() -> None:
    loader = MarkdownDocumentLoader(KNOWLEDGE_BASE)

    document = loader.load_file(KNOWLEDGE_BASE / "payment_policy.md")

    assert document.title == "Payment Dispute Policy"
    assert document.metadata["document_type"] == "Policy"
    assert document.metadata["domain"] == "Payment disputes"
    assert document.metadata["version"] == "1.0"
    assert document.metadata["status"] == "Active"


def test_chunker_preserves_provenance() -> None:
    loader = MarkdownDocumentLoader(KNOWLEDGE_BASE)
    chunker = MarkdownChunker(max_chars=1000, overlap_chars=120)

    document = loader.load_file(KNOWLEDGE_BASE / "payment_policy.md")
    chunks = chunker.chunk_document(document)

    assert chunks
    assert all(chunk.document_id == "payment_policy" for chunk in chunks)
    assert all(chunk.source == "payment_policy.md" for chunk in chunks)
    assert all(chunk.text.strip() for chunk in chunks)
    assert all("section_title" in chunk.metadata for chunk in chunks)
    assert len({chunk.chunk_id for chunk in chunks}) == len(chunks)


def test_chunker_splits_large_section() -> None:
    from src.app.rag.documents.models import Document

    document = Document(
        document_id="synthetic_policy",
        source_path="synthetic_policy.md",
        title="Synthetic Policy",
        content=(
            "# Synthetic Policy\n\n"
            "## Large Section\n\n"
            + "This is a sentence used for chunking. " * 80
        ),
        metadata={"version": "1.0"},
    )

    chunks = MarkdownChunker(max_chars=300, overlap_chars=40).chunk_document(document)

    assert len(chunks) > 1
    assert all(len(chunk.text) <= 360 for chunk in chunks)


def test_loader_rejects_non_markdown(tmp_path: Path) -> None:
    csv_path = tmp_path / "policy.csv"
    csv_path.write_text("hello", encoding="utf-8")

    loader = MarkdownDocumentLoader(tmp_path)

    with pytest.raises(ValueError, match="Unsupported document type"):
        loader.load_file(csv_path)
