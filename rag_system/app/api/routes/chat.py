from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.responses import StreamingResponse
import json

from rag_system_basic.rag_system.app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    SourceResponse
)

from rag_system_basic.rag_system.app.core.security import (
    get_current_user
)

from rag_system_basic.rag_system.app.rag.chains.qa_chain import (
    run_qa_chain,
    run_qa_chain_stream
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    current_user=Depends(
        get_current_user
    )
):

    try:

        result = run_qa_chain(
            query=request.query
        )

        answer = result["answer"]

        documents = result["documents"]

        sources = []

        for doc in documents:

            sources.append(
                SourceResponse(
                    content=doc.page_content[:300],
                    source=doc.metadata.get(
                        "source",
                        "Unknown"
                    ),
                    score=doc.metadata.get(
                        "score"
                    )
                )
            )

        return ChatResponse(
            answer=answer,
            sources=sources
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/stream")
def chat_stream(
    request: ChatRequest,
    current_user=Depends(get_current_user)
):
    """Streaming endpoint — yields tokens as they are generated."""

    def event_stream():
        try:
            for chunk in run_qa_chain_stream(query=request.query):
                # Send each token as SSE
                data = json.dumps({"token": chunk})
                yield f"data: {data}\n\n"
            # Signal completion
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )