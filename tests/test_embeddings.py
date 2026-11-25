from app.embeddings.embedding_model import get_embedding_model


def test_embedding_generation():
    embedding_model = get_embedding_model()
    text = "What is the admission fee?"
    vector = embedding_model.embed_query(text)
    assert len(vector) > 0

    print("\nEmbedding Dimensions:", len(vector))

    print("\nFirst 10 Values:")
    print(vector[:10])