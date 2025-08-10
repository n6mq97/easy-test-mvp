from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://test:test@localhost:5432/testdb"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
