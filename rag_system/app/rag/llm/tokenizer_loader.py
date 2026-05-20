from transformers import (
    AutoTokenizer
)

from rag_system_basic.rag_system.app.core.config import settings 


def load_tokenizer():

    tokenizer = AutoTokenizer.from_pretrained(
        settings.LLM_MODEL
    )

    return tokenizer