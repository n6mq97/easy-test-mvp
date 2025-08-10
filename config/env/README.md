# Конфигурация окружений

## Обзор

Этот пакет содержит централизованную систему конфигурации для всех окружений проекта.

## Структура

```
config/env/
├── __init__.py          # Инициализация пакета
├── validator.py         # Валидатор конфигурации
├── example.py           # Генератор .env.example
└── README.md            # Эта документация
```

## Компоненты

### 1. ConfigValidator (`validator.py`)

Основной класс для валидации и управления конфигурацией.

**Функции:**
- `validate(strict=True)` - проверка конфигурации
- `validate_database_url(config)` - формирование DATABASE_URL
- `get_environment_config(environment)` - конфигурация для конкретного окружения

**Режимы валидации:**
- `strict=True` (по умолчанию) - строгая проверка всех обязательных переменных
- `strict=False` - мягкая проверка с использованием дефолтных значений

### 2. Генератор .env.example (`example.py`)

Автоматически генерирует `.env.example` файл на основе валидатора.

**Использование:**
```bash
python scripts/generate-env-example.py
```

## Переменные окружения

### Обязательные переменные

| Переменная | Описание | Дефолт |
|------------|----------|---------|
| `ENVIRONMENT` | Окружение (dev/ci/prod) | `development` |
| `DB_HOST` | Хост базы данных | `localhost` |
| `DB_PORT` | Порт базы данных | `5432` |
| `DB_NAME` | Имя базы данных | `testdb` |
| `DB_USER` | Пользователь БД | `user` |
| `DB_PASSWORD` | Пароль БД | `password` |
| `BACKEND_PORT` | Порт backend | `8000` |
| `API_BASE_URL` | URL API | `http://localhost:8000` |
| `FRONTEND_PORT` | Порт frontend | `5173` |
| `VITE_API_BASE_URL` | URL API для frontend | `http://localhost:8000` |

### Опциональные переменные

| Переменная | Описание | Дефолт |
|------------|----------|---------|
| `BACKEND_HOST` | Хост backend | `0.0.0.0` |
| `FRONTEND_HOST` | Хост frontend | `0.0.0.0` |
| `CI_DB_PORT` | Порт БД для CI | `5433` |
| `CI_BACKEND_PORT` | Порт backend для CI | `8001` |
| `CI_FRONTEND_PORT` | Порт frontend для CI | `3001` |
| `NGINX_PORT` | Порт nginx | `80` |

## Использование

### В коде

```python
from config.env.validator import validator

# Получить всю конфигурацию
config = validator.validate()

# Получить конфигурацию для CI
ci_config = validator.get_environment_config("ci")

# Получить DATABASE_URL
db_url = ci_config["DATABASE_URL"]
```

### В тестах

```python
# Валидация не строгая для тестов
config = validator.validate(strict=False)
```

## Автоматическая генерация

При изменении валидатора автоматически обновляется `.env.example`:

```bash
# Генерировать .env.example
python scripts/generate-env-example.py

# Скопировать в .env
cp .env.example .env
```

## Преимущества новой системы

1. **Централизация** - все настройки в одном месте
2. **Валидация** - проверка обязательных переменных при старте
3. **Автогенерация** - .env.example создается автоматически
4. **Гибкость** - поддержка разных окружений
5. **Безопасность** - нет захардкоженных значений в коде
