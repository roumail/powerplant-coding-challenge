from pydantic import BaseSettings, Field
import sys
import logging
from loguru import logger
from app.core.logging import InterceptHandler


class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    VERSION: str = "0.1.0"
    DEBUG: bool = Field(False, env="DEBUG")
    PROJECT_NAME: str = Field("unit_commitment", env="PROJECT_NAME")
    INPUT_EXAMPLE: str = Field("./examples/", env="INPUT_EXAMPLE")

    class Config:
        env_file = ".env"


settings = Settings()

# logging configuration
LOGGING_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
