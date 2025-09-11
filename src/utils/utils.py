import os
import pickle
from typing import Any

import pandas as pd
import yaml

from .paths import MODELS_DIR, PROCESSED_DATA_DIR


def save_objects(**kwargs):
    """
    Save DataFrames as parquet fiels and objects as pickle files to disk.
    """
    for name, obj in kwargs.items():
        if isinstance(obj, pd.DataFrame):
            path = os.path.join(PROCESSED_DATA_DIR, f"{name}.parquet")
            obj.to_parquet(path)
        else:
            path = os.path.join(MODELS_DIR, f"{name}.pkl")
            with open(path, "wb") as f:
                pickle.dump(obj, f)
        print(f"Saved {name} -> {path}")


def load_model_metadata(model_name: str) -> dict[str, Any]:
    """
    Load and return metadata/configuration for the specified model.
    """
    meta_path = os.path.join(MODELS_DIR, "metadata", f"{model_name}.yml")
    with open(meta_path, "r") as file:
        return yaml.safe_load(file)
