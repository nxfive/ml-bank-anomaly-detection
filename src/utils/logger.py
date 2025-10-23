import logging
import logging.config
import os
import yaml
from datetime import datetime
from .settings import settings


class RequestLoggerAdapter(logging.LoggerAdapter):
    """Ensures standard HTTP request fields exist in 'extra'."""

    def process(self, msg: str, kwargs: dict) -> tuple[str, dict]:
        """
        Add default HTTP request fields to the log record.
        """
        extra = kwargs.get('extra', {})
        extra.setdefault('method', '')
        extra.setdefault('url', '')
        extra.setdefault('status', '')
        extra.setdefault('duration', '')
        extra.setdefault('client', '')
        kwargs['extra'] = extra
        return msg, kwargs


def setup_logging():
    """
    Configure logging for the application.

    Loads logging settings from a logger config file if it exists, 
    otherwise uses basic logging with a default level. 
    """
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    log_filename = os.path.join(settings.LOG_DIR, f"log_{timestamp}.log")

    if os.path.exists(settings.LOG_CONFIG_FILE):
        with open(settings.LOG_CONFIG_FILE) as f:
            config = yaml.safe_load(f)

        if "handlers" in config and "file" in config["handlers"]:
            config["handlers"]["file"]["filename"] = log_filename
        
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=settings.LOGGING_LEVEL)


def get_logger() -> logging.Logger:
    """
    Return a configured logger.

    Uses a RequestLoggerAdapter in dev environment, 
    otherwise returns a standard logger.
    """
    base_logger = logging.getLogger("app")
    if settings.ENV == "dev":
        return RequestLoggerAdapter(base_logger, {})
    else:
        return base_logger


setup_logging()
logger = get_logger()