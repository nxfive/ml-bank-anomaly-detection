#!/bin/bash
set -e

export ENV=dev

echo "Synchronizing test dependencies..."
uv sync --group build

echo "Running tests..."
uv run --group build pytest -v