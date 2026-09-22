from sqlalchemy.orm import Session

from app.db.models.pipeline_quarantine import PipelineQuarantine
from app.pipeline.quality.case import QualityResult


class QuarantineStore:
    """
    Persists records rejected by dataset-level quality checks.
    """

    def store(
        self,
        session: Session,
        source_name: str,
        batch_id: str,
        raw_records: list[dict],
        quality_result: QualityResult,
    ) -> list[PipelineQuarantine]:

        rows: list[PipelineQuarantine] = []

        for record_index in sorted(
            quality_result.rejected_indexes
        ):
            record_issues = [
                issue
                for issue in quality_result.issues
                if issue.record_index == record_index
            ]

            row = PipelineQuarantine(
                source_name=source_name,
                batch_id=batch_id,
                record_index=record_index,
                raw_record=raw_records[record_index],
                issue_codes=[
                    issue.code
                    for issue in record_issues
                ],
                issue_messages=[
                    issue.message
                    for issue in record_issues
                ],
            )

            session.add(row)
            rows.append(row)

        return rows