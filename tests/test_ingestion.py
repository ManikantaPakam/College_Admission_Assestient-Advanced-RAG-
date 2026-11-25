from app.ingestion.loader import load_pdf_documents


def test_pdf_loading():
    documents = load_pdf_documents()
    assert len(documents) > 0
    for index, doc in enumerate(documents):
        print("\n---------------------------")
        print(f"Document: {index + 1}")
        print("\nPage Content:")
        print(doc.page_content)
        print("\nMetadata:")
        print(doc.metadata)


if __name__ == "__main__":

    test_pdf_loading()