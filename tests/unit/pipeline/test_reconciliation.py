import pytest

from app.pipeline.reconciliation.case import (
    ReconciliationReport,
)


def test_reconciliation_passes_when_all_records_are_accounted_for():
    report = ReconciliationReport(
        source_count=10,
        standardized_count=10,
        rejected_count=2,
        already_present_count=3,
        persisted_count=5,
    )

    assert report.accounted_count == 10
    assert report.is_consistent

    report.validate()


def test_reconciliation_fails_when_records_are_missing():
    report = ReconciliationReport(
        source_count=10,
        standardized_count=10,
        rejected_count=2,
        already_present_count=3,
        persisted_count=4,
    )

    assert report.accounted_count == 9
    assert not report.is_consistent

    with pytest.raises(
        ValueError,
        match="Pipeline reconciliation failed",
    ):
        report.validate()


def test_reconciliation_detects_standardization_count_mismatch():
    report = ReconciliationReport(
        source_count=10,
        standardized_count=9,
        rejected_count=1,
        already_present_count=3,
        persisted_count=6,
    )

    assert not report.is_consistent