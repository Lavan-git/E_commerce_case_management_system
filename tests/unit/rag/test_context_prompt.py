
import pytest

from src.app.rag.context import ContextBuilder
from src.app.rag.prompting import RAGPromptBuilder
from src.app.rag.retrieval import RetrievalResult


def make_result(
    chunk_id: str,
    source: str,
    section: str,
    text: str,
    score: float,
) -> RetrievalResult:
    return RetrievalResult(
        rank=1,
        chunk_id=chunk_id,
        score=score,
        text=text,
        source=source,
        section=section,
        metadata={"version": "1.0"},
    )


def test_context_builder_preserves_sources() -> None:
    results = [
        make_result(
            "payment_01",
            "payment_policy.md",
            "Payment deducted but order not created",
            "Verify payment status and check whether an order exists.",
            0.7468,
        ),
        make_result(
            "payment_02",
            "payment_policy.md",
            "Failed payments",
            "A confirmed failed payment may be resolved after verification.",
            0.4613,
        ),
    ]

    context = ContextBuilder().build(results)

    assert context.result_count == 2
    assert "payment_policy.md" in context.text
    assert "Payment deducted but order not created" in context.text
    assert len(context.sources) == 2


def test_context_builder_respects_character_limit() -> None:
    results = [
        make_result(
            "one",
            "one.md",
            "Section",
            "A" * 100,
            0.9,
        ),
        make_result(
            "two",
            "two.md",
            "Section",
            "B" * 100,
            0.8,
        ),
    ]

    context = ContextBuilder(max_context_chars=150).build(results)

    assert len(context.text) <= 150
    assert context.result_count == 1


def test_prompt_requires_grounded_answers() -> None:
    results = [
        make_result(
            "payment_01",
            "payment_policy.md",
            "Payment deducted but order not created",
            "Check payment status and verify whether an order exists.",
            0.7468,
        )
    ]

    context = ContextBuilder().build(results)
    prompt = RAGPromptBuilder().build(
        "What should I do?",
        context,
    )

    assert "Answer using ONLY the retrieved policy context." in prompt.system_prompt
    assert "Do not use general knowledge" in prompt.system_prompt
    assert "Do not invent deadlines" in prompt.system_prompt
    assert "What should I do?" in prompt.user_prompt
    assert "payment_policy.md" in prompt.user_prompt


def test_prompt_handles_missing_context() -> None:
    context = ContextBuilder().build([])

    prompt = RAGPromptBuilder().build(
        "What is the refund deadline?",
        context,
    )

    assert "NO RETRIEVED POLICY EVIDENCE" in prompt.user_prompt
    assert "does not provide enough information" in prompt.system_prompt


def test_prompt_rejects_empty_question() -> None:
    context = ContextBuilder().build([])

    with pytest.raises(ValueError, match="Question cannot be empty"):
        RAGPromptBuilder().build("   ", context)