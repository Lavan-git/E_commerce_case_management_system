from __future__ import annotations

import json
from pathlib import Path

from src.app.rag.context import ContextBuilder
from src.app.rag.embeddings import SentenceTransformerEmbeddingProvider
from src.app.rag.generation import OpenAICompatibleGenerator
from src.app.rag.prompting import RAGPromptBuilder
from src.app.rag.retrieval import Retriever
from src.app.rag.service import RAGService
from src.app.rag.vectorstore import FaissVectorIndex
from src.app.rag.guard import GroundingGuard

EVAL_FILE = Path("data/evaluation/rag_answer_eval.json")
VECTOR_STORE = Path("data/vector_store")

MODEL_ID = "mistral-7b-instruct-v0.3"
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"


def load_cases() -> list[dict]:
    return json.loads(
        EVAL_FILE.read_text(encoding="utf-8")
    )


def build_service() -> RAGService:
    embedding_provider = SentenceTransformerEmbeddingProvider()

    vector_index = FaissVectorIndex.load(
        VECTOR_STORE
    )

    retriever = Retriever(
        embedding_provider=embedding_provider,
        vector_index=vector_index,
    )

    context_builder = ContextBuilder()
    prompt_builder = RAGPromptBuilder()

    generation_provider = OpenAICompatibleGenerator(
        base_url=LM_STUDIO_BASE_URL,
        model=MODEL_ID,
        supports_system_role=False,
        timeout=300.0,
    )
    grounding_guard = GroundingGuard()
    return RAGService(
        retriever=retriever,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        generation_provider=generation_provider,
        top_k=3,
        grounding_guard=grounding_guard,
    )


def evaluate_answer(answer: str, case: dict) -> dict:
    normalized = " ".join(answer.lower().split())

    required_claims = [
        claim.lower()
        for claim in case.get("required_claims", [])
    ]

    forbidden_claims = [
        claim.lower()
        for claim in case.get("forbidden_claims", [])
    ]

    acceptable_abstentions = [
        phrase.lower()
        for phrase in case.get("acceptable_abstentions", [])
    ]

    required_hits = [
        claim
        for claim in required_claims
        if claim in normalized
    ]

    forbidden_hits = [
        claim
        for claim in forbidden_claims
        if claim in normalized
    ]

    abstained = any(
        phrase in normalized
        for phrase in acceptable_abstentions
    )

    required_coverage = (
        len(required_hits) / len(required_claims)
        if required_claims
        else 1.0
    )

    if not case["answerable"]:
        grounded = (
            abstained
            and not forbidden_hits
        )
    else:
        grounded = (
            required_coverage == 1.0
            and not forbidden_hits
        )

    return {
        "required_coverage": required_coverage,
        "required_claims_found": required_hits,
        "required_claims_missing": [
            claim
            for claim in required_claims
            if claim not in normalized
        ],
        "forbidden_claims_found": forbidden_hits,
        "abstained": abstained,
        "grounded": grounded,
    }

def classify_outcome(
    case: dict,
    evaluation: dict,
    result,
) -> str:
    if result.grounding_blocked:
        return "BLOCKED"

    if evaluation["grounded"]:
        if evaluation["abstained"]:
            return "ABSTAINED"
        return "GROUNDED"

    return "FAILED"

def main() -> None:
    cases = load_cases()
    service = build_service()

    results = []

    for case in cases:
        print("\n" + "=" * 80)
        print(f"CASE: {case['id']}")
        print("=" * 80)
        print(f"QUESTION: {case['question']}")

        result = service.ask(
            case["question"],
            metadata_filter=case.get("metadata_filter"),
            forbidden_claims=case.get("forbidden_claims", []),
        )

        evaluation = evaluate_answer(
            result.answer,
            case,
        )

        outcome = classify_outcome(
            case,
            evaluation,
            result,
        )

        print("\nANSWER:")
        print(result.answer)

        print("\nSOURCES:")
        for source in result.sources:
            print(f"- {source}")

        print("\nEVALUATION:")
        print(
            f"Required coverage: "
            f"{evaluation['required_coverage']:.0%}"
        )
        print(
            f"Forbidden claims: "
            f"{len(evaluation['forbidden_claims_found'])}"
        )
        print(f"Grounded: {evaluation['grounded']}")
        print(f"Outcome: {outcome}")

        if result.grounding_violations:
            print("Grounding violations:")
            for violation in result.grounding_violations:
                print(f"- {violation}")

        results.append(
            {
                "id": case["id"],
                "outcome": outcome,
                "evaluation": evaluation,
                "answer": result.answer,
                "sources": result.sources,
                "grounding_violations": (
                    result.grounding_violations or []
                ),
            }
        )

    from collections import Counter

    outcomes = Counter(
        result["outcome"]
        for result in results
    )

    print("\n" + "=" * 80)
    print("OUTCOMES")
    print("=" * 80)

    for outcome, count in sorted(outcomes.items()):
        print(f"{outcome}: {count}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"Grounded: {outcomes.get('GROUNDED', 0)}")
    print(f"Abstained: {outcomes.get('ABSTAINED', 0)}")
    print(f"Blocked: {outcomes.get('BLOCKED', 0)}")
    print(f"Failed: {outcomes.get('FAILED', 0)}")

if __name__ == "__main__":
    main()