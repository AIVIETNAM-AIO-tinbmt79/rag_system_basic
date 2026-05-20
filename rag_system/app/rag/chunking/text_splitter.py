from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_system_basic.rag_system.app.core.config import settings


def split_documents(
    docs
):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(
        docs
    )

    for idx, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = idx

    return chunks