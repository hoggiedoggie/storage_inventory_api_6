import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional

class Settings(BaseSettings):
    # Данные для MongoDB
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    MONGO_URI: str 

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str
    CACHE_TTL_DEFAULT: int = 300

    PROJECT_NAME: str = "Storage Inventory API"
    VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    JWT_ACCESS_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str = "http://localhost:8000/api/v1/yandex/callback"

    JWT_REFRESH_SECRET: str
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    @field_validator(
        "DB_USER", "DB_PASSWORD", "DB_NAME", "MONGO_URI",
        "JWT_ACCESS_SECRET", "REDIS_HOST", "REDIS_PASSWORD",
        "YANDEX_CLIENT_ID", "YANDEX_CLIENT_SECRET",
        mode="before"
    )
    @classmethod
    def strip_spaces(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def REDIS_URL(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
    
    @property
    def SHOW_DOCS(self) -> bool:
        return self.APP_ENV.lower() == "development"

    @property
    def DOCS_URL(self) -> Optional[str]:
        return "/api/docs" if self.SHOW_DOCS else None

    @property
    def OPENAPI_URL(self) -> Optional[str]:
        return "/api/openapi.json" if self.SHOW_DOCS else None

settings = Settings()