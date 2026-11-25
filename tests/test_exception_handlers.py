from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import chat


client = TestClient(
    app,
    raise_server_exceptions=False
)


def test_empty_question_validation():

    response = client.post(
        "/api/v1/chat",
        json={"question": ""}
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Validation Error"


def test_missing_question_validation():

    response = client.post(
        "/api/v1/chat",
        json={}
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Validation Error"


def test_global_exception_handler(monkeypatch):

    def mock_rag_pipeline(question):
        raise RuntimeError("Test exception")

    monkeypatch.setattr(
        chat,
        "run_rag_pipeline",
        mock_rag_pipeline
    )

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What are the hostel fees?"
        }
    )

    assert response.status_code == 500

    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Internal Server Error"