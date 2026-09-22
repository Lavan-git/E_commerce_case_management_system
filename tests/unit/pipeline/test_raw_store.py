import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.pipeline.raw.store import RawFileStore


def test_raw_store_preserves_original_file(tmp_path: Path):
    source = tmp_path / "cases.csv"

    original_content = (
        "case_id,priority\n"
        "101,HIGH\n"
    )

    source.write_text(
        original_content,
        encoding="utf-8",
    )

    raw_root = tmp_path / "raw"

    store = RawFileStore(raw_root)

    metadata = store.persist(
        source_path=source,
        source_name="csv",
        batch_id="batch-001",
        ingested_at=datetime(
            2026,
            9,
            22,
            10,
            0,
            tzinfo=timezone.utc,
        ),
    )

    stored_file = (
        raw_root
        / "csv"
        / "batch-001"
        / "cases.csv"
    )

    assert stored_file.exists()

    assert (
        stored_file.read_text(
            encoding="utf-8"
        )
        == original_content
    )

    assert metadata.source_name == "csv"
    assert metadata.batch_id == "batch-001"
    assert metadata.original_filename == "cases.csv"


def test_raw_store_records_file_integrity_metadata(tmp_path: Path):
    source = tmp_path / "cases.json"

    content = '{"caseId": 101}'

    source.write_text(
        content,
        encoding="utf-8",
    )

    raw_root = tmp_path / "raw"

    store = RawFileStore(raw_root)

    metadata = store.persist(
        source_path=source,
        source_name="json",
        batch_id="batch-002",
    )

    expected_hash = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    assert metadata.size_bytes == len(
        content.encode("utf-8")
    )

    assert metadata.sha256 == expected_hash


def test_raw_store_writes_manifest(tmp_path: Path):
    source = tmp_path / "cases.csv"

    source.write_text(
        "case_id\n101\n",
        encoding="utf-8",
    )

    raw_root = tmp_path / "raw"

    store = RawFileStore(raw_root)

    store.persist(
        source_path=source,
        source_name="csv",
        batch_id="batch-003",
    )

    manifest = (
        raw_root
        / "csv"
        / "batch-003"
        / "manifest.json"
    )

    assert manifest.exists()

    payload = json.loads(
        manifest.read_text(
            encoding="utf-8"
        )
    )

    assert payload["source_name"] == "csv"
    assert payload["batch_id"] == "batch-003"
    assert payload["original_filename"] == "cases.csv"


def test_raw_store_rejects_missing_source(tmp_path: Path):
    store = RawFileStore(tmp_path / "raw")

    with pytest.raises(FileNotFoundError):
        store.persist(
            source_path=tmp_path / "missing.csv",
            source_name="csv",
            batch_id="batch-004",
        )