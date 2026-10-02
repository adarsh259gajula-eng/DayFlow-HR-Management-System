import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dayflow HRMS"
    MONGO_URI: str = "mongodb+srv://adarsh25:Adarsh_2509@cluster0.utawc6s.mongodb.net/?appName=Cluster0"
    DATABASE_URL: str = ""
    DB_NAME: str = "dayflow_hrms"
    JWT_SECRET_KEY: str = "dayflow_hrms_super_secret_jwt_key_change_in_production_2026"
    JWT_REFRESH_SECRET_KEY: str = "dayflow_hrms_super_secret_refresh_jwt_key_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: List[str] = [
        "https://day-flow-hr-management-system.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ]

    @property
    def mongo_connection_uri(self) -> str:
        return (
            self.DATABASE_URL or
            self.MONGO_URI or
            os.environ.get("DATABASE_URL") or
            os.environ.get("MONGO_URI") or
            "mongodb+srv://adarsh25:Adarsh_2509@cluster0.utawc6s.mongodb.net/?appName=Cluster0"
        ).strip()

    # SMTP Mail Server Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply.dayflow@gmail.com"
    SMTP_FROM_NAME: str = "Dayflow HRMS System"
    SMTP_TLS: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
