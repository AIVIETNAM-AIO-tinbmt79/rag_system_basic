from fastapi import FastAPI

from rag_system_basic.rag_system.app.api.routes import (
    upload
)

from rag_system_basic.rag_system.app.database.session import (
    engine
)

from rag_system_basic.rag_system.app.database.models import Base

from rag_system_basic.rag_system.app.services.indexing_service import rebuild_bm25_on_startup
from rag_system_basic.rag_system.app.api.routes import auth, chat, health


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Business RAG API"
)


@app.on_event("startup")
def on_startup():
    rebuild_bm25_on_startup()


app.include_router(
    health.router
)

app.include_router(
    auth.router
)

app.include_router(
    upload.router
)

app.include_router(
    chat.router
)