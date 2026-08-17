import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "NovaAgent"
    API_V1_STR: str = "/api/v1"

    # Security settings
    SECRET_KEY: str = "SUPER_SECRET_SECURITY_KEY_FOR_LOCAL_DEVELOPMENT_CHANGE_IN_PROD"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS origins
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/novaagent"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Supabase (Auth and Storage)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_JWT_SECRET: Optional[str] = None

    # AI Configurations
    OPENAI_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_PROVIDER: str = "ollama"  # or "openai" or "mock"
    LLM_MODEL: str = "llama3"     # or "gpt-4-turbo", "gpt-3.5-turbo"
    EMBEDDING_PROVIDER: str = "ollama"  # or "openai" or "mock"
    EMBEDDING_MODEL: str = "nomic-embed-text" # or "text-embedding-3-small"

    # Storage settings
    STORAGE_PROVIDER: str = "local"  # or "supabase"
    LOCAL_STORAGE_DIR: str = "./storage_vault"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

settings = Settings()
