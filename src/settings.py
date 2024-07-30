from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Dagster constants
    APPLICATION_NAME: str
    DAGSTER_BASE_URL: str
    DEFAULT_SENSOR_INTERVAL_SECONDS: int = 60

    # Email service-agnostic settings
    ALERT_EMAIL_RECIPIENTS: list[str] = []
    SENDER_EMAIL: str

    # Email service-specific settings
    AWS_SES_ACCESS_KEY: str
    AWS_SES_SECRET_KEY: str
    AWS_SES_CONFIGURATION_SET: str
    AWS_REGION: str

    # Slack settings
    SLACK_CHANNEL: str
    SLACK_TOKEN: str


@lru_cache
def _get_settings():
    return Settings()


settings = _get_settings()
