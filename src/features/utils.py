import numpy as np
import pandas as pd


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds rolling mean features for TransactionAmount and TransactionDuration per AccountID.
    """
    df = df.copy()
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
    df = df.copy()
    agg = df.groupby("AccountID").agg(
        most_frequent_ip=(
            "IPAddress",
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
    df = df.copy()
    df["is_not_most_frequent_ip"] = (
        df["IPAddress"] != df["most_frequent_ip"]
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
    df = df.copy()
    df = df.sort_values(by=["AccountID"])

    ts_list = []
    for _, group in df.groupby("AccountID"):
        diff_seconds = group.index.to_series().diff().dt.total_seconds().copy()
        diff_seconds.iloc[0] = 0
        ts_list.append(diff_seconds)

    ts = pd.concat(ts_list)
    df["time_since_last_transaction"] = ts.loc[df.index]

    return df
