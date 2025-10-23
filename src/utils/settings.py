import os
import logging
from .paths import CONFIG_DIR, ELK_CONFIG_DIR, LOGS_DIR, ELK_LOGS_DIR


class Settings:
    ENV: str = os.getenv("ENV", "dev")
    LOGGING_LEVEL: int = logging.DEBUG if ENV == "dev" else logging.INFO
    FASTAPI_LOG_LEVEL: str = "debug" if ENV == "dev" else "info"
    LOG_CONFIG_FILE: str = os.path.join(CONFIG_DIR, "logger.yml") if ENV == "dev" else os.path.join(ELK_CONFIG_DIR, "elk_logger.yml")
    LOG_DIR: str = LOGS_DIR if ENV == "dev" else ELK_LOGS_DIR


settings = Settings()