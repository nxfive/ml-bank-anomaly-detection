import yaml
import os

import pandas as pd


def get_model_features(
    train_df: pd.DataFrame, test_df: pd.DataFrame | None = None
) -> tuple[pd.DataFrame, pd.DataFrame] | pd.DataFrame:
    """
    Remove not-useful features from train/test DataFrames or from a single DataFrame
    based on config.yml.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    with open(config_path, "r") as file:
        params = yaml.safe_load(file)

    drop_cols = params["not_usefull_features"]

    if test_df is not None:
        train_df, test_df = train_df.copy(), test_df.copy()
        return (
            train_df.drop(columns=drop_cols, errors="ignore"),
            test_df.drop(columns=drop_cols, errors="ignore"),
        )
    else:
        train_df = train_df.copy()
        return train_df.drop(columns=drop_cols, errors="ignore")
