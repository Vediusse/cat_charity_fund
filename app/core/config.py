from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "QrKot"
    database_url: str = "sqlite+aiosqlite:///./qrkot.db"
    secret: str = "secret"
    lifetime_jwt: int = 3600
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
