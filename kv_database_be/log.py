import logging

LOGGER_NAME = "api_logger"
LOG_FORMAT = "%(levelprefix)s [%(asctime)s] %(message)s"
LOG_LEVEL = "DEBUG"

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,  # Access the LOG_FORMAT from LogConfig
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},  # Access LOGGER_NAME and LOG_LEVEL from LogConfig
    },
}

logging.config.dictConfig(log_config)
logger = logging.getLogger(LOGGER_NAME)