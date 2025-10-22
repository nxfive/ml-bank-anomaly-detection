#!/bin/bash
set -e  

echo "Synchronizing build dependencies..."
uv sync --group build

echo "Running build..."
uv run python -m src.main
