from fastapi.testclient import TestClient

from simple_agent.server import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invocations_contract() -> None:
    response = client.post("/invocations", json={"message": "What tier is $225/night?"})
    assert response.status_code == 200
    body = response.json()
    assert "Premium" in body["answer"]
    assert body["tool_calls"] == 1
    assert body["backend"] == "fake"
    assert body["request_id"]
    assert body["latency_ms"] >= 0


def test_empty_message_rejected() -> None:
    response = client.post("/invocations", json={"message": ""})
    assert response.status_code == 422
