import os

import pandas as pd
from src.utils.paths import RAW_DATA_DIR


def read_data() -> pd.DataFrame:
    """
    Load raw bank transactions CSV into a pandas DataFrame.
    """
    csv_path = os.path.join(RAW_DATA_DIR, "bank_transactions_data.csv")
    df = pd.read_csv(csv_path)
    df.rename(columns={"IP Address": "IPAddress"}, inplace=True)

    return df


def data_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns to datetime and set index to TransactionDate.
    """
    df = df.copy()
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])
    df["PreviousTransactionDate"] = pd.to_datetime(df["PreviousTransactionDate"])
    df = df.set_index("TransactionDate").sort_index()

    return df
