#!/bin/bash
set -e

# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    sleep 1
done
echo "Ollama ready."

# Pull model if not already present
if ! ollama list | grep -q "mistral:7b-instruct-q4_0"; then
    echo "Pulling mistral:7b-instruct-q4_0..."
    ollama pull mistral:7b-instruct-q4_0
fi

echo "Starting FastAPI..."
exec uvicorn app:app --host 0.0.0.0 --port 8000
