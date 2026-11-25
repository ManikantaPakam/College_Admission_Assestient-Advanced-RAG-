from app.retrieval.retriever import retrieve_documents_with_scores


def test_similarity_scores():

    # Step 1: User question
    question = "What is the B.Tech CSE tuition fee?"

    # Step 2: Retrieve documents with scores
    results = retrieve_documents_with_scores(
        question=question,
        k=3
    )

    # Step 3: Verify results
    assert len(results) > 0

    # Step 4: Verify scores
    for document, score in results:

        assert isinstance(score, (int, float))

        print("\nScore Type:", type(score))