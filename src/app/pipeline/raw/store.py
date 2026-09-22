import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, Field


class RawFileMetadata(BaseModel):
    """
    Metadata describing a file stored in the raw layer.
    """

    source_name: str
    batch_id: str
    original_filename: str
    stored_path: str
    ingested_at: datetime
    size_bytes: int = Field(ge=0)
    sha256: str


class RawFileStore:
    """
    Stores source files in the raw landing zone without
    changing their original contents.
    """

    def __init__(self, root: Path) -> None:
        self.root = root

    def persist(
        self,
        source_path: Path,
        source_name: str,
        batch_id: str | None = None,
        ingested_at: datetime | None = None,
    ) -> RawFileMetadata:
        if not source_path.is_file():
            raise FileNotFoundError(
                f"Source file not found: {source_path}"
            )

        batch_id = batch_id or uuid4().hex
        ingested_at = (
            ingested_at
            or datetime.now(timezone.utc)
        )

        batch_directory = (
            self.root
            / source_name
            / batch_id
        )

        batch_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            batch_directory
            / source_path.name
        )

        shutil.copy2(
            source_path,
            destination,
        )

        file_bytes = destination.read_bytes()

        sha256 = hashlib.sha256(
            file_bytes
        ).hexdigest()

        metadata = RawFileMetadata(
            source_name=source_name,
            batch_id=batch_id,
            original_filename=source_path.name,
            stored_path=str(
                destination.relative_to(self.root)
            ),
            ingested_at=ingested_at,
            size_bytes=len(file_bytes),
            sha256=sha256,
        )

        manifest_path = (
            batch_directory
            / "manifest.json"
        )

        manifest_path.write_text(
            json.dumps(
                metadata.model_dump(mode="json"),
                indent=2,
            ),
            encoding="utf-8",
        )

        return metadata