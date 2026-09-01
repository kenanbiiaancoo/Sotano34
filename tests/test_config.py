"""Tests for centralized application settings."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from pydantic import SecretStr

from app.core.config import Settings, get_settings


SUPPORTED_ENVIRONMENT_VARIABLES = (
    "APP_ENV",
    "DEMO_MODE",
    "PUBLIC_BASE_URL",
    "DATABASE_URL",
    "APP_SECRET",
    "OPENAI_API_KEY",
    "OPENAI_INTAKE_MODEL",
    "OPENAI_DIAGNOSIS_MODEL",
    "GEMINI_API_KEY",
    "GEMINI_MODEL",
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "ATICO34_KNOWLEDGE_PATH",
    "TIMEZONE",
)


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Iterator[None]:
    """Prevent cached settings from leaking between environment-based tests."""

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_documented_defaults_load_without_env_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The application can start from its safe defaults alone."""

    for variable in SUPPORTED_ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable, raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_env == "development"
    assert settings.demo_mode is True
    assert settings.public_base_url == ""
    assert settings.database_url == "sqlite:///data/legal_intake.db"
    assert settings.app_secret.get_secret_value() == ""
    assert settings.openai_api_key.get_secret_value() == ""
    assert settings.openai_intake_model == "gpt-5.6-terra"
    assert settings.openai_diagnosis_model == "gpt-5.6-sol"
    assert isinstance(settings.gemini_api_key, SecretStr)
    assert settings.gemini_api_key.get_secret_value() == ""
    assert settings.gemini_model == "gemini-2.5-flash-lite"
    assert settings.twilio_account_sid.get_secret_value() == ""
    assert settings.twilio_auth_token.get_secret_value() == ""
    assert settings.atico34_knowledge_path == Path("docs/atico34_knowledge.md")
    assert settings.timezone == "Europe/Madrid"


def test_environment_values_override_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pydantic parses environment overrides through the cached accessor."""

    monkeypatch.setenv("DEMO_MODE", "false")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///data/overridden.db")
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    monkeypatch.setenv("GEMINI_MODEL", "test-gemini-model")

    settings = get_settings()

    assert settings.demo_mode is False
    assert settings.database_url == "sqlite:///data/overridden.db"
    assert isinstance(settings.gemini_api_key, SecretStr)
    assert settings.gemini_api_key.get_secret_value() == "test-gemini-key"
    assert settings.gemini_model == "test-gemini-model"
