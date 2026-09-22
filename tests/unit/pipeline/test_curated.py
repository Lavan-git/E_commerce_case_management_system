from unittest.mock import MagicMock

from app.pipeline.contracts import StandardizedCaseRecord
from app.pipeline.curated.store import CuratedCaseStore


def make_record(
    case_id: int,
) -> StandardizedCaseRecord:
    return StandardizedCaseRecord(
        case_id=case_id,
        actor_type="CUSTOMER",
        actor_id=1,
        case_type="PAYMENT",
        priority="HIGH",
        status="OPEN",
        category="PAYMENT_NOT_REFLECTED",
        description="Payment deducted.",
        created_at="2026-09-22T10:30:00",
    )


def test_empty_records_insert_nothing():
    session = MagicMock()

    result = CuratedCaseStore().store_idempotent(
        session=session,
        source_name="csv",
        batch_id="batch-001",
        records=[],
    )

    assert result == 0
    session.execute.assert_not_called()


def test_idempotent_insert_builds_database_statement():
    session = MagicMock()

    session.execute.return_value.scalars.return_value.all.return_value = [
        101,
        102,
    ]

    records = [
        make_record(101),
        make_record(102),
    ]

    result = CuratedCaseStore().store_idempotent(
        session=session,
        source_name="csv",
        batch_id="batch-001",
        records=records,
    )

    assert result == 2
    session.execute.assert_called_once()