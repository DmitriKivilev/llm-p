# app/core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс настроек.
    Читаем поля из .env файла.
    Если переменной нет то используем значение по умолчанию(в .env)
    """
    
    # Название приложения и окружение
    APP_NAME: str = "llm-p"
    ENV: str = "local"

   
    JWT_SECRET: str = "change_me_super_secret"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # БД
    SQLITE_PATH: str = "./app.db"

    # OpenRouter API (LLM сервис)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"
    OPENROUTER_SITE_URL: str = "https://example.com"
    OPENROUTER_APP_NAME: str = "llm-fastapi-openrouter"

    class Config:
        """Доп. настройки Pydantic."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
