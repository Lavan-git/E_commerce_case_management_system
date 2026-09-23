from pydantic import BaseModel, Field


class Document(BaseModel):
    """A loaded knowledge-base document."""

    document_id: str
    source_path: str
    title: str
    content: str
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentSection(BaseModel):
    """A Markdown H2 section extracted from a document."""

    document_id: str
    index: int
    title: str
    content: str


class DocumentChunk(BaseModel):
    """A retrieval-ready text chunk with provenance metadata."""

    chunk_id: str
    document_id: str
    source: str
    section: str
    text: str
    metadata: dict[str, str] = Field(default_factory=dict)
