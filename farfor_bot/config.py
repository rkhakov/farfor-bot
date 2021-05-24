from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Farfor Bot"
    DEV_SERVER_PORT: int = 8900
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 дней
    SECRET_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


# https://fastapi.tiangolo.com/advanced/settings/#creating-the-settings-only-once-with-lru_cache
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
