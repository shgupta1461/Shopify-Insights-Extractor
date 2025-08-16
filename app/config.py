from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Shopify Insights Fetcher"
    APP_ENV: str = "dev"
    DATABASE_URL: str = "sqlite:///./data.db"

    class Config:
        env_file = ".env"  # loads values from .env

settings = Settings()
