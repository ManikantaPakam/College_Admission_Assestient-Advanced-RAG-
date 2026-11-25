from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import chat


client = TestClient(app)


# Test 1: Valid Chat Request
def test_chat_api_success(monkeypatch):

    def mock_rag_pipeline(question):
        return {
            "original_question": question,
            "rewritten_query": "College hostel fees and accommodation",
            "answer": "Hostel fee is Rs. 80,000 per year.",
            "sources": [
                {
                    "file": "admission_policy.pdf",
                    "page": 0,
                    "category": "admission"
                }
            ]
        }

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

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "Hostel fee is Rs. 80,000 per year."
    assert data["rewritten_query"] == "College hostel fees and accommodation"
    assert len(data["sources"]) == 1


# Test 2: Empty Question
def test_chat_api_empty_question():

    response = client.post(
        "/api/v1/chat",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


# Test 3: Short Question
def test_chat_api_short_question():

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "Hi"
        }
    )

    assert response.status_code == 422


# Test 4: Missing Question
def test_chat_api_missing_question():

    response = client.post(
        "/api/v1/chat",
        json={}
    )

    assert response.status_code == 422


# Test 5: RAG Pipeline Failure
def test_chat_api_pipeline_failure(monkeypatch):

    def mock_rag_pipeline(question):
        raise RuntimeError("Test pipeline failure")

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

    assert response.json()["detail"] == (
        "RAG pipeline error: Test pipeline failure"
    )