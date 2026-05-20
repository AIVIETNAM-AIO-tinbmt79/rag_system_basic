from rag_system_basic.rag_system.app.rag.chunking.text_splitter import (
    split_documents
)

from rag_system_basic.rag_system.app.rag.vectorstore.chroma_store import (
    create_vector_store,
    get_vector_store
)

from rag_system_basic.rag_system.app.rag.retrieval.bm25_retriever import (
    build_bm25_retriever
)

from rag_system_basic.rag_system.app.rag.loaders.documents_loader import loaders
from rag_system_basic.rag_system.app.core.config import settings


def rebuild_bm25_on_startup():
    """Rebuild BM25 retriever from existing uploaded documents on app startup."""
    try:
        documents = loaders(settings.UPLOAD_DIR)
        if documents:
            from rag_system_basic.rag_system.app.rag.chunking.text_splitter import split_documents
            chunks = split_documents(documents)
            build_bm25_retriever(chunks)
    except Exception:
        pass  # No documents yet, BM25 stays None until first upload



def indexing_pipeline(
    documents
):
    if not documents:
        raise ValueError("No documents were loaded. Check the uploaded file.")

    # =========================
    # Chunking
    # =========================

    chunks = split_documents(documents)

    if not chunks:
        raise ValueError(
            f"Splitting produced 0 chunks from {len(documents)} document(s). "
            "The file may be empty, scanned-only, or unsupported."
        )

    # Filter empty chunks before indexing
    chunks = [c for c in chunks if c.page_content.strip()]

    if not chunks:
        raise ValueError(
            "All chunks are empty after filtering. "
            "The document may contain only images or non-extractable content."
        )

    # =========================
    # Vector Store
    # =========================

    vector_store = create_vector_store(
        chunks
    )

    # =========================
    # BM25
    # =========================

    build_bm25_retriever(
        chunks
    )

    return {
        "status": "success",
        "num_documents": len(documents),
        "num_chunks": len(chunks)
    }