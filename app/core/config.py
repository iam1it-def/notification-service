from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс с настройками проекта"""
    
    DATABASE_URL: str      # адрес базы данных
    REDIS_URL: str         # адрес Redis

    model_config = SettingsConfigDict(
        env_file=".env",           # берём настройки из файла .env
        env_file_encoding="utf-8",
        extra="ignore"             # игнор лишние переменные
    )


# Создаём объект с настройками
settings = Settings()