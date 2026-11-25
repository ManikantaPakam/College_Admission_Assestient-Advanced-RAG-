
from app.generation.prompts import RAG_PROMPT

def test_rag_prompt():

    formatted_prompt = RAG_PROMPT.format(
        context="Hostel fee is Rs. 80,000 per year.",
        question="What is the hostel fee?"
    )

    print("\nFormatted Prompt:")
    print(formatted_prompt)

    assert "Hostel fee is Rs. 80,000 per year." in formatted_prompt
    assert "What is the hostel fee?" in formatted_prompt