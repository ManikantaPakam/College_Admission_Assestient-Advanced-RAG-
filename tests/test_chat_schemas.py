from app.api.schemas.chat import ChatRequest, ChatResponse


def test_chat_request():
    request = ChatRequest(
        question="What are the hostel fees?"
    )

    assert request.question == "What are the hostel fees?"


def test_chat_response():
    response = ChatResponse(
        question="What are the hostel fees?",
        rewritten_query="College hostel fees and accommodation",
        answer="Hostel fee is Rs. 80,000 per year.",
        sources=[
            {
                "file": "admission_policy.pdf",
                "page": 1,
                "category": "admission"
            }
        ]
    )

    assert response.answer == "Hostel fee is Rs. 80,000 per year."
    assert len(response.sources) == 1