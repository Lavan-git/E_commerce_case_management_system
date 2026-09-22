from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.models.curated_case import CuratedCase
from app.pipeline.contracts import StandardizedCaseRecord


class CuratedCaseStore:
    """
    Persists validated, standardized case records into the
    curated data layer.

    Database uniqueness is the final idempotency guarantee.
    """

    def store_idempotent(
        self,
        session: Session,
        source_name: str,
        batch_id: str,
        records: list[StandardizedCaseRecord],
    ) -> int:
        if not records:
            return 0

        values = [
            {
                "source_name": source_name,
                "batch_id": batch_id,
                "case_id": record.case_id,
                "actor_type": record.actor_type,
                "actor_id": record.actor_id,
                "case_type": record.case_type,
                "priority": record.priority,
                "status": record.status,
                "category": record.category,
                "description": record.description,
                "source_created_at": record.created_at,
            }
            for record in records
        ]

        statement = (
            insert(CuratedCase)
            .values(values)
            .on_conflict_do_nothing(
                index_elements=[
                    "source_name",
                    "case_id",
                ]
            )
            .returning(CuratedCase.case_id)
        )

        result = session.execute(statement)

        inserted_ids = result.scalars().all()

        return len(inserted_ids)