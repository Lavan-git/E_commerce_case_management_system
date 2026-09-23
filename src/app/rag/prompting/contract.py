from __future__ import annotations

from dataclasses import dataclass

from src.app.rag.context import RetrievalContext


@dataclass(frozen=True)
class RAGPrompt:
    """A complete prompt contract for grounded RAG generation."""

    system_prompt: str
    user_prompt: str


class RAGPromptBuilder:
    """Build a grounded prompt from a question and retrieved evidence."""

    SYSTEM_PROMPT = """
    You are a policy assistant for an e-commerce dispute resolution system.

    Answer using ONLY the retrieved policy context.

    Rules:
    - Do not use general knowledge, prior knowledge, or assumptions.
    - Do not infer an unsupported next step.
    - If the retrieved context is insufficient, say:
    "The retrieved policy evidence does not provide enough information to answer this."
    - Do not invent deadlines, amounts, eligibility, guarantees, escalations,
    refunds, compensation, or other policy outcomes.
    - Every substantive policy statement must be supported by the retrieved
    context.
    - Cite each substantive policy statement using the EXACT source filename
    and section provided in the context:
    [<source filename> — <section>]
    - Never replace the actual source filename with a placeholder such as
    "source.md".
    - Check all claims against the retrieved context before answering.
    - If a claim is not supported, remove it.
    - Keep the answer concise.
    """

    def build(
        self,
        question: str,
        context: RetrievalContext,
    ) -> RAGPrompt:
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        if context.text:
            context_text = context.text
        else:
            context_text = (
                "[NO RETRIEVED POLICY EVIDENCE]\n"
                "No policy context was retrieved for this question."
            )

        user_prompt = (
            "--- BEGIN POLICY CONTEXT ---\n"
            f"{context_text}\n"
            "--- END POLICY CONTEXT ---\n\n"
            f"User question:\n{question}"
        )

        return RAGPrompt(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
