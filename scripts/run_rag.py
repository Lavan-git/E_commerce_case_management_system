from pathlib import Path

from src.app.rag.context import ContextBuilder
from src.app.rag.embeddings import SentenceTransformerEmbeddingProvider
from src.app.rag.generation import OpenAICompatibleGenerator
from src.app.rag.prompting import RAGPromptBuilder
from src.app.rag.retrieval import Retriever
from src.app.rag.service import RAGService
from src.app.rag.vectorstore import FaissVectorIndex


VECTOR_STORE = Path("data/vector_store")

# Replace this with the exact ID returned by:
# Invoke-RestMethod http://localhost:1234/v1/models
MODEL_ID = "mistral-7b-instruct-v0.3"

LM_STUDIO_BASE_URL = "http://localhost:1234/v1"


def build_rag_service() -> RAGService:
    embedding_provider = SentenceTransformerEmbeddingProvider()

    vector_index = FaissVectorIndex.load(
        VECTOR_STORE,
    )

    retriever = Retriever(
        embedding_provider=embedding_provider,
        vector_index=vector_index,
    )

    context_builder = ContextBuilder(
        max_context_chars=6000,
    )

    prompt_builder = RAGPromptBuilder()

    generation_provider = OpenAICompatibleGenerator(
    base_url=LM_STUDIO_BASE_URL,
    model=MODEL_ID,
    supports_system_role=False,
    )

    return RAGService(
        retriever=retriever,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        generation_provider=generation_provider,
        top_k=3,
    )


def main() -> None:
    service = build_rag_service()

    question = (
        "A customer says their payment was deducted, "
        "but the order was never created. What should the "
        "support agent do?"
    )

    result = service.ask(question)

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result.answer)

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for source in result.sources:
        print(f"- {source}")

    print("\n" + "=" * 80)
    print("RETRIEVED CHUNKS")
    print("=" * 80)

    for result_item in result.retrieved_chunks:
        print(
            f"\n#{result_item.rank} "
            f"score={result_item.score:.4f}"
        )
        print(f"{result_item.source} — {result_item.section}")
        print(result_item.text[:500])


if __name__ == "__main__":
    main()