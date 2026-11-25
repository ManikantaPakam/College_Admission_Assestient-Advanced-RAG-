from app.retrieval.retriever import get_vector_store


def retrieve_with_metadata_filter(
    question,
    metadata_filter,
    k=3
):
    """
    Retrieve documents using metadata filtering.
    """

    # Step 1: Get existing vector store
    vector_store = get_vector_store()

    # Step 2: Perform metadata-filtered search
    retrieved_docs = vector_store.similarity_search(
        query=question,
        k=k,
        filter=metadata_filter
    )
    return retrieved_docs


def matches_metadata_filter(metadata, metadata_filter):

    if not metadata_filter:
        return True

    for key, value in metadata_filter.items():

        # Handle AND condition
        if key == "$and":
            if not all(
                matches_metadata_filter(metadata, condition)
                for condition in value
            ):
                return False

        # Handle OR condition
        elif key == "$or":
            if not any(
                matches_metadata_filter(metadata, condition)
                for condition in value
            ):
                return False

        # Handle normal key-value condition
        elif metadata.get(key) != value:
            return False

    return True


def filter_documents_by_metadata(documents, metadata_filter):

    filtered_documents = []

    for document in documents:

        if matches_metadata_filter(
            document.metadata,
            metadata_filter
        ):
            filtered_documents.append(document)

    return filtered_documents