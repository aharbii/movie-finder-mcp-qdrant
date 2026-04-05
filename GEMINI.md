# AI Agent Context — movie-finder-mcp-qdrant

Foundational mandate for `movie-finder-mcp-qdrant` (`mcp/qdrant-explorer`).

## What this submodule does

Internal Model Context Protocol (MCP) server for local DX and AI tooling.
It runs exclusively via `stdio` and is not deployed to production.

## Technology stack

- Python 3.13
- `mcp` (FastMCP)
- `uv` workspace
- `pydantic` v2

## Coding standards

- **Line length:** 100 characters (`ruff`)
- **Type annotations:** Required — `mypy --strict` must pass
- **Dependencies:** Isolated in local `uv.lock`. Do not pollute production dependencies.

## Workflow invariants

- This is a local DX utility.
- Must execute via `uv run` for clients like Cursor or Claude Desktop.
