from rag_system_basic.rag_system.app.rag.retrieval.hybrid_search import (
    hybrid_search
)

from rag_system_basic.rag_system.app.rag.retrieval.reranker import (
    rerank_documents
)

from rag_system_basic.rag_system.app.rag.prompts.qa_prompt import (
    QA_PROMPT
)

from rag_system_basic.rag_system.app.rag.llm.inference import (
    generate_answer,
    generate_answer_stream
)

from rag_system_basic.rag_system.app.rag.chains.base_chain import (
    build_context
)

from rag_system_basic.rag_system.app.core.config import settings


def _build_prompt(query):
    """Shared retrieval + rerank + prompt building."""
    retrieved_docs = hybrid_search(
        query=query,
        final_k=settings.TOP_K_RETRIEVAL
    )

    retrieved_docs = [
        item["doc"]
        for item in retrieved_docs
    ]

    reranked_docs = rerank_documents(
        query=query,
        docs=retrieved_docs,
        top_k=settings.TOP_K_RERANK
    )

    context = build_context(reranked_docs)

    prompt = QA_PROMPT.format(
        context=context,
        question=query
    )

    return prompt, reranked_docs


def run_qa_chain(query):

    prompt, reranked_docs = _build_prompt(query)

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "documents": reranked_docs
    }


def run_qa_chain_stream(query):
    """Yields tokens one by one. Documents are retrieved first (blocking),
    then answer tokens stream in real time."""

    prompt, _ = _build_prompt(query)

    yield from generate_answer_stream(prompt)