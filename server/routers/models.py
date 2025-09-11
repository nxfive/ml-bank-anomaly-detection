from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from server.schemas import Transaction
from src.models.inference import (MODELS, prepare_data,
                                  run_single_model_prediction)

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
def get_models():
    return {
        "available_models": list(
            model.title().replace("_", " ") for model in MODELS.keys()
        )
    }


@router.post("/{model_name}/predict")
def predict(
    model_name: Literal["isolation_forest", "local_outlier_factor"],
    data: list[Transaction],
) -> list[dict[str, Any]]:
    if model_name not in MODELS.keys():
        raise HTTPException(status_code=404, detail="Model not found")

    df_raw, df = prepare_data(data)
    df_raw["isFraud"] = run_single_model_prediction(model_name, df)

    return df_raw.to_dict(orient="records")


@router.post("/predict")
def predict_both(data: list[Transaction]) -> list[dict[str, Any]]:
    df_raw, df = prepare_data(data)

    pred_if = run_single_model_prediction("isolation_forest", df)
    pred_lof = run_single_model_prediction("local_outlier_factor", df)

    fraud = ((pred_if == -1) & (pred_lof == -1)).astype(int)

    df_raw["isFraud"] = fraud
    df_raw["if_pred"] = pred_if
    df_raw["lof_pred"] = pred_lof

    return df_raw.to_dict(orient="records")
