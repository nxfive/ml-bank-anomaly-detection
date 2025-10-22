#!/bin/bash
set -e

echo "Running build stage..."
bash ./scripts/build.sh

echo "Build stage completed"

echo "Runing server stage..."
bash ./scripts/server.sh &    

echo "Runing client stage..."
bash ./scripts/client.sh
