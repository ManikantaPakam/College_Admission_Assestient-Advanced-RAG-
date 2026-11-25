from app.ingestion.loader import load_pdf_documents
from app.ingestion.chunking import split_documents
from app.ingestion.ingest import create_vector_store


def test_create_vector_store():
    documents = load_pdf_documents()
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks)
    assert vector_store is not None
    total_records = vector_store._collection.count()

    print("\nTotal records in ChromaDB:", total_records)

    assert total_records > 0