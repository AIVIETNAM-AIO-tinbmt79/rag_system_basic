from rag_system_basic.rag_system.app.rag.chains.qa_chain import (
    run_qa_chain
)

from rag_system_basic.rag_system.app.rag.chains.citation_chain import (
    build_citations
)


def process_chat(
    query
):

    result = run_qa_chain(
        query=query
    )

    citations = build_citations(
        result["documents"]
    )

    return {
        "answer": result["answer"],
        "citations": citations
    }