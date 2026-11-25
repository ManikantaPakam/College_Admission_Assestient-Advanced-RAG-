from app.generation.answer_generator import extract_sources
from langchain_core.documents import Document


def test_extract_sources():

    documents = [
        Document(
            page_content="Hostel fee is Rs. 80,000.",
            metadata={
                "source": "admission_policy.pdf",
                "page": 0,
                "category": "admission"
            }
        ),
        Document(
            page_content="Hostel accommodation details.",
            metadata={
                "source": "admission_policy.pdf",
                "page": 0,
                "category": "admission"
            }
        )
    ]

    sources = extract_sources(documents)

    print("\nExtracted Sources:")
    print(sources)

    assert len(sources) == 1
    assert sources[0]["file"] == "admission_policy.pdf"
    assert sources[0]["page"] == 0