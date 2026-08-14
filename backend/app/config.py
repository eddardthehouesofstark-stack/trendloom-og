from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "TrendLoom"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./trendloom.db"
    # For production with PostgreSQL (Supabase), use:
    # postgresql+asyncpg://user:password@host:port/database
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    
    # API Keys
    HUGGINGFACE_API_KEY: str = ""
    
    # Scheduler
    SCHEDULER_ENABLED: bool = True
    DATA_COLLECTION_INTERVAL_HOURS: int = 6
    
    # Region
    DEFAULT_STATE: str = "Tamil Nadu"
    DEFAULT_COUNTRY: str = "India"
    
    # Scraping
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # AI Models
    MODEL_CACHE_DIR: str = "./models_cache"
    USE_GPU: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/trendloom.log"
    
    # CORS - Development: Allow all localhost and 127.0.0.1 variants
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:8080,http://127.0.0.1:8080,http://127.0.0.1:8000,http://localhost:8000"
    
    # Cache TTL
    CACHE_TTL_SHORT: int = 300
    CACHE_TTL_MEDIUM: int = 1800
    CACHE_TTL_LONG: int = 3600
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
