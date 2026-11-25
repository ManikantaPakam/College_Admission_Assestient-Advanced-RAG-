from app.retrieval.metadata_filter import (
    retrieve_with_metadata_filter
)


def test_metadata_filter():

    # Step 1: User question
    question = "What is the B.Tech CSE tuition fee?"

    # Step 2: Define metadata filter
    metadata_filter = {
        "category": "admission"
    }

    # Step 3: Retrieve filtered documents
    results = retrieve_with_metadata_filter(
        question=question,
        metadata_filter=metadata_filter,
        k=3
    )

    # Step 4: Verify results
    assert len(results) > 0

    # Step 5: Verify metadata
    for index, doc in enumerate(results):

        print("\n-------------------------")
        print(f"Rank: {index + 1}")

        print("\nContent:")
        print(doc.page_content)

        print("\nCategory:")
        print(doc.metadata.get("category"))

        assert doc.metadata.get("category") == "admission"