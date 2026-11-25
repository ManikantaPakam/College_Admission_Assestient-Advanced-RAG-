from langchain_chroma import Chroma
from app.core.config import CHROMA_DB_DIR, COLLECTION_NAME
from app.embeddings.embedding_model import get_embedding_model


def get_vector_store():
    embedding_model = get_embedding_model()
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DB_DIR)
    )
    return vector_store


def retrieve_documents(question, k=3):
    vector_store = get_vector_store()
    retrieved_docs = vector_store.similarity_search(
        query=question,
        k=k
    )
    return retrieved_docs


def retrieve_documents_with_scores(question, k=3):

    # Step 1: Get existing vector store
    vector_store = get_vector_store()

    # Step 2: Retrieve documents with distance scores
    results = vector_store.similarity_search_with_score(
        query=question,
        k=k
    )

    # Step 3: Display documents and scores
    for index, (document, score) in enumerate(results):

        print("\n-----------------------------")
        print(f"Document Rank: {index + 1}")

        print("\nDistance Score:", score)

        print("\nDocument Content:")
        print(document.page_content)

        print("\nMetadata:")
        print(document.metadata)

    return results