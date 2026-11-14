"""Reconcile the local Power BI Overview CSV against the validated source."""

from pathlib import Path

import pandas as pd

from .convert_transactions import OUTPUT
from .validate_transactions import load_transactions


OVERVIEW = OUTPUT.parent / "powerbi" / "Overview_Daily.csv"
VALUE_COLUMN = "FraudLabelledTransactionValue"


def reconcile_overview(source: Path, overview: Path) -> int:
    transactions = load_transactions(source)
    dates = transactions["TX_DATETIME"].dt.normalize()
    labels = transactions["TX_FRAUD"]
    amounts = transactions["TX_AMOUNT"]
    above_220 = amounts.gt(220)
    at_or_below_220 = amounts.le(220)

    # Aggregate directly from source rows, retaining their shared row index.
    daily_counts = pd.DataFrame({
        "Date": dates,
        "TransactionCount": 1,
        "FraudLabelledCount": labels,
        "Above220TransactionCount": above_220.astype("int64"),
        "Above220FraudLabelledCount": labels * above_220,
        "AtOrBelow220TransactionCount": at_or_below_220.astype("int64"),
        "AtOrBelow220FraudLabelledCount": labels * at_or_below_220,
    }).groupby("Date").sum()
    fraud_labelled = labels.eq(1)
    daily_value = (
        amounts[fraud_labelled].groupby(dates[fraud_labelled]).sum()
        .reindex(daily_counts.index, fill_value=0)
        .rename(VALUE_COLUMN)
    )

    exported = pd.read_csv(overview, dtype={"Date": "string"}, float_precision="round_trip")
    exported["Date"] = pd.to_datetime(exported["Date"], format="%Y-%m-%d")
    exported = exported.set_index("Date", verify_integrity=True).sort_index()

    pd.testing.assert_index_equal(exported.index, daily_counts.index)
    pd.testing.assert_frame_equal(
        exported[daily_counts.columns],
        daily_counts,
        check_dtype=False,
        check_exact=True,
    )
    pd.testing.assert_series_equal(
        exported[VALUE_COLUMN],
        daily_value,
        check_dtype=False,
        check_exact=False,
        rtol=0,
        atol=1e-6,
    )
    return len(exported)


def main() -> None:
    days = reconcile_overview(OUTPUT, OVERVIEW)
    print(f"PASS: all seven Overview_Daily metrics match the validated source on {days:,} dates.")


if __name__ == "__main__":
    main()
