#!/bin/bash

echo "🧪 Running Tests Locally (Dev Container)"
echo "========================================"

# Check if we're in the project root
if [ ! -f "docker-compose.dev.yml" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Check if dev containers are running
if ! docker ps | grep -q "backend"; then
    echo "❌ Error: Dev containers are not running. Start them first with:"
    echo "   docker-compose -f docker-compose.dev.yml up -d"
    exit 1
fi

echo "✅ Dev containers are running"

# Variables to track test results
BACKEND_EXIT_CODE=0
FRONTEND_EXIT_CODE=0
TOTAL_ERRORS=0

echo ""
echo "🧪 Running Backend Tests..."
echo "---------------------------"
if docker exec easy-test-mvp-backend-1 poetry run pytest -v; then
    echo "✅ Backend tests PASSED"
else
    echo "❌ Backend tests FAILED"
    BACKEND_EXIT_CODE=1
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
fi

echo ""
echo "🧪 Running Frontend Tests..."
echo "----------------------------"
if docker exec easy-test-mvp-frontend-1 npm run test:run; then
    echo "✅ Frontend tests PASSED"
else
    echo "❌ Frontend tests FAILED"
    FRONTEND_EXIT_CODE=1
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
fi

echo ""
echo "📊 Test Results Summary:"
echo "========================"
echo "Backend Tests: $([ $BACKEND_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")"
echo "Frontend Tests: $([ $FRONTEND_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")"
echo "Total Errors: $TOTAL_ERRORS"

if [ $TOTAL_ERRORS -eq 0 ]; then
    echo ""
    echo "🎉 All tests passed successfully!"
    exit 0
else
    echo ""
    echo "⚠️  Some tests failed. Check the output above for details."
    exit 1
fi

