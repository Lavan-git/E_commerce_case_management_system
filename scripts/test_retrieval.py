from pathlib import Path

from src.app.rag.embeddings import SentenceTransformerEmbeddingProvider
from src.app.rag.retrieval import Retriever
from src.app.rag.vectorstore import FaissVectorIndex


VECTOR_STORE = Path("data/vector_store")


def main() -> None:
    provider = SentenceTransformerEmbeddingProvider()

    index = FaissVectorIndex.load(VECTOR_STORE)

    retriever = Retriever(
        embedding_provider=provider,
        vector_index=index,
    )

    queries = [
        "Customer says money was deducted but the order was never created.",
        "How should a customer refund be handled?",
        "A customer says the order was not delivered.",
        "A vendor says their payout amount is lower than expected.",
    ]

    for query in queries:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        results = retriever.search(query, top_k=3)

        for result in results:
            print(f"\n#{result.rank} | score={result.score:.4f}")
            print(f"Source:  {result.source}")
            print(f"Section: {result.section}")
            print(f"Chunk:   {result.chunk_id}")
            print(f"Text:    {result.text[:500]}")


if __name__ == "__main__":
    main()