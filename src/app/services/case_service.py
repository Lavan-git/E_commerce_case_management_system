from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.case import Case
from app.db.models.case_update import CaseUpdate
from app.exceptions.case import (
    CaseNotFoundError,
    InvalidCaseResolutionError,
    InvalidCaseStatusTransitionError,
    InvalidCaseTypeError,
)
from app.repositories.case_repository import CaseRepository
from app.schemas.case import CaseCreate, CaseUpdateRequest
import logging
logger = logging.getLogger("app.case")
class CaseService:
    SUPPORTED_CASE_TYPES = {
        "ACCOUNT",
        "ORDER",
        "PAYMENT",
        "DELIVERY",
        "RETURN",
        "REFUND",
        "PAYOUT",
        "VENDOR",
        "OTHER",
    }

    VALID_PRIORITIES = {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }

    VALID_STATUSES = {
        "OPEN",
        "IN_PROGRESS",
        "WAITING_FOR_CUSTOMER",
        "WAITING_FOR_VENDOR",
        "WAITING_FOR_EXTERNAL",
        "RESOLVED",
        "CLOSED",
        "CANCELLED",
    }

    TERMINAL_STATUSES = {
        "CLOSED",
        "CANCELLED",
    }

    def __init__(
        self,
        repository: CaseRepository,
    ) -> None:
        self.repository = repository

    def create_case(
        self,
        db: Session,
        payload: CaseCreate,
    ) -> Case:
        self._validate_case_type(payload.case_type)
        self._validate_priority(payload.priority)

        now = datetime.now(timezone.utc)

        case = Case(
            raised_by_customer_id=payload.raised_by_customer_id,
            raised_by_vendor_id=payload.raised_by_vendor_id,
            case_type=payload.case_type,
            category=payload.category,
            reason=payload.reason,
            description=payload.description,
            priority=payload.priority,
            assigned_agent_id=payload.assigned_agent_id,
            order_id=payload.order_id,
            order_item_id=payload.order_item_id,
            payment_id=payload.payment_id,
            delivery_id=payload.delivery_id,
            return_id=payload.return_id,
            refund_id=payload.refund_id,
            vendor_payout_id=payload.vendor_payout_id,
            status="OPEN",
            created_at=now,
            updated_at=now,
        )

        self.repository.create(db, case)

        initial_update = CaseUpdate(
            case_id=case.case_id,
            updated_by_agent_id=payload.assigned_agent_id,
            source="AGENT" if payload.assigned_agent_id else "SYSTEM",
            old_status=None,
            new_status="OPEN",
            comment="Case created.",
            created_at=now,
        )

        db.add(initial_update)
        logger.info(
        "case.created",
        extra={
            "case_id": case.case_id,
            "case_type": case.case_type,
            "status": case.status,
            },
        )

        return case

    def get_case(
        self,
        db: Session,
        case_id: int,
    ) -> Case:
        case = self.repository.get_by_id(db, case_id)

        if case is None:
            raise CaseNotFoundError(
                f"Case {case_id} was not found."
            )

        return case

    def list_cases(
        self,
        db: Session,
        *,
        status: str | None = None,
        case_type: str | None = None,
        priority: str | None = None,
        assigned_agent_id: int | None = None,
    ) -> list[Case]:

        if status is not None:
            self._validate_status(status)

        if case_type is not None:
            self._validate_case_type(case_type)

        if priority is not None:
            self._validate_priority(priority)

        return self.repository.list(
            db,
            status=status,
            case_type=case_type,
            priority=priority,
            assigned_agent_id=assigned_agent_id,
        )

    def update_case(
        self,
        db: Session,
        case: Case,
        payload: CaseUpdateRequest,
    ) -> Case:

        old_status = case.status

        if payload.status is not None:
            self._validate_status(payload.status)

            if payload.status != old_status:
                self._validate_status_transition(
                    old_status,
                    payload.status,
                )

        if payload.priority is not None:
            self._validate_priority(payload.priority)

        if (
            payload.status in {"RESOLVED", "CLOSED"}
            and not payload.resolution
            and not case.resolution
        ):
            raise InvalidCaseResolutionError(
                "A resolution is required when resolving or closing a case."
            )

        changes = payload.model_dump(
            exclude_unset=True
        )

        for field, value in changes.items():
            setattr(case, field, value)

        now = datetime.now(timezone.utc)
        case.updated_at = now

        if payload.status in {"RESOLVED", "CLOSED"}:
            if case.resolved_at is None:
                case.resolved_at = now
        elif payload.status is not None and payload.status not in {
            "RESOLVED",
            "CLOSED",
        }:
            case.resolved_at = None

        if payload.status is not None and payload.status != old_status:
            update = CaseUpdate(
                case_id=case.case_id,
                updated_by_agent_id=case.assigned_agent_id,
                source=(
                    "AGENT"
                    if case.assigned_agent_id is not None
                    else "SYSTEM"
                ),
                old_status=old_status,
                new_status=payload.status,
                comment=(
                    f"Case status changed from "
                    f"{old_status} to {payload.status}."
                ),
                created_at=now,
            )

            db.add(update)
            logger.info(
            "case.status_changed",
            extra={
                "case_id": case.case_id,
                "case_type": case.case_type,
                "status": payload.status,
                },
            )

        self.repository.update(db, case)

        return case

    def _validate_case_type(
        self,
        case_type: str,
    ) -> None:
        if case_type not in self.SUPPORTED_CASE_TYPES:
            raise InvalidCaseTypeError(
                f"Unsupported case type: {case_type}."
            )

    def _validate_priority(
        self,
        priority: str,
    ) -> None:
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority: {priority}."
            )

    def _validate_status(
        self,
        status: str,
    ) -> None:
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status: {status}."
            )

    def _validate_status_transition(
        self,
        old_status: str,
        new_status: str,
    ) -> None:
        if old_status in self.TERMINAL_STATUSES:
            raise InvalidCaseStatusTransitionError(
                f"Cannot change a terminal case "
                f"from {old_status} to {new_status}."
            )