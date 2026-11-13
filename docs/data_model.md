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
4. A [held-out reporting export](#september-review-rank-export) keyed by transaction ID, with ranks for both policies and both eligible cohorts.
5. The export can support a Power BI capacity comparison and, when suitable transaction-level detail is available to the intended audience, a review queue and drillthrough. Use the validated export and publication scope to propose the report views for owner approval. Transaction-level exports and reports containing them stay local pending publication clearance.

P2 verifies one row per transaction, unique keys, chronological boundaries and historical feature availability. P4 reconciles queue counts and monetary exposure to the held-out rows. [Methodology](methodology.md)

## Scoring-time features and partitions

The [feature module](../src/transaction_features.py) exposes the predictor list as `MODEL_FEATURES`. It includes the current amount, 24-hour and seven-day transaction counts for each customer and terminal, the customer's seven-day mean transaction amount, and seconds since the customer's last strictly earlier transaction. The rolling windows include their lower boundary and exclude events at the current timestamp. Counts with empty history are zero. Prior mean and elapsed time are missing when their respective history is unavailable. Fraud labels and scenario values remain available for retrospective evaluation and stay outside the predictor list.

The 2018 split uses April through July for training, August for validation and September for final testing. Earlier events can provide history across these boundaries. The [notebook](../notebooks/02_fraud_feature_engineering.ipynb) verifies unique transaction coverage and exactly reproduces the training features using only training-period events. Any model preprocessing that learns from the data, including imputation, is fitted on training data during P3.

## September review rank export

The [P4 notebook](../notebooks/04_fraud_holdout_evaluation.ipynb) writes one row per September transaction to the local `data/processed/september_review_ranks.csv`. Each policy ranks the same eligible rows independently within each calendar day.

| Fields | Meaning |
|---|---|
| `TRANSACTION_ID`, `TX_DATETIME`, `TX_AMOUNT`, `TX_FRAUD` | Unique transaction key, event time, observed amount and retrospective fraud label |
| `model_score` | Logistic regression decision score used for ranking |
| `tx_amount_rank_all`, `model_score_rank_all` | One-based daily ranks across all transactions |
| `tx_amount_rank_le_220`, `model_score_rank_le_220` | One-based daily ranks recalculated within the restricted cohort. Rows above 220 have blank restricted ranks. |

The notebook reconciles counts and values when each rank is at or below 50 or 100. A consumer of restricted ranks must explicitly exclude blank ranks when applying the capacity filter. For a selected range of dates, calculate recall from the eligible fraud total across those dates and precision from the selected review count.


## P5 Power BI reporting outputs

[Notebook 05](../notebooks/05_power_bi_data_preparation.ipynb) creates the following local-only reporting tables after re-validating the source and the P4 rank export.

| Output | Grain | Rows expected | Role |
|---|---|---:|---|
| Overview_Daily.csv | One row per source date | 183 | Daily activity, fraud labels, fraud-labelled value and simulator amount-boundary context |
| DimDate.csv | One row per source date | 183 | Shared calendar, month and week attributes |
| September_Ranks.csv | One row per September transaction | 287,873 | P4 policy ranks for the full and restricted cohorts |
| September_Scenario_Lift.csv | One row per cohort and daily capacity | 4 | Fixed full-September comparison matrix |
| September_Queue_Reconciliation_QA.csv | One row per policy, cohort and capacity | 8 | Local reconciliation evidence; not a report table |

All files are written to data/processed/powerbi/, which is Git-ignored. The notebook also writes a local PowerBI_Data_Manifest.json containing input and output fingerprints. Do not commit these generated data files.

### Power BI relationship contract

- DimDate[Date] has a one-to-many, single-direction relationship to Overview_Daily[Date].
- DimDate[Date] has a one-to-many, single-direction relationship to September_Ranks[Date].
- September_Scenario_Lift remains disconnected so the four full-September reference scenarios are not changed by date or cohort slicers.
- The QA reconciliation table is not loaded into the report.
- TRANSACTION_ID and the technical rank columns are hidden from report consumers. No transaction-level drillthrough is included in the approved first release.

The cohort and daily-capacity selector tables are disconnected report controls. Their DAX definitions and the measure layer are the next modelling increment after Notebook 05 and theme import have been checked in the owner's environment.
