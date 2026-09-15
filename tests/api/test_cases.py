from fastapi.testclient import TestClient

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

    assert "X-Request-ID" in response.headers


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

    assert data
    assert all(
        "case_id" in case
        for case in data
    )


def test_filter_delivery_cases():
    response = client.get(
        "/api/v1/cases",
        params={
            "case_type": "DELIVERY",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data
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

    assert "request_id" in body["error"]


def test_invalid_case_actor():
    response = client.post(
        "/api/v1/cases",
        json={
            "raised_by_customer_id": 1,
            "raised_by_vendor_id": 2,
            "case_type": "PAYMENT",
            "category": "TEST",
            "reason": "Invalid actor",
            "description": "Both actors supplied.",
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert body["error"]["code"] == (
        "VALIDATION_ERROR"
    )

    assert "request_id" in body["error"]


def test_invalid_case_type():
    response = client.post(
        "/api/v1/cases",
        json={
            "raised_by_customer_id": 1,
            "case_type": "INVALID_TYPE",
            "category": "TEST",
            "reason": "Invalid case type",
            "description": "Testing error handling.",
        },
    )

    assert response.status_code == 400

    body = response.json()

    assert body["error"]["code"] == (
        "InvalidCaseTypeError"
    )


def test_create_case():
    response = client.post(
        "/api/v1/cases",
        json={
            "raised_by_customer_id": 4,
            "case_type": "VENDOR",
            "category": "GENERAL",
            "reason": "Test case creation",
            "description": "Created during API testing.",
            "priority": "LOW",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["case_id"] > 0
    assert data["status"] == "OPEN"


def test_update_case():
    response = client.patch(
        "/api/v1/cases/10",
        json={
            "status": "IN_PROGRESS",
            "priority": "CRITICAL",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["case_id"] == 10
    assert data["status"] == "IN_PROGRESS"
    assert data["priority"] == "CRITICAL"