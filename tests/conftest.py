import os

import pandas as pd
import pytest
import yaml
from src.data.data import data_transform, read_data
from src.features.features import data_splitting
from src.features.pipeline import run_features_pipeline


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "TransactionDate": ["2023-04-11 16:29:14", "2023-06-27 16:44:19", "2023-07-10 18:16:08"],
        "PreviousTransactionDate": ["2024-11-04 08:08:08", "2024-11-04 08:09:35", "2024-11-04 08:07:04"],
    })


@pytest.fixture
def indexed_df():
    df = read_data()[:100]
    df = data_transform(df)
    return df


@pytest.fixture
def splitted_df(indexed_df):
    train_df, test_df = data_splitting(indexed_df.sort_index(), test_ratio=0.3)
    return train_df, test_df


@pytest.fixture
def df_with_cat_features():
    return pd.DataFrame({
        "AccountID": [1, 1, 1, 2, 2, 3],
        "IP Address": ["10.0.0.1", "10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"],
        "Location": ["NY", "NY", "LA", "LA", "SF", "LA"],
        "DeviceID": ["dev1", "dev1", "dev2", "dev3", "dev4", "dev5"],
        "MerchantID": ["m1", "m1", "m2", "m2", "m3", "m3"]
    })


@pytest.fixture
def prepared_df(indexed_df):
    train_df,  test_df = run_features_pipeline(indexed_df.copy())
    return train_df, test_df


@pytest.fixture
def config_file():
    config_path = os.path.join(os.path.dirname(__file__), "../src/models/config.yml")
    with open(config_path, "r") as file:
        params = yaml.safe_load(file)
    return params
