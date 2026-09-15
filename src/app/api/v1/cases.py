from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.case import (
    CaseCreate,
    CaseResponse,
    CaseUpdateRequest,
)
from app.repositories.case_repository import CaseRepository
from app.services.case_service import CaseService


router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
)


DbSession = Annotated[
    Session,
    Depends(get_db),
]


def get_case_service() -> CaseService:
    return CaseService(
        repository=CaseRepository(),
    )


CaseServiceDependency = Annotated[
    CaseService,
    Depends(get_case_service),
]


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    payload: CaseCreate,
    db: DbSession,
    service: CaseServiceDependency,
) -> CaseResponse:
    case = service.create_case(
        db,
        payload,
    )

    db.commit()
    db.refresh(case)

    return case


@router.get(
    "",
    response_model=list[CaseResponse],
)
def list_cases(
    db: DbSession,
    service: CaseServiceDependency,
    case_status: str | None = Query(
        default=None,
        alias="status",
    ),
    case_type: str | None = None,
    priority: str | None = None,
    assigned_agent_id: int | None = None,
) -> list[CaseResponse]:

    return service.list_cases(
        db,
        status=case_status,
        case_type=case_type,
        priority=priority,
        assigned_agent_id=assigned_agent_id,
    )


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_case(
    case_id: int,
    db: DbSession,
    service: CaseServiceDependency,
) -> CaseResponse:
    return service.get_case(
        db,
        case_id,
    )


@router.patch(
    "/{case_id}",
    response_model=CaseResponse,
)
def update_case(
    case_id: int,
    payload: CaseUpdateRequest,
    db: DbSession,
    service: CaseServiceDependency,
) -> CaseResponse:

    case = service.get_case(
        db,
        case_id,
    )

    case = service.update_case(
        db,
        case,
        payload,
    )

    db.commit()
    db.refresh(case)

    return case