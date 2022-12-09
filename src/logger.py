import logging

from config import config
from json_log_formatter import JSONFormatter


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG if config.debug else logging.INFO)
    return logger


__all__ = ["get_logger"]
