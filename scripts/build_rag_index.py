from pathlib import Path

from src.app.rag.documents import MarkdownChunker, MarkdownDocumentLoader
from src.app.rag.embeddings import SentenceTransformerEmbeddingProvider
from src.app.rag.vectorstore import FaissVectorIndex


KNOWLEDGE_BASE = Path("data/knowledge_base")
VECTOR_STORE = Path("data/vector_store")


def main() -> None:
    loader = MarkdownDocumentLoader(KNOWLEDGE_BASE)
    chunker = MarkdownChunker()

    documents = loader.load_all()
    chunks = chunker.chunk_documents(documents)

    provider = SentenceTransformerEmbeddingProvider()
    embeddings = provider.embed_documents([chunk.text for chunk in chunks])

    index = FaissVectorIndex(provider.dimension)
    index.add(chunks, embeddings)
    index.save(VECTOR_STORE)

    print("RAG index built successfully.")
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Embedding dimension: {provider.dimension}")
    print(f"Index vectors: {index.size}")
    print(f"Saved to: {VECTOR_STORE}")


if __name__ == "__main__":
    main()
