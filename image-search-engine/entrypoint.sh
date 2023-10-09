#!/bin/sh

echo "Start run entrypoint script..."

echo "Waiting for qdrant..."

# Define the URL to check
url="http://$QDRANT_HOST:6333/healthz"

while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$response" -ne 200 ]; then
        echo "URL $url is not healthy (HTTP status code: $response)"
        sleep 0.5
    else
        echo "URL $url is healthy (HTTP status code: $response)"
        break  # Exit the loop when the URL is healthy
    fi
done

echo "Start ingest data to qdrant search..."
python qdrant_ingest.py

echo "Run app with uvicorn server..."
uvicorn app:app --port 7000 --host 0.0.0.0
