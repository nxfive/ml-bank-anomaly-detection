from src.features.pipeline import run_features_pipeline
from src.models.pipeline import model_mapper, run_pipeline


def test_run_features_pipeline(indexed_df, config_file):
    
    train_df, test_df = run_features_pipeline(indexed_df)

    assert len(train_df.columns) > len(indexed_df.columns)
    assert len(train_df.columns) == len(test_df.columns)

    params = config_file

    expected_columns = params["cat_features"] + params["num_features"] + params["not_usefull_features"]

    for col in expected_columns:
        assert col in train_df.columns
        assert col in test_df.columns


def test_run_pipeline_with_dummy_model(prepared_df):
    train_df, test_df = prepared_df  

    def dummy_model(train_df, test_df, **kwargs):
        return train_df.assign(pred=1), test_df.assign(pred=0)

    model_mapper[dummy_model] = "isolation_forest"

    pred_train, pred_test = run_pipeline(train_df.copy(), test_df.copy(), model_fn=dummy_model)

    assert "pred" in pred_train.columns
    assert "pred" in pred_test.columns
