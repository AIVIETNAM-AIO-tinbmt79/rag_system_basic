from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from rag_system_basic.rag_system.app.core.config import settings

COLLECTION_NAME = "rag_documents"

embedding_function = HuggingFaceEmbeddings(
    model_name=settings.EMBED_MODEL,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


def create_vector_store(chunks):

    if not chunks:
        raise ValueError("No chunks provided to create_vector_store.")

    # Filter out empty-content chunks
    valid_chunks = [c for c in chunks if c.page_content.strip()]

    if not valid_chunks:
        raise ValueError(
            "All chunks are empty after filtering. "
            "Check your document loader or text splitter."
        )

    vector_store = Chroma.from_documents(
        documents=valid_chunks,
        embedding=embedding_function,
        persist_directory=settings.CHROMA_DB_PATH,
        collection_name=COLLECTION_NAME,
    )

    return vector_store


def get_vector_store():

    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embedding_function,
        collection_name=COLLECTION_NAME,
    )

    return vector_store