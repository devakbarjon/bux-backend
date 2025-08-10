from pydantic_settings import BaseSettings
import os

ENV = os.getenv("ENV", "development")  # default to development


class Settings(BaseSettings):
    app_name: str = "Gift Giveaway"
    database_url: str
    bot_token: str
    bot_channel_id: int
    admin_chat_id: int
    secret_key: str
    environment: str = ENV

    class Config:
        env_file = f".env.{ENV}"  # loads .env.development or .env.production


settings = Settings()