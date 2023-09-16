#!/bin/sh

echo "Start run entrypoint script..."

echo "Start ingest data to qdrant search..."
python qdrant_ingest.py

echo "Run app with uvicorn server..."
uvicorn app:app --port 7000 --host 0.0.0.0