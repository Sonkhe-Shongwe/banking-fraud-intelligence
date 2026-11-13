# Analytical data model

## Grain and input

One record represents one simulated transaction at its event time. The [source audit](data_sources.md) verified nine fields and a unique `TRANSACTION_ID` across the pinned data.

| Fields | Role |
|---|---|
| `TRANSACTION_ID` | Unique row key for validation, reconciliation and investigation detail. |
| `TX_DATETIME` | Event time for chronology and time-based features. |
| `CUSTOMER_ID`, `TERMINAL_ID` | Keys for grouping earlier transactions. |
| `TX_AMOUNT` | Observed transaction amount and ranking baseline input. |
| `TX_TIME_SECONDS`, `TX_TIME_DAYS` | Source elapsed-time fields. Both are derivable from the timestamp. |
| `TX_FRAUD` | Outcome for model fitting and evaluation subject to label timing. |
| `TX_FRAUD_SCENARIO` | Evaluation diagnostic describing the simulator outcome. Excluded from prediction inputs. |

## Planned Python outputs

1. [Validated transactions](../src/validate_transactions.py) with parsed timestamps and numeric types. The loader retains zero amounts, preserves source order and fails on invalid records. [Run the validator](../data/README.md#validate-the-csv-for-the-pipeline)
2. [Scoring-time feature rows](#scoring-time-features-and-partitions) calculated from the current amount and strictly earlier transaction activity.
3. [Chronological training, validation and test partitions](#scoring-time-features-and-partitions).
4. A held-out reporting export keyed by transaction ID, with event time, amount, evaluation outcome, model score and a precomputed daily rank for each policy. Use the same daily population for both ranks and resolve ties consistently.
5. The export can support a Power BI capacity comparison and, when suitable transaction-level detail is available to the intended audience, a review queue and drillthrough. Use the validated export and publication scope to propose the report views for owner approval. Transaction-level exports and reports containing them stay local pending publication clearance.

P2 verifies one row per transaction, unique keys, chronological boundaries and historical feature availability. P4 reconciles queue counts and monetary exposure to the held-out rows. [Methodology](methodology.md)

## Scoring-time features and partitions

The [feature module](../src/transaction_features.py) exposes the predictor list as `MODEL_FEATURES`. It includes the current amount, 24-hour and seven-day transaction counts for each customer and terminal, the customer's seven-day mean transaction amount, and seconds since the customer's last strictly earlier transaction. The rolling windows include their lower boundary and exclude events at the current timestamp. Counts with empty history are zero. Prior mean and elapsed time are missing when their respective history is unavailable. Fraud labels and scenario values remain available for retrospective evaluation and stay outside the predictor list.

The 2018 split uses April through July for training, August for validation and September for final testing. Earlier events can provide history across these boundaries. The [notebook](../notebooks/02_fraud_feature_engineering.ipynb) verifies unique transaction coverage and exactly reproduces the training features using only training-period events. Any model preprocessing that learns from the data, including imputation, is fitted on training data during P3.
