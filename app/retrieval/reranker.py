from sentence_transformers import CrossEncoder


# Step 1: Load Cross-Encoder Model
def get_reranker_model():

    model = CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    return model


# Step 2: Rerank Retrieved Documents
def rerank_documents(question, documents, top_n=3):

    # Check whether documents are available
    if not documents:
        return []

    # Load Cross-Encoder model
    reranker = get_reranker_model()

    # Prepare question-document pairs
    pairs = [
        (question, document.page_content)
        for document in documents
    ]

    # Generate relevance scores
    scores = reranker.predict(pairs)

    # Combine documents with their scores
    scored_documents = list(zip(documents, scores))

    # Sort documents based on relevance score
    ranked_documents = sorted(
        scored_documents,
        key=lambda item: float(item[1]),
        reverse=True
    )

    # Select top N documents
    top_documents = [
        document
        for document, score in ranked_documents[:top_n]
    ]

    return top_documents