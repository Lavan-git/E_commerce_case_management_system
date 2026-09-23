from functools import lru_cache
from pathlib import Path

from src.app.rag.context import ContextBuilder
from src.app.rag.embeddings import SentenceTransformerEmbeddingProvider
from src.app.rag.generation import OpenAICompatibleGenerator
from src.app.rag.prompting import RAGPromptBuilder
from src.app.rag.retrieval import Retriever
from src.app.rag.service import RAGService
from src.app.rag.vectorstore import FaissVectorIndex
from src.app.rag.guard import GroundingGuard

VECTOR_STORE = Path("data/vector_store")

MODEL_ID = "mistral-7b-instruct-v0.3"
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    embedding_provider = SentenceTransformerEmbeddingProvider()

    vector_index = FaissVectorIndex.load(
        VECTOR_STORE,
    )

    retriever = Retriever(
        embedding_provider=embedding_provider,
        vector_index=vector_index,
    )

    context_builder = ContextBuilder()
    prompt_builder = RAGPromptBuilder()
    grounding_guard = GroundingGuard()
    generation_provider = OpenAICompatibleGenerator(
        base_url=LM_STUDIO_BASE_URL,
        model=MODEL_ID,
        supports_system_role=False,
        timeout=300.0,
    )

    return RAGService(
        retriever=retriever,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        generation_provider=generation_provider,
        top_k=3,
        grounding_guard=grounding_guard,
    )