
from functools import lru_cache
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY

# --------------------------------------------------
# Feature 1: Gemini LLM Initialization
# --------------------------------------------------

@lru_cache(maxsize=1)
def get_llm():

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )

    return llm