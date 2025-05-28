from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    API: str
    AGREEMENT_URL_RU: str
    AGREEMENT_URL_EN: str
    AGREEMENT_URL_UZ: str
    PROMPT: str

    class Config:
        env_file = ".env"

settings = Settings()
