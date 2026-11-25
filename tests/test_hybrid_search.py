from app.retrieval.hybrid_search import hybrid_search


def test_hybrid_search():

    # Step 1: User question
    question = "What is the B.Tech CSE tuition fee?"

    # Step 2: Perform Hybrid Search
    results = hybrid_search(
        question=question,
        top_k=3
    )

    # Step 3: Verify results
    assert len(results) > 0

    # Step 4: Display results
    for index, doc in enumerate(results):

        print("\n-------------------------")
        print(f"Rank: {index + 1}")

        print("\nContent:")
        print(doc.page_content)

        print("\nMetadata:")
        print(doc.metadata)