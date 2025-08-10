# 📚 Документация проекта

## 📖 Основные документы

- **[CI/CD Setup](ci-cd.md)** - Настройка и использование CI/CD pipeline
- **[Backend README](../back/README.md)** - Документация бэкенда
- **[Frontend README](../front/README.md)** - Документация фронтенда

## 🚀 Быстрый старт

### Тестирование
```bash
# Запустить все тесты
make test-all

# Запустить полный CI/CD pipeline
make ci
```

### Разработка
```bash
# Установить зависимости
make install

# Запустить в режиме разработки
make dev
```

## 📁 Структура проекта

```
docs/           # Документация
scripts/        # Shell скрипты
back/           # Backend (Python + FastAPI)
front/          # Frontend (React + Vite)
.github/        # GitHub Actions
```

## 🔗 Полезные ссылки

- [Основной README](../README.md)
- [Makefile](../Makefile) - команды для разработки
