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

1. Validated transactions with consistent types and documented treatment of zero amounts.
2. Feature rows calculated using information available at each transaction's scoring time, with explicit rules for equal timestamps and any label feedback delay.
3. Chronological training, validation and test partitions.
4. Held-out scores keyed by transaction ID with event time, amount and evaluation outcome. Daily review ranks are calculated from those scores.
5. Streamlit consumes the precomputed output for queue inspection and review-capacity simulation, subject to the approved publication scope.

P2 verifies one row per transaction, unique keys, chronological boundaries and historical feature availability. P4 reconciles queue counts and monetary exposure to the held-out rows. [Methodology](methodology.md)
