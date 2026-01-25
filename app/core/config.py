"""
Opti-Scholar: Core Configuration
Centralized settings management using Pydantic Settings
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    app_name: str = "Opti-Scholar"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database (SQLite for demo, PostgreSQL for production)
    database_url: str = "sqlite+aiosqlite:///./opti_scholar.db"
    
    # Gemini AI
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Storage
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 10
    
    # Tesseract
    tesseract_cmd: str = "tesseract"
    
    # Confidence Thresholds
    confidence_auto_approve: float = 0.85
    confidence_hard_flag: float = 0.7
    
    # Anomaly Detection
    zscore_threshold: float = 2.5
    skewness_threshold: float = 1.0
    
    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
