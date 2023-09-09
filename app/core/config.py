import logging
import sys

from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app import PACKAGE_NAME, __version__
from app.core.logging import InterceptHandler


class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    VERSION: str = __version__
    DEBUG: bool = Field(False)
    PROJECT_NAME: str = Field(PACKAGE_NAME)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

# logging configuration
LOGGING_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
