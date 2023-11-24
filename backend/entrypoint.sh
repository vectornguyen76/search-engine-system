#!/bin/sh

# echo "Start run entrypoint script..."

# echo "Waiting for postgres..."

# while ! psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB
# do
#     echo "Waiting for PostgreSQL..."
#     sleep 0.5
# done

# echo "PostgreSQL started"

# echo "Migrate database"
# alembic revision -m "initial" --autogenerate
# alembic upgrade head

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}

# Start Uvicorn
uvicorn --proxy-headers app:app --host $HOST --port $PORT
