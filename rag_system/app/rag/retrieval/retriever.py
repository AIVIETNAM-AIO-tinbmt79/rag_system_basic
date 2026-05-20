from rag_system_basic.rag_system.app.rag.vectorstore.chroma_store import (
    get_vector_store
)

from rag_system_basic.rag_system.app.core.config import settings


vector_store = get_vector_store()


def dense_retrieve(
    query,
    k=settings.TOP_K_RETRIEVAL
):

    results = vector_store.similarity_search_with_score(
        query=query,
        k=k
    )

    formatted_results = []

    for doc, score in results:

        formatted_results.append({
            "doc": doc,
            "score": score
        })

    return formatted_results