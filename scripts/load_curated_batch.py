from pathlib import Path

from app.db.session import SessionLocal
from app.pipeline.audit.run_store import PipelineRunStore
from app.pipeline.curated.store import CuratedCaseStore
from app.pipeline.incremental.case import IncrementalCaseFilter
from app.pipeline.quality.case import CaseQualityChecker
from app.pipeline.quarantine.store import QuarantineStore
from app.pipeline.reconciliation.case import ReconciliationReport
from app.pipeline.sources.csv_source import CSVCaseAdapter
from app.pipeline.standardization.case import CaseStandardizer


SOURCE = Path("data/sources/cases.csv")

SOURCE_NAME = "csv"
BATCH_ID = "week2-csv-001"


def main() -> None:
    # ---------------------------------------------------------
    # 1. Start a database session
    # ---------------------------------------------------------
    session = SessionLocal()

    audit_store = PipelineRunStore()

    # ---------------------------------------------------------
    # 2. Create an audit record with status = RUNNING
    # ---------------------------------------------------------
    run_id = audit_store.start(
        session=session,
        source_name=SOURCE_NAME,
        batch_id=BATCH_ID,
    )

    # IMPORTANT:
    # Commit this separately so the RUNNING record survives
    # even if the actual pipeline later fails.
    session.commit()

    try:
        # -----------------------------------------------------
        # 3. Read source
        # -----------------------------------------------------
        adapter = CSVCaseAdapter(SOURCE)

        raw_records = adapter.read_raw()

        # -----------------------------------------------------
        # 4. Standardize
        # -----------------------------------------------------
        standardizer = CaseStandardizer()

        standardized_records = (
            standardizer.standardize_many(
                SOURCE_NAME,
                raw_records,
            )
        )

        # -----------------------------------------------------
        # 5. Quality checks
        # -----------------------------------------------------
        quality_result = CaseQualityChecker().check(
            standardized_records
        )

        # -----------------------------------------------------
        # 6. Store rejected records in quarantine
        # -----------------------------------------------------
        QuarantineStore().store(
            session=session,
            source_name=SOURCE_NAME,
            batch_id=BATCH_ID,
            raw_records=raw_records,
            quality_result=quality_result,
        )

        # -----------------------------------------------------
        # 7. Find records that are genuinely new
        # -----------------------------------------------------
        new_records = (
            IncrementalCaseFilter().get_new_records(
                session=session,
                source_name=SOURCE_NAME,
                records=quality_result.valid_records,
            )
        )

        already_present_count = (
            len(quality_result.valid_records)
            - len(new_records)
        )

        # -----------------------------------------------------
        # 8. Idempotent database insert
        # -----------------------------------------------------
        persisted_count = (
            CuratedCaseStore().store_idempotent(
                session=session,
                source_name=SOURCE_NAME,
                batch_id=BATCH_ID,
                records=new_records,
            )
        )

        # -----------------------------------------------------
        # 9. Reconciliation
        # -----------------------------------------------------
        report = ReconciliationReport(
            source_count=len(raw_records),
            standardized_count=len(
                standardized_records
            ),
            rejected_count=len(
                quality_result.rejected_records
            ),
            already_present_count=(
                already_present_count
            ),
            persisted_count=persisted_count,
        )

        # This raises an error if records are unaccounted for.
        report.validate()

        # -----------------------------------------------------
        # 10. Mark audit run as SUCCESS
        # -----------------------------------------------------
        audit_store.complete(
            session=session,
            run_id=run_id,
            source_count=len(raw_records),
            standardized_count=len(
                standardized_records
            ),
            rejected_count=len(
                quality_result.rejected_records
            ),
            already_present_count=(
                already_present_count
            ),
            persisted_count=persisted_count,
        )

        # -----------------------------------------------------
        # 11. Commit the entire successful pipeline transaction
        # -----------------------------------------------------
        session.commit()

        print("Pipeline run successful.")
        print(
            f"Run ID: {run_id}"
        )
        print(
            f"Source records: {len(raw_records)}"
        )
        print(
            f"Rejected: "
            f"{len(quality_result.rejected_records)}"
        )
        print(
            f"Already present: "
            f"{already_present_count}"
        )
        print(
            f"Newly persisted: "
            f"{persisted_count}"
        )

    except Exception as exc:
        # -----------------------------------------------------
        # 12. Roll back incomplete business work
        # -----------------------------------------------------
        session.rollback()

        # -----------------------------------------------------
        # 13. Record FAILURE using a NEW session
        # -----------------------------------------------------
        audit_session = SessionLocal()

        try:
            audit_store.fail(
                session=audit_session,
                run_id=run_id,
                error_message=str(exc),
            )

            audit_session.commit()

        finally:
            audit_session.close()

        # Let the original error propagate
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()