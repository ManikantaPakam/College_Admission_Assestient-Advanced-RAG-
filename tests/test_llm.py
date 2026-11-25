from app.generation.llm import get_llm

def test_gemini_llm():

    llm = get_llm()

    response = llm.invoke(
        "Explain RAG in one sentence."
    )

    print("\nGemini Response:")
    print(response.content)

    assert response.content