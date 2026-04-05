# =============================================================================
# MCP Server — Developer contract
#
# Usage:
#   make help
#   make <target>
#
# All developer commands execute locally using uv.
# These are stdio servers meant for local AI tooling integration.
# =============================================================================

.PHONY: help init lint format typecheck test pre-commit check

.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "MCP Server — available targets"
	@echo "=============================="
	@echo "  init           Install dependencies and setup pre-commit"
	@echo "  lint           Run ruff check (report only)"
	@echo "  format         Run ruff format (apply)"
	@echo "  typecheck      Run mypy"
	@echo "  test           Run pytest"
	@echo "  pre-commit     Run all pre-commit hooks"
	@echo "  check          lint + typecheck + test"

init:
	uv sync
	uv run pre-commit install

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy .

test:
	uv run pytest

pre-commit:
	uv run pre-commit run --all-files

check: lint typecheck test
