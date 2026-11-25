from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / 'data'


def load_pdf_documents():
    documents = []
    pdf_files = sorted(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {DATA_DIR}"
        )
    for pdf_file in pdf_files:
        print(f"Loading PDF: {pdf_file.name}")
        loader = PyPDFLoader(
            str(pdf_file)
            )
        pdf_documents = loader.load()
        for doc in pdf_documents:
            doc.metadata["source"] = pdf_file.name
            doc.metadata["category"] = (
                pdf_file.stem.split("_")[0]
            )
            doc.metadata["file_type"] = "pdf"
        documents.extend(pdf_documents)
        print(
            f"Successfully loaded {len(pdf_documents)} pages"
        )
    print(f"\nTotal pages loaded: {len(documents)}")

    return documents
