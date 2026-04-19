# JetBrains AI (Junie) — qdrant-explorer MCP guidelines

This is **`movie-finder-mcp-qdrant`** (`mcp/qdrant-explorer/`) — local DX MCP server for evaluating RAG quality.
GitHub repo: `aharbii/movie-finder-mcp-qdrant` · Tracker: `aharbii/movie-finder`

> **Primary reference:** `CLAUDE.md` in this directory — read it for full context.

---

## What this server does

MCP server exposing Qdrant operations to AI agents (Claude Code, Cursor, etc.) via stdio.
Used during development to debug RAG quality, test embeddings, and evaluate semantic search.

**Status: ✅ Ready** — actively used.

---

## Stack

- Python 3.13, FastMCP, Pydantic v2, `uv`
- Runs via `uv run` (stdio) — never deployed to production

---

## Quality gate

```bash
make check   # ruff + mypy --strict + pytest
```

---

## Key constraints

- `mypy --strict` must pass — no `type: ignore` without explanatory comment
- No bare `except:` — always catch specific types
- No `print()` — use logging
- Dependencies isolated in local `uv.lock` — do not pollute production workspace
- Must remain executable via `uv run src/qdrant/main.py` with no extra setup
