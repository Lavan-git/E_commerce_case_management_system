from __future__ import annotations

from dataclasses import dataclass

from src.app.rag.context import ContextBuilder
from src.app.rag.generation import GenerationProvider
from src.app.rag.prompting import RAGPromptBuilder
from src.app.rag.retrieval import RetrievalResult, Retriever
from src.app.rag.guard import GroundingGuard

@dataclass(frozen=True)
class RAGAnswer:
    """Final answer returned by the RAG application layer."""

    answer: str
    sources: list[str]
    retrieved_chunks: list[RetrievalResult]
    grounding_blocked: bool = False
    grounding_violations: list[str] | None = None


class RAGService:
    """Orchestrate retrieval, context construction, prompting, and generation."""

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        prompt_builder: RAGPromptBuilder,
        generation_provider: GenerationProvider,
        top_k: int = 5,
        grounding_guard: GroundingGuard | None = None,
    ) -> None:
        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        self.retriever = retriever
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.generation_provider = generation_provider
        self.top_k = top_k
        self.grounding_guard = grounding_guard

    def ask(
        self,
        question: str,
        metadata_filter: dict[str, str] | None = None,
        forbidden_claims: list[str] | None = None,
    ) -> RAGAnswer:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        results = self.retriever.search(
            question,
            top_k=self.top_k,
            metadata_filter=metadata_filter,
            min_score=0.55,
        )

        if not results:
            return RAGAnswer(
                answer=(
                    "I don't have enough policy evidence to answer this "
                    "question."
                ),
                sources=[],
                retrieved_chunks=[],
            )

        context = self.context_builder.build(results)

        prompt = self.prompt_builder.build(
            question,
            context,
        )

        answer = self.generation_provider.generate(
            prompt.system_prompt,
            prompt.user_prompt,
            temperature=0.0,
        )

        if self.grounding_guard is not None:
            grounding_check = self.grounding_guard.check(
                answer,
                forbidden_claims or [],
            )

            if not grounding_check.passed:
                return RAGAnswer(
                    answer=(
                        "I could not produce a response that was fully "
                        "supported by the retrieved policy evidence."
                    ),
                    sources=context.sources,
                    retrieved_chunks=results,
                    grounding_blocked=True,
                    grounding_violations=grounding_check.violations,
                )

        return RAGAnswer(
            answer=answer,
            sources=context.sources,
            retrieved_chunks=results,
        )