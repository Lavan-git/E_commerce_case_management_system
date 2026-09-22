from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.pipeline_run import PipelineRun


class PipelineRunStore:

    def start(
        self,
        session: Session,
        source_name: str,
        batch_id: str,
    ) -> UUID:

        run_id = uuid4()

        run = PipelineRun(
            run_id=run_id,
            source_name=source_name,
            batch_id=batch_id,
            status="RUNNING",
            started_at=datetime.now(timezone.utc),
        )

        session.add(run)

        return run_id

    def complete(
        self,
        session: Session,
        run_id: UUID,
        *,
        source_count: int,
        standardized_count: int,
        rejected_count: int,
        already_present_count: int,
        persisted_count: int,
    ) -> None:

        run = session.scalar(
            select(PipelineRun).where(
                PipelineRun.run_id == run_id
            )
        )

        if run is None:
            raise ValueError(
                f"Pipeline run not found: {run_id}"
            )

        run.status = "SUCCESS"
        run.completed_at = datetime.now(timezone.utc)
        run.source_count = source_count
        run.standardized_count = standardized_count
        run.rejected_count = rejected_count
        run.already_present_count = (
            already_present_count
        )
        run.persisted_count = persisted_count

    def fail(
        self,
        session: Session,
        run_id: UUID,
        error_message: str,
    ) -> None:

        run = session.scalar(
            select(PipelineRun).where(
                PipelineRun.run_id == run_id
            )
        )

        if run is None:
            raise ValueError(
                f"Pipeline run not found: {run_id}"
            )

        run.status = "FAILED"
        run.completed_at = datetime.now(timezone.utc)
        run.error_message = error_message