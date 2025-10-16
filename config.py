import os
from datetime import timedelta
from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Code Similarity Checking System"
    DEBUG: bool = False

    # 백엔드 URL 설정
    BACKEND_URL: str = Field(..., validation_alias="BACKEND_URL")

    # 데이터베이스 설정
    DATABASE_URL: str = Field(validation_alias="DATABASE_URL")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # JWT 설정
    JWT_SECRET: str = Field(..., validation_alias="JWT_SECRET")
    JWT_ALG: str = "HS256"
    ACCESS_EXPIRES: int = 15
    REFRESH_EXPIRES: int = 60 * 24 * 14

    @property
    def access_delta(self):
        return timedelta(minutes=self.ACCESS_EXPIRES)

    @property
    def refresh_delta(self):
        return timedelta(minutes=self.REFRESH_EXPIRES)

    # CORS 설정
    CORS_FRONTEND: str = Field(..., validation_alias="CORS_FRONTEND")


class DevSettings(Settings):
    DEBUG: bool = True
    model_config = SettingsConfigDict(env_file=".env.dev", extra="ignore")


class ProdSettings(Settings):
    DEBUG: bool = False
    model_config = SettingsConfigDict(env_file=".env.prod", extra="ignore")


def load_settings() -> Settings:
    env = os.getenv("APP_ENV", "dev").lower()
    cls = {"dev": DevSettings, "prod": ProdSettings}.get(env, Settings)
    return cls()


settings: Final[Settings] = load_settings()
