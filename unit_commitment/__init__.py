import importlib.metadata
import os
import sys

from .core.logging import logger


# Initialize debug information
def debug_info():
    logger.debug(f"Initializing {__name__} package.")
    logger.debug(f"Python Executable: {sys.executable}")
    logger.debug(f"Python Version: {sys.version}")
    logger.debug(f"Python Path: {sys.path}")
    logger.debug(f"Working Directory: {os.getcwd()}")


debug_info()


PACKAGE_NAME = "unit_commitment"
PACKAGE_VERSION = importlib.metadata.version(PACKAGE_NAME)
__version__ = PACKAGE_VERSION
__author__ = "Rohail Taimour <rtaimour@illumina.com>"
