import numpy as np
import pytest

from src.app.rag.context import ContextBuilder
from src.app.rag.generation.base import GenerationProvider
from src.app.rag.prompting import RAGPromptBuilder
from src.app.rag.retrieval import Retriever
from src.app.rag.service import RAGService
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
            "customer was charged": [0.95, 0.05, 0.0],
        }

        return np.asarray(
            [mapping[text] for text in texts],
            dtype=np.float32,
        )


class FakeGenerator:
    def __init__(self) -> None:
        self.system_prompt = None
        self.user_prompt = None

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.0,
    ) -> str:
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

        return (
            "Verify the payment status and check whether an order exists. "
            "[payment_policy.md — Payment dispute]"
        )


def build_service(generator: GenerationProvider) -> RAGService:
    provider = SentenceTransformerEmbeddingProvider(
        model=FakeSentenceTransformer(),
    )

    chunk = DocumentChunk(
        chunk_id="payment_01",
        document_id="payment_policy",
        source="payment_policy.md",
        section="Payment dispute",
        text="Verify payment status and check whether an order exists.",
        metadata={"version": "1.0"},
    )

    embedding = provider.embed_documents(["payment issue"])

    index = FaissVectorIndex(provider.dimension)
    index.add([chunk], embedding)

    retriever = Retriever(
        embedding_provider=provider,
        vector_index=index,
    )

    return RAGService(
        retriever=retriever,
        context_builder=ContextBuilder(),
        prompt_builder=RAGPromptBuilder(),
        generation_provider=generator,
        top_k=1,
    )


def test_rag_service_generates_grounded_answer() -> None:
    generator = FakeGenerator()
    service = build_service(generator)

    result = service.ask("customer was charged")

    assert "Verify the payment status" in result.answer
    assert result.sources == [
        "payment_policy.md — Payment dispute"
    ]
    assert len(result.retrieved_chunks) == 1

    assert generator.system_prompt is not None
    assert "Answer using ONLY the retrieved policy context." in generator.system_prompt

    assert generator.user_prompt is not None
    assert "Verify payment status" in generator.user_prompt


def test_rag_service_rejects_empty_question() -> None:
    service = build_service(FakeGenerator())

    with pytest.raises(ValueError, match="Question cannot be empty"):
        service.ask("   ")



def test_rag_service_passes_metadata_filter() -> None:
    class RecordingRetriever:
        def __init__(self) -> None:
            self.received_filter = None
            self.received_min_score = None

        def search(
            self,
            query: str,
            top_k: int = 5,
            metadata_filter: dict[str, str] | None = None,
            min_score: float | None = None,
        ):
            self.received_filter = metadata_filter
            self.received_min_score = min_score
            return []

    from src.app.rag.context import ContextBuilder
    from src.app.rag.prompting import RAGPromptBuilder

    class DummyGenerator:
        def generate(
            self,
            system_prompt: str,
            user_prompt: str,
            *,
            temperature: float = 0.0,
        ) -> str:
            return "dummy"

    retriever = RecordingRetriever()

    service = RAGService(
        retriever=retriever,
        context_builder=ContextBuilder(),
        prompt_builder=RAGPromptBuilder(),
        generation_provider=DummyGenerator(),
        top_k=3,
    )

    service.ask(
        "What should happen?",
        metadata_filter={"domain": "Delivery disputes"},
    )

    assert retriever.received_filter == {
        "domain": "Delivery disputes"
    }



def test_rag_service_blocks_ungrounded_answer() -> None:
    class HallucinatingGenerator:
        def generate(
            self,
            system_prompt: str,
            user_prompt: str,
            *,
            temperature: float = 0.0,
        ) -> str:
            return "The payment will be refunded immediately."

    from src.app.rag.guard import GroundingGuard

    service = build_service(
        HallucinatingGenerator(),
    )

    service.grounding_guard = GroundingGuard()

    result = service.ask(
        "customer was charged",
        forbidden_claims=[
            "payment will be refunded immediately",
        ],
    )

    assert "fully supported" in result.answer