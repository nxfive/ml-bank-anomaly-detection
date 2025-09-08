import pandas as pd
from .utils import (
    add_rolling_features,
    add_group_based_features,
    add_unusual_usage_features,
    add_time_since_last_transaction,
)
from .features import (
    feature_extraction,
    feature_transformation,
    feature_without_data_leakage_risk,
    data_splitting,
)


def run_features_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Applies all feature engineering steps to the DataFrame.
    """
    df = feature_extraction(df)
    df = feature_transformation(df)
    df = feature_without_data_leakage_risk(df)

    train_df, test_df = data_splitting(df)

    feature_functions = [
        add_rolling_features,
        add_group_based_features,
        add_unusual_usage_features,
        add_time_since_last_transaction,
    ]

    for func in feature_functions:
        train_df = func(train_df)
        test_df = func(test_df)

    return train_df, test_df
