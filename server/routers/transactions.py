import os
from typing import Any

import pandas as pd
from fastapi import APIRouter, HTTPException
from src.utils.paths import PROCESSED_DATA_DIR

router = APIRouter(prefix="/transactions", tags=["transactions"])

PREDICTED_DATA = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "df_predicted.parquet"))


@router.get("/")
def get_all_transactions() -> list[dict[str, Any]]:
    return PREDICTED_DATA.to_dict(orient="records")


@router.get("/{account_id}")
def get_transactions_by_account_id(account_id: str) -> list[dict[str, Any]]:
    if account_id not in set(PREDICTED_DATA["AccountID"]):
        raise HTTPException(status_code=404, detail="Account ID not found")

    df_account = PREDICTED_DATA[PREDICTED_DATA["AccountID"] == account_id]
    return df_account.to_dict(orient="records")
