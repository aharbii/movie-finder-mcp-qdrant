from unittest.mock import MagicMock, patch

import pytest
from qdrant_client.http.models import Record, ScoredPoint

from qdrant.main import (
    compare_cosine_similarity,
    embed_text,
    filtered_search,
    get_collection_status,
    get_movie_data,
    get_openai_client,
    get_qdrant_client,
    get_similar_movies_by_title,
    qdrant_search,
    scroll_movies_by_director,
)


def test_factory_functions_coverage() -> None:
    """Cover the return statements of the factory functions by mocking classes."""
    with patch("qdrant.main.OpenAI") as mock_openai_cls:
        qdrant_client = get_openai_client()
        assert qdrant_client is mock_openai_cls.return_value

    with patch("qdrant.main.QdrantClient") as mock_qdrant_cls:
        openai_client = get_qdrant_client()
        assert openai_client is mock_qdrant_cls.return_value


def test_get_similar_movies_missing_plot_coverage(mock_qdrant_client: MagicMock) -> None:
    """Cover the 'if not movie_plot' return statement."""
    mock_qdrant_client.scroll.return_value = (
        [Record(id=1, payload={"title": "No Plot Movie"}, vector=None, shard_key=None)],
        None,
    )
    result = get_similar_movies_by_title("No Plot Movie")
    assert result == []


def test_embed_text(mock_openai_client: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    mock_openai_client.embeddings.create.return_value = mock_response

    result = embed_text("hello world")

    assert result == [0.1, 0.2, 0.3]
    mock_openai_client.embeddings.create.assert_called_once_with(
        input="hello world", model="text-embedding-3-large"
    )


def test_embed_text_exception(mock_openai_client: MagicMock) -> None:
    mock_openai_client.embeddings.create.side_effect = Exception("OpenAI Error")

    with pytest.raises(RuntimeError, match="Failed to generate embedding for OpenAI"):
        embed_text("hello world")


def test_qdrant_search(mock_openai_client: MagicMock, mock_qdrant_client: MagicMock) -> None:
    mock_openai_response = MagicMock()
    mock_openai_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    mock_openai_client.embeddings.create.return_value = mock_openai_response

    mock_qdrant_response = MagicMock()
    mock_qdrant_response.points = [
        ScoredPoint(id=1, version=0, score=0.99, payload={"title": "Iron Man"}, vector=None)
    ]
    mock_qdrant_client.query_points.return_value = mock_qdrant_response

    result = qdrant_search("superhero movie", limit=2)

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].score == 0.99
    assert result[0].payload == {"title": "Iron Man"}

    mock_qdrant_client.query_points.assert_called_once()
    call_kwargs = mock_qdrant_client.query_points.call_args.kwargs
    assert call_kwargs["query"] == [0.1, 0.2, 0.3]
    assert call_kwargs["limit"] == 2


def test_qdrant_search_exception(
    mock_openai_client: MagicMock, mock_qdrant_client: MagicMock
) -> None:
    mock_openai_client.embeddings.create.side_effect = Exception("Qdrant Error")

    with pytest.raises(RuntimeError, match="Failed to search Qdrant"):
        qdrant_search("superhero movie")


def test_get_movie_data(mock_qdrant_client: MagicMock) -> None:
    mock_qdrant_client.scroll.return_value = (
        [Record(id=1, payload={"title": "Inception"}, vector=None, shard_key=None)],
        None,
    )

    result = get_movie_data("Inception")

    assert len(result) == 1
    assert result[0] == {"id": 1, "payload": {"title": "Inception"}}
    mock_qdrant_client.scroll.assert_called_once()


def test_get_movie_data_exception(mock_qdrant_client: MagicMock) -> None:
    mock_qdrant_client.scroll.side_effect = Exception("Scroll Error")

    with pytest.raises(RuntimeError, match="Failed to get movie data from Qdrant"):
        get_movie_data("Inception")


def test_compare_cosine_similarity(mock_openai_client: MagicMock) -> None:
    mock_response1 = MagicMock()
    mock_response1.data = [MagicMock(embedding=[1.0, 0.0])]
    mock_response2 = MagicMock()
    mock_response2.data = [MagicMock(embedding=[0.0, 1.0])]

    mock_openai_client.embeddings.create.side_effect = [mock_response1, mock_response2]

    result = compare_cosine_similarity("text1", "text2")

    assert result == 0.0


def test_compare_cosine_similarity_exception(mock_openai_client: MagicMock) -> None:
    mock_openai_client.embeddings.create.side_effect = Exception("Embed Error")

    with pytest.raises(RuntimeError, match="Failed to compare cosine similarity"):
        compare_cosine_similarity("text1", "text2")


def test_get_similar_movies_by_title(
    mock_qdrant_client: MagicMock, mock_openai_client: MagicMock
) -> None:
    mock_qdrant_client.scroll.return_value = (
        [
            Record(
                id=1,
                payload={"title": "Iron Man", "plot": "A rich man..."},
                vector=None,
                shard_key=None,
            )
        ],
        None,
    )

    mock_openai_response = MagicMock()
    mock_openai_response.data = [MagicMock(embedding=[0.1, 0.2])]
    mock_openai_client.embeddings.create.return_value = mock_openai_response

    mock_qdrant_response = MagicMock()
    mock_qdrant_response.points = [
        ScoredPoint(id=2, version=0, score=0.99, payload={"title": "Iron Man 2"}, vector=None)
    ]
    mock_qdrant_client.query_points.return_value = mock_qdrant_response

    result = get_similar_movies_by_title("Iron Man")

    assert len(result) == 1
    assert result[0].payload == {"title": "Iron Man 2"}


def test_get_similar_movies_by_title_not_found(mock_qdrant_client: MagicMock) -> None:
    mock_qdrant_client.scroll.return_value = ([], None)

    result = get_similar_movies_by_title("Unknown Movie")

    assert result == []


def test_get_similar_movies_by_title_exception(mock_qdrant_client: MagicMock) -> None:
    mock_qdrant_client.scroll.side_effect = Exception("DB Error")

    with pytest.raises(RuntimeError, match="Failed to get similar movies by title"):
        get_similar_movies_by_title("Iron Man")


def test_get_collection_status(mock_qdrant_client: MagicMock) -> None:
    mock_collection_info = MagicMock()
    mock_collection_info.model_dump.return_value = {"status": "green"}
    mock_qdrant_client.get_collection.return_value = mock_collection_info

    result = get_collection_status()

    assert result == {"status": "green"}


def test_get_collection_status_exception(mock_qdrant_client: MagicMock) -> None:
    mock_qdrant_client.get_collection.side_effect = Exception("DB Error")

    with pytest.raises(RuntimeError, match="Failed to get collection status"):
        get_collection_status()


def test_filtered_search(mock_openai_client: MagicMock, mock_qdrant_client: MagicMock) -> None:
    mock_openai_response = MagicMock()
    mock_openai_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    mock_openai_client.embeddings.create.return_value = mock_openai_response

    mock_qdrant_response = MagicMock()
    mock_qdrant_response.points = [
        ScoredPoint(id=1, version=0, score=0.99, payload={"title": "Iron Man"}, vector=None)
    ]
    mock_qdrant_client.query_points.return_value = mock_qdrant_response

    result = filtered_search("superhero movie", "action")

    assert len(result) == 1
    assert result[0].id == 1


def test_filtered_search_exception(
    mock_openai_client: MagicMock, mock_qdrant_client: MagicMock
) -> None:
    mock_openai_client.embeddings.create.side_effect = Exception("API Error")

    with pytest.raises(RuntimeError, match="Failed to perform filtered search"):
        filtered_search("superhero movie", "action")


def test_scroll_movies_by_director(mock_qdrant_client: MagicMock) -> None:
    mock_qdrant_client.scroll.return_value = (
        [Record(id=1, payload={"title": "Inception"}, vector=None, shard_key=None)],
        None,
    )

    result = scroll_movies_by_director("Christopher Nolan")

    assert len(result) == 1
    assert result[0] == {"id": 1, "payload": {"title": "Inception"}}


def test_scroll_movies_by_director_exception(mock_qdrant_client: MagicMock) -> None:
    mock_qdrant_client.scroll.side_effect = Exception("API Error")

    with pytest.raises(RuntimeError, match="Failed to scroll movies by director"):
        scroll_movies_by_director("Christopher Nolan")
