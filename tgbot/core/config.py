from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    API: str
    AGREEMENT_URL_RU: str
    AGREEMENT_URL_EN: str
    AGREEMENT_URL_UZ: str

    class Config:
        env_file = "tgbot/.env"

settings = Settings()
