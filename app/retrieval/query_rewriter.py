from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY


def get_llm():

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )

    return llm


def rewrite_query(question):

    # Step 1: Initialize LLM
    llm = get_llm()

    # Step 2: Create prompt
    prompt = f"""
    You are an expert search query optimizer.

    Rewrite the following user question into a clear,
    standalone search query for a college admission
    knowledge base.

    Preserve the original meaning.
    Do not answer the question.
    Return only the rewritten query.

    User Question:
    {question}
    """

    # Step 3: Generate rewritten query
    response = llm.invoke(prompt)

    # Step 4: Extract response content
    content = response.content

    if isinstance(content, list):
        rewritten_query = " ".join(
            item["text"] if isinstance(item, dict) else str(item)
            for item in content
        ).strip()
    else:
        rewritten_query = content.strip()

    return rewritten_query