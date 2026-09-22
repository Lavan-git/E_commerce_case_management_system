from dataclasses import dataclass

from app.pipeline.contracts import StandardizedCaseRecord


@dataclass(frozen=True)
class QualityIssue:
    code: str
    message: str
    record_index: int
    case_id: int | None


@dataclass
class QualityResult:
    valid_records: list[StandardizedCaseRecord]
    rejected_records: list[StandardizedCaseRecord]
    rejected_indexes: set[int]
    issues: list[QualityIssue]


class CaseQualityChecker:
    """
    Performs dataset-level quality checks on records that have
    already passed contract validation.
    """

    def check(
        self,
        records: list[StandardizedCaseRecord],
    ) -> QualityResult:

        seen_case_ids: dict[int, int] = {}

        rejected_indexes: set[int] = set()
        issues: list[QualityIssue] = []

        for index, record in enumerate(records):

            if record.case_id in seen_case_ids:
                issues.append(
                    QualityIssue(
                        code="DUPLICATE_CASE_ID",
                        message=(
                            "Case ID appears more than once "
                            "in the same batch."
                        ),
                        record_index=index,
                        case_id=record.case_id,
                    )
                )

                rejected_indexes.add(index)

            else:
                seen_case_ids[record.case_id] = index

        valid_records = [
            record
            for index, record in enumerate(records)
            if index not in rejected_indexes
        ]

        rejected_records = [
            record
            for index, record in enumerate(records)
            if index in rejected_indexes
        ]

        return QualityResult(
            valid_records=valid_records,
            rejected_records=rejected_records,
            rejected_indexes=rejected_indexes,
            issues=issues,
        )