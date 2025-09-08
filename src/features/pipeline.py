import pandas as pd
import time
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
from utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(name="features")


def run_features_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Applies all feature engineering steps to the DataFrame with logging.
    """
    logger.info("Starting feature pipeline...")

    start = time.time()
    df = feature_extraction(df)
    df = feature_transformation(df)
    df = feature_without_data_leakage_risk(df)
    logger.info(f"Basic feature engineering complete in {time.time() - start:.2f}s")

    train_df, test_df = data_splitting(df)
    logger.info(f"Data split into train ({len(train_df)}) and test ({len(test_df)})")

    feature_functions = [
        add_rolling_features,
        add_group_based_features,
        add_unusual_usage_features,
        add_time_since_last_transaction,
    ]

    for func in feature_functions:
        start = time.time()
        train_df = func(train_df)
        test_df = func(test_df)
        logger.info(f"{func.__name__} applied in {time.time() - start:.2f}s")

    logger.info("All feature engineering steps completed.")

    return train_df, test_df
