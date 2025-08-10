#!/bin/bash

echo "🚀 Запуск локального CI/CD pipeline..."
echo "======================================"

echo ""
echo "📦 Backend Tests..."
cd back
if poetry run pytest -v; then
    echo "✅ Backend tests passed"
else
    echo "❌ Backend tests failed"
    exit 1
fi
cd ..

echo ""
echo "📦 Frontend Tests..."
if docker exec easy-test-mvp-frontend-1 npm run test:run; then
    echo "✅ Frontend tests passed"
else
    echo "❌ Frontend tests failed"
    exit 1
fi

echo ""
echo "🔍 Frontend Linting..."
if docker exec easy-test-mvp-frontend-1 npm run lint; then
    echo "✅ Frontend linting passed"
else
    echo "❌ Frontend linting failed"
    exit 1
fi

echo ""
echo "🏗️  Frontend Build..."
if docker exec easy-test-mvp-frontend-1 npm run build; then
    echo "✅ Frontend build passed"
else
    echo "❌ Frontend build failed"
    exit 1
fi

echo ""
echo "🎉 All checks passed! Ready for deployment."
echo "======================================"
