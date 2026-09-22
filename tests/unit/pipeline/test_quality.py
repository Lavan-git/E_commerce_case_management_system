from app.pipeline.contracts import StandardizedCaseRecord
from app.pipeline.quality.case import CaseQualityChecker


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


def test_valid_records_pass_quality_checks():
    records = [
        make_record(101),
        make_record(102),
        make_record(103),
    ]

    result = CaseQualityChecker().check(records)

    assert len(result.valid_records) == 3
    assert len(result.rejected_records) == 0
    assert result.rejected_indexes == set()
    assert result.issues == []


def test_duplicate_case_id_is_rejected():
    records = [
        make_record(101),
        make_record(101),
        make_record(102),
    ]

    result = CaseQualityChecker().check(records)

    assert len(result.valid_records) == 2
    assert len(result.rejected_records) == 1
    assert result.rejected_indexes == {1}

    assert result.issues[0].code == "DUPLICATE_CASE_ID"
    assert result.issues[0].case_id == 101