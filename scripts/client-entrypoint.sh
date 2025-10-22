#!/bin/bash
echo "Waiting for server to be ready..."

for i in {1..30}; do
    if curl -s "http://$SERVER_HOST:$SERVER_PORT" > /dev/null; then
        echo "Server is ready!"
        break
    else
        echo "Server not ready yet... retrying ($i/30)"
        sleep 1
    fi
done

echo "Starting Streamlit client..."
streamlit run ./client/main.py --server.port 8501 --server.address 0.0.0.0
