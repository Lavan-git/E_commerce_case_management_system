import pytest
from pydantic import ValidationError

from app.pipeline.contracts import StandardizedCaseRecord


def test_valid_case_record():
    record = StandardizedCaseRecord(
        case_id=101,
        actor_type="CUSTOMER",
        actor_id=1,
        case_type="PAYMENT",
        priority="HIGH",
        status="OPEN",
        category="PAYMENT_NOT_REFLECTED",
        description="Payment was deducted but the order was not created.",
        created_at="2026-09-22T10:30:00",
    )

    assert record.case_id == 101
    assert record.actor_type == "CUSTOMER"
    assert record.case_type == "PAYMENT"
    assert record.priority == "HIGH"
    assert record.status == "OPEN"


def test_invalid_case_id_is_rejected():
    with pytest.raises(ValidationError):
        StandardizedCaseRecord(
            case_id=0,
            actor_type="CUSTOMER",
            actor_id=1,
            case_type="PAYMENT",
            priority="HIGH",
            status="OPEN",
            category="PAYMENT_NOT_REFLECTED",
            description="Payment was deducted.",
            created_at="2026-09-22T10:30:00",
        )


def test_invalid_priority_is_rejected():
    with pytest.raises(ValidationError):
        StandardizedCaseRecord(
            case_id=101,
            actor_type="CUSTOMER",
            actor_id=1,
            case_type="PAYMENT",
            priority="URGENT",
            status="OPEN",
            category="PAYMENT_NOT_REFLECTED",
            description="Payment was deducted.",
            created_at="2026-09-22T10:30:00",
        )


def test_invalid_status_is_rejected():
    with pytest.raises(ValidationError):
        StandardizedCaseRecord(
            case_id=101,
            actor_type="CUSTOMER",
            actor_id=1,
            case_type="PAYMENT",
            priority="HIGH",
            status="SOMETHING_RANDOM",
            category="PAYMENT_NOT_REFLECTED",
            description="Payment was deducted.",
            created_at="2026-09-22T10:30:00",
        )


def test_extra_fields_are_rejected():
    with pytest.raises(ValidationError):
        StandardizedCaseRecord(
            case_id=101,
            actor_type="CUSTOMER",
            actor_id=1,
            case_type="PAYMENT",
            priority="HIGH",
            status="OPEN",
            category="PAYMENT_NOT_REFLECTED",
            description="Payment was deducted.",
            created_at="2026-09-22T10:30:00",
            unexpected_field="should fail",
        )