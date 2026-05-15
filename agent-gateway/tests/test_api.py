from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_endpoint() -> None:
    client = TestClient(app)
    response = client.post(
        "/chat",
        json={"message": "What is the refund policy?", "session_id": "test-1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["session_id"] == "test-1"
    assert data["intent"] == "knowledge_search"


def test_session_management() -> None:
    client = TestClient(app)

    response = client.post(
        "/chat",
        json={"message": "Hello", "session_id": "test-sess"},
    )
    assert response.status_code == 200

    response = client.get("/api/sessions")
    assert response.status_code == 200
    assert "test-sess" in response.json()["sessions"]

    response = client.delete("/api/sessions/test-sess")
    assert response.status_code == 200
