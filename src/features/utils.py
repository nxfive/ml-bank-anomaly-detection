import numpy as np
import pandas as pd


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds rolling mean features for TransactionAmount and TransactionDuration per AccountID.
    """
    df["rolling_mean_amount"] = (
        df.groupby("AccountID")["TransactionAmount"]
        .transform(lambda x: x.shift().rolling(window=2, min_periods=1).mean())
        .fillna(0)
    )

    df["rolling_mean_duration"] = (
        df.groupby("AccountID")["TransactionDuration"]
        .transform(lambda x: x.shift().rolling(window=2, min_periods=1).mean())
        .fillna(0)
    )

    return df


def add_group_based_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds per-account most frequent categorical values for IP, Location, Device and Merchant.
    """
    agg = df.groupby("AccountID").agg(
        most_frequent_ip=(
            "IP Address",
            lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        ),
        most_frequent_location=(
            "Location",
            lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        ),
        most_frequent_device=(
            "DeviceID",
            lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        ),
        most_frequent_merchant=(
            "MerchantID",
            lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        ),
    )

    df = df.merge(agg, on="AccountID", how="left").set_index(df.index)
    return df


def add_unusual_usage_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates boolean features indicating if current transaction deviates from most
    frequent account behavior.
    """
    df["is_not_most_frequent_ip"] = (
        df["IP Address"] != df["most_frequent_ip"]
    ).astype(int)

    df["is_not_most_frequent_location"] = (
        df["Location"] != df["most_frequent_location"]
    ).astype(int)

    df["is_not_most_frequent_device"] = (
        df["DeviceID"] != df["most_frequent_device"]
    ).astype(int)
    
    df["is_not_most_frequent_merchant"] = (
        df["MerchantID"] != df["most_frequent_merchant"]
    ).astype(int)

    return df


def add_time_since_last_transaction(df: pd.DataFrame) -> pd.DataFrame:
    """
    Measures time difference from previous transaction per AccountID.
    """
    df["time_since_last_transaction"] = (
        df.groupby("AccountID")
        .apply(lambda g: g.index.to_series().diff().dt.total_seconds())
        .reset_index(level=0, drop=True)
    ).fillna(0)

    return df
