# GitHub Copilot — movie-finder-mcp-qdrant

Local DX MCP server for querying Qdrant, embedding text, and evaluating RAG quality — runs via `stdio` only, never deployed to production.

> For full project context, persona prompts, and architecture reference: see root `.github/copilot-instructions.md`.

---

## Python standards

- FastMCP docstring-as-contract: the tool's docstring is the schema exposed to the MCP client — keep it accurate and concise
- Tool names are breaking changes — renaming a tool breaks any client prompt that references it by name
- All tools must be read-only: no writes to Qdrant, no side effects on production data
- Dependencies stay isolated in local `uv.lock` — do not add packages that are also in the production backend
- Run via `uv run` — required for Cursor, Claude Desktop, and other MCP clients

---

## Design patterns

| Pattern              | Rule                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------ |
| **Docstring-as-contract** | Every `@tool` function docstring defines the MCP tool schema. Write it for the AI client, not for human readers. |
| **Read-only access** | Tools query or read data only. Any write operation is out of scope for this server.        |
| **Typed returns**    | All tool return values use Pydantic v2 models — no raw dicts returned to the client.       |

---

## Key files

| Path           | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| `server.py`    | FastMCP server entry point — tool registrations                     |
| `tools/`       | Individual tool implementations (embed, search, compare, scroll)    |
| `pyproject.toml` | Standalone `uv` project — isolated from production dependencies   |
| `.mcp.json`    | (in repo root) MCP client configuration referencing this server     |
