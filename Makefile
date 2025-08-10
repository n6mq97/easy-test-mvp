.PHONY: help test-backend test-frontend test-all install-backend install-frontend

help: ## Show help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-backend: ## Install backend dependencies
	cd back && poetry install --with dev

install-frontend: ## Install frontend dependencies
	docker exec easy-test-mvp-frontend-1 npm install

install: install-backend install-frontend ## Install all dependencies

test-backend: ## Run backend tests
	cd back && poetry run pytest -v

test-frontend: ## Run frontend tests
	docker exec easy-test-mvp-frontend-1 npm run test:run

test-all: test-backend test-frontend ## Run all tests

lint-frontend: ## Run frontend linter
	docker exec easy-test-mvp-frontend-1 npm run lint

build-frontend: ## Build frontend
	docker exec easy-test-mvp-frontend-1 npm run build

dev-backend: ## Run backend in development mode
	cd back && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run frontend in development mode
	docker exec easy-test-mvp-frontend-1 npm run dev

dev: ## Run both services in development mode
	@echo "Starting backend in background..."
	@$(MAKE) dev-backend &
	@echo "Starting frontend..."
	@$(MAKE) dev-frontend

ci: ## Run full CI/CD pipeline locally
	./scripts/test-ci.sh
