from typing import Any

from app.pipeline.contracts import StandardizedCaseRecord


class CaseStandardizer:
    """
    Converts source-specific case records into the
    canonical StandardizedCaseRecord contract.
    """

    FIELD_MAPPINGS = {
        "csv": {
            "case_id": "case_id",
            "actor_id": "customer_id",
            "case_type": "case_type",
            "priority": "priority",
            "status": "status",
            "category": "category",
            "description": "description",
            "created_at": "created_at",
        },
        "json": {
            "case_id": "caseId",
            "actor_id": "customerId",
            "case_type": "caseType",
            "priority": "priority",
            "status": "status",
            "category": "category",
            "description": "description",
            "created_at": "createdAt",
        },
        "parquet": {
            "case_id": "case_identifier",
            "actor_id": "actor_id",
            "case_type": "type",
            "priority": "severity",
            "status": "state",
            "category": "reason",
            "description": "details",
            "created_at": "created",
        },
    }

    def standardize(
        self,
        source_name: str,
        record: dict[str, Any],
    ) -> StandardizedCaseRecord:
        if source_name not in self.FIELD_MAPPINGS:
            raise ValueError(
                f"Unsupported source: {source_name}"
            )

        mapping = self.FIELD_MAPPINGS[source_name]

        return StandardizedCaseRecord(
            case_id=int(record[mapping["case_id"]]),
            actor_type="CUSTOMER",
            actor_id=int(record[mapping["actor_id"]]),
            case_type=str(
                record[mapping["case_type"]]
            ).strip().upper(),
            priority=str(
                record[mapping["priority"]]
            ).strip().upper(),
            status=str(
                record[mapping["status"]]
            ).strip().upper(),
            category=str(
                record[mapping["category"]]
            ).strip(),
            description=str(
                record[mapping["description"]]
            ).strip(),
            created_at=record[mapping["created_at"]],
        )

    def standardize_many(
        self,
        source_name: str,
        records: list[dict[str, Any]],
    ) -> list[StandardizedCaseRecord]:
        return [
            self.standardize(
                source_name,
                record,
            )
            for record in records
        ]