#!/bin/bash

echo "🧪 Testing CI Pipeline Locally"
echo "================================"

# Проверяем, что мы в корневой директории
if [ ! -f "docker-compose.dev.yml" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Проверяем права Docker
if ! docker info >/dev/null 2>&1; then
    echo "❌ Error: Docker is not accessible. You may need to:"
    echo "   1. Add your user to the docker group: sudo usermod -aG docker \$USER"
    echo "   2. Log out and log back in, or run: newgrp docker"
    echo "   3. Or run this script with sudo: sudo ./scripts/test-ci.sh"
    echo "   4. Or use: make test-ci-sudo"
    exit 1
fi

# Останавливаем существующие контейнеры
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.dev.yml down

# Запускаем PostgreSQL
echo "🐘 Starting PostgreSQL..."
docker-compose -f docker-compose.dev.yml up -d db

# Ждем, пока PostgreSQL будет готов
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker exec easy-test-mvp-db-1 pg_isready -U user -d testdb; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done
echo "✅ PostgreSQL is ready!"

# Устанавливаем зависимости бэкенда
echo "📦 Installing backend dependencies..."
cd back
poetry install --with dev
cd ..

# Запускаем миграции
echo "🔄 Running database migrations..."
cd back
export DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
poetry run alembic upgrade head
cd ..

# Запускаем тесты
echo "🧪 Running backend tests..."
cd back
export DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
poetry run pytest -v
cd ..

# Останавливаем контейнеры
echo "🛑 Stopping containers..."
docker-compose -f docker-compose.dev.yml down

echo "✅ CI pipeline test completed!"
