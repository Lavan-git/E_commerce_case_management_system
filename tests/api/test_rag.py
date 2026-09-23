from types import SimpleNamespace

from fastapi.testclient import TestClient

from src.app.main import app
from src.app.api.v1.rag import get_rag_service


client = TestClient(app)


class FakeRAGService:
    def __init__(self, blocked: bool = False):
        self.blocked = blocked

    def ask(
        self,
        question: str,
        metadata_filter: dict[str, str] | None = None,
        forbidden_claims: list[str] | None = None,
    ):
        if self.blocked:
            return SimpleNamespace(
                answer=(
                    "I could not produce a response that was fully "
                    "supported by the retrieved policy evidence."
                ),
                sources=[
                    "payment_policy.md — Payment deducted but order not created"
                ],
                retrieved_chunks=["payment_policy_03_01"],
                grounding_blocked=True,
                grounding_violations=[
                    "follow the applicable refund procedure"
                ],
            )

        return SimpleNamespace(
            answer=(
                "Verify the payment transaction and check whether "
                "an order exists."
            ),
            sources=[
                "payment_policy.md — Payment deducted but order not created"
            ],
            retrieved_chunks=["payment_policy_03_01"],
            grounding_blocked=False,
            grounding_violations=[],
        )


def test_rag_query_returns_grounded_answer():
    app.dependency_overrides[get_rag_service] = (
        lambda: FakeRAGService(blocked=False)
    )

    try:
        response = client.post(
            "/api/v1/rag/query",
            json={
                "question": (
                    "A customer says their payment was deducted "
                    "but the order was never created."
                )
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["grounding_blocked"] is False
        assert data["grounding_violations"] == []
        assert data["retrieved_chunks"] == 1
        assert data["sources"][0]["source"] == "payment_policy.md"

    finally:
        app.dependency_overrides.clear()


def test_rag_query_returns_grounding_block():
    app.dependency_overrides[get_rag_service] = (
        lambda: FakeRAGService(blocked=True)
    )

    try:
        response = client.post(
            "/api/v1/rag/query",
            json={
                "question": (
                    "A customer says their payment was deducted "
                    "but the order was never created."
                )
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["grounding_blocked"] is True
        assert "follow the applicable refund procedure" in (
            data["grounding_violations"]
        )
        assert "fully supported" in data["answer"]

    finally:
        app.dependency_overrides.clear()


def test_rag_query_rejects_empty_question():
    app.dependency_overrides[get_rag_service] = (
        lambda: FakeRAGService(blocked=False)
    )

    try:
        response = client.post(
            "/api/v1/rag/query",
            json={"question": ""},

        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()