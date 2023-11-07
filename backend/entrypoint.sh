#!/usr/bin/env bash

set -e

DEFAULT_MODULE_NAME=app

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}


# Start Uvicorn
uvicorn --proxy-headers $APP_MODULE --host $HOST --port $PORT
