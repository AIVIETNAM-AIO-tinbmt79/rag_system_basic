def build_context(
    docs,
    separator="\n\n"
):

    return separator.join([
        doc.page_content
        for doc in docs
    ])