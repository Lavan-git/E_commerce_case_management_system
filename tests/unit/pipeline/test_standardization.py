from pathlib import Path

from app.pipeline.standardization.case import (
    CaseStandardizer,
)
from app.pipeline.sources.csv_source import CSVCaseAdapter
from app.pipeline.sources.json_source import JSONCaseAdapter
from app.pipeline.sources.parquet_source import (
    ParquetCaseAdapter,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = PROJECT_ROOT / "data" / "sources"


def test_csv_is_standardized_to_contract():
    raw_records = CSVCaseAdapter(
        SOURCE_DIR / "cases.csv"
    ).read_raw()

    records = CaseStandardizer().standardize_many(
        "csv",
        raw_records,
    )

    assert len(records) == 3
    assert records[0].case_id == 101
    assert records[0].actor_id == 1
    assert records[0].case_type == "PAYMENT"
    assert records[0].priority == "HIGH"


def test_json_is_standardized_to_contract():
    raw_records = JSONCaseAdapter(
        SOURCE_DIR / "cases.json"
    ).read_raw()

    records = CaseStandardizer().standardize_many(
        "json",
        raw_records,
    )

    assert len(records) == 3
    assert records[0].case_id == 104
    assert records[0].actor_id == 1
    assert records[0].case_type == "PAYMENT"
    assert records[1].priority == "MEDIUM"


def test_parquet_is_standardized_to_contract():
    raw_records = ParquetCaseAdapter(
        SOURCE_DIR / "cases.parquet"
    ).read_raw()

    records = CaseStandardizer().standardize_many(
        "parquet",
        raw_records,
    )

    assert len(records) == 3
    assert records[0].case_id == 107
    assert records[0].actor_id == 1
    assert records[0].case_type == "PAYMENT"
    assert records[1].status == "IN_PROGRESS"


def test_all_sources_produce_same_contract_shape():
    standardizer = CaseStandardizer()

    csv_records = standardizer.standardize_many(
        "csv",
        CSVCaseAdapter(
            SOURCE_DIR / "cases.csv"
        ).read_raw(),
    )

    json_records = standardizer.standardize_many(
        "json",
        JSONCaseAdapter(
            SOURCE_DIR / "cases.json"
        ).read_raw(),
    )

    parquet_records = standardizer.standardize_many(
        "parquet",
        ParquetCaseAdapter(
            SOURCE_DIR / "cases.parquet"
        ).read_raw(),
    )

    records = (
        csv_records
        + json_records
        + parquet_records
    )

    assert len(records) == 9

    assert all(
        record.case_type
        for record in records
    )