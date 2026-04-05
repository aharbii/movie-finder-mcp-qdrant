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
    qdrant_collection_name: str = Field(
        "text-embedding-3-large", validation_alias="QDRANT_COLLECTION_NAME"
    )

    # OpenAI
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")
    openai_embedding_model: str = Field(
        "text-embedding-3-large", validation_alias="OPENAI_EMBEDDING_MODEL"
    )


settings = RAGConfig()
