from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from src.models.model_features import get_model_features
from src.models.models import model_if, model_lof
from src.models.utils import save_model_with_metadata


def test_get_model_features(prepared_df, config_file):
    train_df, test_df = prepared_df
    train, test = get_model_features(train_df.copy(), test_df.copy())

    params = config_file

    for cols in params["not_usefull_features"]:
        assert cols not in train.columns
        assert cols not in test.columns


@pytest.mark.parametrize(
    "model_fn, extra_params",
    [
        (model_if, {}),  
        (model_lof, {"num_features": "num_features"}), 
    ]
)
def test_models(prepared_df, config_file, model_fn, extra_params):
    train_df, test_df = prepared_df
    train, test = get_model_features(train_df.copy(), test_df.copy())

    model_params = {
        "train_df": train,
        "test_df": test,
        "cat_features": config_file["cat_features"]
    }

    if extra_params:
        for key, value in extra_params.items():
            model_params[key] = config_file[value]

    train_pred, test_pred = model_fn(**model_params)

    for df, df_pred in [(train_df, train_pred), (test_df, test_pred)]:
        assert "isFraud" in df_pred.columns
        assert len(df) == len(df_pred)
        assert np.issubdtype(df_pred["isFraud"].dtype, np.integer)
        assert np.all(np.isin(df_pred["isFraud"].values, [0, 1]))


class DummyModel:
    def fit(self): pass
    def predict(self): pass


def test_save_model_with_metadata_mock():
    model = DummyModel()
    train_preds = np.array([0, 1, 0])
    test_preds = np.array([1, 0])
    cat_features = ["cat1", "cat2"]
    num_features = [1, 2]
    params = {"param1": 10}
    model_name = "Test Model"

    with patch("joblib.dump") as mock_dump, \
         patch("builtins.open", new_callable=MagicMock) as mock_open:

        save_model_with_metadata(
            model=model,
            model_name=model_name,
            train_preds=train_preds,
            test_preds=test_preds,
            cat_features=cat_features,
            num_features=num_features,
            params=params
        )

        assert mock_dump.call_count == 1
        args, _ = mock_dump.call_args
        assert args[0] is model
        assert args[1].endswith("test_model.pkl")  

        mock_open.assert_called()
        metadata_path = mock_open.call_args[0][0]
        assert metadata_path.endswith("metadata/test_model.yml")
