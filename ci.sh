#!/usr/bin/env bash
set -euo pipefail

uv sync --dev
uv run black --check src/ tests/
uv run ruff check src/ tests/
uv run pytest tests/ -v
uv build
