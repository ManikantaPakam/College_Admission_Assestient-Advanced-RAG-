from app.retrieval.query_rewriter import rewrite_query
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.reranker import rerank_documents

from app.retrieval.metadata_filter import (
    filter_documents_by_metadata
)

from app.generation.answer_generator import generate_answer


# --------------------------------------------------
# Feature 1: Advanced Retrieval Pipeline
# --------------------------------------------------

def advanced_retrieval_pipeline(
    question,
    top_k=5,
    top_n=3,
    metadata_filter=None
):

    # Step 1: Rewrite user question
    rewritten_query = rewrite_query(question)

    print("\nRewritten Query:")
    print(rewritten_query)

    # Step 2: Hybrid Search
    retrieved_documents = hybrid_search(
        rewritten_query,
        top_k=top_k
    )

    print("\nHybrid Search Results:")
    print(len(retrieved_documents))

    # Step 3: Metadata Filtering
    filtered_documents = filter_documents_by_metadata(
        retrieved_documents,
        metadata_filter
    )

    print("\nMetadata Filter:")
    print(metadata_filter)

    print("\nDocuments After Metadata Filtering:")
    print(len(filtered_documents))

    # Step 4: Cross-Encoder Reranking
    reranked_documents = rerank_documents(
        question,
        filtered_documents,
        top_n=top_n
    )

    print("\nDocuments After Reranking:")
    print(len(reranked_documents))

    return {
        "original_question": question,
        "rewritten_query": rewritten_query,
        "documents": reranked_documents
    }


# --------------------------------------------------
# Feature 2: Complete RAG Pipeline
# --------------------------------------------------

def run_rag_pipeline(
    question,
    metadata_filter=None
):

    # Step 1: Advanced Retrieval
    retrieval_result = advanced_retrieval_pipeline(
        question=question,
        top_k=5,
        top_n=3,
        metadata_filter=metadata_filter
    )

    documents = retrieval_result["documents"]

    # Step 2: Generate Answer + Sources
    result = generate_answer(
        question,
        documents
    )

    # Step 3: Return Final Response
    return {
        "original_question": question,
        "rewritten_query": retrieval_result["rewritten_query"],
        "answer": result["answer"],
        "sources": result["sources"]
    }