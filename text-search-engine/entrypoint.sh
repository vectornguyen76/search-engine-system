#!/bin/sh

echo "Start run entrypoint script..."

echo "Start ingest data to elastic search..."
python ingest_data.py

echo "Run app with uvicorn server..."
uvicorn app:app --port 8000