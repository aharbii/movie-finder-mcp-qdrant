import pytest
from pydantic import ValidationError

from qdrant.config import RAGConfig


def test_rag_config_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that RAGConfig accepts valid environment variables via monkeypatch."""
    monkeypatch.setenv("QDRANT_URL", "http://test-qdrant:6333")
    monkeypatch.setenv("QDRANT_API_KEY_RO", "test-qdrant-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("QDRANT_COLLECTION_NAME", "custom-collection")

    config = RAGConfig()

    assert config.qdrant_url == "http://test-qdrant:6333"
    assert config.qdrant_api_key_ro == "test-qdrant-key"
    assert config.openai_api_key == "test-openai-key"
    assert config.qdrant_collection_name == "custom-collection"


def test_rag_config_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that RAGConfig uses the correct default values when optional vars are missing."""
    monkeypatch.setenv("QDRANT_URL", "http://test-qdrant:6333")
    monkeypatch.setenv("QDRANT_API_KEY_RO", "test-qdrant-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")

    # We must explicitly delete the env vars that might exist in the local .env
    # so we can strictly test the Pydantic default fallback logic.
    monkeypatch.delenv("QDRANT_COLLECTION_NAME", raising=False)
    monkeypatch.delenv("OPENAI_EMBEDDING_MODEL", raising=False)

    # Pass _env_file=None to ignore any local .env file created by `make dev`
    config = RAGConfig(_env_file=None)

    assert config.qdrant_collection_name == "text-embedding-3-large"
    assert config.openai_embedding_model == "text-embedding-3-large"


def test_rag_config_missing_required(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that RAGConfig raises ValidationError if required vars are missing."""
    monkeypatch.delenv("QDRANT_URL", raising=False)
    monkeypatch.delenv("QDRANT_API_KEY_RO", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValidationError):
        # We pass _env_file=None to bypass the local .env file
        RAGConfig(_env_file=None)
