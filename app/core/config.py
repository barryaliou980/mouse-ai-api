"""
Global configuration settings for Mouse AI application.
"""
import os
from typing import Optional


class Settings:
    """Application settings configuration."""
    
    APP_NAME: str = "Mouse AI Engine"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Future ML model settings
    MODEL_PATH: Optional[str] = os.getenv("MODEL_PATH")
    USE_AI_AGENT: bool = os.getenv("USE_AI_AGENT", "false").lower() == "true"
    
    # API settings
    MAX_LABYRINTH_SIZE: int = int(os.getenv("MAX_LABYRINTH_SIZE", "100"))
    
    # Log settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_LOGS: int = int(os.getenv("MAX_LOGS", "1000"))


settings = Settings()