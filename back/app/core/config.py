from pydantic_settings import BaseSettings, SettingsConfigDict
import sys
import os

# Добавляем путь к корневой директории проекта для импорта config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from config.database import config as app_config
except ImportError:
    # Fallback для случаев, когда config недоступен
    app_config = None

class Settings(BaseSettings):
    # Используем централизованную конфигурацию, если доступна
    DATABASE_URL: str = app_config.database_url if app_config else None
    
    # Дополнительные настройки
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    API_BASE_URL: str = os.getenv("API_BASE_URL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Игнорируем дополнительные переменные
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Валидация обязательных переменных
        if not self.DATABASE_URL:
            raise ValueError(
                "Отсутствует обязательная переменная: DATABASE_URL\n"
                "Скопируйте config/env.example в .env и заполните значения"
            )
        
        if not self.API_BASE_URL:
            raise ValueError(
                "Отсутствует обязательная переменная: API_BASE_URL\n"
                "Скопируйте config/env.example в .env и заполните значения"
            )

settings = Settings()
