from transformers import AutoTokenizer

from rag_system_basic.rag_system.app.core.config import settings


tokenizer = AutoTokenizer.from_pretrained(
    settings.LLM_MODEL
)


def count_tokens(
    text
):

    return len(
        tokenizer.encode(text)
    )