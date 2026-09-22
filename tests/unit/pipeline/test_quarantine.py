from unittest.mock import MagicMock

from app.pipeline.quality.case import (
    QualityIssue,
    QualityResult,
)
from app.pipeline.quarantine.store import (
    QuarantineStore,
)


def test_quarantine_store_persists_rejected_raw_record():
    session = MagicMock()

    raw_records = [
        {
            "case_id": 101,
            "priority": "HIGH",
        },
        {
            "case_id": 101,
            "priority": "HIGH",
        },
    ]

    quality_result = QualityResult(
        valid_records=[],
        rejected_records=[],
        rejected_indexes={1},
        issues=[
            QualityIssue(
                code="DUPLICATE_CASE_ID",
                message=(
                    "Case ID appears more than once "
                    "in the same batch."
                ),
                record_index=1,
                case_id=101,
            )
        ],
    )

    rows = QuarantineStore().store(
        session=session,
        source_name="csv",
        batch_id="batch-001",
        raw_records=raw_records,
        quality_result=quality_result,
    )

    assert len(rows) == 1

    assert rows[0].source_name == "csv"
    assert rows[0].batch_id == "batch-001"
    assert rows[0].record_index == 1
    assert rows[0].raw_record == raw_records[1]
    assert rows[0].issue_codes == [
        "DUPLICATE_CASE_ID"
    ]

    session.add.assert_called_once()