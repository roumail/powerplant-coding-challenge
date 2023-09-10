import logging
import sys

from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from unit_commitment import PACKAGE_NAME, PACKAGE_VERSION
from unit_commitment.core.logging import InterceptHandler


class Settings(BaseSettings):
    API_PREFIX: str = "/api/v1"
    VERSION: str = PACKAGE_VERSION
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
