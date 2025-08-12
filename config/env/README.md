# Конфигурация окружений

## Обзор

Этот пакет содержит централизованную систему конфигурации для всех окружений проекта.

## Структура

```
config/env/
├── __init__.py          # Инициализация пакета
├── validator.py         # Валидатор и генератор .env.example
└── README.md            # Эта документация
```

## Компоненты

### ConfigValidator (`validator.py`)

Основной класс для валидации, управления конфигурацией и генерации `.env.example`.

**Функции:**
- `validate(strict=True)` - проверка конфигурации
- `validate_database_url(config)` - формирование DATABASE_URL
- `get_environment_config(environment)` - конфигурация для конкретного окружения
- `generate_env_example_content()` - генерация содержимого `.env.example`

**Режимы валидации:**
- `strict=True` (по умолчанию) - строгая проверка всех обязательных переменных
- `strict=False` - мягкая проверка с использованием дефолтных значений

## Генерация .env.example

Файл `validator.py` является исполняемым. При запуске он автоматически генерирует `.env.example` в корне проекта на основе переменных, определенных в валидаторе.

**Использование:**
```bash
python config/env/validator.py
```

Это гарантирует, что `.env.example` всегда синхронизирован с кодом.

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

При изменении `validator.py` (например, при добавлении новой переменной), запустите команду для обновления `.env.example`:

```bash
# Сгенерировать .env.example
python config/env/validator.py

# Скопировать в .env и заполнить
cp .env.example .env
```

## Преимущества системы

1. **Централизация** - все настройки в `validator.py`
2. **Валидация** - проверка обязательных переменных при старте
3. **Автогенерация** - .env.example всегда актуален
4. **Гибкость** - поддержка разных окружений
5. **Безопасность** - нет захардкоженных значений в коде
