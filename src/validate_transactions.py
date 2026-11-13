"""Validate the local fraud transaction CSV and report its data quality."""

import argparse
import csv
from pathlib import Path
import warnings

import pandas as pd

if __package__:
    from .convert_transactions import COLUMNS, OUTPUT
else:
    from convert_transactions import COLUMNS, OUTPUT


DATASET_START = pd.Timestamp("2018-04-01")
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
SOURCE_DTYPES = dict.fromkeys(COLUMNS, "Int64")
SOURCE_DTYPES.update(TX_DATETIME="string", TX_AMOUNT="float64")


def load_transactions(path: Path = OUTPUT) -> pd.DataFrame:
    """Return validated, typed transactions in source order or raise an error."""
    with path.open(encoding="utf-8-sig", newline="") as source:
        if tuple(next(csv.reader(source), ())) != COLUMNS:
            raise ValueError(f"Expected the nine source columns in this order: {', '.join(COLUMNS)}.")
        source.seek(0)
        with warnings.catch_warnings():
            # Disable implicit index inference and fail if pandas would truncate fields.
            warnings.simplefilter("error", pd.errors.ParserWarning)
            try:
                transactions = pd.read_csv(
                    source, dtype=SOURCE_DTYPES, float_precision="round_trip",
                    index_col=False, skip_blank_lines=False,
                )
            except pd.errors.ParserWarning as error:
                raise ValueError("CSV rows contain more fields than the header.") from error
    if transactions.empty:
        raise ValueError("The CSV contains no transactions.")

    missing = transactions.isna().sum()
    if missing.any():
        details = ", ".join(f"{column}: {count:,}" for column, count in missing[missing.gt(0)].items())
        raise ValueError(f"Missing values by column: {details}.")

    event_time = pd.to_datetime(
        transactions["TX_DATETIME"], format=TIMESTAMP_FORMAT, errors="coerce",
    )
    if event_time.isna().any():
        raise ValueError(f"Invalid TX_DATETIME values: {event_time.isna().sum():,}.")
    transactions["TX_DATETIME"] = event_time
    elapsed = event_time - DATASET_START
    identifiers = transactions[["TRANSACTION_ID", "CUSTOMER_ID", "TERMINAL_ID"]]
    amounts = transactions["TX_AMOUNT"]
    labels = transactions["TX_FRAUD"]
    scenarios = transactions["TX_FRAUD_SCENARIO"]
    checks = {
        "duplicate TRANSACTION_ID values": transactions["TRANSACTION_ID"].duplicated().sum(),
        "negative identifier rows": identifiers.lt(0).any(axis=1).sum(),
        "negative or non-finite TX_AMOUNT values": (~(amounts.ge(0) & amounts.lt(float("inf")))).sum(),
        "timestamps before the dataset start": event_time.lt(DATASET_START).sum(),
        "rows out of chronological order": event_time.diff().lt(pd.Timedelta(0)).sum(),
        "TX_TIME_SECONDS mismatches": transactions["TX_TIME_SECONDS"].ne(elapsed.dt.total_seconds()).sum(),
        "TX_TIME_DAYS mismatches": transactions["TX_TIME_DAYS"].ne(elapsed.dt.days).sum(),
        "invalid TX_FRAUD values": (~labels.isin([0, 1])).sum(),
        "invalid TX_FRAUD_SCENARIO values": (~scenarios.isin([0, 1, 2, 3])).sum(),
        "fraud label and scenario disagreements": labels.ne(scenarios.ne(0)).sum(),
    }
    failures = [f"{name}: {count:,}" for name, count in checks.items() if count]
    if failures:
        raise ValueError("\n".join(failures))
    return transactions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=OUTPUT, help="Path to the combined CSV.")
    options = parser.parse_args()
    try:
        transactions = load_transactions(options.input)
    except FileNotFoundError:
        parser.exit(1, f"CSV not found at {options.input}. See data/README.md to prepare it.\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Validation failed for {options.input}:\n{error}\n")

    event_time = transactions["TX_DATETIME"]
    rows = len(transactions)
    observed_days = event_time.dt.normalize().nunique()
    print(f"Validation passed: {options.input}")
    print(f"Rows read: {rows:,} | Rows ready: {rows:,} | Rows dropped: 0")
    print("Preparation: parsed timestamps and numeric types. No source values corrected.")
    print(f"Coverage: {event_time.min():%Y-%m-%d} to {event_time.max():%Y-%m-%d} ({observed_days:,} days)")
    print(f"Fraud labels: {transactions['TX_FRAUD'].sum():,}")
    print(f"Zero-amount rows retained: {transactions['TX_AMOUNT'].eq(0).sum():,}")
    print("Checks passed: schema, required values, keys, amounts, event order, elapsed time and fraud fields.")


if __name__ == "__main__":
    main()
