from app.ingestion.loader import load_pdf_documents
from app.ingestion.chunking import split_documents


def test_document_chunking():
    documents = load_pdf_documents()
    chunks = split_documents(documents)
    assert len(chunks) > 0
    for index, chunk in enumerate(chunks):
        print("\n---------------------------")
        print(f"Chunk: {index + 1}")
        print("\nChunk Content:")
        print(chunk.page_content)
        print("\nChunk Metadata:")
        print(chunk.metadata)