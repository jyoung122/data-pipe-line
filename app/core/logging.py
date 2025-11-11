import logging
from typing import Optional

from .config import get_settings


def configure_logging(level: int = logging.INFO) -> None:
    settings = get_settings()
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger(settings.app_name).setLevel(level)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name or get_settings().app_name)
