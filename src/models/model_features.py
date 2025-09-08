import yaml
import pandas as pd


def get_model_features(
    train_df: pd.DataFrame, test_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Remove not-useful features from train and test DataFrames based on config.yml.
    """
    with open("config.yml", "r") as file:
        params = yaml.safe_load(file)

    train_df.drop(columns=params["not_usefull_features"], inplace=True)
    test_df.drop(column=params["not_usefull_features"], inplace=True)

    return train_df, test_df
