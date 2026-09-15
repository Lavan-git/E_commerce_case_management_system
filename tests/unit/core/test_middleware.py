import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.middleware import request_logging_middleware


@pytest.fixture
def middleware_test_app():
    app = FastAPI()

    app.middleware("http")(request_logging_middleware)

    @app.get("/test")
    def test_endpoint():
        return {"message": "ok"}

    @app.get("/error")
    def error_endpoint():
        raise RuntimeError("test failure")

    return app


def test_middleware_generates_request_id(middleware_test_app):
    client = TestClient(middleware_test_app)

    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")
    assert len(response.headers["X-Request-ID"]) > 0


def test_middleware_preserves_existing_request_id(middleware_test_app):
    client = TestClient(middleware_test_app)

    request_id = "test-request-id"

    response = client.get(
        "/test",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id


def test_middleware_logs_successful_request(
    middleware_test_app,
    caplog,
):
    client = TestClient(middleware_test_app)

    with caplog.at_level(logging.INFO, logger="app.http"):
        response = client.get("/test")

    assert response.status_code == 200

    messages = [
        record.getMessage()
        for record in caplog.records
    ]

    assert "http.request" in messages


def test_middleware_logs_failed_request(
    middleware_test_app,
    caplog,
):
    client = TestClient(middleware_test_app)

    with caplog.at_level(logging.ERROR, logger="app.http"):
        with pytest.raises(RuntimeError, match="test failure"):
            client.get("/error")

    messages = [
        record.getMessage()
        for record in caplog.records
    ]

    assert "http.request.failed" in messages