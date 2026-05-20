def build_citations(
    docs
):

    citations = []

    for idx, doc in enumerate(docs, start=1):

        citations.append({
            "id": idx,
            "source": doc.metadata.get(
                "source",
                "Unknown"
            ),
            "content": doc.page_content[:300]
        })

    return citations