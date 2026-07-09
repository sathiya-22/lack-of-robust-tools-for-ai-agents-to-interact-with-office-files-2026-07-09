import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configuration settings for the AI agent prototype.
    Loads environment variables or defaults.
    """
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.3
    max_tokens: int = 1500
    api_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
