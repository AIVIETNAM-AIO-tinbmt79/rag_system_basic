from langchain_community.retrievers import (
    BM25Retriever
)

bm25_retriever = None

def build_bm25_retriever(
    chunks,
    k=5
):

    global bm25_retriever

    bm25_retriever = BM25Retriever.from_documents(
        chunks
    )

    bm25_retriever.k = k

    return bm25_retriever


def sparse_retrieve(query):

    if bm25_retriever is None:

        raise ValueError(
            "BM25 retriever has not been initialized"
        )

    docs = bm25_retriever.invoke(query)

    formatted_results = []

    for rank, doc in enumerate(docs):

        score = 1 / (rank + 1)

        formatted_results.append({
            "doc": doc,
            "score": score
        })

    return formatted_results