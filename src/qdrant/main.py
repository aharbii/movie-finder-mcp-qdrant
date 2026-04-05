from typing import Any

from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models

from qdrant.config import settings
from qdrant.math import search
from qdrant.models.search import QdrantSearchResult

mcp = FastMCP("qdrant-evaluator")
openai_client = OpenAI(api_key=settings.openai_api_key)
qdrant_client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key_ro)


@mcp.tool()
def embed_text(text: str) -> list[float]:
    """
    Calls OpenAI to generate a vector for a test string.

    Args:
        text (str): Text to be embedded

    Returns:
        list[float]: Embedded vector for the provided text
    """
    try:
        response = openai_client.embeddings.create(
            input=text, model=settings.openai_embedding_model
        )
        return response.data[0].embedding
    except Exception as e:
        raise RuntimeError(f"Failed to generate embedding for OpenAI: {str(e)}") from e


@mcp.tool()
def qdrant_search(query: str, limit: int = 5) -> list[QdrantSearchResult]:
    """
    Perform a vector search in Qdrant and return Movie objects
    with distance scores.

    Args:
        query (str): The search query
        limit (int, optional): The maximum number of results to return. Defaults to 5.

    Returns:
        list[QdrantSearchResult]: List of candidates with distance scores
    """

    try:
        query_vector = openai_client.embeddings.create(
            input=query,
            model=settings.openai_embedding_model,
        )
        results = qdrant_client.query_points(
            query=query_vector.data[0].embedding,
            collection_name=settings.qdrant_collection_name,
            with_payload=True,
            limit=limit,
        )

        return [
            QdrantSearchResult(
                id=point.id,
                payload=point.payload or {},
                score=point.score,
            )
            for point in results.points
        ]
    except Exception as e:
        raise RuntimeError(f"Failed to search Qdrant: {str(e)}") from e


@mcp.tool()
def get_movie_data(title: str) -> list[dict[str, Any]]:
    """
    Retrieves the exact metadata for a movie stored in Qdrant

    Args:
        title (str): The title of the movie to retrieve

    Returns:
        list[dict[str, Any]]: List of movies matches the title with their metadata
    """
    try:
        movie_filter = models.Filter(
            must=[models.FieldCondition(key="title", match=models.MatchValue(value=title))]
        )

        records, _ = qdrant_client.scroll(
            scroll_filter=movie_filter,
            collection_name=settings.qdrant_collection_name,
            limit=5,
            with_payload=True,
            with_vectors=False,
        )

        results: list[dict[str, Any]] = []
        for record in records:
            results.append({"id": record.id, "payload": record.payload})
        return results
    except Exception as e:
        raise RuntimeError(f"Failed to get movie data from Qdrant: {str(e)}") from e


@mcp.tool()
def compare_cosine_similarity(text1: str, text2: str) -> float:
    """
    Calculate cosine similarity between two text based on their
    embedded vectors

    Args:
        text1 (str): The first text
        text2 (str): The second text to compare with

    Returns:
        float: Cosine Similarity
    """
    try:
        query_vector1 = openai_client.embeddings.create(
            input=text1,
            model=settings.openai_embedding_model,
        )

        query_vector2 = openai_client.embeddings.create(
            input=text2,
            model=settings.openai_embedding_model,
        )

        cosine_similarity = search.cosine_similarity(
            query_vector1.data[0].embedding, query_vector2.data[0].embedding
        )
        return cosine_similarity
    except Exception as e:
        raise RuntimeError(f"Failed to compare cosine similarity: {str(e)}") from e


@mcp.tool()
def get_similar_movies_by_title(title: str, limit: int = 5) -> list[QdrantSearchResult]:
    """
    Returns movies that has similar plots based on the Qdrant
    Search feature and their embedded vectors

    Args:
        title (str): The title of the movie to retrieve
        limit (int, optional):  The maximum number of results to return. Defaults to 5.

    Returns:
        list[QdrantSearchResult]: List of candidates with distance scores
    """
    try:
        get_movie_data_result = get_movie_data(title)
        if not get_movie_data_result:
            return []

        movie_plot = str(get_movie_data_result[0]["payload"]["plot"])

        qdrant_search_result: list[QdrantSearchResult] = qdrant_search(movie_plot, limit)
        return qdrant_search_result
    except Exception as e:
        raise RuntimeError(f"Failed to get similar movies by title: {str(e)}") from e


@mcp.tool()
def get_collection_status() -> dict[str, Any]:
    """
    Retrieves the status and statistic of the Qdrant collection.

    Returns:
        dict: Collection statistics including point count and vector size.
    """
    try:
        collection_info = qdrant_client.get_collection(
            collection_name=settings.qdrant_collection_name
        )
        return collection_info.model_dump()
    except Exception as e:
        raise RuntimeError(f"Failed to get collection status: {str(e)}") from e


@mcp.tool()
def filtered_search(query: str, genre: str, limit: int = 5) -> list[QdrantSearchResult]:
    """
    Perform a vector search in Qdrant, filtered by a specific genre.

    Args:
        query (str): The search query
        genre (str): The genre to filter the search by
        limit (int, optional):  The maximum number of results to return. Defaults to 5.

    Returns:
        List[QdrantSearchResult]: List of filtered candidates with distance scores
    """

    try:
        query_vector = openai_client.embeddings.create(
            input=query,
            model=settings.openai_embedding_model,
        )

        genre_filter = models.Filter(
            must=[models.FieldCondition(key="genre", match=models.MatchValue(value=genre))]
        )

        results = qdrant_client.query_points(
            query=query_vector.data[0].embedding,
            collection_name=settings.qdrant_collection_name,
            with_payload=True,
            limit=limit,
            filter=genre_filter,
        )

        return [
            QdrantSearchResult(
                id=point.id,
                payload=point.payload or {},
                score=point.score,
            )
            for point in results.points
        ]
    except Exception as e:
        raise RuntimeError(f"Failed to perform filtered search: {str(e)}") from e


@mcp.tool()
def scroll_movies_by_director(director: str, limit: int = 5) -> list[dict[str, Any]]:
    """
    Retrieves movies directed by a specific director.

    Args:
        director (str): The name of the director
        limit (int, optional): The maximum number of results to return. Defaults to 5.

    Returns:
        list[dict[str, Any]]: List of movies directed by the director with distance scores
    """
    try:
        director_filter = models.Filter(
            must=[models.FieldCondition(key="director", match=models.MatchValue(value=director))]
        )

        records, _ = qdrant_client.scroll(
            scroll_filter=director_filter,
            collection_name=settings.qdrant_collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        results: list[dict[str, Any]] = []
        for record in records:
            results.append(
                {
                    "id": record.id,
                    "payload": record.payload,
                }
            )
        return results
    except Exception as e:
        raise RuntimeError(f"Failed to scroll movies by director: {str(e)}") from e


if __name__ == "__main__":
    mcp.run()
