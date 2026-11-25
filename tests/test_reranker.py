from app.retrieval.retriever import retrieve_documents
from app.retrieval.reranker import rerank_documents


def test_reranking():

    # Step 1: User Question
    question = "What is the hostel fee?"

    # Step 2: Retrieve documents
    documents = retrieve_documents(
        question,
        k=5
    )

    # Step 3: Rerank documents
    reranked_documents = rerank_documents(
        question,
        documents,
        top_n=3
    )

    # Step 4: Validate results
    assert len(reranked_documents) <= 3
    assert all(
        isinstance(doc.page_content, str)
        for doc in reranked_documents
    )

    # Step 5: Display results
    print("\nOriginal Question:")
    print(question)

    print("\nReranked Documents:")

    for index, document in enumerate(
        reranked_documents,
        start=1
    ):
        print(f"\nRank: {index}")
        print(document.page_content)