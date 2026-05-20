from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # =========================
    # APP
    # =========================

    APP_NAME: str = "Business RAG System"

    DEBUG: bool = True

    # =========================
    # DATABASE
    # =========================

    DATABASE_URL: str

    # =========================
    # JWT
    # =========================

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # =========================
    # EMBEDDING
    # =========================

    EMBED_MODEL: str

    # =========================
    # CHUNKING
    # =========================

    CHUNK_SIZE: int = 1000

    CHUNK_OVERLAP: int = 200

    # =========================
    # LLM
    # =========================

    LLM_MODEL: str

    MAX_NEW_TOKENS: int = 512

    TEMPERATURE: float = 0

    RERANK_MODEL: str

    # =========================
    # VECTOR DB
    # =========================

    CHROMA_DB_PATH: str

    # =========================
    # FILES
    # =========================

    UPLOAD_DIR: str = "data/uploads"

    RAW_DATA_DIR: str = "data/raw"

    PROCESSED_DATA_DIR: str = "data/processed"

    # =========================
    # RETRIEVAL
    # =========================

    TOP_K_RETRIEVAL: int = 10

    TOP_K_RERANK: int = 5

    ALPHA: float = 0.7

    BETA: float = 0.3

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()