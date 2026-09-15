from app.db.session import SessionLocal
from app.repositories.case_repository import CaseRepository


def test_get_case_by_id():
    repository = CaseRepository()

    with SessionLocal() as db:
        case = repository.get_by_id(db, 4)

        assert case is not None
        assert case.case_id == 4
        assert case.case_type == "DELIVERY"
        assert case.status == "IN_PROGRESS"


def test_list_cases():
    repository = CaseRepository()

    with SessionLocal() as db:
        cases = repository.list(db)

        assert cases
        assert all(
            case.case_id is not None
            for case in cases
        )


def test_list_cases_by_type():
    repository = CaseRepository()

    with SessionLocal() as db:
        cases = repository.list(
            db,
            case_type="DELIVERY",
        )

        assert cases
        assert all(
            case.case_type == "DELIVERY"
            for case in cases
        )


def test_list_cases_by_status():
    repository = CaseRepository()

    with SessionLocal() as db:
        cases = repository.list(
            db,
            status="OPEN",
        )

        assert cases
        assert all(
            case.status == "OPEN"
            for case in cases
        )