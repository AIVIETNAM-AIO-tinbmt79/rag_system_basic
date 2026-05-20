from rag_system_basic.rag_system.app.rag.retrieval.hybrid_search import (
    hybrid_search
)

from rag_system_basic.rag_system.app.rag.chains.summarize_chain import (
    run_summary_chain
)


def summarize_documents(
    query,
    top_k=10
):

    retrieved_results = hybrid_search(
        query=query,
        final_k=top_k
    )

    docs = [
        item["doc"]
        for item in retrieved_results
    ]

    summary = run_summary_chain(
        docs
    )

    return {
        "summary": summary
    }