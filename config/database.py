"""
Централизованная конфигурация базы данных
"""
import os
from typing import Optional
from urllib.parse import urlparse

try:
    from .env.validator import validator
except ImportError:
    # Fallback для случаев, когда validator недоступен
    validator = None


class DatabaseConfig:
    """Конфигурация базы данных"""
    
    def __init__(self):
        if validator:
            # Используем валидатор
            config = validator.validate()
            self.host = config["DB_HOST"]
            self.port = int(config["DB_PORT"])
            self.name = config["DB_NAME"]
            self.user = config["DB_USER"]
            self.password = config["DB_PASSWORD"]
        else:
            # Fallback - читаем напрямую из env
            self.host = os.getenv("DB_HOST")
            self.port = int(os.getenv("DB_PORT", "5432"))
            self.name = os.getenv("DB_NAME")
            self.user = os.getenv("DB_USER")
            self.password = os.getenv("DB_PASSWORD")
            
            # Проверяем обязательные переменные
            if not all([self.host, self.name, self.user, self.password]):
                raise ValueError(
                    "Отсутствуют обязательные переменные БД: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD\n"
                    "Скопируйте config/env.example в .env и заполните значения"
                )
        
    @property
    def url(self) -> str:
        """Получить полный URL базы данных"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
    @property
    def connection_params(self) -> dict:
        """Получить параметры подключения как словарь"""
        return {
            "host": self.host,
            "port": self.port,
            "database": self.name,
            "user": self.user,
            "password": self.password
        }
    
    def get_url_for_environment(self, environment: str) -> str:
        """Получить URL для конкретного окружения"""
        if validator:
            # Используем валидатор для получения конфигурации окружения
            config = validator.get_environment_config(environment)
            return config["DATABASE_URL"]
        else:
            # Fallback логика
            if environment == "ci":
                port = os.getenv("CI_DB_PORT", "5433")
                host = "test_postgres"  # Имя сервиса в docker-compose.ci.yml
            elif environment == "production":
                host = os.getenv("PROD_DB_HOST", self.host)
                port = os.getenv("PROD_DB_PORT", self.port)
            else:  # development
                host = self.host
                port = self.port
                
            return f"postgresql://{self.user}:{self.password}@{host}:{port}/{self.name}"


class AppConfig:
    """Основная конфигурация приложения"""
    
    def __init__(self):
        if validator:
            # Используем валидатор
            config = validator.validate()
            self.environment = config["ENVIRONMENT"]
            self.database = DatabaseConfig()
            
            # Backend настройки
            self.backend_host = config["BACKEND_HOST"]
            self.backend_port = int(config["BACKEND_PORT"])
            self.api_base_url = config["API_BASE_URL"]
            
            # Frontend настройки
            self.frontend_host = config["FRONTEND_HOST"]
            self.frontend_port = int(config["FRONTEND_PORT"])
            self.frontend_api_base_url = config["VITE_API_BASE_URL"]
        else:
            # Fallback - читаем напрямую из env
            self.environment = os.getenv("ENVIRONMENT", "development")
            self.database = DatabaseConfig()
            
            # Backend настройки
            self.backend_host = os.getenv("BACKEND_HOST", "0.0.0.0")
            self.backend_port = int(os.getenv("BACKEND_PORT", "8000"))
            self.api_base_url = os.getenv("API_BASE_URL")
            
            # Frontend настройки
            self.frontend_host = os.getenv("FRONTEND_HOST", "0.0.0.0")
            self.frontend_port = int(os.getenv("FRONTEND_PORT", "5173"))
            self.frontend_api_base_url = os.getenv("VITE_API_BASE_URL")
            
            # Проверяем обязательные переменные
            if not self.api_base_url:
                raise ValueError("Отсутствует обязательная переменная: API_BASE_URL")
            if not self.frontend_api_base_url:
                raise ValueError("Отсутствует обязательная переменная: VITE_API_BASE_URL")
    
    @property
    def database_url(self) -> str:
        """Получить URL БД для текущего окружения"""
        return self.database.get_url_for_environment(self.environment)
    
    @property
    def is_development(self) -> bool:
        """Проверить, является ли окружение разработкой"""
        return self.environment == "development"
    
    @property
    def is_ci(self) -> bool:
        """Проверить, является ли окружение CI/CD"""
        return self.environment == "ci"
    
    @property
    def is_production(self) -> bool:
        """Проверить, является ли окружение продакшном"""
        return self.environment == "production"


# Глобальный экземпляр конфигурации
config = AppConfig()
