from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set dummy environment variables for tests to avoid Pydantic validation errors."""
    monkeypatch.setenv("QDRANT_URL", "https://localhost:6333")
    monkeypatch.setenv("QDRANT_API_KEY_RO", "dummy-key")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")


@pytest.fixture(autouse=True)
def reset_config_cache() -> Generator[None]:
    from qdrant.config import get_settings
    from qdrant.main import get_openai_client, get_qdrant_client

    get_settings.cache_clear()
    get_openai_client.cache_clear()
    get_qdrant_client.cache_clear()
    yield
    get_settings.cache_clear()
    get_openai_client.cache_clear()
    get_qdrant_client.cache_clear()


@pytest.fixture
def mock_qdrant_client() -> Generator[MagicMock]:
    with patch("qdrant.main.get_qdrant_client") as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_openai_client() -> Generator[MagicMock]:
    with patch("qdrant.main.get_openai_client") as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client
