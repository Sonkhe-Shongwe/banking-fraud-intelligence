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
FULL_COHORT = "All transactions"
RESTRICTED_COHORT = "Amount at or below 220"


def eligible_populations(scored: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        FULL_COHORT: scored,
        RESTRICTED_COHORT: scored.loc[scored["TX_AMOUNT"] <= AMOUNT_BOUNDARY],
    }


def rank_daily(population: pd.DataFrame, score_column: str) -> pd.DataFrame:
    """Assign one-based daily ranks, breaking score ties by transaction ID."""
    event_time = cast(pd.Series, population["TX_DATETIME"])
    ranked = population.assign(day=event_time.dt.normalize()).sort_values(
        ["day", score_column, "TRANSACTION_ID"], ascending=[True, False, True],
    )
    return ranked.assign(review_rank=ranked.groupby("day", sort=False).cumcount() + 1)


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
    for cohort, population in eligible_populations(scored).items():
        if population.empty:
            raise ValueError(f"No transactions in the {cohort} cohort.")
        fraud_total = int(population["TX_FRAUD"].sum())
        for policy, score_column in POLICIES.items():
            ranked = rank_daily(population, score_column)
            precision_results.append({
                "Cohort": cohort,
                "Policy": policy,
                "Average precision": average_precision_score(population["TX_FRAUD"], population[score_column])
                if fraud_total else float("nan"),
            })
            for limit in REVIEW_LIMITS:
                queue = ranked.loc[ranked["review_rank"] <= limit]
                caught = queue.loc[queue["TX_FRAUD"].eq(1)]
                queue_results.append({
                    "Cohort": cohort,
                    "Daily limit": limit,
                    "Policy": policy,
                    "Reviews": len(queue),
                    "Fraud caught": len(caught),
                    "Legitimate reviews": len(queue) - len(caught),
                    "Precision": len(caught) / len(queue),
                    "Recall": len(caught) / fraud_total if fraud_total else float("nan"),
                    "Fraud-labelled value caught": caught["TX_AMOUNT"].sum(),
                })

    return pd.DataFrame(queue_results), pd.DataFrame(precision_results)
