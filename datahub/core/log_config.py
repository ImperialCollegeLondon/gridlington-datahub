"""Dict configuration for formal logging."""
import os

LOG_LEVEL: str = os.environ.get("API_LOG_LEVEL", "DEBUG")
FORMAT: str = "[%(levelname)s] %(asctime)s | %(message)s"
logging_dict_config = {
    "version": 1,
    "formatters": {
        "basic": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": FORMAT,
        }
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        },
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.FileHandler",
            "filename": "./log/logging_file.log",
            "formatter": "basic",
        },
    },
    "loggers": {
        "api_logger": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
        },
    },
}
