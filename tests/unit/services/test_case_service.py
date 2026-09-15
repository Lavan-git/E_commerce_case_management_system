from unittest.mock import Mock

import pytest

from app.db.models.case import Case
from app.exceptions.case import (
    CaseNotFoundError,
    InvalidCaseStatusTransitionError,
    InvalidCaseTypeError,
)
from app.schemas.case import CaseCreate, CaseUpdateRequest
from app.services.case_service import CaseService


def make_service():
    repository = Mock()
    return CaseService(repository), repository


def make_case(**overrides):
    values = {
        "case_id": 1,
        "raised_by_customer_id": 1,
        "raised_by_vendor_id": None,
        "case_type": "PAYMENT",
        "category": "PAYMENT_WITHOUT_ORDER",
        "reason": "Payment deducted but order not created",
        "description": "Customer was charged but no order exists.",
        "priority": "HIGH",
        "status": "OPEN",
        "assigned_agent_id": None,
        "resolution": None,
        "resolved_at": None,
    }

    values.update(overrides)

    return Case(**values)


def test_create_case():
    service, repository = make_service()

    repository.create.side_effect = lambda db, case: setattr(
        case,
        "case_id",
        100,
    )

    payload = CaseCreate(
        raised_by_customer_id=1,
        case_type="PAYMENT",
        category="PAYMENT_WITHOUT_ORDER",
        reason="Payment deducted",
        description="Order was not created.",
        priority="HIGH",
    )

    db = Mock()

    result = service.create_case(
        db,
        payload,
    )

    assert result.case_id == 100
    assert result.status == "OPEN"

    repository.create.assert_called_once()
    db.add.assert_called_once()


def test_create_case_rejects_invalid_type():
    service, _ = make_service()

    payload = CaseCreate(
        raised_by_customer_id=1,
        case_type="NOT_REAL",
        category="TEST",
        reason="Invalid type",
        description="Invalid case.",
    )

    with pytest.raises(InvalidCaseTypeError):
        service.create_case(
            Mock(),
            payload,
        )


def test_get_case_not_found():
    service, repository = make_service()

    repository.get_by_id.return_value = None

    with pytest.raises(CaseNotFoundError):
        service.get_case(
            Mock(),
            999,
        )


def test_update_case_status():
    service, repository = make_service()

    case = make_case()

    payload = CaseUpdateRequest(
        status="IN_PROGRESS",
    )

    result = service.update_case(
        Mock(),
        case,
        payload,
    )

    assert result.status == "IN_PROGRESS"
    repository.update.assert_called_once()


def test_cannot_modify_closed_case():
    service, repository = make_service()

    case = make_case(
        status="CLOSED",
    )

    payload = CaseUpdateRequest(
        status="OPEN",
    )

    with pytest.raises(
        InvalidCaseStatusTransitionError
    ):
        service.update_case(
            Mock(),
            case,
            payload,
        )

    repository.update.assert_not_called()


def test_resolved_case_gets_resolved_at():
    service, _ = make_service()

    case = make_case()

    payload = CaseUpdateRequest(
        status="RESOLVED",
        resolution="Refund processed.",
    )

    result = service.update_case(
        Mock(),
        case,
        payload,
    )

    assert result.status == "RESOLVED"
    assert result.resolution == "Refund processed."
    assert result.resolved_at is not None