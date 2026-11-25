from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import chat


client = TestClient(app, raise_server_exceptions=False)


def mock_rag_pipeline(question):

    return {
        "original_question": question,
        "rewritten_query": question,
        "answer": "Test answer",
        "sources": []
    }


def test_rate_limit_exceeded(monkeypatch):

    # Mock RAG pipeline to avoid Gemini API calls
    monkeypatch.setattr(
        chat,
        "run_rag_pipeline",
        mock_rag_pipeline
    )

    # Reset rate limiter storage for isolated test
    app.state.limiter.reset()

    responses = []

    # Send 6 requests
    for _ in range(6):

        response = client.post(
            "/api/v1/chat",
            json={
                "question": "What are the hostel fees?"
            }
        )

        responses.append(response.status_code)

    # First 5 requests should succeed
    assert responses[:5] == [200, 200, 200, 200, 200]

    # Sixth request should be rate limited
    assert responses[5] == 429