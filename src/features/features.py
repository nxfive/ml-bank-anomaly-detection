import numpy as np
import pandas as pd


def feature_extraction(df: pd.DataFrame) -> pd.DataFrame:
    df["Year"] = df.index.year
    df["Month"] = df.index.month
    df["Day"] = df.index.day
    df["Weekday"] = df.index.weekday
    df["Hour"] = df.index.hour

    return df


def feature_transformation(df: pd.DataFrame) -> pd.DataFrame:
    df["month_sin"] = np.sin(2 * np.pi * df["Month"]/12)
    df["month_cos"] = np.cos(2 * np.pi * df["Month"]/12)
    df["weekday_sin"] = np.sin(2 * np.pi * df["Weekday"]/7)
    df["weekday_cos"] = np.cos(2 * np.pi * df["Weekday"]/7)
    df["day_sin"] = np.sin(2 * np.pi * df["Day"]/31)
    df["day_cos"] = np.sin(2 * np.pi * df["Day"]/31)

    return df


def feature_without_data_leakage_risk(df: pd.DataFrame) -> pd.DataFrame:
    df["exceeds_75_percent_balance"] = df["TransactionAmount"] >= 0.75 * (df["TransactionAmount"] + df["AccountBalance"]).astype(int)

    return df 


def data_splitting(df: pd.DataFrame, test_ratio=0.1) -> tuple[pd.DataFrame, pd.DataFrame]:
    n = len(df)
    test_size = int(n * test_ratio)

    train_df = df.iloc[:-test_size].copy()
    test_df = df.iloc[-test_size:].copy()

    return train_df, test_df
