#!/bin/bash

set -e

echo "Building backend..."
python -m src.main

echo "Start server"
exec python -m server.run