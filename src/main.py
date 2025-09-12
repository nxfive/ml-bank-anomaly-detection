from src.data.data import read_data, data_transform
from src.features.pipeline import run_features_pipeline
from src.models.pipeline import run_if_pipeline, run_lof_pipeline
from src.utils.utils import save_objects
from src.utils.logger import setup_logging, get_logger

import pandas as pd
import logging

setup_logging()
logger = get_logger(name="main")


def main():
    logger.info("Starting main pipeline...")

    df_raw = read_data()
    logger.info(f"Data loaded: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")

    df = data_transform(df_raw)
    logger.info("Data transformation complete")

    train_df, test_df = run_features_pipeline(df)
    logger.info(
        f"Feature pipeline completed: train={len(train_df)}, test={len(test_df)}"
    )

    # Isolation Forest
    logger.info("Running Isolation Forest model...")
    pred_if_train, pred_if_test = run_if_pipeline(
        train_df=train_df, test_df=test_df
    )
    logger.info("Isolation Forest completed")

    # Local Outlier Factor
    logger.info("Running Local Outlier Factor model...")
    pred_lof_train, pred_lof_test = run_lof_pipeline(
        train_df=train_df, test_df=test_df
    )
    logger.info("Local Outlier Factor completed")

    df_if_full = pd.concat([pred_if_train, pred_if_test]).sort_index()
    df_lof_full = pd.concat([pred_lof_train, pred_lof_test]).sort_index()

    df["common_fraud"] = (
        (df_if_full["isFraud"] == 1) & (df_lof_full["isFraud"] == 1)
    )
    logger.info("Merged model predictions: 'common_fraud' column added")

    save_objects(
        train_df=train_df,
        test_df=test_df,
        pred_if_train=pred_if_train,
        pred_if_test=pred_if_test,
        pred_lof_train=pred_lof_train,
        pred_lof_test=pred_lof_test,
        df_predicted=df,
    )
    logger.info("All processed data saved successfully")


if __name__ == "__main__":
    main()
    logging.shutdown()
