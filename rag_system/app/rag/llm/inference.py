import torch
from threading import Thread
from transformers import TextIteratorStreamer

from rag_system_basic.rag_system.app.rag.llm.generator import (
    model,
    tokenizer
)

from rag_system_basic.rag_system.app.core.config import settings


def generate_answer(
    prompt,
    max_new_tokens=512
):
    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            temperature = settings.TEMPERATURE
        )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return response


def generate_answer_stream(
    prompt,
    max_new_tokens=512
):
    """Generator that yields tokens one by one for streaming."""
    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True
    )

    generation_kwargs = dict(
        **inputs,
        streamer=streamer,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
        temperature = settings.TEMPERATURE
    )

    # Run generation in background thread so we can stream
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    for token in streamer:
        yield token

    thread.join()