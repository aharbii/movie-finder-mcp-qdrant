# Qdrant Evaluator MCP Server (`movie-finder-mcp-qdrant`)

A Model Context Protocol (MCP) server built to evaluate, debug, and interact with Qdrant vector databases and OpenAI embeddings.

While this server was built as part of the internal developer tooling for the [Movie Finder](https://github.com/aharbii/movie-finder) application (specifically to debug its RAG ingestion pipelines), **it is designed as a standalone tool**. Anyone building AI applications with Qdrant and OpenAI embeddings can plug this MCP server into their AI assistant (Claude Desktop, Cursor, Gemini CLI) to get deep visibility into their vector store.

## Features & Available Tools

This MCP server exposes the following tools to your AI agent:

### Embedding & Vector Analysis

- **`embed_text(text)`**: Calls OpenAI to generate an embedding vector for a test string.
- **`compare_cosine_similarity(text1, text2)`**: Calculates the exact cosine similarity between the embeddings of two text strings (useful for testing embedding model logic without hitting the DB).

### Vector Search & Evaluation

- **`qdrant_search(query, limit)`**: Performs a standard vector similarity search in Qdrant based on a text query.
- **`filtered_search(query, genre, limit)`**: Performs a vector search with a strict payload filter applied (e.g., `genre`), useful for debugging hybrid search logic.
- **`get_similar_movies_by_title(title, limit)`**: Evaluates vector clustering by finding a specific record (movie) by title and using its exact vector to find nearest neighbors.

### Data Retrieval & Health Checks

- **`get_movie_data(title)`**: Uses the Qdrant Scroll API to retrieve the exact, unvectorized JSON metadata payload for a specific point. Critical for verifying ingestion integrity.
- **`scroll_movies_by_director(director, limit)`**: Retrieves all points matching a specific director using an exact-match filter.
- **`get_collection_status()`**: Retrieves high-level database health metrics (total point count, vector dimension size, status).

---

## Integration Guidelines

This server operates exclusively via `stdio`. It requires Python 3.13 and the `uv` package manager.

### 1. Prerequisites

- Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Clone the repository and navigate to `mcp/qdrant-explorer` (or clone this directory if extracted).
- Copy `.env.example` to `.env` and fill in your keys:
  ```env
  OPENAI_API_KEY=sk-your-key
  QDRANT_URL=http://localhost:6333
  QDRANT_API_KEY_RO=your-read-only-qdrant-key
  ```

### 2. Running Locally (CLI)

You can run the server directly from the terminal to test it:

```bash
uv run src/qdrant/main.py
```

### 3. Connecting to AI Clients

Because this is a FastMCP server running over `stdio`, you integrate it by providing the execution command to your AI client.

#### Claude Desktop Integration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "qdrant-evaluator": {
      "command": "uv",
      "args": [
        "run",
        "/absolute/path/to/movie-finder/mcp/qdrant-explorer/src/qdrant/main.py"
      ],
      "cwd": "/absolute/path/to/movie-finder/mcp/qdrant-explorer",
      "env": {
        "OPENAI_API_KEY": "sk-your-key",
        "QDRANT_URL": "http://localhost:6333",
        "QDRANT_API_KEY_RO": "your-qdrant-key",
        "QDRANT_COLLECTION_NAME": "movies"
      }
    }
  }
}
```

#### Cursor Integration

1. Open Cursor Settings > Features > MCP.
2. Click **+ Add new MCP server**.
3. Name: `qdrant-evaluator`
4. Type: `command`
5. Command: `uv run /absolute/path/to/movie-finder/mcp/qdrant-explorer/src/qdrant/main.py`
6. Make sure your `.env` file is located in the directory where the command is executed, or provide environment variables natively in Cursor's UI if supported.

## Architecture

- **Framework**: `mcp` (FastMCP)
- **Vector DB Client**: `qdrant-client`
- **Embedding Client**: `openai`
- **Typing**: Strict `mypy` enforcement
- **Validation**: `pydantic`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on local development, testing, and submitting pull requests.
