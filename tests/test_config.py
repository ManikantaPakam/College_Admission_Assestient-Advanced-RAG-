from app.core.config import (
    GOOGLE_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_DB_DIR,
    COLLECTION_NAME
)


def test_configuration():

    assert GOOGLE_API_KEY
    assert EMBEDDING_MODEL
    assert CHROMA_DB_DIR
    assert COLLECTION_NAME

    print("\nEmbedding Model:", EMBEDDING_MODEL)

    print("\nChromaDB Directory:", CHROMA_DB_DIR)

    print("\nCollection Name:", COLLECTION_NAME)