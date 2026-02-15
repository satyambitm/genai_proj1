"""
Centralized application configuration using Pydantic Settings.
Reads from .env file and environment variables.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    APP_NAME: str = "MedReport AI"
    APP_ENV: str = "development"
    APP_VERSION: str = "1.0.0"

    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_VISION_MODEL: str = "gemini-2.0-flash"

    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: list[str] = ["pdf", "png", "jpg", "jpeg", "txt"]

    # ChromaDB
    CHROMA_PERSIST_DIR: str = "chroma_db"
    CHROMA_COLLECTION_NAME: str = "medical_references"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance — call this to access config anywhere."""
    return Settings()
