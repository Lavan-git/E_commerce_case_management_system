from dataclasses import dataclass


@dataclass(frozen=True)
class ReconciliationReport:
    source_count: int
    standardized_count: int
    rejected_count: int
    already_present_count: int
    persisted_count: int

    @property
    def accounted_count(self) -> int:
        return (
            self.rejected_count
            + self.already_present_count
            + self.persisted_count
        )

    @property
    def is_consistent(self) -> bool:
        return (
            self.standardized_count == self.source_count
            and self.accounted_count == self.source_count
        )

    def validate(self) -> None:
        if not self.is_consistent:
            raise ValueError(
                "Pipeline reconciliation failed: "
                f"source={self.source_count}, "
                f"standardized={self.standardized_count}, "
                f"rejected={self.rejected_count}, "
                f"already_present={self.already_present_count}, "
                f"persisted={self.persisted_count}"
            )