#!/bin/sh
set -e

# Apply database migrations
./migrate.sh

# Start the production server
cd back && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
