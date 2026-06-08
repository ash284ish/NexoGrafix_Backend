from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ENV: str = "production"
    APP_URL: str = "https://nexografix.com"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
