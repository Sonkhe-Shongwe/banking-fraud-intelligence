"""Fit the fraud ranker and evaluate both policies at fixed daily review budgets."""

from typing import cast

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .transaction_features import MODEL_FEATURES


REVIEW_LIMITS = (50, 100)
AMOUNT_BOUNDARY = 220
POLICIES = {"Amount baseline": "TX_AMOUNT", "Logistic regression": "model_score"}


def fit_ranker(training: pd.DataFrame) -> Pipeline:
    """Fit the fixed model and its preprocessing on training rows."""
    model = Pipeline([
        ("impute", SimpleImputer(strategy="median", add_indicator=True)),
        ("scale", StandardScaler()),
        ("rank", LogisticRegression(solver="lbfgs", class_weight="balanced", C=1.0, max_iter=1000)),
    ])
    model.fit(training[list(MODEL_FEATURES)], training["TX_FRAUD"])
    return model


def score_transactions(model: Pipeline, transactions: pd.DataFrame) -> pd.DataFrame:
    """Attach the ranking score to the evaluation columns in source order."""
    scores = model.decision_function(transactions[list(MODEL_FEATURES)])
    return transactions[["TRANSACTION_ID", "TX_DATETIME", "TX_AMOUNT", "TX_FRAUD"]].assign(
        model_score=scores,
    )


def compare_review_queues(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return daily-budget metrics and average precision for both eligible cohorts."""
    queue_results = []
    precision_results = []
    populations = {
        "All transactions": scored,
        "Amount at or below 220": scored.loc[scored["TX_AMOUNT"] <= AMOUNT_BOUNDARY],
    }
    for cohort, population in populations.items():
        if population.empty:
            raise ValueError(f"No transactions in the {cohort} cohort.")
        event_time = cast(pd.Series, population["TX_DATETIME"])
        daily = population.assign(day=event_time.dt.normalize())
        fraud = daily.loc[daily["TX_FRAUD"].eq(1)]
        for policy, score_column in POLICIES.items():
            ranked = daily.sort_values(["day", score_column, "TRANSACTION_ID"], ascending=[True, False, True])
            by_day = ranked.groupby("day", sort=False)
            precision_results.append({
                "Cohort": cohort,
                "Policy": policy,
                "Average precision": average_precision_score(daily["TX_FRAUD"], daily[score_column])
                if len(fraud) else float("nan"),
            })
            for limit in REVIEW_LIMITS:
                queue = by_day.head(limit)
                caught = queue.loc[queue["TX_FRAUD"].eq(1)]
                queue_results.append({
                    "Cohort": cohort,
                    "Daily limit": limit,
                    "Policy": policy,
                    "Reviews": len(queue),
                    "Fraud caught": len(caught),
                    "Legitimate reviews": len(queue) - len(caught),
                    "Precision": len(caught) / len(queue),
                    "Recall": len(caught) / len(fraud) if len(fraud) else float("nan"),
                    "Fraud-labelled value caught": caught["TX_AMOUNT"].sum(),
                })

    return pd.DataFrame(queue_results), pd.DataFrame(precision_results)
