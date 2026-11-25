from langchain_community.retrievers import BM25Retriever

from app.ingestion.loader import load_pdf_documents
from app.ingestion.chunking import split_documents
from app.retrieval.retriever import get_vector_store


def create_bm25_retriever():

    # Step 1: Load documents
    documents = load_pdf_documents()

    # Step 2: Split documents into chunks
    chunks = split_documents(documents)

    # Step 3: Create BM25 retriever
    bm25_retriever = BM25Retriever.from_documents(
        documents=chunks,
        k=5
    )

    return bm25_retriever


def reciprocal_rank_fusion(
    semantic_results,
    bm25_results,
    k=60
):
    """
    Combine semantic and BM25 rankings using RRF.
    """

    fused_scores = {}
    documents = {}

    # Process Semantic Search results
    for rank, doc in enumerate(semantic_results, start=1):

        doc_id = doc.page_content

        fused_scores[doc_id] = fused_scores.get(doc_id, 0) + (
            1 / (k + rank)
        )

        documents[doc_id] = doc

    # Process BM25 Search results
    for rank, doc in enumerate(bm25_results, start=1):

        doc_id = doc.page_content

        fused_scores[doc_id] = fused_scores.get(doc_id, 0) + (
            1 / (k + rank)
        )

        documents[doc_id] = doc

    # Sort documents based on combined RRF score
    ranked_documents = sorted(
        fused_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        documents[doc_id]
        for doc_id, score in ranked_documents
    ]


def hybrid_search(question, top_k=3):

    vector_store = get_vector_store()

    # Step 2: Semantic Search
    semantic_results = vector_store.similarity_search(
        query=question,
        k=5
    )

    # Step 3: BM25 Search
    bm25_retriever = create_bm25_retriever()

    bm25_results = bm25_retriever.invoke(question)

    # Step 4: Combine both search results
    fused_results = reciprocal_rank_fusion(
        semantic_results=semantic_results,
        bm25_results=bm25_results
    )

    # Step 5: Return top relevant documents
    return fused_results[:top_k]