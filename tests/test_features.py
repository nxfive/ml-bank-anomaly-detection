import numpy as np
import pandas as pd
from src.features.features import (
    data_splitting, 
    feature_extraction,
    feature_transformation,
    feature_without_data_leakage_risk
)
from src.features.utils import (
    add_group_based_features,
    add_rolling_features,
    add_time_since_last_transaction,
    add_unusual_usage_features
)


def test_feature_extraction_columns(indexed_df):
    df = feature_extraction(indexed_df)
    assert all(col in df.columns for col in ["Year", "Month", "Day", "Weekday", "Hour"])


def test_feature_transformation(indexed_df):
    df = feature_extraction(indexed_df)
    df = feature_transformation(df)
    
    for col in [
        "month_sin", "month_cos", "weekday_sin", "weekday_cos", "day_sin", "day_cos"
    ]:
        assert col in df.columns
        assert np.issubdtype(df[col].dtype, np.floating)
        assert df[col].between(-1, 1).all()


def test_feature_without_data_leakage_risk(indexed_df):
    df = feature_without_data_leakage_risk(indexed_df)

    assert "exceeds_75_percent_balance" in df.columns
    assert np.issubdtype(df["exceeds_75_percent_balance"].dtype, np.integer)
    assert df["exceeds_75_percent_balance"].isin([0, 1]).all()


def test_data_splitting_ratio(indexed_df):
    train, test = data_splitting(indexed_df, test_ratio=0.5)
    assert len(test) == 0.5 * len(indexed_df)
    assert len(train) == len(test)


def test_add_rolling_features():
    df = pd.DataFrame({
        "AccountID": [1, 1, 1, 2, 2],
        "TransactionAmount": [100, 200, 300, 50, 150],
        "TransactionDuration": [10, 20, 30, 5, 15],
        "TransactionDate": pd.date_range("2025-01-01", periods=5)
    }).set_index("TransactionDate")

    df = add_rolling_features(df)

    expected_amount = [0, 100, 150, 0, 50]
    expected_duration = [0, 10, 15, 0, 5]

    np.testing.assert_array_equal(df["rolling_mean_amount"].values, expected_amount)
    np.testing.assert_array_equal(df["rolling_mean_duration"].values, expected_duration)


def test_add_group_based_features(df_with_cat_features):
    df = df_with_cat_features
    df = add_group_based_features(df)

    features = [
        "most_frequent_ip", "most_frequent_location", "most_frequent_device", "most_frequent_merchant"
    ]

    assert all(col in df.columns for col in features)

    account_1 = df[df["AccountID"] == 1].iloc[0]
    assert account_1["most_frequent_ip"] == "10.0.0.1"
    assert account_1["most_frequent_location"] == "NY"
    assert account_1["most_frequent_device"] == "dev1"
    assert account_1["most_frequent_merchant"] == "m1"

    account_3 = df[df["AccountID"] == 3].iloc[0]
    assert all(not pd.isna(account_3[col]) for col in features)


def test_add_unusual_usage_features(df_with_cat_features):
    df = df_with_cat_features

    features = [
        "is_not_most_frequent_ip",
        "is_not_most_frequent_location",
        "is_not_most_frequent_device",
        "is_not_most_frequent_merchant"
    ]
    df = add_group_based_features(df)
    df = add_unusual_usage_features(df)

    assert all(col in df.columns for col in features)

    account_1 = df[df["AccountID"] == 1].iloc[0]
    assert all(account_1[feature] == 0 for feature in features)

    account_3 = df[df["AccountID"] == 3].iloc[0]
    assert all(account_3[feature] == 0 for feature in features)


def test_add_time_since_last_transaction():
    df = pd.DataFrame({
        "AccountID": [1, 1, 2, 2, 2],
        "TransactionAmount": [100, 200, 150, 300, 250],
        "TransactionDate": [
            "2023-01-01 10:00:00",
            "2023-01-01 11:00:00",
            "2023-01-02 09:00:00",
            "2023-01-02 12:00:00",
            "2023-01-02 15:30:00"
        ]
    })
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])
    df = df.set_index("TransactionDate")

    df = add_time_since_last_transaction(df)
    assert "time_since_last_transaction" in df.columns

    assert df[df["AccountID"] == 1]["time_since_last_transaction"].iloc[0] == 0
    assert df[df["AccountID"] == 2]["time_since_last_transaction"].iloc[0] == 0

    delta_1 = (df[df["AccountID"] == 1].index[1] - df[df["AccountID"] == 1].index[0]).total_seconds()
    assert df[df["AccountID"] == 1]["time_since_last_transaction"].iloc[1] == delta_1
    
    delta_2 = (df[df["AccountID"] == 2].index[1] - df[df["AccountID"] == 2].index[0]).total_seconds()
    assert df[df["AccountID"] == 2]["time_since_last_transaction"].iloc[1] == delta_2
    
    delta_3 = (df[df["AccountID"] == 2].index[2] - df[df["AccountID"] == 2].index[1]).total_seconds()
    assert df[df["AccountID"] == 2]["time_since_last_transaction"].iloc[2] == delta_3
