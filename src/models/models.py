import pandas as pd

from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, RobustScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from .utils import save_model_with_metadata
from src.utils.utils import save_objects

import logging
from src.utils.logger import logger


def model_if(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    cat_features: list[str],
    contamination: float = 0.05,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fit Isolation Forest model on training data and predict anomaly for train and test sets.
    Returns train_df and test_df with 'isFraud' column.
    """
    train_df, test_df = train_df.copy(), test_df.copy()

    # scale numeric features
    orde = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    train_df[cat_features] = orde.fit_transform(train_df[cat_features])
    test_df[cat_features] = orde.transform(test_df[cat_features])

    # fit and predict
    iso_forest = IsolationForest(contamination=contamination, random_state=random_state)
    train_preds = iso_forest.fit_predict(train_df)
    test_preds = iso_forest.predict(test_df)

    train_df["isFraud"] = (train_preds == -1).astype(int)
    test_df["isFraud"] = (test_preds == -1).astype(int)

    save_objects(ordinal_encoder=orde)

    save_model_with_metadata(
        model=iso_forest,
        model_name="Isolation Forest",
        train_preds=train_df["isFraud"],
        test_preds=test_df["isFraud"],
        cat_features=cat_features,
        params={"contamination": contamination, "random_state": random_state},
    )

    return train_df, test_df


def model_lof(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    cat_features: list[str],
    num_features: list[str],
    contamination: float = 0.05,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fit LOF model on training data and predict anomaly for train and test sets.
    Returns train_df and test_df with 'isFraud' column.
    """
    train_df, test_df = train_df.copy(), test_df.copy()

    # encode categorical features
    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    train_cat = pd.DataFrame(
        ohe.fit_transform(train_df[cat_features]),
        columns=ohe.get_feature_names_out(cat_features),
        index=train_df.index,
    )
    test_cat = pd.DataFrame(
        ohe.transform(test_df[cat_features]),
        columns=ohe.get_feature_names_out(cat_features),
        index=test_df.index,
    )

    train_encoded = pd.concat([train_df.drop(columns=cat_features), train_cat], axis=1)
    test_encoded = pd.concat([test_df.drop(columns=cat_features), test_cat], axis=1)

    # scale numeric features
    rbs = RobustScaler()
    train_encoded[num_features] = rbs.fit_transform(train_encoded[num_features])
    test_encoded[num_features] = rbs.transform(test_encoded[num_features])

    # === debug ===
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Comparing columns and data types before LOF...")

        missing_cols = [
            col for col in train_encoded.columns if col not in test_encoded.columns
        ]
        if missing_cols:
            logger.debug(f"Missing columns in test_encoded: {missing_cols}")

        # Check column order
        same_order = all(train_encoded.columns == test_encoded.columns)
        logger.debug(f"Column order identical: {same_order}")

        # Check data types
        same_dtype = all(
            train_encoded[col].dtype == test_encoded[col].dtype
            for col in train_encoded.columns
        )
        logger.debug(f"Column data types identical: {same_dtype}")
    # ========

    # fit and predict
    train_X = train_encoded.values.astype(float)
    test_X = test_encoded.values.astype(float)

    lof = LocalOutlierFactor(contamination=contamination, novelty=True)
    lof.fit(train_X)

    train_preds = lof.predict(train_X)
    test_preds = lof.predict(test_X)

    train_encoded["isFraud"] = (train_preds == -1).astype(int)
    test_encoded["isFraud"] = (test_preds == -1).astype(int)

    save_objects(one_hot_encoder=ohe, robust_scaler=rbs)

    save_model_with_metadata(
        model=lof,
        model_name="Local Outlier Factor",
        train_preds=train_encoded["isFraud"],
        test_preds=test_encoded["isFraud"],
        cat_features=cat_features,
        num_features=num_features,
        params={"contamination": contamination},
    )

    return train_encoded, test_encoded
