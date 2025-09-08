import os


def save_data(**kwargs):
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    processed_dir = os.path.join(PROJECT_ROOT, "data", "processed")

    for name, data in kwargs.items():
        data.to_parquet(os.path.join(processed_dir, f"{name}.parquet"))
