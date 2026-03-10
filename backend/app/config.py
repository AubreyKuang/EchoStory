"""
Configuration settings for EchoStory backend
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "EchoStory"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Google Cloud settings
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_APPLICATION_CREDENTIALS: str = ""

    # Gemini API settings
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"

    # Vertex AI settings
    VERTEX_AI_LOCATION: str = "us-central1"
    IMAGEN_MODEL: str = "imagegeneration@006"

    # Storage settings
    STORAGE_BUCKET_NAME: str

    # Firestore settings
    FIRESTORE_COLLECTION: str = "story_sessions"

    # WebSocket settings
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MAX_MESSAGE_SIZE: int = 10 * 1024 * 1024  # 10MB

    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
