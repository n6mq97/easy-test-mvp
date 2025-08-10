# CI/CD Setup - Quick Guide

## 🚀 Quick Start

### Local Testing
```bash
# Run all tests
make test-all

# Run full CI/CD pipeline
make ci

# Or use script directly
./test-ci.sh
```

### Individual Commands
```bash
# Backend
make test-backend          # Tests
make install-backend       # Install dependencies

# Frontend
make test-frontend         # Tests
make lint-frontend         # Linting
make build-frontend        # Build
make install-frontend      # Install dependencies
```

## 📋 What is Checked

### Backend (Python + FastAPI)
- ✅ Tests with pytest
- ✅ `/health` endpoint
- ✅ Main endpoint `/`

### Frontend (React + Vite)
- ✅ Tests with Vitest + React Testing Library
- ✅ Linting with ESLint
- ✅ Production build

## 🔧 GitHub Actions

On push to `main` or `develop` branches, the following runs automatically:
1. **Backend Tests** - Python tests
2. **Frontend Tests** - React tests + linting + build
3. **Deploy** - Conditional deployment (only for main)

## 📁 File Structure

```
.github/workflows/ci.yml    # GitHub Actions workflow
back/tests/                 # Backend tests
front/src/test/             # Frontend tests
Makefile                    # Development commands
test-ci.sh                  # Local CI/CD script
pytest.ini                  # pytest configuration
vite.config.js              # Vite + tests configuration
```

## 🐛 Troubleshooting

### Backend tests failing
```bash
cd back
poetry install --with dev
poetry run pytest -v
```

### Frontend tests failing
```bash
docker exec easy-test-mvp-frontend-1 npm install
docker exec easy-test-mvp-frontend-1 npm run test:run
```

### Update dependencies
```bash
make install
```

## 🎯 Next Steps

1. **Add more tests** - cover main logic
2. **Set up real deployment** - replace echo commands in GitHub Actions
3. **Add E2E tests** - Playwright or Cypress
4. **Set up monitoring** - service health checks
5. **Add security scanning** - vulnerability checks
