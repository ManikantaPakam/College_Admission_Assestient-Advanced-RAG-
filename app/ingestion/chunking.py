from langchain_text_splitters import RecursiveCharacterTextSplitter


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Original documents: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")

    return chunks