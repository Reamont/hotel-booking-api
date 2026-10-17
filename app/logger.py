import logging
import logging.config
from contextvars import ContextVar
from pathlib import Path

from app.config import settings

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
APP_LOGGER_PREFIX = "hotel_api"

# ID текущего HTTP-запроса, проставляется middleware в app/main.py
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class ContextFilter(logging.Filter):
    """Добавляет в запись тег-подпись и ID запроса."""

    def filter(self, record: logging.LogRecord) -> bool:
        if record.name.startswith(f"{APP_LOGGER_PREFIX}."):
            record.tag = record.name.removeprefix(f"{APP_LOGGER_PREFIX}.").upper()
        else:
            record.tag = record.name
        record.request_id = request_id_var.get()
        return True


LOG_FORMAT = "%(asctime)s | %(levelname)-8s | [%(tag)s] | req:%(request_id)s | %(message)s"


def setup_logging() -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    handlers = ["console", "app_file", "errors_file"]
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"context": {"()": ContextFilter}},
            "formatters": {
                "default": {"format": LOG_FORMAT, "datefmt": "%Y-%m-%d %H:%M:%S"},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": settings.LOG_LEVEL,
                    "formatter": "default",
                    "filters": ["context"],
                },
                "app_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "default",
                    "filters": ["context"],
                    "filename": LOGS_DIR / "app.log",
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 3,
                    "encoding": "utf-8",
                    "delay": True,
                },
                "errors_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "WARNING",
                    "formatter": "default",
                    "filters": ["context"],
                    "filename": LOGS_DIR / "errors.log",
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 3,
                    "encoding": "utf-8",
                    "delay": True,
                },
            },
            "loggers": {
                APP_LOGGER_PREFIX: {"level": "DEBUG", "handlers": handlers, "propagate": False},
                "uvicorn": {"level": "INFO", "handlers": handlers, "propagate": False},
                # запросы логирует наш middleware, access-лог uvicorn дублировал бы их
                "uvicorn.access": {"level": "WARNING", "handlers": handlers, "propagate": False},
                "sqlalchemy.engine": {"level": "WARNING"},
                "celery": {"level": "INFO"},
            },
            "root": {"level": "WARNING", "handlers": handlers},
        }
    )


def get_logger(tag: str) -> logging.Logger:
    """Логгер с подписью: get_logger("db") -> строки вида `[DB] ...`."""
    return logging.getLogger(f"{APP_LOGGER_PREFIX}.{tag}")
