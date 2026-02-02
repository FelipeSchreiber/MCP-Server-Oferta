"""Configuration settings for the orchestrator agent."""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    mongodb_uri: str = Field(
        default="mongodb://admin:admin123@localhost:27017/agent_memory?authSource=admin",
        env="MONGODB_URI"
    )
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
