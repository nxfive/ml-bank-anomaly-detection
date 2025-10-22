#!/bin/bash
set -e

echo "Synchronizing server dependencies..."
uv sync --group server

echo "Running server..."
uv run --group server python -m services.server.run