from collections import defaultdict

from rag_system_basic.rag_system.app.rag.retrieval.retriever import (
    dense_retrieve
)

from rag_system_basic.rag_system.app.rag.retrieval.bm25_retriever import (
    sparse_retrieve
)

from rag_system_basic.rag_system.app.core.config import settings


ALPHA = settings.ALPHA

BETA = settings.BETA


def hybrid_search(
    query,
    final_k=settings.TOP_K_RETRIEVAL
):

    dense_results = dense_retrieve(
        query=query,
        k=settings.TOP_K_RETRIEVAL
    )

    sparse_results = sparse_retrieve(
        query=query
    )

    hybrid_scores = defaultdict(float)

    doc_mapping = {}

    # =========================
    # Dense Retrieval
    # =========================

    for item in dense_results:

        doc = item["doc"]

        dense_score = item["score"]

        chunk_id = doc.metadata["chunk_id"]

        dense_similarity = 1 / (
            1 + dense_score
        )

        hybrid_scores[chunk_id] += (
            ALPHA * dense_similarity
        )

        doc_mapping[chunk_id] = doc

    # =========================
    # Sparse Retrieval
    # =========================

    for item in sparse_results:

        doc = item["doc"]

        sparse_score = item["score"]

        chunk_id = doc.metadata["chunk_id"]

        hybrid_scores[chunk_id] += (
            BETA * sparse_score
        )

        doc_mapping[chunk_id] = doc

    sorted_results = sorted(
        hybrid_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    final_docs = []

    for chunk_id, final_score in sorted_results[:final_k]:

        final_docs.append({
            "doc": doc_mapping[chunk_id],
            "score": final_score
        })

    return final_docs