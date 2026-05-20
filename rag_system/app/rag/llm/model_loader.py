from transformers import (
    AutoModelForCausalLM
)

from rag_system_basic.rag_system.app.core.config import settings


def load_model():

    model = AutoModelForCausalLM.from_pretrained(
        settings.LLM_MODEL,
        device_map="auto",
        torch_dtype="auto"
    )

    return model