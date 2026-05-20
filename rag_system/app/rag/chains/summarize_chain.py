from rag_system_basic.rag_system.app.rag.prompts.summary_prompt import (
    SUMMARY_PROMPT
)

from rag_system_basic.rag_system.app.rag.llm.inference import (
    generate_answer
)

from rag_system_basic.rag_system.app.rag.chains.base_chain import (
    build_context
)


def run_summary_chain(
    docs
):

    context = build_context(
        docs
    )

    prompt = SUMMARY_PROMPT.format(
        context=context
    )

    summary = generate_answer(
        prompt
    )

    return summary