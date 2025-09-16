import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

CONFIG_DIR = os.path.join(PROJECT_ROOT, "src", "config")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
