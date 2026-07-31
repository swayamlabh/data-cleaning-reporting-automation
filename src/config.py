from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed application configuration."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.5"
    ollama_model: str | None = None
    app_output_dir: Path = Path("reports")


settings = Settings()
