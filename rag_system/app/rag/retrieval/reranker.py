from sentence_transformers import (
    CrossEncoder
)

from rag_system_basic.rag_system.app.core.config import settings


reranker_model = CrossEncoder(
    settings.RERANK_MODEL
)


def rerank_documents(
    query,
    docs,
    top_k=settings.TOP_K_RERANK
):

    if len(docs) == 0:
        return []

    pairs = []

    for doc in docs:

        pairs.append([
            query,
            doc.page_content
        ])

    scores = reranker_model.predict(
        pairs
    )

    scored_docs = list(
        zip(docs, scores)
    )

    scored_docs.sort(
        key=lambda x: x[1],
        reverse=True
    )

    final_docs = [
        doc
        for doc, score in scored_docs[:top_k]
    ]

    return final_docs