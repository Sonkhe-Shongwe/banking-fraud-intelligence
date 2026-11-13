"""Prepare and save local held-out transaction ranks for reporting."""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd

from .fraud_model import POLICIES, RESTRICTED_COHORT, eligible_populations, rank_daily


def build_rank_export(scored: pd.DataFrame) -> pd.DataFrame:
    """Return one row per transaction and separate ranks for each eligible cohort."""
    if not scored["TRANSACTION_ID"].is_unique:
        raise ValueError("The rank export requires unique transaction IDs.")

    export = scored.set_index("TRANSACTION_ID")
    for cohort, population in eligible_populations(scored).items():
        suffix = "le_220" if cohort == RESTRICTED_COHORT else "all"
        for score_column in POLICIES.values():
            ranked = rank_daily(population, score_column).set_index("TRANSACTION_ID")
            export[f"{score_column.lower()}_rank_{suffix}"] = ranked["review_rank"].astype("Int64")

    return export.reset_index()


def save_rank_export(export: pd.DataFrame, path: Path) -> None:
    """Write a complete CSV before replacing a previous local export."""
    with NamedTemporaryFile(dir=path.parent, suffix=".part", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        export.to_csv(temporary, index=False)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
