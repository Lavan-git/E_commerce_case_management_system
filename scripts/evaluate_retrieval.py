import json
from pathlib import Path

from src.app.rag.embeddings import SentenceTransformerEmbeddingProvider
from src.app.rag.retrieval import Retriever
from src.app.rag.vectorstore import FaissVectorIndex


EVAL_FILE = Path("data/evaluation/rag_eval.json")
VECTOR_STORE = Path("data/vector_store")

COMPARISON_OUTPUT = Path(
    "data/evaluation/rag_retrieval_comparison.json"
)

THRESHOLD_OUTPUT = Path(
    "data/evaluation/rag_threshold_comparison.json"
)


def load_cases() -> list[dict]:
    return json.loads(
        EVAL_FILE.read_text(encoding="utf-8")
    )


def serialize_result(result) -> dict:
    return {
        "rank": result.rank,
        "chunk_id": result.chunk_id,
        "score": result.score,
        "source": result.source,
        "section": result.section,
        "metadata": result.metadata,
    }


def evaluate_case(
    retriever: Retriever,
    case: dict,
    top_k: int,
    use_metadata_filter: bool,
    min_score: float | None = None,
) -> dict:
    metadata_filter = (
        case.get("metadata_filter")
        if use_metadata_filter
        else None
    )

    results = retriever.search(
        case["question"],
        top_k=top_k,
        metadata_filter=metadata_filter,
        min_score=min_score,
    )

    retrieved_sources = {
        result.source
        for result in results
    }

    retrieved_sections = {
        result.section
        for result in results
    }

    expected_sources = set(case["expected_sources"])
    expected_sections = set(case["expected_sections"])

    source_hit = (
        bool(retrieved_sources & expected_sources)
        if case["answerable"]
        else False
    )

    section_hit = (
        bool(retrieved_sections & expected_sections)
        if case["answerable"]
        else False
    )

    return {
        "id": case["id"],
        "answerable": case["answerable"],
        "metadata_filter": metadata_filter,
        "min_score": min_score,
        "source_hit": source_hit,
        "section_hit": section_hit,
        "retrieved": bool(results),
        "results": [
            serialize_result(result)
            for result in results
        ],
    }


def evaluate_threshold(
    retriever: Retriever,
    cases: list[dict],
    threshold: float,
) -> dict:
    evaluations = [
        evaluate_case(
            retriever=retriever,
            case=case,
            top_k=3,
            use_metadata_filter=True,
            min_score=threshold,
        )
        for case in cases
    ]

    answerable = [
        result
        for result in evaluations
        if result["answerable"]
    ]

    unsupported = [
        result
        for result in evaluations
        if not result["answerable"]
    ]

    answerable_retained = sum(
        result["retrieved"]
        for result in answerable
    )

    answerable_source_hits = sum(
        result["source_hit"]
        for result in answerable
    )

    answerable_section_hits = sum(
        result["section_hit"]
        for result in answerable
    )

    unsupported_rejected = sum(
        not result["retrieved"]
        for result in unsupported
    )

    return {
        "top_k": 3,
        "metadata_filter": True,
        "min_score": threshold,
        "answerable_cases": len(answerable),
        "unsupported_cases": len(unsupported),
        "answerable_retained": answerable_retained,
        "answerable_retention_rate": (
            answerable_retained / len(answerable)
            if answerable
            else 0.0
        ),
        "source_hit_rate_on_retained": (
            answerable_source_hits / len(answerable)
            if answerable
            else 0.0
        ),
        "section_hit_rate_on_retained": (
            answerable_section_hits / len(answerable)
            if answerable
            else 0.0
        ),
        "unsupported_rejected": unsupported_rejected,
        "unsupported_rejection_rate": (
            unsupported_rejected / len(unsupported)
            if unsupported
            else 0.0
        ),
        "cases": evaluations,
    }


def main() -> None:
    cases = load_cases()

    embedding_provider = SentenceTransformerEmbeddingProvider()
    vector_index = FaissVectorIndex.load(VECTOR_STORE)

    retriever = Retriever(
        embedding_provider=embedding_provider,
        vector_index=vector_index,
    )

    thresholds = [
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
    ]

    threshold_results = []

    print("=" * 80)
    print("RAG RETRIEVAL THRESHOLD EVALUATION")
    print("=" * 80)

    for threshold in thresholds:
        result = evaluate_threshold(
            retriever=retriever,
            cases=cases,
            threshold=threshold,
        )

        threshold_results.append(result)

        print(
            f"\nThreshold: {threshold:.2f}"
        )
        print(
            f"  Answerable retention: "
            f"{result['answerable_retention_rate']:.2%}"
        )
        print(
            f"  Source Hit on answerable cases: "
            f"{result['source_hit_rate_on_retained']:.2%}"
        )
        print(
            f"  Section Hit on answerable cases: "
            f"{result['section_hit_rate_on_retained']:.2%}"
        )
        print(
            f"  Unsupported rejection: "
            f"{result['unsupported_rejection_rate']:.2%}"
        )

        for case in result["cases"]:
            status = (
                "RETRIEVED"
                if case["retrieved"]
                else "REJECTED"
            )

            top_score = (
                case["results"][0]["score"]
                if case["results"]
                else None
            )

            score_text = (
                f"{top_score:.4f}"
                if top_score is not None
                else "N/A"
            )

            print(
                f"    {case['id']}: "
                f"{status} | top_score={score_text}"
            )

    output = {
        "evaluation_file": str(EVAL_FILE),
        "vector_store": str(VECTOR_STORE),
        "top_k": 3,
        "metadata_filter": True,
        "thresholds": threshold_results,
    }

    THRESHOLD_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    THRESHOLD_OUTPUT.write_text(
        json.dumps(
            output,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n" + "=" * 80)
    print("THRESHOLD SUMMARY")
    print("=" * 80)

    print(
        f"{'Threshold':<12}"
        f"{'Answerable Retention':>22}"
        f"{'Unsupported Rejection':>24}"
    )

    print("-" * 58)

    for result in threshold_results:
        print(
            f"{result['min_score']:<12.2f}"
            f"{result['answerable_retention_rate']:>21.2%}"
            f"{result['unsupported_rejection_rate']:>23.2%}"
        )

    print("\nSaved threshold evaluation to:")
    print(THRESHOLD_OUTPUT)


if __name__ == "__main__":
    main()