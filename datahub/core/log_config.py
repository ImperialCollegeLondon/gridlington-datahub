"""Dict configuration for formal logging."""
LOG_LEVEL: str = "DEBUG"
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
        }
    },
    "loggers": {
        "api_logger": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        }
    },
}
