from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_qdrant_client() -> Generator[MagicMock]:
    with patch("qdrant.main.qdrant_client", new_callable=MagicMock) as mock:
        yield mock


@pytest.fixture
def mock_openai_client() -> Generator[MagicMock]:
    with patch("qdrant.main.openai_client", new_callable=MagicMock) as mock:
        yield mock
