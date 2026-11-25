from app.generation.llm import get_llm
from app.generation.prompts import RAG_PROMPT



def extract_answer_text(content):

    # Case 1: Gemini returns normal string
    if isinstance(content, str):
        return content

    # Case 2: Gemini returns list of content blocks
    if isinstance(content, list):

        text_parts = []

        for block in content:

            if isinstance(block, dict):

                if block.get("type") == "text":
                    text_parts.append(block.get("text", ""))

            elif isinstance(block, str):
                text_parts.append(block)

        return "\n".join(text_parts).strip()

    raise TypeError(
        f"Unsupported Gemini response content type: {type(content)}"
    )


# --------------------------------------------------
# Feature 1: Prepare Context
# --------------------------------------------------

def prepare_context(documents):

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context


# --------------------------------------------------
# Feature 2: Extract Source Information
# --------------------------------------------------

def extract_sources(documents):

    sources = []

    for document in documents:

        source = {
            "file": document.metadata.get("source"),
            "page": document.metadata.get("page"),
            "category": document.metadata.get("category")
        }

        if source not in sources:
            sources.append(source)

    return sources


# --------------------------------------------------
# Feature 3: Generate Answer with Sources
# --------------------------------------------------

def generate_answer(question, documents):

    context = prepare_context(documents)

    llm = get_llm()

    prompt = RAG_PROMPT.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(prompt)

    answer = extract_answer_text(
    response.content
    )

    sources = extract_sources(documents)

    return {
        "answer": answer,
        "sources": sources
    }