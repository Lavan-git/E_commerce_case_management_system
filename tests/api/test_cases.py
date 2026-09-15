from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app


client = TestClient(app)


def test_health():
    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_get_case():
    response = client.get(
        "/api/v1/cases/4"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["case_id"] == 4
    assert data["case_type"] == "DELIVERY"
    assert data["status"] == "IN_PROGRESS"


def test_list_cases():
    response = client.get(
        "/api/v1/cases"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 9


def test_filter_delivery_cases():
    response = client.get(
        "/api/v1/cases",
        params={
            "case_type": "DELIVERY",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert all(
        case["case_type"] == "DELIVERY"
        for case in data
    )


def test_case_not_found():
    response = client.get(
        "/api/v1/cases/999999"
    )

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == (
        "CaseNotFoundError"
    )