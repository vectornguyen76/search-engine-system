#!/bin/sh

echo "Start ingest data to Faiss search..."
python faiss_ingest.py

# echo "Start ingest data to Qdrant search..."
# python qdrant_ingest.py

echo "Run app with uvicorn server..."
uvicorn app:app --port 7000 --host 0.0.0.0 --workers 1
