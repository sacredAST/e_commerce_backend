import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USERNAME: str = "dev"
    DB_PASSOWRD: str = "dev"
    DB_URL: str = "localhost"
    DB_NAME: str = "e_commerce"
    DB_PORT: str = "5432"
    DATABASE_URL: str = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSOWRD}@{DB_URL}/{DB_NAME}"
    SECRET_KEY: str = os.urandom(32).hex()
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

settings = Settings()
