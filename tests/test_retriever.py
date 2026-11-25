from app.retrieval.retriever import retrieve_documents


def test_retrieve_documents():
    question = "explain scholarship policyes?"
    retrieved_docs = retrieve_documents(
        question=question,
        k=1
    )
    assert len(retrieved_docs) > 0

    for index, doc in enumerate(retrieved_docs):

        print("\n--------------------------")
        print(f"Retrieved Document: {index + 1}")

        print("\nContent:")
        print(doc.page_content)

        print("\nMetadata:")
        print(doc.metadata)