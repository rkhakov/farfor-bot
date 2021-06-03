from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Farfor Bot"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 дней
    SECRET_KEY: str

    # Telegram
    TELEGRAM_TOKEN: str

    # Database
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            host=values["DATABASE_HOST"],
            port=values["DATABASE_PORT"],
            user=values["DATABASE_USER"],
            password=values["DATABASE_PASSWORD"],
            path=f'/{values["DATABASE_NAME"]}',
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


# https://fastapi.tiangolo.com/advanced/settings/#creating-the-settings-only-once-with-lru_cache
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
