from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RAGConfig(BaseSettings):
    """
    MCP Server configuration manged by Pydantic
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Qdrant Cloud
    qdrant_url: str = Field(..., validation_alias="QDRANT_URL")
    qdrant_api_key_ro: str = Field(..., validation_alias="QDRANT_API_KEY_RO")
    vector_store_target_name: str = Field(
        "movies_text_embedding_3_large_3072", validation_alias="VECTOR_STORE_TARGET_NAME"
    )

    # OpenAI
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")
    openai_embedding_model: str = Field(
        "text-embedding-3-large", validation_alias="OPENAI_EMBEDDING_MODEL"
    )


@lru_cache(maxsize=1)
def get_settings() -> RAGConfig:
    """Return the singleton RAGConfig (cached after first call)."""
    return RAGConfig()
