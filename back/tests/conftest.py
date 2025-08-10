import pytest
import os

# Устанавливаем переменные окружения для тестов
@pytest.fixture(autouse=True)
def setup_test_env():
    """Автоматически устанавливает тестовое окружение для всех тестов"""
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/testdb"
    yield
    # Очищаем переменные после тестов
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]
