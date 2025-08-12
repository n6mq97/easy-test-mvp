"""
Валидатор конфигурации окружения
"""
import os
from typing import Dict, List, Optional


class ConfigValidator:
    """Валидатор конфигурации"""
    
    def __init__(self):
        self.required_vars = {
            # Окружение
            "ENVIRONMENT": "development",
            
            # База данных
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_NAME": "testdb",
            "DB_USER": "user",
            "DB_PASSWORD": "password",
            
            # Backend
            "BACKEND_HOST": "0.0.0.0",
            "BACKEND_PORT": "8000",
            "API_BASE_URL": "http://localhost:8000",
            
            # Frontend
            "FRONTEND_HOST": "0.0.0.0",
            "FRONTEND_PORT": "5173",
            "VITE_API_BASE_URL": "http://localhost:8000",
        }
        
        self.optional_vars = {
            # CI/CD
            "CI_DB_PORT": "5433",
            "CI_BACKEND_PORT": "8001",
            "CI_FRONTEND_PORT": "3001",
            
            # Nginx
            "NGINX_PORT": "80",
        }
    
    def validate(self, strict: bool = True) -> Dict[str, str]:
        """Проверить конфигурацию и вернуть все переменные"""
        missing_vars = []
        config = {}
        
        # Проверяем обязательные переменные
        for var, default in self.required_vars.items():
            value = os.getenv(var)
            if value is None:
                if strict and default is None:
                    missing_vars.append(var)
                else:
                    value = default
            config[var] = value
        
        # Добавляем опциональные переменные
        for var, default in self.optional_vars.items():
            value = os.getenv(var, default)
            config[var] = value
        
        # Проверяем наличие обязательных переменных только в строгом режиме
        if strict and missing_vars:
            raise ValueError(
                f"Отсутствуют обязательные переменные окружения: {', '.join(missing_vars)}\n"
                f"Скопируйте config/env.example в .env и заполните значения"
            )
        
        return config
    
    def validate_database_url(self, config: Dict[str, str]) -> str:
        """Проверить и сформировать DATABASE_URL"""
        db_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
        
        for var in db_vars:
            if var not in config or not config[var]:
                raise ValueError(f"Отсутствует переменная для БД: {var}")
        
        # Формируем URL
        user = config["DB_USER"]
        password = config["DB_PASSWORD"]
        host = config["DB_HOST"]
        port = config["DB_PORT"]
        name = config["DB_NAME"]
        
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    
    def get_environment_config(self, environment: str) -> Dict[str, str]:
        """Получить конфигурацию для конкретного окружения"""
        config = self.validate(strict=False)  # Не строгий режим для внутреннего использования
        
        if environment == "ci":
            # Переопределяем порты для CI
            config["DB_PORT"] = config["CI_DB_PORT"]
            config["BACKEND_PORT"] = config["CI_BACKEND_PORT"]
            config["FRONTEND_PORT"] = config["CI_FRONTEND_PORT"]
            config["DB_HOST"] = "test_postgres"  # Имя сервиса в docker-compose.ci.yml
        
        elif environment == "production":
            # Для продакшна можно добавить дополнительные проверки
            pass
        
        # Формируем DATABASE_URL
        config["DATABASE_URL"] = self.validate_database_url(config)
        
        return config

    def generate_env_example_content(self) -> str:
        """Сгенерировать содержимое .env.example файла"""
        template = """# =============================================================================
# Шаблон конфигурации проекта
# Скопируйте этот файл в .env и заполните значения
# =============================================================================

# =============================================================================
# ОКРУЖЕНИЕ
# =============================================================================
ENVIRONMENT={ENVIRONMENT}

# =============================================================================
# БАЗА ДАННЫХ
# =============================================================================
# Основные параметры БД
DB_HOST={DB_HOST}
DB_PORT={DB_PORT}
DB_NAME={DB_NAME}
DB_USER={DB_USER}
DB_PASSWORD={DB_PASSWORD}

# Полный URL подключения (автоматически формируется из параметров выше)
DATABASE_URL=postgresql://${{DB_USER}}:${{DB_PASSWORD}}@${{DB_HOST}}:${{DB_PORT}}/${{DB_NAME}}

# =============================================================================
# BACKEND
# =============================================================================
BACKEND_HOST={BACKEND_HOST}
BACKEND_PORT={BACKEND_PORT}
API_BASE_URL={API_BASE_URL}

# =============================================================================
# FRONTEND
# =============================================================================
FRONTEND_HOST={FRONTEND_HOST}
FRONTEND_PORT={FRONTEND_PORT}
VITE_API_BASE_URL={VITE_API_BASE_URL}

# =============================================================================
# CI/CD (используются только в CI окружении)
# =============================================================================
CI_DB_PORT={CI_DB_PORT}
CI_BACKEND_PORT={CI_BACKEND_PORT}
CI_FRONTEND_PORT={CI_FRONTEND_PORT}

# =============================================================================
# NGINX (если используется)
# =============================================================================
NGINX_PORT={NGINX_PORT}
"""
        
        # Используем validate со strict=False, чтобы получить все переменные с дефолтами
        config = self.validate(strict=False)
        
        # Заполняем шаблон
        return template.format(**config)


# Глобальный экземпляр валидатора
validator = ConfigValidator()

if __name__ == "__main__":
    # Определяем корневую директорию проекта
    # (два уровня вверх от текущего файла: config/env -> config -> корень)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(project_root, '.env.example')
    
    # Генерируем и записываем контент
    content = validator.generate_env_example_content()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✅ .env.example успешно сгенерирован в: {output_path}")
