# =============================================================================
# Qdrant MCP Server — Developer contract
#
# Usage:
#   make help
#   make <target>
#
# All developer commands execute locally using uv.
# These are stdio servers meant for local AI tooling integration.
# =============================================================================

.PHONY: help init lint format fix typecheck test test-coverage detect-secrets pre-commit check clean

.DEFAULT_GOAL := help

SOURCE_PATHS := .
COVERAGE_XML ?= coverage.xml
COVERAGE_HTML ?= htmlcov
JUNIT_XML ?= junit.xml

help:
	@echo ""
	@echo "Qdrant MCP Server — available targets"
	@echo "=============================="
	@echo "  init           Install dependencies and setup pre-commit"
	@echo "  dev.           Install dev dependencies and setup pre-commit"
	@echo "  lint           Run ruff check (report only)"
	@echo "  format         Run ruff format (apply)"
	@echo "  fix            Run ruff check --fix + ruff format (apply all auto-fixes)"
	@echo "  typecheck      Run mypy"
	@echo "  test           Run pytest"
	@echo "  test-coverage  Run pytest with coverage + JUnit output"
	@echo "  detect-secrets Run detect-secrets scan"
	@echo "  pre-commit     Run all pre-commit hooks"
	@echo "  check          lint + typecheck + test"
	@echo "  clean          Remove __pycache__, .pytest_cache, .mypy_cache, reports"

init:
	@if [ ! -f .env ]; then cp .env.example .env && echo ">>> .env created from .env.example"; fi
	uv sync
	uv run pre-commit install

dev:
	@if [ ! -f .env ]; then cp .env.example .env && echo ">>> .env created from .env.example"; fi
	uv sync --dev
	uv run pre-commit install

lint:
	uv run ruff check $(SOURCE_PATHS)

format:
	uv run ruff format $(SOURCE_PATHS)

fix:
	uv run ruff check --fix $(SOURCE_PATHS)
	uv run ruff format $(SOURCE_PATHS)

typecheck:
	uv run mypy $(SOURCE_PATHS)

test:
	uv run pytest tests/ -v --tb=short --junitxml=$(JUNIT_XML)

test-coverage:
	uv run pytest tests/ -v --tb=short \
		--junitxml=$(JUNIT_XML) \
		--cov=qdrant \
		--cov-report=term-missing \
		--cov-report=xml:$(COVERAGE_XML) \
		--cov-report=html:$(COVERAGE_HTML)

detect-secrets:
	uv run detect-secrets scan --baseline .secrets.baseline

pre-commit:
	uv run pre-commit run --all-files

check: lint typecheck test-coverage

clean:
	@echo ">>> Removing Python cache files..."
	$(find . -type d -name "__pycache__" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true)
	$(find . -type d -name ".pytest_cache" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true)
	$(find . -type d -name ".mypy_cache" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true)
	$(find . -type d -name ".ruff_cache" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true)
	$(find . -name "*.egg-info" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true)
	$(find . -name "$(COVERAGE_XML)" -not -path "./.git/*" -delete 2>/dev/null || true)
	$(find . -name "$(JUNIT_XML)" -not -path "./.git/*" -delete 2>/dev/null || true)
	$(find . -type d -name "$(COVERAGE_HTML)" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true)
