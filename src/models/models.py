import pandas as pd

from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, RobustScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from .utils import save_model_with_metadata
from src.utils.utils import save_objects


def model_if(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    cat_features: list[str],
    contamination: float = 0.05,
    random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fit Isolation Forest model on training data and predict anomaly for train and test sets.
    Returns train_df and test_df with 'isFraud' column.
    """
    train_if = train_df.copy()
    test_if = test_df.copy()

    orde = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    train_if[cat_features] = orde.fit_transform(train_if[cat_features])
    test_if[cat_features] = orde.transform(test_if[cat_features])

    iso_forest = IsolationForest(contamination=contamination, random_state=random_state)
    train_labels = iso_forest.fit_predict(train_if)
    train_if["isFraud"] = (train_labels == -1).astype(int)

    test_labels = iso_forest.predict(test_if)
    test_if["isFraud"] = (test_labels == -1).astype(int)

    save_objects(
        ordinal_encoder=orde
    )

    save_model_with_metadata(
        model=iso_forest,
        model_name="Isolation Forest",
        train_labels=train_if["isFraud"],
        test_labels=test_if["isFraud"],
        cat_features=cat_features,
        params={"contamination": contamination, "random_state": random_state},
    )

    return train_if, test_if


def model_lof(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    cat_features: list[str],
    num_features: list[str],
    contamination: float = 0.05
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fit LOF model on training data and predict anomaly for train and test sets.
    Returns train_df and test_df with 'isFraud' column.
    """
    train_lof = train_df.copy()
    test_lof = test_df.copy()

    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    cat_encoded_train = ohe.fit_transform(train_lof[cat_features])
    cat_encoded_train_df = pd.DataFrame(cat_encoded_train, 
                                        columns=ohe.get_feature_names_out(cat_features), 
                                        index=train_lof.index)
    train_lof_dropped = train_lof.drop(columns=cat_features)
    train_lof_encoded = pd.concat([train_lof_dropped, cat_encoded_train_df], axis=1)

    cat_encoded_test = ohe.transform(test_lof[cat_features])
    cat_encoded_test_df = pd.DataFrame(cat_encoded_test,
                                       columns=ohe.get_feature_names_out(cat_features),
                                       index=test_lof.index)
    test_lof_dropped = test_lof.drop(columns=cat_features)
    test_lof_encoded = pd.concat([test_lof_dropped, cat_encoded_test_df], axis=1)

    rbs = RobustScaler()
    train_lof_encoded[num_features] = rbs.fit_transform(train_lof_encoded[num_features])
    test_lof_encoded[num_features] = rbs.transform(test_lof_encoded[num_features])

    lof = LocalOutlierFactor(contamination=contamination, novelty=True)
    lof.fit(train_lof_encoded)
    train_labels = lof.predict(train_lof_encoded)
    test_labels = lof.predict(test_lof_encoded)

    train_lof_encoded["isFraud"] = (train_labels == -1).astype(int)
    test_lof_encoded["isFraud"] = (test_labels == -1).astype(int)

    save_objects(
        one_hot_encoder=ohe,
        robust_scaler=rbs
    )

    save_model_with_metadata(
        model=lof,
        model_name="Local Outlier Factor",
        train_labels=train_lof_encoded["isFraud"],
        test_labels=test_lof_encoded["isFraud"],
        cat_features=cat_features,
        num_features=num_features,
        params={"contamination": contamination},
    )

    return train_lof_encoded, test_lof_encoded
