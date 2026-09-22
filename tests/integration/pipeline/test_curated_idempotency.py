from app.db.session import SessionLocal
from app.pipeline.contracts import StandardizedCaseRecord
from app.pipeline.curated.store import CuratedCaseStore


def make_record(
    case_id: int,
) -> StandardizedCaseRecord:
    return StandardizedCaseRecord(
        case_id=case_id,
        actor_type="CUSTOMER",
        actor_id=1,
        case_type="PAYMENT",
        priority="HIGH",
        status="OPEN",
        category="IDEMPOTENCY_TEST",
        description="Temporary idempotency test record.",
        created_at="2026-09-22T10:30:00",
    )


def test_curated_insert_is_idempotent():
    session = SessionLocal()

    try:
        records = [
            make_record(900001),
        ]

        store = CuratedCaseStore()

        first_insert = store.store_idempotent(
            session=session,
            source_name="idempotency_test",
            batch_id="test-batch-001",
            records=records,
        )

        second_insert = store.store_idempotent(
            session=session,
            source_name="idempotency_test",
            batch_id="test-batch-001",
            records=records,
        )

        assert first_insert == 1
        assert second_insert == 0

        session.rollback()

    finally:
        session.close()