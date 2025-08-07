from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    OPENAI_API_KEY: str
    ADMIN_ID: int
    YKASSA_TOKEN: str
    PRICE_MONTH: int = 29900  # 299 руб в копейках

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()