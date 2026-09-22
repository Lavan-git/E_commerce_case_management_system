from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.curated_case import CuratedCase
from app.pipeline.contracts import StandardizedCaseRecord


class IncrementalCaseFilter:
    """
    Returns only case records that have not already been
    persisted for the given source.
    """

    def get_new_records(
        self,
        session: Session,
        source_name: str,
        records: list[StandardizedCaseRecord],
    ) -> list[StandardizedCaseRecord]:

        if not records:
            return []

        case_ids = [
            record.case_id
            for record in records
        ]

        existing_ids = set(
            session.scalars(
                select(CuratedCase.case_id).where(
                    CuratedCase.source_name == source_name,
                    CuratedCase.case_id.in_(case_ids),
                )
            ).all()
        )

        return [
            record
            for record in records
            if record.case_id not in existing_ids
        ]