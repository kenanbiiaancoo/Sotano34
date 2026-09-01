"""Centralized application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or ``.env``."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = "development"
    demo_mode: bool = True

    public_base_url: str = ""
    database_url: str = "sqlite:///data/legal_intake.db"
    app_secret: SecretStr = SecretStr("")

    openai_api_key: SecretStr = SecretStr("")
    openai_intake_model: str = "gpt-5.6-terra"
    openai_diagnosis_model: str = "gpt-5.6-sol"

    gemini_api_key: SecretStr = SecretStr("")
    gemini_model: str = "gemini-2.5-flash-lite"

    twilio_account_sid: SecretStr = SecretStr("")
    twilio_auth_token: SecretStr = SecretStr("")

    atico34_knowledge_path: Path = Path("docs/atico34_knowledge.md")
    timezone: str = "Europe/Madrid"


@lru_cache
def get_settings() -> Settings:
    """Return the application's shared, validated settings instance."""

    return Settings()
