from typing import Any, Literal

from fastapi import APIRouter, HTTPException

from services.server.app.schemas import Transaction
from src.models.inference import (MODELS, prepare_data,
                                  run_single_model_prediction)

from .metrics import track_metrics

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
def get_models():
    return {
        "available_models": list(
            model.title().replace("_", " ") for model in MODELS.keys()
        )
    }


@router.post("/{model_name}/predict")
@track_metrics
async def predict(
    model_name: Literal["isolation_forest", "local_outlier_factor"],
    data: list[Transaction],
) -> list[dict[str, Any]]:
    if model_name not in MODELS.keys():
        raise HTTPException(status_code=404, detail="Model not found")

    df_raw, df = prepare_data(data)
    df_raw["isFraud"] = (run_single_model_prediction(model_name, df) == -1)

    return df_raw.to_dict(orient="records")


@router.post("/predict")
@track_metrics
async def predict_both(data: list[Transaction]) -> list[dict[str, Any]]:
    df_raw, df = prepare_data(data)

    pred_if = run_single_model_prediction("isolation_forest", df)
    pred_lof = run_single_model_prediction("local_outlier_factor", df)

    df_raw["if_pred"] = (pred_if == -1)
    df_raw["lof_pred"] = (pred_lof == -1)
    df_raw["isFraud"] = df_raw["if_pred"] & df_raw["lof_pred"]

    return df_raw.to_dict(orient="records")
