# Embedding model wrapper placeholder
from rag_system_basic.rag_system.app.core.config import settings
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    settings.EMBED_MODEL
)

def get_embedding_model():
    return embedding_model