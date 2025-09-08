import logging
import logging.config
import os
import yaml
from datetime import datetime

def setup_logging(default_level=logging.INFO):
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    config_path = os.path.join(PROJECT_ROOT, "config", "logger.yml")

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        log_dir = os.path.join(os.path.dirname(config_path), "../logs")
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        log_filename = os.path.join(log_dir, f"log_{timestamp}.log")

        config["handlers"]["file"]["filename"] = log_filename

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_logger(name: str):
    return logging.getLogger(name)
