"""Build scoring-time features and chronological partitions for the pinned dataset."""

from typing import cast

import numpy as np
import pandas as pd

from .validate_transactions import DATASET_START


DAY_SECONDS = 24 * 60 * 60
SPLIT_PERIODS = {
    "train": (DATASET_START, pd.Timestamp("2018-08-01")),
    "validation": (pd.Timestamp("2018-08-01"), pd.Timestamp("2018-09-01")),
    "test": (pd.Timestamp("2018-09-01"), pd.Timestamp("2018-10-01")),
}
MODEL_FEATURES = (
    "TX_AMOUNT",
    "customer_tx_count_24h", "customer_tx_count_7d",
    "terminal_tx_count_24h", "terminal_tx_count_7d",
    "customer_mean_amount_7d", "customer_seconds_since_previous",
)
FEATURE_TABLE_COLUMNS = (
    "TRANSACTION_ID", "TX_DATETIME", "TX_FRAUD", "TX_FRAUD_SCENARIO", "TX_AMOUNT",
)


def build_features(transactions: pd.DataFrame) -> pd.DataFrame:
    """Use validated, chronological input and retain one feature row per transaction."""
    times = cast(pd.Series, transactions["TX_DATETIME"])
    if not times.is_monotonic_increasing:
        raise ValueError("Feature input must be in chronological order.")

    seconds = times.to_numpy(dtype="datetime64[s]").astype(np.int64)
    amounts = transactions["TX_AMOUNT"].to_numpy(dtype=np.float64)
    row_count = len(transactions)
    features = transactions[list(FEATURE_TABLE_COLUMNS)].copy()
    mean_amount = np.full(row_count, np.nan)
    previous_seconds = np.full(row_count, np.nan)

    for entity, key in (("customer", "CUSTOMER_ID"), ("terminal", "TERMINAL_ID")):
        count_24h = np.zeros(row_count, dtype=np.int64)
        count_7d = np.zeros(row_count, dtype=np.int64)
        for positions in transactions.groupby(key, sort=False).indices.values():
            history = seconds[positions]
            # The left insertion point excludes all events at the current timestamp.
            end = np.searchsorted(history, history, side="left")
            start_24h = np.searchsorted(history, history - DAY_SECONDS, side="left")
            start_7d = np.searchsorted(history, history - 7 * DAY_SECONDS, side="left")
            count_24h[positions] = end - start_24h
            count_7d[positions] = end - start_7d

            if entity == "customer":
                totals = np.concatenate(([0.0], np.cumsum(amounts[positions])))
                has_recent = end > start_7d
                mean_amount[positions[has_recent]] = (
                    (totals[end[has_recent]] - totals[start_7d[has_recent]]) / count_7d[positions[has_recent]]
                )
                has_previous = end > 0
                previous_seconds[positions[has_previous]] = history[has_previous] - history[end[has_previous] - 1]

        features[f"{entity}_tx_count_24h"] = count_24h
        features[f"{entity}_tx_count_7d"] = count_7d

    features["customer_mean_amount_7d"] = mean_amount
    features["customer_seconds_since_previous"] = previous_seconds
    return features


def split_features(features: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Assign the full feature table to the three fixed, half-open date ranges."""
    times = cast(pd.Series, features["TX_DATETIME"])
    partitions = {
        name: features.loc[(times >= start) & (times < stop)]
        for name, (start, stop) in SPLIT_PERIODS.items()
    }
    if sum(len(partition) for partition in partitions.values()) != len(features):
        raise ValueError("The feature table contains timestamps outside April–September 2018 or missing timestamps.")
    if any(partition.empty for partition in partitions.values()):
        raise ValueError("Training, validation and test periods each require transactions.")
    return partitions
