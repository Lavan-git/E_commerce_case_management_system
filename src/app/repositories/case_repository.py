from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.case import Case


class CaseRepository:
    """
    Handles database operations for the Case entity.

    Repository responsibilities:
    - Build database queries
    - Persist ORM entities
    - Retrieve ORM entities

    Repository does NOT:
    - Apply business rules
    - Decide HTTP status codes
    - Commit/rollback transactions
    """

    def create(
        self,
        db: Session,
        case: Case,
    ) -> Case:
        db.add(case)
        db.flush()
        db.refresh(case)

        return case

    def get_by_id(
        self,
        db: Session,
        case_id: int,
    ) -> Case | None:

        statement = select(Case).where(
            Case.case_id == case_id
        )

        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        status: str | None = None,
        case_type: str | None = None,
        priority: str | None = None,
        assigned_agent_id: int | None = None,
    ) -> list[Case]:

        statement = select(Case)

        if status is not None:
            statement = statement.where(
                Case.status == status
            )

        if case_type is not None:
            statement = statement.where(
                Case.case_type == case_type
            )

        if priority is not None:
            statement = statement.where(
                Case.priority == priority
            )

        if assigned_agent_id is not None:
            statement = statement.where(
                Case.assigned_agent_id == assigned_agent_id
            )

        statement = statement.order_by(
            Case.created_at.desc()
        )

        return list(
            db.scalars(statement).all()
        )

    def update(
        self,
        db: Session,
        case: Case,
    ) -> Case:

        db.flush()
        db.refresh(case)

        return case