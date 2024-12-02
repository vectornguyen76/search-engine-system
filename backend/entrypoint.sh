#!/bin/sh

echo "Start run entrypoint script..."

echo "Migrate database"
alembic revision -m "initial" --autogenerate
alembic upgrade head

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}

# Start Uvicorn
uvicorn --proxy-headers app:app --host $HOST --port $PORT
