# Changelog - movie-finder-mcp-qdrant

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- **Diagnostic Tool `get_movie_data`:** Retrieves exact, unvectorized metadata for a given movie title via the Qdrant Scroll API to help verify raw RAG ingestion payloads.
- **Diagnostic Tool `compare_cosine_similarity`:** Calculates the direct cosine similarity between the OpenAI embeddings of two arbitrary text strings without interacting with the Qdrant store.
- **Diagnostic Tool `get_similar_movies_by_title`:** Evaluates vector clustering by taking an existing movie title, finding its plot payload, and querying Qdrant for nearest neighbors.
- **Diagnostic Tool `get_collection_status`:** Retrieves high-level Qdrant database health metrics including total point count and vector dimension size.
- **Diagnostic Tool `filtered_search`:** Performs a hybrid vector similarity search constrained by a strict payload filter (e.g., `genre`) to debug metadata filtering pipelines.
- **Diagnostic Tool `scroll_movies_by_director`:** Performs exact-match retrieval for all movies by a specific director using the Scroll API.
- **Project Tooling:** Expanded `Makefile` with `dev`, `test-coverage`, `detect-secrets`, `fix`, and `clean` targets to support local DX and CI pipelines.
- **Ignore Rules:** Updated `.gitignore` to exclude IDE configs, test coverage reports (`coverage.xml`, `htmlcov/`), and secrets.
