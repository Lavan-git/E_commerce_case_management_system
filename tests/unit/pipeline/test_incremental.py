from unittest.mock import MagicMock

from app.pipeline.contracts import StandardizedCaseRecord
from app.pipeline.incremental.case import (
    IncrementalCaseFilter,
)


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
        description="Payment issue.",
        created_at="2026-09-22T10:30:00",
    )


def test_only_new_records_are_returned():
    session = MagicMock()

    session.scalars.return_value.all.return_value = [
        101,
        102,
        103,
    ]

    records = [
        make_record(101),
        make_record(102),
        make_record(103),
        make_record(104),
        make_record(105),
    ]

    result = IncrementalCaseFilter().get_new_records(
        session=session,
        source_name="csv",
        records=records,
    )

    assert [
        record.case_id
        for record in result
    ] == [104, 105]


def test_all_records_are_new_when_source_has_no_existing_records():
    session = MagicMock()

    session.scalars.return_value.all.return_value = []

    records = [
        make_record(101),
        make_record(102),
    ]

    result = IncrementalCaseFilter().get_new_records(
        session=session,
        source_name="csv",
        records=records,
    )

    assert [
        record.case_id
        for record in result
    ] == [101, 102]


def test_empty_input_returns_empty_result():
    session = MagicMock()

    result = IncrementalCaseFilter().get_new_records(
        session=session,
        source_name="csv",
        records=[],
    )

    assert result == []
    session.scalars.assert_not_called()