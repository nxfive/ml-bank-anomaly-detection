import os

import joblib
import numpy as np
import pandas as pd
from src.data.data import data_transform
from src.features.pipeline import run_features_pipeline
from src.models.model_features import get_model_features
from src.utils.paths import MODELS_DIR
from src.utils.utils import load_model_metadata


MODELS = {
    "isolation_forest": joblib.load(os.path.join(MODELS_DIR, "isolation_forest.pkl")),
    "local_outlier_factor": joblib.load(
        os.path.join(MODELS_DIR, "local_outlier_factor.pkl")
    ),
}


ENCODERS = {
    "isolation_forest": joblib.load(os.path.join(MODELS_DIR, "ordinal_encoder.pkl")),
    "local_outlier_factor": {
        "ohe": joblib.load(os.path.join(MODELS_DIR, "one_hot_encoder.pkl")),
        "rbs": joblib.load(os.path.join(MODELS_DIR, "robust_scaler.pkl")),
    },
}


def transform_features(model_name: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categorical features and scale numerical features for the given model.
    """
    params = load_model_metadata(model_name)
    if model_name == "isolation_forest":
        ord = ENCODERS[model_name]
        cat_features = params["features_processed"]["cat_features"]
        df.loc[:, cat_features] = ord.transform(df[cat_features])

    elif model_name == "local_outlier_factor":
        ohe = ENCODERS[model_name]["ohe"]
        rbs = ENCODERS[model_name]["rbs"]
        cat_features = params["features_processed"]["cat_features"]
        num_features = params["features_processed"]["num_features"]

        ohe_encoded = ohe.transform(df[cat_features])
        ohe_encoded_df = pd.DataFrame(
            ohe_encoded, columns=ohe.get_feature_names_out(cat_features), index=df.index
        )

        dropped_cat_df = df.drop(columns=cat_features)
        df = pd.concat([ohe_encoded_df, dropped_cat_df], axis=1)
        df[num_features] = rbs.transform(df[num_features])

    return df


def run_single_model_prediction(model_name: str, df: pd.DataFrame) -> np.ndarray:
    """
    Processes the data and returns predictions for the selected model.
    """
    df_encoded = transform_features(model_name, df.copy())
    model = MODELS[model_name]
    
    return model.predict(df_encoded)


def prepare_data(data: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare user-provided transaction data for model prediction.
    """
    df_raw = data_transform(pd.DataFrame([t.model_dump() for t in data]))
    df = run_features_pipeline(df_raw.copy(), split_data=False)
    df = get_model_features(df)
    
    return df_raw, df
