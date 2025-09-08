import pandas as pd
import os


def read_data() -> pd.DataFrame:
    """
    Load raw bank transactions CSV into a pandas DataFrame.
    """
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    csv_path = os.path.join(PROJECT_ROOT, "data", "raw", "bank_transactions_data.csv")
    df = pd.read_csv(csv_path)

    return df


def data_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns to datetime and set index to TransactionDate.
    """
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])
    df["PreviousTransactionDate"] = pd.to_datetime(df["PreviousTransactionDate"])
    df = df.set_index("TransactionDate").sort_index()

    return df
