from app.retrieval.query_rewriter import rewrite_query


def test_query_rewriting():

    # Step 1: Original user question
    question = "What about hostel?"

    # Step 2: Rewrite query
    rewritten_query = rewrite_query(question)

    # Step 3: Verify response
    assert rewritten_query
    assert isinstance(rewritten_query, str)

    # Step 4: Display results
    print("\nOriginal Question:")
    print(question)

    print("\nRewritten Query:")
    print(rewritten_query)