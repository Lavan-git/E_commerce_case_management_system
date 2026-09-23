from __future__ import annotations

import re
from pathlib import Path

from .models import Document


class MarkdownDocumentLoader:
    """Load Markdown knowledge-base documents and extract document metadata."""

    METADATA_PATTERN = re.compile(r"^\*\*(?P<key>[^*]+):\*\*\s*(?P<value>.+?)\s*$")
    TITLE_PATTERN = re.compile(r"^#\s+(?P<title>.+?)\s*$")

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def load_file(self, path: Path) -> Document:
        path = path.resolve()

        if path.suffix.lower() != ".md":
            raise ValueError(f"Unsupported document type: {path.suffix}")

        if not path.is_file():
            raise FileNotFoundError(path)

        try:
            relative_path = path.relative_to(self.root)
        except ValueError as exc:
            raise ValueError(f"Document must be inside knowledge-base root: {path}") from exc

        content = path.read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError(f"Document is empty: {path}")

        title = self._extract_title(content, path)
        metadata = self._extract_metadata(content)

        return Document(
            document_id=path.stem,
            source_path=relative_path.as_posix(),
            title=title,
            content=content,
            metadata=metadata,
        )

    def load_all(self) -> list[Document]:
        if not self.root.exists():
            raise FileNotFoundError(f"Knowledge-base directory does not exist: {self.root}")

        paths = sorted(self.root.rglob("*.md"))
        return [self.load_file(path) for path in paths]

    def _extract_title(self, content: str, path: Path) -> str:
        for line in content.splitlines():
            match = self.TITLE_PATTERN.match(line.strip())
            if match:
                return match.group("title").strip()
        return path.stem.replace("_", " ").title()

    def _extract_metadata(self, content: str) -> dict[str, str]:
        metadata: dict[str, str] = {}

        for line in content.splitlines():
            stripped = line.strip()

            # Document metadata appears before the first H2 section.
            if stripped.startswith("## "):
                break

            match = self.METADATA_PATTERN.match(stripped)
            if not match:
                continue

            key = self._normalize_key(match.group("key"))
            value = match.group("value").strip()
            metadata[key] = value

        return metadata

    @staticmethod
    def _normalize_key(value: str) -> str:
        normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
        return normalized.strip("_")
