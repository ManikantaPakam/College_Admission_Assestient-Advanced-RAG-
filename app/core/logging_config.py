import logging
import logging.config
from app.core.config import LOG_LEVEL


def setup_logging():

    logging_config = {
        "version": 1,

        "disable_existing_loggers": False,

        "formatters": {
            "standard": {
                "format": (
                    "%(asctime)s | "
                    "%(levelname)s | "
                    "%(name)s | "
                    "%(message)s"
                )
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL,
                "formatter": "standard",
            }
        },

        "root": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
    }

    logging.config.dictConfig(logging_config)