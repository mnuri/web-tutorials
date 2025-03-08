import logging
import os


logging.basicConfig(level=os.getenv("LOG_LEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

VERSION = os.getenv("VERSION", "0.1.0")
