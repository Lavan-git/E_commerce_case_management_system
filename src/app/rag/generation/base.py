from __future__ import annotations

from typing import Protocol


class GenerationProvider(Protocol):
    """Interface for LLM text generation."""

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.0,
    ) -> str:
        ...