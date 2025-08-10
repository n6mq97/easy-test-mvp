# CI/CD Setup - Краткая инструкция

## 🚀 Быстрый старт

### Локальное тестирование
```bash
# Запустить все тесты
make test-all

# Запустить полный CI/CD pipeline
make ci

# Или использовать скрипт напрямую
./test-ci.sh
```

### Отдельные команды
```bash
# Бэкенд
make test-backend          # Тесты
make install-backend       # Установка зависимостей

# Фронтенд
make test-frontend         # Тесты
make lint-frontend         # Линтинг
make build-frontend        # Сборка
make install-frontend      # Установка зависимостей
```

## 📋 Что проверяется

### Backend (Python + FastAPI)
- ✅ Тесты с pytest
- ✅ Эндпоинт `/health`
- ✅ Основной эндпоинт `/`

### Frontend (React + Vite)
- ✅ Тесты с Vitest + React Testing Library
- ✅ Линтинг с ESLint
- ✅ Сборка production версии

## 🔧 GitHub Actions

При push в `main` или `develop` ветки автоматически запускается:
1. **Backend Tests** - Python тесты
2. **Frontend Tests** - React тесты + линтинг + сборка
3. **Deploy** - Условный деплой (только для main)

## 📁 Структура файлов

```
.github/workflows/ci.yml    # GitHub Actions workflow
back/tests/                 # Тесты бэкенда
front/src/test/             # Тесты фронтенда
Makefile                    # Команды для разработки
test-ci.sh                  # Скрипт локального CI/CD
pytest.ini                  # Конфигурация pytest
vite.config.js              # Конфигурация Vite + тестов
```

## 🐛 Troubleshooting

### Backend тесты не проходят
```bash
cd back
poetry install --with dev
poetry run pytest -v
```

### Frontend тесты не проходят
```bash
docker exec easy-test-mvp-frontend-1 npm install
docker exec easy-test-mvp-frontend-1 npm run test:run
```

### Обновить зависимости
```bash
make install
```

## 🎯 Следующие шаги

1. **Добавить больше тестов** - покрыть основную логику
2. **Настроить реальный деплой** - заменить echo команды в GitHub Actions
3. **Добавить E2E тесты** - Playwright или Cypress
4. **Настроить мониторинг** - проверка здоровья сервисов
5. **Добавить security scanning** - проверка уязвимостей
