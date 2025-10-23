import time

import pandas as pd
from src.utils.logger import logger

from .features import (
    data_splitting,
    feature_extraction,
    feature_transformation,
    feature_without_data_leakage_risk,
)
from .utils import (
    add_group_based_features,
    add_rolling_features,
    add_time_since_last_transaction,
    add_unusual_usage_features,
)


def run_features_pipeline(
    df: pd.DataFrame, split_data: bool = True
) -> tuple[pd.DataFrame, pd.DataFrame] | pd.DataFrame:
    """
    Applies all feature engineering steps to the DataFrame with logging.
    Optionally splits the data into training and testing sets.
    """
    logger.info("Starting feature pipeline...")

    start = time.time()
    df = df.copy()
    df = feature_extraction(df)
    df = feature_transformation(df)
    df = feature_without_data_leakage_risk(df)
    logger.info(f"Basic feature engineering complete in {time.time() - start:.2f}s")

    feature_functions = [
        add_rolling_features,
        add_group_based_features,
        add_unusual_usage_features,
        add_time_since_last_transaction,
    ]

    if split_data:
        train_df, test_df = data_splitting(df)
        logger.info(
            f"Data split into train ({len(train_df)}) and test ({len(test_df)})"
        )

        for func in feature_functions:
            start = time.time()
            train_df = func(train_df)
            test_df = func(test_df)
            logger.info(f"{func.__name__} applied in {time.time() - start:.2f}s")

        logger.info("All feature engineering steps completed.")
        return train_df, test_df

    else:
        for func in feature_functions:
            start = time.time()
            df = func(df)
            logger.info(f"{func.__name__} applied in {time.time() - start:.2f}s")

        logger.info("All feature engineering steps completed.")
        return df
