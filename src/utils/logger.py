import logging
import logging.config
import os
import yaml
from datetime import datetime

from .paths import CONFIG_DIR, ELK_CONFIG_DIR, LOGS_DIR, ELK_LOGS_DIR


def setup_logging(default_level=logging.INFO):
    env = os.getenv("ENV", "dev")

    if env == "prod":
        config_path = os.path.join(ELK_CONFIG_DIR, "elk_logger.yml")
    else:
        config_path = os.path.join(CONFIG_DIR, "logger.yml")

    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(ELK_LOGS_DIR, exist_ok=True)

    if env == "prod":
        log_filename = os.path.join(ELK_LOGS_DIR, "app.log")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = os.path.join(LOGS_DIR, f"log_{timestamp}.log")

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        if "handlers" in config and "file" in config["handlers"]:
            config["handlers"]["file"]["filename"] = log_filename

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
