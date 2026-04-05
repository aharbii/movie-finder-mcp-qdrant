# Contributing to Qdrant Evaluator MCP Server

First off, thank you for considering contributing to the `movie-finder-mcp-qdrant` server! It's people like you that make tools like this robust and useful for the community.

## Development Setup

This project uses `uv` for lightning-fast Python package management and virtual environment creation.

1. **Install `uv`**: Follow the instructions at [astral.sh/uv](https://docs.astral.sh/uv/).
2. **Clone the repo** and navigate to the `mcp/qdrant-explorer` directory.
3. **Initialize the workspace**:
   Run the setup `make` command to install dependencies, create the `.env` file, and install `pre-commit` hooks.
   ```bash
   make dev
   ```

## Development Workflow

The `Makefile` at the root of this project contains all the necessary commands to build, test, and lint the code. We enforce strict typing and code formatting to keep the repository clean.

### Available Make Commands

- **`make lint`**: Runs `ruff check` to report any linting errors.
- **`make format`**: Runs `ruff format` to auto-format your code.
- **`make fix`**: Automatically fixes linting errors and formats your code. Run this before committing!
- **`make typecheck`**: Runs `mypy` to enforce strict type hinting.
- **`make test`**: Runs the `pytest` suite.
- **`make test-coverage`**: Runs `pytest` with coverage reporting.
- **`make detect-secrets`**: Scans the codebase for accidentally hardcoded secrets.
- **`make check`**: Runs the full CI-equivalent suite locally (lint, typecheck, and test-coverage).

### Pre-commit Hooks

When you ran `make dev`, pre-commit hooks were installed. These hooks automatically format your code and run linters before every commit. If a hook fails, simply review the changes it made, stage them (`git add`), and try committing again.

## Submitting a Pull Request

1. **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name`
2. **Write your code**. If you are adding a new MCP tool, make sure to add a comprehensive docstring and appropriate type hints.
3. **Write tests**. Add corresponding unit tests in the `tests/` directory.
4. **Run the local checks**:
   ```bash
   make fix
   make check
   ```
5. Ensure `make check` passes completely with no typing or test failures.
6. Push your branch and open a PR against the `main` branch.

Thank you!
