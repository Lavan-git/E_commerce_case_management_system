from pathlib import Path

from app.pipeline.sources.csv_source import CSVCaseAdapter
from app.pipeline.sources.json_source import JSONCaseAdapter
from app.pipeline.sources.parquet_source import (
    ParquetCaseAdapter,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = PROJECT_ROOT / "data" / "sources"


def test_csv_adapter_reads_native_records():
    adapter = CSVCaseAdapter(
        SOURCE_DIR / "cases.csv"
    )

    records = adapter.read_raw()

    assert len(records) == 3

    assert "case_id" in records[0]
    assert "customer_id" in records[0]


def test_json_adapter_reads_native_records():
    adapter = JSONCaseAdapter(
        SOURCE_DIR / "cases.json"
    )

    records = adapter.read_raw()

    assert len(records) == 3

    assert "caseId" in records[0]
    assert "customerId" in records[0]


def test_parquet_adapter_reads_native_records():
    adapter = ParquetCaseAdapter(
        SOURCE_DIR / "cases.parquet"
    )

    records = adapter.read_raw()

    assert len(records) == 3

    assert "case_identifier" in records[0]
    assert "actor_id" in records[0]