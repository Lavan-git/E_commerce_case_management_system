from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class GroundingCheck:
    passed: bool
    violations: list[str]


class GroundingGuard:
    """
    Deterministic grounding guard for generated RAG answers.

    This guard is intentionally conservative. It checks:
    1. Explicit forbidden claims.
    2. Lexical support of generated claims/clauses against retrieved evidence.

    It is not a semantic entailment model.
    """

    STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "can",
        "case",
        "customer",
        "do",
        "does",
        "for",
        "from",
        "has",
        "have",
        "if",
        "in",
        "is",
        "it",
        "may",
        "of",
        "on",
        "or",
        "should",
        "that",
        "the",
        "their",
        "this",
        "to",
        "until",
        "was",
        "were",
        "what",
        "when",
        "whether",
        "with",
    }

    MIN_SUPPORT_RATIO = 0.65
    MIN_PHRASE_WORDS = 3

    def check(
        self,
        answer: str,
        forbidden_claims: list[str] | None = None,
        evidence_text: str | None = None,
    ) -> GroundingCheck:
        normalized = " ".join(answer.lower().split())

        violations: list[str] = []

        # ---------------------------------------------------------
        # 1. Explicit forbidden-claim detection
        # ---------------------------------------------------------
        for claim in forbidden_claims or []:
            if claim.lower() in normalized:
                violations.append(claim)

        # ---------------------------------------------------------
        # 2. Evidence-based grounding check
        # ---------------------------------------------------------
        if evidence_text:
            evidence_tokens = self._content_token_list(evidence_text)

            for claim in self._split_claims(answer):
                clauses = self._split_clauses(claim)

                for clause in clauses:
                    clause_tokens = self._content_token_list(clause)

                    if not clause_tokens:
                        continue

                    support_ratio = self._support_ratio(
                        clause_tokens,
                        evidence_tokens,
                    )

                    longest_phrase = self._longest_common_phrase(
                        clause_tokens,
                        evidence_tokens,
                    )

                    supported = (
                        support_ratio >= self.MIN_SUPPORT_RATIO
                        and longest_phrase >= self.MIN_PHRASE_WORDS
                            
                    )

                    if not supported:
                        violations.append(
                            "Unsupported generated statement: "
                            f"{clause.strip()}"
                        )

        return GroundingCheck(
            passed=not violations,
            violations=violations,
        )

    @classmethod
    def _content_token_list(cls, text: str) -> list[str]:
        tokens = re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9_-]*\b",
            text.lower(),
        )

        return [
            token
            for token in tokens
            if token not in cls.STOPWORDS
            and len(token) > 2
        ]

    @classmethod
    def _support_ratio(
        cls,
        claim_tokens: list[str],
        evidence_tokens: list[str],
    ) -> float:
        if not claim_tokens:
            return 1.0

        evidence_set = set(evidence_tokens)

        supported_tokens = {
            token
            for token in claim_tokens
            if token in evidence_set
        }

        return len(supported_tokens) / len(claim_tokens)

    @classmethod
    def _longest_common_phrase(
        cls,
        claim_tokens: list[str],
        evidence_tokens: list[str],
    ) -> int:
        """
        Find the longest contiguous phrase from the generated clause
        that also appears contiguously in the retrieved evidence.
        """
        if not claim_tokens or not evidence_tokens:
            return 0

        longest = 0
        evidence_length = len(evidence_tokens)

        for start in range(len(claim_tokens)):
            for end in range(
                start + cls.MIN_PHRASE_WORDS,
                len(claim_tokens) + 1,
            ):
                phrase = claim_tokens[start:end]
                phrase_length = len(phrase)

                if phrase_length <= longest:
                    continue

                for evidence_start in range(
                    0,
                    evidence_length - phrase_length + 1,
                ):
                    evidence_phrase = evidence_tokens[
                        evidence_start:
                        evidence_start + phrase_length
                    ]

                    if evidence_phrase == phrase:
                        longest = phrase_length
                        break

        return longest

    @staticmethod
    def _split_claims(text: str) -> list[str]:
        """
        Split a generated answer into independently checkable claims.

        Numbered/bulleted answers are handled item-by-item.
        Non-list answers are split into normal sentences.
        """
        lines = text.splitlines()

        has_list = any(
            re.match(
                r"^\s*(?:\d+\.\s+|[-*]\s+)",
                line,
            )
            for line in lines
        )

        if has_list:
            claims: list[str] = []
            current: list[str] = []
            collecting_list = False

            for line in lines:
                stripped = line.strip()

                if not stripped:
                    continue

                list_match = re.match(
                    r"^\s*(?:\d+\.\s+|[-*]\s+)(.*)$",
                    stripped,
                )

                if list_match:
                    if current:
                        claims.append(" ".join(current).strip())

                    current = [list_match.group(1).strip()]
                    collecting_list = True
                    continue

                if collecting_list:
                    current.append(stripped)

            if current:
                claims.append(" ".join(current).strip())

            return [
                claim
                for claim in claims
                if claim
            ]

        return [
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?])\s+",
                text,
            )
            if sentence.strip()
        ]

    @staticmethod
    def _split_clauses(claim: str) -> list[str]:
        """
        Split an individual generated claim into smaller clauses.

        Commas and semicolons are useful boundaries for policy actions,
        e.g.:
            "After investigation, follow the refund procedure."

        This makes unsupported trailing actions independently checkable.
        """
        clauses = re.split(
            r"(?<=[,;])\s+",
            claim,
        )

        return [
            clause.strip(" ,;")
            for clause in clauses
            if clause.strip(" ,;")
        ]