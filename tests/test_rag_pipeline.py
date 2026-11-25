from app.rag.pipeline import advanced_retrieval_pipeline


def test_advanced_retrieval_pipeline():

    # Step 1: User question
    question = "What about hostel?"

    # Step 2: Metadata filter
    metadata_filter = {
        "category": "admission"
    }

    # Step 3: Execute complete retrieval pipeline
    result = advanced_retrieval_pipeline(
        question=question,
        top_k=5,
        top_n=3,
        metadata_filter=metadata_filter
    )

    # Step 4: Validate output
    assert result is not None

    assert result["original_question"] == question

    assert isinstance(
        result["rewritten_query"],
        str
    )

    assert len(result["documents"]) <= 3

    # Step 5: Display final results
    print("\nOriginal Question:")
    print(result["original_question"])

    print("\nRewritten Query:")
    print(result["rewritten_query"])

    print("\nFinal Retrieved Documents:")

    for index, document in enumerate(
        result["documents"],
        start=1
    ):
        print(f"\nRank: {index}")
        print(document.page_content)


from app.rag.pipeline import run_rag_pipeline


def test_complete_rag_pipeline():

    question = "What is the hostel fee?"

    result = run_rag_pipeline(question)

    print("\nFinal RAG Response:")
    print(result)

    # Validate answer
    assert result["answer"]

    # Validate sources
    assert isinstance(result["sources"], list)