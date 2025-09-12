import os
from datetime import datetime
from typing import Any

import joblib
import numpy as np
import yaml
from src.utils.paths import MODELS_DIR


def save_model_with_metadata(
    *,
    model: Any,
    model_name: str,
    train_preds: np.ndarray,
    test_preds: np.ndarray,
    cat_features: list[str],
    num_features: list[str] | None = None,
    params: dict[str, float | int],
):
    """
    Save model and corresponding metadata to disk.
    """
    file_name = model_name.lower().replace(" ", "_")
    model_path = os.path.join(MODELS_DIR, f"{file_name}.pkl")
    joblib.dump(model, model_path)

    metadata = {
        "model_name": model_name,
        "version": "1.0",
        "date_trained": datetime.today().strftime("%Y-%m-%d"),
        "features_processed": {
            "cat_features": cat_features or [],
            "num_features": num_features or []
        },
        "params": params or {},
        "metrics": {
            "n_train_anomalies": int((train_preds == 1).sum()),
            "n_test_anomalies": int((test_preds == 1).sum())
        }
    }

    metadata_path = os.path.join(MODELS_DIR, "metadata", f"{file_name}.yml")
    with open(metadata_path, "w") as f:
        yaml.safe_dump(metadata, f)
