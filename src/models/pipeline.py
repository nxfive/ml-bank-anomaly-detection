import os
import time

import pandas as pd
import yaml

from src.utils.logger import logger

from .model_features import get_model_features
from .models import model_if, model_lof


model_mapper = {model_if: "isolation_forest", model_lof: "local_outlier_factor"}


def run_pipeline(
    train_df: pd.DataFrame, test_df: pd.DataFrame, model_fn: callable
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generic pipeline runner for anomaly detection models.
    """
    logger.info(f"Starting pipeline for model: {model_fn.__name__}")
    train_df, test_df = train_df.copy(), test_df.copy()
    start_pipeline = time.time()
    train_df, test_df = get_model_features(train_df, test_df)
    logger.info(f"Prepared train/test features: train={len(train_df)}, test={len(test_df)}")

    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    with open(config_path, "r") as file:
        params = yaml.safe_load(file)

    model_name = model_mapper[model_fn]
    logger.info(f"Model configuration loaded: {model_name}")

    model_params = dict(
        train_df=train_df,
        test_df=test_df,
        cat_features=params["cat_features"],
        contamination=params[model_name]["contamination"],
    )

    if params[model_name].get("random_state"):
        model_params["random_state"] = params[model_name]["random_state"]

    if params[model_name].get("preprocess_num_features", False):
        model_params["num_features"] = params["num_features"]

    logger.info(
        f"Running model {model_fn.__name__} with parameters: { 
            {k: v for k, v in model_params.items() if k != 'train_df' and k != 'test_df'} 
        }"
    )
    start_model = time.time()
    pred_train, pred_test = model_fn(**model_params)
    logger.info(
        f"Model {model_fn.__name__} completed in {time.time() - start_model:.2f}s"
    )
    logger.info(f"Pipeline finished in {time.time() - start_pipeline:.2f}s")

    return pred_train, pred_test


def run_lof_pipeline(
    train_df: pd.DataFrame, test_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    return run_pipeline(
        train_df,
        test_df,
        model_fn=model_lof
    )


def run_if_pipeline(
    train_df: pd.DataFrame, test_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    return run_pipeline(
        train_df,
        test_df,
        model_fn=model_if
    )
