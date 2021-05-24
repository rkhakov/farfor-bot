from typing import Optional, Dict, Any
from functools import lru_cache

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Farfor Bot"
    DEV_SERVER_PORT: int = 8900
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 дней
    SECRET_KEY: str
    
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
            host=values.get("DATABASE_HOST"),
            port=values.get("DATABASE_PORT"),
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            path=f'/{values.get("DATABASE_NAME", "")}',
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


# https://fastapi.tiangolo.com/advanced/settings/#creating-the-settings-only-once-with-lru_cache
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
