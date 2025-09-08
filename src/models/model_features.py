import yaml
import os

import pandas as pd


def get_model_features(
    train_df: pd.DataFrame, test_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Remove not-useful features from train and test DataFrames based on config.yml.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    with open(config_path, "r") as file:
        params = yaml.safe_load(file)

    train_df.drop(columns=params["not_usefull_features"], inplace=True)
    test_df.drop(columns=params["not_usefull_features"], inplace=True)

    return train_df, test_df
