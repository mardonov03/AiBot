from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int
    class Config:
        env_file = "fast/.env"

settings = Settings()
