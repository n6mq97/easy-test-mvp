.PHONY: help test-backend test-frontend test-all install-backend install-frontend

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-backend: ## Установить зависимости бэкенда
	cd back && poetry install --with dev

install-frontend: ## Установить зависимости фронтенда
	docker exec easy-test-mvp-frontend-1 npm install

install: install-backend install-frontend ## Установить все зависимости

test-backend: ## Запустить тесты бэкенда
	cd back && poetry run pytest -v

test-frontend: ## Запустить тесты фронтенда
	docker exec easy-test-mvp-frontend-1 npm run test:run

test-all: test-backend test-frontend ## Запустить все тесты

lint-frontend: ## Запустить линтер фронтенда
	docker exec easy-test-mvp-frontend-1 npm run lint

build-frontend: ## Собрать фронтенд
	docker exec easy-test-mvp-frontend-1 npm run build

dev-backend: ## Запустить бэкенд в режиме разработки
	cd back && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Запустить фронтенд в режиме разработки
	docker exec easy-test-mvp-frontend-1 npm run dev

dev: ## Запустить оба сервиса в режиме разработки
	@echo "Запуск бэкенда в фоне..."
	@$(MAKE) dev-backend &
	@echo "Запуск фронтенда..."
	@$(MAKE) dev-frontend

ci: ## Запустить полный CI/CD pipeline локально
	./scripts/test-ci.sh
