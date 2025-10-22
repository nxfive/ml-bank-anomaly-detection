#!/bin/bash
set -e

echo "Synchronizing client dependencies..."
uv sync --group client

echo "Running client..."
uv run --group client streamlit run services/client/main.py