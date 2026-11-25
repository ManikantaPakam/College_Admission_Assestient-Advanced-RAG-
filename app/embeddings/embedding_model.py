from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import EMBEDDING_MODEL


def get_embedding_model():
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    return embedding_model