import yaml
import joblib
from datetime import datetime
import os


def save_model_with_metadata(
    model,
    model_name: str,
    train_labels=None,
    test_labels=None,
    cat_features=None,
    num_features=None,
    params=None,
):
    """
    Save model and corresponding metadata to disk.
    """
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    model_dir = os.path.join(PROJECT_ROOT, "models")

    file_name = model_name.lower().replace(" ", "_")

    model_path = os.path.join(model_dir, f"{file_name}.pkl")
    print("model_path", model_path)
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
            "n_train_anomalies": int((train_labels == 1).sum()) if train_labels is not None else None,
            "n_test_anomalies": int((test_labels == 1).sum()) if test_labels is not None else None
        }
    }

    metadata_path = os.path.join(model_dir, "metadata", f"{file_name}.yml")
    with open(metadata_path, "w") as f:
        yaml.safe_dump(metadata, f)
