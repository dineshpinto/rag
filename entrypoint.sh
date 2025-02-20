#!/bin/bash
# Start Qdrant in ephemeral mode
qdrant &

# Wait until Qdrant is ready
echo "Waiting for Qdrant to initialize..."
until curl -s http://localhost:6333/collections >/dev/null; do
  echo "Qdrant is not ready yet, waiting..."
  sleep 10
done
echo "Qdrant is up and running!"

# Start RAG application
uv run start-rag
