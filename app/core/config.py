"""
Global configuration settings for Mouse AI application.
"""
from typing import Optional


class Settings:
    """Application settings configuration."""
    
    APP_NAME: str = "Mouse AI Engine"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Future ML model settings
    MODEL_PATH: Optional[str] = None
    USE_AI_AGENT: bool = False
    
    # API settings
    MAX_LABYRINTH_SIZE: int = 100
    

settings = Settings()