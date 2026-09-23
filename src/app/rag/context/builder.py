from __future__ import annotations

from dataclasses import dataclass

from src.app.rag.retrieval import RetrievalResult


@dataclass(frozen=True)
class RetrievalContext:
    """Formatted evidence ready to be passed to an LLM."""

    text: str
    sources: list[str]
    result_count: int


class ContextBuilder:
    """Turn ranked retrieval results into bounded, cited context."""

    def __init__(self, max_context_chars: int = 6000) -> None:
        if max_context_chars <= 0:
            raise ValueError("max_context_chars must be positive.")

        self.max_context_chars = max_context_chars

    def build(
        self,
        results: list[RetrievalResult],
    ) -> RetrievalContext:
        if not results:
            return RetrievalContext(
                text="",
                sources=[],
                result_count=0,
            )

        sections: list[str] = []
        sources: list[str] = []
        current_length = 0

        for result in results:
            source_label = (
                f"{result.source} — {result.section}"
            )

            block = (
                f"[Source: {source_label}]\n"
                f"[Similarity: {result.score:.4f}]\n"
                f"{result.text.strip()}"
            )

            separator = "\n\n"

            additional_length = len(block)
            if sections:
                additional_length += len(separator)

            if current_length + additional_length > self.max_context_chars:
                break

            sections.append(block)
            sources.append(source_label)
            current_length += additional_length

        return RetrievalContext(
            text="\n\n".join(sections),
            sources=sources,
            result_count=len(sections),
        )