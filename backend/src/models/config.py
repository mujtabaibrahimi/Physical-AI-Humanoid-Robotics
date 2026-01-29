"""
Configuration Models
Pydantic settings for environment variables and application configuration
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    environment: str = "development"
    log_level: str = "INFO"

    # Qdrant Vector Database (optional for dev mode)
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "robotics-textbook-v1"

    # Neon PostgreSQL (optional for dev mode)
    neon_database_url: Optional[str] = None

    # Groq API (optional for dev mode)
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    groq_max_tokens: int = 500

    # Redis Cache
    redis_url: str = "redis://localhost:6379"
    cache_ttl_seconds: int = 900  # 15 minutes

    # CORS - accepts comma-separated string or list
    allowed_origins: Union[str, List[str]] = "http://localhost:3000,https://*.github.io"

    @field_validator('allowed_origins', mode='before')
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    # Rate Limiting
    rate_limit_per_minute: int = 10

    # Free-tier Monitoring
    qdrant_storage_limit_gb: float = 1.0
    neon_storage_limit_gb: float = 0.5
    groq_rate_limit_per_min: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_qdrant_configured(self) -> bool:
        return bool(self.qdrant_url and self.qdrant_api_key)

    @property
    def is_groq_configured(self) -> bool:
        return bool(self.groq_api_key)


# Global settings instance
settings = Settings()
