import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ENV = os.environ.get("APP_ENV", "development")


class BaseConfig(BaseSettings):
    """Base configuration."""

    APP_ENV: str = "base"
    APP_NAME: str = "In.Sight"
    SECRET_KEY: str = "secret-key"
    DATABASE_CONNECTION: str = "local"
    SCHEDULER_ACCESS_TOKEN: str = "scheduler-token"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///app.db"
    CLOUD_SQL_INSTANCE: str = ""
    OPENAI_API_KEY: str = "open-ai-key"

    ADMIN_USERNAME: str = "admin_name"
    ADMIN_EMAIL: str = "admin@mail.com"
    ADMIN_PASSWORD: str = "some_password"

    PAYMENTS_SOURCE_FOLDER: str = "static/payments"

    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"
    GMAIL_TOKEN_PATH: str = "token.pickle"

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass

    model_config = SettingsConfigDict(extra="allow", env_file=(".env"))


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    ALCHEMICAL_DATABASE_URL: str = Field(
        alias="DEVEL_DATABASE_URL",
        default="sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3"),
    )

    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING: bool = True
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = False
    ALCHEMICAL_DATABASE_URL: str = "sqlite:///" + os.path.join(
        BASE_DIR, "database-test.sqlite3"
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    ALCHEMICAL_DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED: bool = True


def config(name: str = APP_ENV) -> DevelopmentConfig | TestingConfig | ProductionConfig:
    if os.environ.get("TEST_UUID"):
        name = "testing"
    CONF_MAP = dict(
        development=DevelopmentConfig,
        testing=TestingConfig,
        production=ProductionConfig,
    )
    configuration = CONF_MAP[name]()
    configuration.ENV = name
    return configuration
