import logging
import logging.config
import sys
from pathlib import Path

def setup_logging() -> None:
    """Setup application logging configuration."""
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "level": logging.INFO,
                "formatter": "default",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": logging.INFO,
                "formatter": "default",
                "filename": Path("{}/logs/app.log".format(PROJECT_ROOT)),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": logging.ERROR,
                "formatter": "default",
                "filename": Path("{}/logs/error.log".format(PROJECT_ROOT)),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "": {
                "level": logging.INFO,
                "handlers": ["default", "file", "error_file"],
            },
        },
    }
    Path("{}/logs".format(PROJECT_ROOT)).mkdir(exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)

