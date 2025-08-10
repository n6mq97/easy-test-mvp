#!/bin/sh
set -e

cd back && poetry run alembic upgrade head
