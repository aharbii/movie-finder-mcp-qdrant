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
- **Project Tooling:** Expanded `Makefile` with `dev`, `ci`, `test-coverage`, `detect-secrets`, `fix`, and `clean` targets to support local DX and CI pipelines.
- **Ignore Rules:** Updated `.gitignore` to exclude IDE configs, test coverage reports (`coverage.xml`, `htmlcov/`), and secrets.
- **Testing Infrastructure:** Added comprehensive Pytest suite mocking `qdrant_client` and `openai_client` globally, achieving 97%+ test coverage.
- **Continuous Integration:** Added `.github/workflows/ci.yml` (GitHub Actions) and `Jenkinsfile` for automated linting, typechecking, and coverage reporting on PRs and `main`. Includes test results and coverage visualizations for GitHub PRs.
- **GitHub Templates:** Added standardized `PULL_REQUEST_TEMPLATE.md` and `ISSUE_TEMPLATE/*.yml` definitions reflecting the `movie-finder` multi-repo issue lifecycle.
- **Type Safety:** Added `py.typed` marker file to support PEP 561 type checking for consumers.

### Fixed

- **CI Dependency Installation:** Replaced `make dev` with `make ci` in CI pipelines to prevent `pre-commit install` from crashing Jenkins runs with global hook paths.
- **Math Robustness:** Updated `cosine_similarity` to safely handle zero-magnitude vectors, preventing `ZeroDivisionError`.
- **Payload Safety:** Updated `get_similar_movies_by_title` to gracefully handle missing `plot` fields in Qdrant payloads.

### Changed

- **Architecture:** Refactored `qdrant.config` and `qdrant.main` to use `lru_cache` lazy instantiation (`get_settings()`, `get_openai_client()`, `get_qdrant_client()`). This aligns the MCP server with the FastAPI backend's dependency injection patterns, removes the need to patch `os.environ` in `conftest.py`, and prevents Pydantic `ValidationError` crashes during `pytest` collection on CI servers.

### Security

- **CI Secret Detection:** Integrated `make detect-secrets` into the GitHub Actions workflow to prevent accidental credential leakage.
