from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Document, DocumentChunk, DocumentSection


@dataclass(frozen=True)
class MarkdownChunker:
    """Structure-aware Markdown chunker with bounded chunk size and local overlap."""

    max_chars: int = 1000
    overlap_chars: int = 120

    SECTION_PATTERN = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)
    SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")

    def chunk_document(self, document: Document) -> list[DocumentChunk]:
        sections = self._extract_sections(document)

        chunks: list[DocumentChunk] = []
        for section in sections:
            chunks.extend(self._chunk_section(document, section))

        return chunks

    def chunk_documents(self, documents: list[Document]) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []
        for document in documents:
            chunks.extend(self.chunk_document(document))
        return chunks

    def _extract_sections(self, document: Document) -> list[DocumentSection]:
        matches = list(self.SECTION_PATTERN.finditer(document.content))
        sections: list[DocumentSection] = []

        if not matches:
            return [
                DocumentSection(
                    document_id=document.document_id,
                    index=1,
                    title=document.title,
                    content=self._clean_text(document.content),
                )
            ]

        intro = document.content[: matches[0].start()].strip()
        if intro:
            sections.append(
                DocumentSection(
                    document_id=document.document_id,
                    index=1,
                    title=document.title,
                    content=self._clean_text(intro),
                )
            )

        start_index = len(sections) + 1

        for match_index, match in enumerate(matches):
            start = match.end()
            end = (
                matches[match_index + 1].start()
                if match_index + 1 < len(matches)
                else len(document.content)
            )

            section_title = match.group("title").strip()
            section_content = document.content[start:end].strip()

            if section_content:
                sections.append(
                    DocumentSection(
                        document_id=document.document_id,
                        index=start_index + match_index,
                        title=section_title,
                        content=self._clean_text(section_content),
                    )
                )

        return sections

    def _chunk_section(
        self,
        document: Document,
        section: DocumentSection,
    ) -> list[DocumentChunk]:
        units = self._build_units(section.content)

        if not units:
            return []

        chunks: list[DocumentChunk] = []
        current_units: list[str] = []
        current_length = 0

        for unit in units:
            if not current_units:
                current_units.append(unit)
                current_length = len(unit)
                continue

            candidate_length = current_length + 2 + len(unit)
            if candidate_length <= self.max_chars:
                current_units.append(unit)
                current_length = candidate_length
                continue

            chunks.append(
                self._make_chunk(
                    document=document,
                    section=section,
                    part_number=len(chunks) + 1,
                    text="\n\n".join(current_units),
                )
            )

            overlap = self._tail_overlap("\n\n".join(current_units), len(unit))
            current_units = [overlap, unit] if overlap else [unit]
            current_length = len(unit) + (2 + len(overlap) if overlap else 0)

        if current_units:
            chunks.append(
                self._make_chunk(
                    document=document,
                    section=section,
                    part_number=len(chunks) + 1,
                    text="\n\n".join(current_units),
                )
            )

        return chunks

    def _build_units(self, text: str) -> list[str]:
        paragraphs = [
            paragraph.strip()
            for paragraph in re.split(r"\n\s*\n", text)
            if paragraph.strip()
        ]
        units: list[str] = []

        for paragraph in paragraphs:
            if len(paragraph) <= self.max_chars:
                units.append(paragraph)
                continue

            sentences = [
                sentence.strip()
                for sentence in self.SENTENCE_SPLIT_PATTERN.split(paragraph)
                if sentence.strip()
            ]

            if not sentences:
                units.extend(
                    paragraph[i : i + self.max_chars]
                    for i in range(0, len(paragraph), self.max_chars)
                )
                continue

            current = ""
            for sentence in sentences:
                if len(sentence) > self.max_chars:
                    if current:
                        units.append(current)
                        current = ""
                    units.extend(
                        sentence[i : i + self.max_chars]
                        for i in range(0, len(sentence), self.max_chars)
                    )
                    continue

                candidate = sentence if not current else f"{current} {sentence}"
                if len(candidate) <= self.max_chars:
                    current = candidate
                else:
                    if current:
                        units.append(current)
                    current = sentence

            if current:
                units.append(current)

        return units

    def _make_chunk(
        self,
        document: Document,
        section: DocumentSection,
        part_number: int,
        text: str,
    ) -> DocumentChunk:
        clean_text = self._clean_text(text)
        chunk_id = f"{document.document_id}_{section.index:02d}_{part_number:02d}"

        metadata = dict(document.metadata)
        metadata.update(
            {
                "title": document.title,
                "section_index": str(section.index),
                "section_title": section.title,
            }
        )

        return DocumentChunk(
            chunk_id=chunk_id,
            document_id=document.document_id,
            source=document.source_path,
            section=section.title,
            text=clean_text,
            metadata=metadata,
        )

    def _tail_overlap(self, text: str, next_unit_length: int) -> str:
        if self.overlap_chars <= 0:
            return ""

        # Leave room for the next unit and the two newlines.
        available = min(self.overlap_chars, self.max_chars - next_unit_length - 2)
        if available <= 0:
            return ""

        tail = text[-available:]
        if " " in tail:
            tail = tail.split(" ", 1)[1]
        return tail.strip()

    @staticmethod
    def _clean_text(text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text.strip())
