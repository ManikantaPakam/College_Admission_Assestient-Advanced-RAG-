from langchain_chroma import Chroma
from app.core.config import CHROMA_DB_DIR, COLLECTION_NAME
from app.embeddings.embedding_model import get_embedding_model


def create_vector_store(chunks):
    embedding_model = get_embedding_model()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DB_DIR)
    )
    print(f"Successfully stored {len(chunks)} chunks in ChromaDB")

    return vector_store