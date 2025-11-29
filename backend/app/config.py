from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys (optional - can be provided per request)
    GEMINI_API_KEY: Optional[str] = None
    XAI_API_KEY: Optional[str] = None
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8001  # DEV VERSION - different port from production
    DEBUG: bool = True
    
    # Models
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GROK_MODEL: str = "grok-4"
    
    # Timeouts
    CONNECT_TIMEOUT: int = 10
    READ_TIMEOUT: int = 120
    
    # D/S Cycle
    MAX_DS_ITERATIONS: int = 3
    CONVERGENCE_THRESHOLD: float = 0.05
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
